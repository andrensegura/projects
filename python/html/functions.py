#PRINTS OUT A FILE
def print_html_file(file_name):
    with open(file_name, 'r') as fin:
        print fin.read()

def print_header():
    print "Content-type: text/html\n"
    print_html_file("header.html")
    print_nav()

def print_nav():
    user = get_session_user()
    print "<hr>"
    print """<a href="/">Home</a>"""
    print "&nbsp;|&nbsp;"
    if user:
        print """<a href="u/%s">%s</a>""" % (user, user)
        print """<a href="/login?action=logout">(logout)</a>"""
        print "&nbsp;|&nbsp;"
    else:
        print """<a href="login">Log In</a>"""
        print "&nbsp;|&nbsp;"
    print """<a href="/register"> Register</a>"""

    print """<span style="float:right" >"""
    print """<input type="image" style="height:20px;width:20px;vertical-align:middle"
             src="/pics/search.png" />"""
    print """<input type="text">"""
    print """&nbsp;</span>"""
    print "<hr>"

def get_session_user():
    from config import USERNAME

    username = ""
    session = get_cookie()
    if session:
        import mysql
        result = mysql.execute_mysql("""SELECT * FROM users WHERE logged_in = %s"""
                   , (session["session"].value,))
        username = result[0][USERNAME] if result else username
    return username

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
