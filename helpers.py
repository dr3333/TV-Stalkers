import PySimpleGUI as sg
import requests
import datetime


def search_title(title):
    try:
        url = f"https://www.episodate.com/api/search?q={title}&page=1"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        sg.popup('Unable to Connect to Server', 'Please try again later')
        return None
    try:
        t_i = response.json()
        title_info = []
        for aa in t_i["tv_shows"]:
            t_row = {
                "name": aa["name"],
                "id": aa["id"]
            }
            title_info.append(t_row)
    except (KeyError, TypeError, ValueError):
        return None
    return title_info
    # student = [list(d.values()) for d in students]


def add_title(title_id):
    try:
        url = f"https://www.episodate.com/api/show-details?q={title_id}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        sg.popup('Unable to Connect to Server', 'Please try again later')
        return None
    try:
        t_i = response.json()
        title_info = {
            'name': t_i["tvShow"]["name"],
            'id': t_i["tvShow"]["id"],
            'season_episode': t_i["tvShow"]["countdown"]
        }
    except (KeyError, ValueError):
        sg.popup('Error JSONIFYing Response', 'Please try again')
        return None

    new_data = {}

    new_data['name'] = title_info['name']
    new_data['id'] = title_info['id']
    if title_info['season_episode'] is None:
        new_data['season_episode'] = 'Ended'
        new_data['airdate'] = 'Ended'
    else:
        new_data['season_episode'] = f"S {title_info['season_episode']['season']} : Ep {title_info['season_episode']['episode']}"
        new_data['airdate'] = f"{title_info['season_episode']['air_date']}"

    return new_data


def distinct_list(watchlist, data):
    wl_len = len(watchlist)
    for row in range(wl_len):
        if watchlist[row]['id'] == data['id']:
            watchlist[row].update(data)
            return watchlist
    watchlist.append(data)
    watchlist.sort(key=lambda x: x['airdate'])
    return watchlist


def auto_update(watchlist):
    wl_len = len(watchlist)
    for row in range(wl_len):
        wl_id = watchlist[row]['id']
        data0 = add_title(wl_id)
        watchlist[row].update(data0)
    watchlist.sort(key=lambda x: x['airdate'])
    return watchlist


def update_datetime(watchlist):
    wl_len = len(watchlist)
    for row in range(wl_len):
        data = watchlist[row]['airdate']
        if data != 'Ended':
            diff = get_time(data)
            if diff is not None:
                watchlist[row]['timetildrop'] = diff
            elif diff is None:
                watchlist[row]['timetildrop'] = 'Released'
    wl = [list(d.values()) for d in watchlist]
    return wl


def get_time(airdate):
    timenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start = datetime.datetime.strptime(timenow, '%Y-%m-%d %H:%M:%S')
    ends = datetime.datetime.strptime(airdate, '%Y-%m-%d %H:%M:%S')
    diff = (ends - start)
    if ends > start:
        return diff
    else:
        return 'Released'
