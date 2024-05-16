from typing import Literal, Optional
from . import reqs
from requests.models import Response
from requests.sessions import Session


class Request(Session):

    def __init__(self, proxy=None):
        self._proxy = proxy

    def get(
        self,
        url: str | bytes,
        referer="https://www.google.com/",
        params=None,
        data=None,
        headers=None,
        browser: Optional[Literal["firefox", "chrome"]] = "firefox",
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
    ) -> Response:

        # Only update kwargs with non-None named arguments
        named_args = {
            "params": params,
            "data": data,
            "headers": headers,
            "cookies": cookies,
            "files": files,
            "auth": auth,
            "timeout": timeout,
            "allow_redirects": allow_redirects,
            "proxies": proxies or self._proxy,
            "hooks": hooks,
            "stream": stream,
            "verify": verify,
            "cert": cert,
            "json": json,
            # Special Param
            "browser": browser,
            "referer": referer,
        }

        kwargs = {k: v for k, v in named_args.items() if v is not None}

        return reqs.get(url, **kwargs)

    def options(
        self,
        url: str | bytes,
        params=None,
        data=None,
        headers=None,
        browser: Optional[Literal["firefox", "chrome"]] = "firefox",
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=False,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
    ) -> Response:
        kwargs = self._merge_kwargs(
            {
                "params": params,
                "data": data,
                "headers": headers,
                "cookies": cookies,
                "files": files,
                "auth": auth,
                "timeout": timeout,
                "allow_redirects": allow_redirects,
                "proxies": proxies or self._proxy,
                "hooks": hooks,
                "stream": stream,
                "verify": verify,
                "cert": cert,
                "json": json,
                "browser": browser,
            }
        )
        return reqs.options(url, **self._merge_kwargs(kwargs))

    def head(
        self,
        url: str | bytes,
        params=None,
        data=None,
        headers=None,
        browser: Optional[Literal["firefox", "chrome"]] = "firefox",
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
    ) -> Response:
        kwargs = self._merge_kwargs(
            {
                "params": params,
                "data": data,
                "headers": headers,
                "cookies": cookies,
                "files": files,
                "auth": auth,
                "timeout": timeout,
                "allow_redirects": allow_redirects,
                "proxies": proxies or self._proxy,
                "hooks": hooks,
                "stream": stream,
                "verify": verify,
                "cert": cert,
                "json": json,
                "browser": browser,
            }
        )
        return reqs.head(url, **self._merge_kwargs(kwargs))

    def post(
        self,
        url: str | bytes,
        data=None,
        json=None,
        params=None,
        headers=None,
        browser: Optional[Literal["firefox", "chrome"]] = "firefox",
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
    ) -> Response:
        kwargs = self._merge_kwargs(
            {
                "data": data,
                "json": json,
                "params": params,
                "headers": headers,
                "cookies": cookies,
                "files": files,
                "auth": auth,
                "timeout": timeout,
                "allow_redirects": allow_redirects,
                "proxies": proxies or self._proxy,
                "hooks": hooks,
                "stream": stream,
                "verify": verify,
                "cert": cert,
                "browser": browser,
            }
        )
        return reqs.post(url, **self._merge_kwargs(kwargs))

    def put(
        self,
        url: str | bytes,
        data=None,
        json=None,
        params=None,
        headers=None,
        browser: Optional[Literal["firefox", "chrome"]] = "firefox",
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
    ) -> Response:
        kwargs = self._merge_kwargs(
            {
                "data": data,
                "json": json,
                "params": params,
                "headers": headers,
                "cookies": cookies,
                "files": files,
                "auth": auth,
                "timeout": timeout,
                "allow_redirects": allow_redirects,
                "proxies": proxies or self._proxy,
                "hooks": hooks,
                "stream": stream,
                "verify": verify,
                "cert": cert,
                "browser": browser,
            }
        )
        return reqs.put(url, **kwargs)

    def patch(
        self,
        url: str | bytes,
        data=None,
        json=None,
        params=None,
        headers=None,
        browser: Optional[Literal["firefox", "chrome"]] = "firefox",
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
    ) -> Response:
        kwargs = self._merge_kwargs(
            {
                "data": data,
                "params": params,
                "headers": headers,
                "cookies": cookies,
                "files": files,
                "auth": auth,
                "timeout": timeout,
                "allow_redirects": allow_redirects,
                "proxies": proxies or self._proxy,
                "hooks": hooks,
                "stream": stream,
                "verify": verify,
                "cert": cert,
                "json": json,
                "browser": browser,
            }
        )
        return reqs.patch(url, **self._merge_kwargs(kwargs))

    def delete(
        self,
        url: str | bytes,
        params=None,
        data=None,
        headers=None,
        browser: Optional[Literal["firefox", "chrome"]] = "firefox",
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=False,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
    ) -> Response:
        kwargs = self._merge_kwargs(
            {
                "params": params,
                "data": data,
                "headers": headers,
                "cookies": cookies,
                "files": files,
                "auth": auth,
                "timeout": timeout,
                "allow_redirects": allow_redirects,
                "proxies": proxies or self._proxy,
                "hooks": hooks,
                "stream": stream,
                "verify": verify,
                "cert": cert,
                "json": json,
                "browser": browser,
            }
        )
        return reqs.delete(url, **self._merge_kwargs(kwargs))

    def _merge_kwargs(self, kwargs):
        return {k: v for k, v in kwargs.items() if v is not None}
