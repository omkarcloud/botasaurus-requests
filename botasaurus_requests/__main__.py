import os
import re
import subprocess
import sys
from dataclasses import dataclass
from functools import total_ordering
from pathlib import Path
from typing import Optional

import click
from rich import print as rprint
from rich.panel import Panel
from rich.status import Status

from __version__ import BRIDGE_VERSION
from .cffi import LibraryManager, root_dir
from .headers import ChromeVersions, FirefoxVersions

@total_ordering
@dataclass
class Version:
    version: str

    def __post_init__(self) -> None:
        self.sort_version = tuple(int(x) for x in self.version.split('.'))

    def __eq__(self, other) -> bool:
        return self.sort_version == other.sort_version

    def __lt__(self, other) -> bool:
        return self.sort_version < other.sort_version

    def __str__(self) -> str:
        return self.version

    @staticmethod
    def get_version(name) -> 'Version':
        ver: Optional[re.Match] = LibraryUpdate.FILE_NAME.search(name)
        if not ver:
            raise ValueError(f'Could not find version in {name}')
        return Version(ver[1])


@dataclass
class Asset:
    url: str
    name: str

    def __post_init__(self) -> None:
        self.version: Version = Version.get_version(self.name)


class LibraryUpdate(LibraryManager):

    FILE_NAME: re.Pattern = re.compile(r'^hrequests-cgo-([\d\.]+)')

    def __init__(self) -> None:
        self.parent_path: Path = root_dir / 'bin'
        self.file_cont, self.file_ext = self.get_name()
        self.file_pref = f'hrequests-cgo-{BRIDGE_VERSION}'

    @property
    def path(self) -> Optional[str]:
        if paths := self.get_files():
            return paths[0]

    @property
    def full_path(self) -> Optional[str]:
        if path := self.path:
            return os.path.join(self.parent_path, path)

    def latest_asset(self) -> Asset:
        releases = self.get_releases()
        for release in releases:
            if asset := self.check_assets(release['assets']):
                url, name = asset
                return Asset(url, name)
        raise ValueError('No assets found')

    def install(self) -> None:
        filename = super().check_library()
        ver: Version = Version.get_version(filename)

        rprint(
            f'[bright_green]:sparkles: Successfully installed dependencies v{ver}! :tada:[/]'
        )

    def update(self) -> None:
        '''
        Updates the library if needed
        '''
        path = self.path
        if not path:
            # install the library if it doesn't exist
            return self.install()

        # get the version
        current_ver: Version = Version.get_version(path)

        # check if the version is the same as the latest avaliable version
        asset: Asset = self.latest_asset()
        if current_ver >= asset.version:
            rprint('[bright_green]:sparkles: library up to date! :tada:')
            rprint(f'Current version: [green]v{current_ver}\n')
            return

        # download updated file
        rprint(f'Updating dependencies from [red]v{current_ver}[/] => v{asset.version}')
        # download new, remove old
        self.download_file(self.full_path, asset.url)
        try:
            os.remove(os.path.join(self.parent_path, path))
        except OSError:
            rprint('[yellow]Warning: Could not remove outdated library files.')


class HeaderUpdate:
    def update(self) -> None:
        '''
        Updates the saved header versions
        '''
        ChromeVersions(force_dl=True)
        FirefoxVersions(force_dl=True)



@click.group()
def cli() -> None:
    pass


@cli.command(name='update')
@click.option('--headers', is_flag=True, help='Update headers only')
@click.option('--library', is_flag=True, help='Update library only')
def update(headers=False, library=False):
    '''
    Update all library components
    '''
    # if no options passed, mark both as True
    if not headers ^ library:
        headers = library = True
    library and LibraryUpdate().update()
    headers and HeaderUpdate().update()




if __name__ == '__main__':
    cli()
