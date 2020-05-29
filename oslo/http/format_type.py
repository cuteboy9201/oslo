XML = "XML"
JSON = "JSON"
RAW = "RAW"
APPLICATION_FORM = "application/x-www-form-urlencoded"
APPLICATION_XML = "application/xml"
APPLICATION_JSON = "application/json"
APPLICATION_OCTET_STREAM = "application/octet-stream"
TEXT_XML = "text/xml"


def map_format_to_accept(format):
    if format == XML:
        return APPLICATION_XML
    if format == JSON:
        return APPLICATION_JSON
    return APPLICATION_OCTET_STREAM


def map_accept_to_format(accept):
    if accept.lower() == APPLICATION_XML or accept.lower() == TEXT_XML:
        return XML
    if accept.lower() == APPLICATION_JSON:
        return JSON
    return RAW
