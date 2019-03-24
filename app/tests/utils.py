
def get_cookie_from_response(response, cookie_name):
    """Extra the cookies from the response

    Arguments:
        response {Response} -- Response object
        cookie_name {String} -- Name of the cookie to extra

    Returns:
        dictionary -- Key-value pair of the cookie name and value
    """

    cookie_headers = response.headers.getlist('Set-Cookie')
    for header in cookie_headers:
        attributes = header.split(';')
        if cookie_name in attributes[0]:
            cookie = {}
            for attr in attributes:
                split = attr.split('=')
                cookie[split[0].strip().lower()] = split[1] if len(
                    split) > 1 else True
            return cookie
    return None
