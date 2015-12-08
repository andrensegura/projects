def get_cookie():
    import Cookie, os
    session = Cookie.SimpleCookie()
    try:
        session.load(os.environ["HTTP_COOKIE"])
        if session["session"].value == "0":
            session = ""
    except ((Cookie.CookieError, KeyError)):
        session = ""
    return session

