import json

from requests.utils import get_encoding_from_headers
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from http.client import responses as status_codes
from typing import List, Literal, Optional, Union

from json import dumps, loads
from requests.exceptions import HTTPError


from . import client
from .cffi import library
from .exceptions import ClientException

from .cookies import RequestsCookieJar
from .toolbelt import CaseInsensitiveDict, FileUtils

try:
    import turbob64 as base64
except ImportError:
    import base64


class ProcessResponse:
    def __init__(
        self,
        session,
        method: str,
        url: str,
        files: Optional[dict] = None,
        cookies: Optional[Union[RequestsCookieJar, dict, list]] = None,
        **kwargs,
    ) -> None:
        self.session= session
        self.method: str = method
        self.url: str = url

        if files:
            data = kwargs['data']
            headers = kwargs['headers']
            # assert that data is a dict
            if data is not None:
                assert isinstance(data, dict), "Data must be a dict when files are passed"
            # convert files to multipart/form-data
            kwargs['data'], content_type = FileUtils.encode_files(files, data)
            # content_type needs to be set to Content-Type header
            if headers is None:
                headers = {}
            # else if headers were provided, append Content-Type to those
            elif isinstance(headers, dict):
                headers = CaseInsensitiveDict(headers)
            headers['Content-Type'] = content_type
            kwargs['headers'] = headers

        self.cookies: Optional[Union[RequestsCookieJar, dict, list]] = cookies
        self.kwargs: dict = kwargs
        self.response: Response

    def send(self) -> None:
        time: datetime = datetime.now()
        self.response = self.execute_request()
        self.response.elapsed = datetime.now() - time

    def execute_request(self) -> 'Response':
        try:
            resp = self.session.execute_request(
                method=self.method,
                url=self.url,
                cookies=self.cookies,
                **self.kwargs,
            )
        except ClientException as e:
            raise e
        except IOError as e:
            raise ClientException('Connection error') from e
        resp.session = None if self.session.temp else self.session
        resp.browser = self.session.browser
        return resp


class ProcessResponsePool:
    '''
    Processes a pool of ProcessResponse objects
    '''

    def __init__(self, pool: List[ProcessResponse]) -> None:
        self.pool: List[ProcessResponse] = pool

    def execute_pool(self) -> List['Response']:
        values: list = []
        for proc in self.pool:
            # get the request data
            payload, headers = proc.session.build_request(
                method=proc.method,
                url=proc.url,
                cookies=proc.cookies,
                **proc.kwargs,
            )
            # remember full set of headers (including from session)
            proc.full_headers = headers
            # add to values
            values.append(payload)
        # execute the pool
        try:
            # send request
            resp = proc.session.server.post(
                f'http://127.0.0.1:{library.PORT}/multirequest', body=dumps(values)
            )
            response_object = loads(resp.read())
        except Exception as e:
            raise ClientException('Connection error') from e
        # process responses
        return [
            proc.session.build_response(proc.url, proc.full_headers, data, payload['proxyUrl'])
            for proc, data in zip(self.pool, response_object)
        ]
    
def extract_next_data(html_string):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html_string, "html.parser")
    el = soup.select_one("#__NEXT_DATA__")
    if not el:
        raise Exception("No Next.js Data Found")

    next_data = json.loads(el.text)

    if "props" in next_data:
                next_data = next_data.get("props")
    if "pageProps" in next_data:
                next_data = next_data.get("pageProps")
    return next_data

