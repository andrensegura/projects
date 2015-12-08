def print_header():
    print "Content-type: text/html\n"
    print_html_file("header.html")

def print_nav(user):
    print """<a href="/">Home</a>"""
    print "&nbsp;|&nbsp;"
    if user:
        print """<a href="u/%s">%s</a>""" % (user, user)
        print """<a href="login?action=logout">(logout)</a>"""
        print "&nbsp;|&nbsp;"
    else:
        print """<a href="login">Log In</a>"""
        print "&nbsp;|&nbsp;"
    print """<a href="register"> Register</a>"""
