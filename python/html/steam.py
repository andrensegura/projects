#!/usr/bin/python
import pycurl, json
from StringIO import StringIO


STEAM_KEY = "F5A08C50EEFCE8675A2DD909C6F05EEB"

def get_steam_json(url):
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
        inventory_json = json.loads(get_steam_json(inventory_link))
    except:
        return []
    games_list = []
    try:
        for key in inventory_json['rgDescriptions']:
            game_title = inventory_json['rgDescriptions'][key]['name']
            try:
                game_link = inventory_json['rgDescriptions'][key]['actions'][0]['link']
            except KeyError:
                game_link = ""
            games_list.append((game_title, game_link))
        games_list.sort()
        return games_list
    except:
        return []

def get_profile(steam_id_64):
    #you can find your 64bit id here: https://steamid.io/lookup
    link = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%s" \
            % (STEAM_KEY, steam_id_64)
    try:
        profile_json = json.loads(get_steam_json(link))
    except:
        return ""

    # lots of stuff can be found in this!
    profile_link = profile_json['response']['players'][0]['profileurl']
    return profile_link
