import re
import pytz
from datetime import datetime
from pytz import timezone
from bs4 import BeautifulSoup
from .exceptions import CustomHTTPException
from typing import Union


class Convert:
    """Centralize conversion and casting methods

    This module centralize all methods to convert different type of data
    to each other, also have custom methods to convert certain objects.

    Examples:
            b = Convert().str2bool('true')
            i = Convert().str2int('0')
    """

    def str2bool(self, v: any, default: any = None) -> Union[bool, any]:
        """Method to convert a string into a boolean. This attempt to convert
        strings that contain things like: Y, y, 1, T, t, TRUE, true to 'true'
        and strings that contain things like: 0, F, f, N, n, false, FALSE,
        no to 'false'

        Args:
                v (any): Value to be converted
                default (any, optional): [description]. Defaults to None.

        Returns:
                Union[bool, any]: Bool if v is one of the expected values
                        to be converted, otherwise takes default value and if is not
                        set returns v value
        """
        if not v or v == 0:
            return False

        if v and v == 1:
            return True

        if isinstance(v, str):
            v = v.encode("utf-8").decode("utf-8").strip().lower()
            if v in ("y", "yes", "true", "1", "on"):
                return True
            elif v in ("n", "no", "false", "0", "off"):
                return False
        if default is not None:
            return default
        return v

    def str2int(self, v: Union[str, any]) -> int:
        """Converts a string to a integer.

        Args:
                v (Union[str, any]):  Value to be converted

        Returns:
                int: integer number according what the ``v`` parameter is;
                        If it is not a number will return the same value it was sent
                        as argument.
        """
        if isinstance(v, str):
            v = v.encode("utf-8").decode("utf-8").strip()
            pattern = re.compile("^[-+]?[0-9]+$")
            if pattern.match(v):
                return int(v)
        return v

    def str2datetime(self, v: Union[str, any]) -> datetime:
        """Convert string to datetime object, for now

        Args:
                v (Union[str, any]): Value to be converted

        Returns:
                datetime: Datetime of the string
        """
        if isinstance(v, str):
            v = v.rstrip("Z")
            v = v.rstrip("z")
            patterns = {
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%dT%H:%M:%Sz",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M:%S",
            }

            for pattern in patterns:
                p = pattern.replace("%Y", r"\d{4}")
                p = re.sub(r"%\w", "\\\\d{2}", p)
                if re.match(re.compile(p), v):
                    v = datetime.strptime(v.strip(), pattern)
                    break
        elif isinstance(v, int) or isinstance(v, float):
            v = datetime.fromtimestamp(int(v))
        elif isinstance(v, datetime):
            pass
        else:
            msg = "Not pattern match for datetime convertion: {}"
            raise CustomHTTPException(500, msg.format(v))
        return v

    def datetime2str(
        self, dt: datetime = None, tz: timezone = None, format: str = None
    ) -> str:
        """Convert datetime object to string format.


        Args:
                dt (datetime): A valid datetime object. For None,
                        a current datetime with UTC TZ will be used.
                tz (timezone): A valid timezone object. For None,
                        the current timezone (UTC) will remain.
                format (str): String with the convertion pattern.
                        When "format" is not provided a IsoFormat without
                        microseconds will be returned.

        Returns:
                str: String representation of datetime object
        """
        if dt is None:
            dt = datetime.now(pytz.utc)

        if tz:
            dt = dt.astimezone(tz)

        if not isinstance(dt, datetime):
            msg = "Not valid datatime object for string convertion"
            raise CustomHTTPException(500, msg)

        if isinstance(format, str):
            return dt.strftime(format)

        return dt.replace(microsecond=0).isoformat()

    def html2text(self, html: str) -> str:
        """Convert any HTML string to plain text

        Args:
                html (str): HTML string

        Returns:
                str: Pure TEXT plan text
        """
        html = re.sub(r"<br\s*/?>", "\n", html)
        soup = BeautifulSoup(html, "html.parser")
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = "\n".join(chunk for chunk in chunks if chunk)
        return text
