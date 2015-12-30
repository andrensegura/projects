#!/usr/bin/python
import json
from config import STEAM_KEY


def get_steam_json(url):
    from StringIO import StringIO
    import pycurl

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
            try:
                game_id = inventory_json['rgDescriptions'][key]['actions'][0]['link'].split('/')[-2]
            except KeyError:
                game_id = ""
            game_info = get_game_info(game_id)
            games_list.append(game_info)
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
    profile_link = profile_json['response']['players'][0]
    return profile_link


# This returns a list of games found by steams search function
# list structure is [title, id, img]
def steam_search(query):
    from lxml import html, etree
    import requests

    all_games = []
    url = "http://store.steampowered.com/search/?term=%s" % (query)
    page = requests.get(url)
    tree = html.fromstring(page.content)

    app_data = tree.xpath('//div[@id="search_result_container"]/div/a')

    for app in app_data:
        app_id = app.get("data-ds-appid").encode('ascii', 'ignore')
        app_img = next(app.iter("img")).get("src").encode('ascii', 'ignore')
        app_title = next(app.iter("span")).text.encode('ascii', 'ignore')
        all_games.append([app_title, app_id, app_img])

    return all_games

def get_game_info(id):
    from lxml import html, etree
    import requests

    url = "http://store.steampowered.com/app/%s/" % (id)

    game_info = []
    page = requests.get(url)
    tree = html.fromstring(page.content)

    try:
        title = tree.xpath('//div[@class="apphub_AppName"]/text()')[0]
        game_info.append(title.encode('ascii', 'ignore'))
    
        game_info.append(id)
    
        img = tree.xpath('//img[@class="game_header_image_full"]')[0].get("src")
        game_info.append(img.encode('ascii', 'ignore'))
    except:
        pass
    return tuple(game_info)


