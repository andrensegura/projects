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

def create_session(user, passw):
    import Cookie, random, mysql
    from datetime import datetime, timedelta
    from string import ascii_uppercase, digits

    expires = datetime.now() + timedelta(days=3)
    cookie = Cookie.SimpleCookie()
    random.seed(passw)
    key = ''.join(random.SystemRandom().choice(ascii_uppercase + digits) for _ in range(16))
    cookie["session"] = key
    cookie["session"]["domain"] = "keycellar.com"
    cookie["session"]["path"] = "/"
    cookie["session"]["expires"] = expires.strftime("%a, %d-%b-%Y %H:%M:%S PST")
    #set key in database
    mysql.execute_mysql("""UPDATE users SET logged_in = %s WHERE username = %s;"""
                        , (key, user,) )
    return cookie
