import requests

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


class Token(object):
    OLD_AUTH_URL = "https://datamarket.accesscontrol.windows.net/v2/OAuth2-13"
    NEW_AUTH_URL = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken"

    def __init__(self, client_secret, client_id="", new_auth=False, scope=""):
        self.__token = ""
        if new_auth:
            self.__authorize_new(client_secret)
        else:
            self.__authorize_old(client_id, client_secret, scope)

    def __authorize_new(self, client_secret):
        headers = {
            "Ocp-Apim-Subscription-Key": client_secret
        }

        resp = requests.post(self.NEW_AUTH_URL, headers=headers)
        if resp.ok:
            self.__token = resp.text
        else:
            resp.raise_for_status()

    def __authorize_old(self, client_id, client_secret, scope):
        headers = {
            "Content-type": "application/x-www-form-urlencoded"
        }

        params = urlencode({
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": scope
        })

        resp = requests.post(self.OLD_AUTH_URL, data=params, headers=headers)
        if resp.ok:
            _body = resp.json()

    def authorization(self):
        return "Bearer {0}".format(self.__token)

    def make_header(self):
        return {
            "Authorization": self.authorization()
        }
