from pyoxford.token import Token

def speech(path_or_client_id="", client_secret=""):
    from pyoxford.speech_api import Speech
    api = None
    if path_or_client_id and client_secret:
        api = Speech(client_secret)
    else:
        key = _read_key(path_or_client_id, "speech")
        api = Speech(key.primary)

    return api


def vision(path_or_key=""):
    from pyoxford.vision_api import Vision
    api = None
    if path_or_key.find(".yaml") > 0:
        key = _read_key(path_or_key, "vision")
        api = Vision(key.primary)
    else:
        api = Vision(path_or_key)

    return api


def translator(path_or_client_id="", client_secret=""):
    from pyoxford.translator_api import Translator
    api = None
    if path_or_client_id.find(".yaml") > 0:
        key = _read_key(path_or_client_id, "translator")
        api = Translator(key.primary, key.secondary)
    elif path_or_client_id and client_secret:
        api = Translator(path_or_client_id, client_secret)
    else:
        api = Translator("unused", path_or_client_id, True)

    return api


def _read_key(path, service_name):
    import yaml
    from collections import namedtuple
    ApiKey = namedtuple("apiKey", ["primary", "secondary"])
    key = ApiKey("", "")
    with open(path, "rb") as config:
        settings = yaml.load(config)
        key1 = settings[service_name]["primary"]
        key2 = settings[service_name]["secondary"]
        key = ApiKey(key1, key2)

    return key
