#!/usr/bin/python
import pycurl, json
from StringIO import StringIO


def get_inventory_json(url):
    buffer = StringIO()
    c= pycurl.Curl()
    #must have inventory settings set to public and "keep steam gift inventory private"  unchecked
    c.setopt(c.URL, url) 
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()
    c.close()

    json = buffer.getvalue()
    return json


def get_inventory(profile_link):
    if not profile_link:
        return []
    
    inventory_link = "%s/inventory/json/753/1" % (profile_link)
    try:
        inventory_json = json.loads(get_inventory_json(inventory_link))
    except:
        return []
    games_list = []
    for key in inventory_json['rgDescriptions']:
        game_title = inventory_json['rgDescriptions'][key]['name']
        try:
            game_link = inventory_json['rgDescriptions'][key]['actions'][0]['link']
        except KeyError:
            game_link = ""
        games_list.append((game_title, game_link))
    games_list.sort()
    return games_list