@dataclass
class Response:
    """
    Response object

    Methods:
        json: Returns the response body as json
        render: Renders the response body with BrowserSession
        find: Shortcut to .html.find

    Attributes:
        url (str): Response url
        status_code (int): Response status code
        reason (str): Response status reason
        headers (CaseInsensitiveDict): Response headers
        cookies (RequestsCookieJar): Response cookies
        text (str): Response body as text
        content (Union[str, bytes]): Response body as bytes or str
        ok (bool): True if status code is less than 400
        elapsed (datetime.timedelta): Time elapsed between sending the request and receiving the response
        html (parser.HTML): Response body as HTML parser object
    """

    url: str
    status_code: int
    headers: 'client.CaseInsensitiveDict'
    cookies: RequestsCookieJar
    raw: Union[str, bytes] = None

    # set by ProcessResponse
    history: Optional[List['Response']] = None
    session= None
    browser: Optional[Literal['firefox', 'chrome']] = None
    elapsed: Optional[timedelta] = None
    encoding: str = 'UTF-8'
    is_utf8: bool = True
    proxy: Optional[str] = None

    def __post_init__(self) -> None:
        self.encoding = get_encoding_from_headers(self.headers) or 'utf-8'
        
    @property
    def reason(self) -> str:
        return status_codes[self.status_code]

    def json(self, **kwargs) -> Union[dict, list]:
        return loads(self.content, **kwargs)

    @property
    def content(self) -> bytes:
        # note: this will convert the content to bytes on each access
        return self.raw if type(self.raw) is bytes else self.raw.encode(self.encoding)

    @property
    def text(self) -> str:
        return self.raw if type(self.raw) is str else self.raw.decode(self.encoding)


    @property
    def ok(self) -> bool:
        return self.status_code < 400

    @property
    def links(self) -> dict:
        '''Returns the parsed header links of the response, if any'''
        header = self.headers.get("link")
        resolved_links = {}

        if not header:
            return resolved_links

        links = parse_header_links(header)
        for link in links:
            key = link.get("rel") or link.get("url")
            resolved_links[key] = link
        return resolved_links

    def __bool__(self) -> bool:
        '''Returns True if :attr:`status_code` is less than 400'''
        return self.ok

    def get_next_data(self):
        # Ensure headers attribute is accessed correctly
        content_type = self.headers.get('Content-Type', '').lower()
        if 'text/html' in content_type:
            # Assuming extract_next_data is a function that needs to be defined or imported
            return extract_next_data(self.text)
        else:
            raise ValueError("Content Type must be HTML")
    def raise_for_status(self):
        """Raises :class:`HTTPError`, if one occurred."""

        http_error_msg = ""
        if isinstance(self.reason, bytes):
            # We attempt to decode utf-8 first because some servers
            # choose to localize their reason strings. If the string
            # isn't utf-8, we fall back to iso-8859-1 for all other
            # encodings. (See PR #3538)
            try:
                reason = self.reason.decode("utf-8")
            except UnicodeDecodeError:
                reason = self.reason.decode("iso-8859-1")
        else:
            reason = self.reason

        if 400 <= self.status_code < 500:
            http_error_msg = (
                f"{self.status_code} Client Error: {reason} for url: {self.url}"
            )

        elif 500 <= self.status_code < 600:
            http_error_msg = (
                f"{self.status_code} Server Error: {reason} for url: {self.url}"
            )

        if http_error_msg:
            raise HTTPError(http_error_msg, response=self)

    def __enter__(self):
        return self

    def __repr__(self):
        return f"<Response [{self.status_code}]>"


def parse_header_links(value):
    '''
    Return a list of parsed link headers proxies.
    i.e. Link: <http:/.../front.jpeg>; rel=front; type="image/jpeg",<http://.../back.jpeg>; rel=back;type="image/jpeg"
    :rtype: list
    '''
    links = []
    replace_chars = " '\""
    value = value.strip(replace_chars)

    if not value:
        return links

    for val in re.split(", *<", value):
        try:
            url, params = val.split(";", 1)
        except ValueError:
            url, params = val, ""
        link = {"url": url.strip("<> '\"")}
        for param in params.split(";"):
            try:
                key, value = param.split("=")
            except ValueError:
                break
            link[key.strip(replace_chars)] = value.strip(replace_chars)
        links.append(link)
    return links


def build_response(
    res: Union[dict, list], res_cookies: RequestsCookieJar, proxy: Optional[str]
) -> Response:
    '''Builds a Response object'''
    # build headers
    if res["headers"] is None:
        res_headers = {}
    else:
        res_headers = {
            header_key: header_value[0] if len(header_value) == 1 else header_value
            for header_key, header_value in res["headers"].items()
        }
    # decode bytes response
    if res.get('isBase64'):
        res['body'] = base64.b64decode(res['body'].encode())
    return Response(
        # add target / url
        url=res["target"],
        # add status code
        status_code=res["status"],
        # add headers
        headers=client.CaseInsensitiveDict(res_headers),
        # add cookies
        cookies=res_cookies,
        # add response body
        raw=res["body"],
        # if response was utf-8 validated
        is_utf8=not res.get('isBase64'),
        # add proxy
        proxy=proxy,
    )
