#PRINTS OUT A FILE
def print_html_file(file_name):
    with open(file_name, 'r') as fin:
        print fin.read()

def print_header():
    print "Content-type: text/html\n"
    print_html_file("html/header.html")
    print_nav()
    print """<div class="content">"""

def print_nav():
    print """<div class="navbar">"""
    user = get_session_user()

    #mailbox
    if user:
        import mysql
        result = mysql.execute_mysql("""SELECT * FROM mail WHERE recipient = %s AND is_read = '0';"""
                    , (user,) )
        if result: 
            mailbox = """<a href="/inbox">
                     <img src="/pics/unread.png" alt="inbox" style="width:15px;height:12px;"></a>"""
        else:
            mailbox = """<a href="/inbox">
                     <img src="/pics/mailbox.png" alt="inbox" style="width:15px;height:12px;"></a>"""
    else:
        mailbox = ""

    
    print "<br>"

    print """<form method="post" action="/search">"""
    print """<ul> <li><a href="/">Home</a>"""
    if user:
        print """<li><a href="/u/%s">%s</a>""" % (user, user)
        print mailbox
        print """<li><a href="/login?action=logout">logout</a>"""
    else:
        print """<li><a href="/login">Log In</a>"""
    if not user:
        print """<li><a href="/register"> Register</a>"""

    print """<span style="float:right" >"""
    print """<input type="image" style="height:20px;width:20px;vertical-align:middle"
             src="/pics/search.png" />"""
    print """<input type="text" name="search" placeholder="Search" accesskey="s" title="try Alt+s!">"""
    print """&nbsp;</span>"""
    print """</form>"""

    print """</div>"""


def is_verified(user):
    import mysql
    result = mysql.execute_mysql("""SELECT verified FROM users WHERE username = %s;""", (user,) )
    if result[0][0] == "0":
        return True
    else:
        return False

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

def create_password_hash(passw):
    from passlib.hash import pbkdf2_sha256
    return pbkdf2_sha256.encrypt(passw, rounds=200000, salt_size=16)
