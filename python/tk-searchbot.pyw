import praw #this is the Python Reddit API Wrapper. install with: "pip install praw"
import _thread as thread
from tkinter import Tk, Label, Entry, Button, Text, Radiobutton, IntVar
from tkinter import LEFT, RIGHT, HORIZONTAL, END

NEW=1
HOT=2
TOP=3
RISING=4
CONTROVERSIAL=5
LIMIT = 25              #how many posts to grab
SUBREDDIT = ''
SEARCH_FOR = []
already_done = []       #array containing ids of submissions/comments that have been seached already

#creates a connection to Reddit and identifies the script. You have to do this.
r = praw.Reddit(user_agent="Searches for things I want in various trading subreddits. By /u/bibbleskit")

def find_stuff(root, sub, search_items, sort, limit):
    global LIMIT
    LIMIT = int(limit)
    thread.start_new_thread(actually_find_stuff, (root, sub, search_items, sort))

def actually_find_stuff(root, sub, search_items, sort):
    #exit if nothing given
    if not sub or not search_items:
        return

    textarea = Text(root, height=15, width=40)
    textarea.grid(row=4, column=0, columnspan=3, sticky="news", padx=1, pady=1)
    
    SUBREDDIT=sub
    SEARCH_FOR=search_items.split(',')
    
    #reddit stuff
    submissions = r.get_subreddit(SUBREDDIT).get_new(limit=LIMIT); #default, in case something goes wrong.
    if sort is NEW:
        submissions = r.get_subreddit(SUBREDDIT).get_new(limit=LIMIT);
    if sort is HOT:
        submissions = r.get_subreddit(SUBREDDIT).get_hot(limit=LIMIT);
    if sort is TOP:
        submissions = r.get_subreddit(SUBREDDIT).get_top(limit=LIMIT);
    if sort is RISING:
        submissions = r.get_subreddit(SUBREDDIT).get_rising(limit=LIMIT); 
    if sort is CONTROVERSIAL:
        submissions = r.get_subreddit(SUBREDDIT).get_controversial(limit=LIMIT);
    count = 0
    for s in submissions:
        count += 1
        textarea.delete('1.0', '1.end')
        textarea.insert('1.0', "%d/%d" % (count,LIMIT))
        contains_search_item = any(string in s.title.lower() for string in SEARCH_FOR)
        if s.id not in already_done and contains_search_item:
            textarea.insert(END, "\r\n%s: http://reddit.com/%s" % (s.title, s.id))
            already_done.append(s.id)
            textarea.insert(END, "\r\n-----------------")
            continue

        #called it forest_comments because the comments are organized just like in a reddit submission
        comments = praw.helpers.flatten_tree(s.comments)
        for c in comments:
            if not hasattr(c, 'body'):
                continue
            if not isinstance(c, praw.objects.Comment):
                continue
            contains_search_item = any(string in c.body.lower() for string in SEARCH_FOR)
            if contains_search_item:
                if s.id not in already_done:
                    textarea.insert(END, "\r\n%s: http://reddit.com/%s" % (s.title, s.id))
                    already_done.append(s.id)
                textarea.insert(END, "\r\n  comment: %s" % (c.body))
                already_done.append(c.id)
        if s.id in already_done:
            textarea.insert(END, "\r\n-----------------")
    textarea.insert(END, "\r\nDone!")
root = Tk() #parent window
root.wm_title("Reddit Search")
#column geometry
root.geometry("+%d+%d"% (root.winfo_screenwidth()/8, root.winfo_screenheight()/10)) #window placement.
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=4)
root.columnconfigure(2, weight=1)

#radio buttons
sort = IntVar()
new = Radiobutton(root, text="new", variable=sort, value=NEW)
hot = Radiobutton(root, text="hot", variable=sort, value=HOT)
top = Radiobutton(root, text="top", variable=sort, value=TOP)
rising = Radiobutton(root, text="rising", variable=sort, value=RISING)
controv = Radiobutton(root, text="controv.", variable=sort, value=CONTROVERSIAL)
new.grid(row=2, column=1)
hot.grid(row=2, column=2)
top.grid(row=3, column=0)
rising.grid(row=3, column=1)
controv.grid(row=3, column=2)

new.select()

#limit
limit_entry = Entry(root, bd = 3, width=2)
limit_entry.insert(0, "25") #index to start string, then the string.
limit_entry.grid(row=2, column=0)

#subreddit query
subreddit_label = Label(root, text="Subreddit:").grid(row=0)
subreddit_entry = Entry(root, bd = 3) #bd is border. takes an int as pixels
subreddit_entry.grid(row=0, column=1, sticky="ew")
subreddit_entry.focus() #the below makes it so that Enter is the same as hitting the button.
subreddit_entry.bind('<Return>', lambda _: find_stuff(root, subreddit_entry.get(),
                                search_entry.get(), sort.get(), limit_entry.get()))

#search query
search_label = Label(root, text="Search for:").grid(row=1)
search_entry = Entry(root, bd = 3)
search_entry.grid(row=1, column=1, sticky="ew")
search_entry.bind('<Return>', lambda _: find_stuff(root, subreddit_entry.get(),
                            search_entry.get(), sort.get(), limit_entry.get()) )

#search button
search_button = Button(root, text = "Search",
                       command = lambda: find_stuff(root, subreddit_entry.get(),
                       search_entry.get(), sort.get(), limit_entry.get())
                       ).grid(row=0, rowspan=2, column=2, sticky="news", padx=1, pady=1)

root.mainloop()
