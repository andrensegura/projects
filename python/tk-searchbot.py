import praw #this is the Python Reddit API Wrapper. install with: "pip install praw"
from tkinter import Tk, Label, Entry, Button
from tkinter import LEFT, RIGHT

LIMIT = 25                          #how many posts to grab
SUBREDDIT = 'tsumtsumtrades'
SEARCH_FOR = ['oswald', 'liberty']
already_done = []                   #array containing ids of submissions/comments that have been seached already

#creates a connection to Reddit and identifies the script. You have to do this.
r = praw.Reddit(user_agent="Searches for things I want in various trading subreddits. By /u/bibbleskit")

def find_stuff(sub, search_items):
    new_submissions = r.get_subreddit(SUBREDDIT).get_new(limit=LIMIT);
    for s in new_submissions:
        contains_search_item = any(string in s.title.lower() for string in SEARCH_FOR)
        if s.id not in already_done and contains_search_item:
            print("%s: http://reddit.com/%s" % (s.title, s.id))
            already_done.append(s.id)
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
                print("%s: http://reddit.com/%s" % (s.title, s.id))
                print("comment: %s" % (c.body))
                already_done.append(c.id)
        already_done.append(s.id)
    
root = Tk() #parent window
subreddit_label = Label(root, text="Subreddit:").grid(row=0)
subreddit_entry = Entry(root, bd = 3).grid(row=0, column=1) #bd is border. takes an int as pixels
search_label = Label(root, text="Search for:").grid(row=1)
search_entry = Entry(root, bd = 3).grid(row=1, column=1)
search_button = Button(root, text = "Search",
                       command = lambda: find_stuff(subreddit_entry.get(), search_entry.get())
                       ).grid(row=3, columnspan=2)


root.mainloop()
