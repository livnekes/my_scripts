import urllib, urllib2
import requests
import cookielib

def send_http_post(cookies, url, referer, payload = {}):
    """ Send data via http post command """

    data 	=	 urllib.urlencode(payload)
    req 	=	 urllib2.Request(url, data)
    opener 	=	 urllib2.build_opener()
    opener 	=	 urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
    opener.addheaders.append(('Referer', referer))

    return opener.open(req)

def makeCookie(name, value, domain):
    """ make a simple cookie to add to the jar """
    return cookielib.Cookie(
        version = 0,
        name = name,
        value = value,
        port = None,
        port_specified = False,
        domain = domain,
        domain_specified = True,
        domain_initial_dot = True,
        path = "/",
        path_specified = True,
        secure = False,
        expires = None,
        discard = False,
        comment = None,
        comment_url = None,
        rest = {'httponly': None},
        rfc2109 = False
        )

def get_url_cookies(url, referer ,payload):
    """ Login to url and retrive cookies """

    cj      =   cookielib.CookieJar()
    resp    =   send_http_post(cj, url, referer, payload)
    resp.close()

    return cj


