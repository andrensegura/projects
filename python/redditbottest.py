#! /usr/bin/python

import praw
import pprint

user_agent = "Module testing for /u/bibbleskit"
r = praw.Reddit(user_agent=user_agent)

user_name = "pseudogenesis"
user = r.get_redditor(user_name)

thing_limit = None
gen = user.get_submitted(limit=thing_limit)

karma_by_subreddit = {}
for thing in gen:
    subreddit = thing.subreddit.display_name
    karma_by_subreddit[subreddit] = (karma_by_subreddit.get(subreddit, 0) + thing.score)

for item in karma_by_subreddit:
    print "%s: %d" % (item, karma_by_subreddit.get(item))
