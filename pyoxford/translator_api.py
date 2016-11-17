from xml.etree import ElementTree
from pyoxford.token import Token
import requests

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


class Translator():
    API_ROOT = "http://api.microsofttranslator.com/v2/Http.svc"

    def __init__(self, client_id, client_secret, new_auth=False):
        self.__token = Token(client_secret, client_id, new_auth, "http://api.microsofttranslator.com")

    def detect(self, text):
        params = {
            "text": text
        }
        url = self.API_ROOT + "/Detect?" + urlencode(params)
        resp = requests.get(url, headers=self._make_header())
        result = {}
        if resp.ok:
            root = ElementTree.fromstring(resp.content)
            result = root.text
        else:
            resp.raise_for_status()
        return result

    def translate(self, text, lang_to, lang_from=""):
        # language codes
        # https://msdn.microsoft.com/en-us/library/hh456380.aspx
        params = {
            "text": text,
            "to": lang_to
        }

        if lang_from:
            params["from"] = lang_from

        url = self.API_ROOT + "/Translate?" + urlencode(params)
        resp = requests.get(url, headers=self.__token.make_header())
        result = {}
        if resp.ok:
            root = ElementTree.fromstring(resp.content)
            result = root.text
        else:
            resp.raise_for_status()
        return result
