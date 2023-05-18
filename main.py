import PySimpleGUI as sg
from json import (load as jsonload, dump as jsondump)
from os import path
from datetime import date
from helpers import search_title, add_title, distinct_list, get_time
from icons import title_bar_icon

TITLE_BAR_ICON = title_bar_icon
# Headings for main window table
headings = ['Title', 'id', 'Season/Episode', 'Release Date']
# Save File JSON
DATA_FILE = path.join(path.dirname(__file__), r'data.json')
# Theme
sg.theme('TealMono')


def load_data(data_file):
    try:
        with open(data_file, 'r') as f:
            data = jsonload(f)
    except (KeyError, TypeError, ValueError):
        data = []
    return data


def save_data(data_file, watchlist):
    try:
        with open(data_file, 'w') as f:
            jsondump(watchlist, f, indent=4)
    except (KeyError, TypeError, ValueError):
        sg.popup('Error SAVING Data')


def main_window():
    layout = [
        [sg.T('Watch List', font='_ 14', justification='c'), sg.Push(),
         sg.T('', key='main_win_date', enable_events=True)],
        [sg.Table(values=[],
                  headings=headings,
                  key='main_watchlist_table',
                  visible_column_map=[True, False, True, True],
                  auto_size_columns=False,
                  col_widths=[30, 1, 12, 15],
                  max_col_width=100,
                  row_height=50,
                  justification='l', background_color='#dcedf7',
                  alternating_row_color='#b1daf2',
                  enable_events=True
                  )],
        [sg.Button('Title Info', key='INFO'), sg.Button('Update'), sg.Button('ADD'), sg.Push(), sg.Button('Delete')]
    ]

    main_win = sg.Window('TV Stalker', layout,
                         auto_size_text=True, auto_size_buttons=True, icon=TITLE_BAR_ICON, grab_anywhere=False, finalize=True)
    return main_win


def search_window():
    layout = [[sg.Text('Search', font='_ 12')],
              [sg.Input(key='query_title', enable_events=True), sg.Button('Search')],
              [sg.Listbox(values=[], select_mode='extended', key='title_info_list', enable_events=True,
                          size=(50, 10))],
              [sg.Button('Clear'), sg.Button('Add to Watchlist'), sg.Button('Exit')]]

    search_win = sg.Window('Search Window', layout, icon=TITLE_BAR_ICON, auto_size_text=True, modal=True, finalize=True)

    return search_win


def info_window(row_info):
    layout = [
        [sg.Text("Name:"), sg.Text(row_info['name'])],
        [sg.Text("ID:"), sg.Text(row_info['id'])],
        [sg.Text("Release Date:"), sg.Text(row_info['airdate'])],
        [sg.Text("Time to Release:"), sg.Text("", key='time_to_release', enable_events=True)]
    ]

    info_win = sg.Window('Title Info', layout, icon=TITLE_BAR_ICON, auto_size_text=True, size=(400, 150), finalize=True)

    # Auto update the time.
    if row_info:
        if row_info['airdate'] != 'Ended':
            while True:
                event, values = info_win.read(timeout=500)
                if event == sg.WIN_CLOSED or event == 'Exit':
                    break
                t = row_info['airdate']
                till_date = get_time(t)
                info_win['time_to_release'].update(till_date)

    return info_win


def load_main_window():
    watchlist = load_data(DATA_FILE)
    wl_len = len(watchlist)

    layout = [[sg.Text('Loading TV Stalker')],
              [sg.ProgressBar(max_value=wl_len + 1, orientation='h', size=(20, 20), key='progress_bar')]]

    load_win = sg.Window('Loading Watchlist', layout, icon=TITLE_BAR_ICON, no_titlebar=True, finalize=True)
    progress_bar = load_win['progress_bar']

    if watchlist:
        for row in range(wl_len):
            wl_id = watchlist[row]['id']
            data0 = add_title(wl_id)
            if data0 is None:
                sg.popup("Error Loading File")
            watchlist[row].update(data0)
            progress_bar.update_bar(row)
        watchlist.sort(key=lambda x: x['airdate'])

    save_data(DATA_FILE, watchlist)  # Save updated File
    progress_bar.update_bar(wl_len + 1)

    load_win.close()


def main():
    load_main, main_win, search_win, info_win = None, None, None, None

    watchlist_array = []
    search_array = []

    while True:
        if main_win is None:
            load_main_window()
            watchlist_array = load_data(DATA_FILE)  # Load Data into watchlist
            wl = [list(d.values()) for d in watchlist_array]  # turn dict into a list
            date_today = date.today()
            main_win = main_window()
            main_win['main_win_date'].update(date_today)
            main_win['main_watchlist_table'].update(wl)

        window, event, values = sg.read_all_windows(timeout=500)
        if event == sg.WIN_CLOSED or event == 'Exit':
            window.close()
            if window == search_win:  # if closing search_win, mark as closed
                search_win = None
            if window == info_win:  # if closing search_win, mark as closed
                info_win = None
            elif window == main_win:  # if closing main_win, exit program
                break

        #################### For Main Window ###########################
        if event == 'ADD' and not search_win:
            search_win = search_window()
        if event == 'Delete':  # Delete, Update and Save new list
            d_title_index = values['main_watchlist_table']
            if d_title_index:
                watchlist_array.pop(d_title_index[0])
                user_wl = [list(d.values()) for d in watchlist_array]
                main_win['main_watchlist_table'].update(user_wl)
                save_data(DATA_FILE, watchlist_array)
            else:
                sg.popup("Select a title")
        if event == 'Update':
            d_title_index = values['main_watchlist_table']
            if d_title_index:
                tt_id = watchlist_array[d_title_index[0]]
                title_id = tt_id['id']
                wl = add_title(title_id)
                watchlist_array = distinct_list(watchlist_array, wl)
                wl = [list(d.values()) for d in watchlist_array]  # turn dict into a list
                main_win['main_watchlist_table'].update(wl)  # update the main windows table with information
                save_data(DATA_FILE, watchlist_array)
            else:
                sg.popup("Select a Title")
        if event == 'INFO':
            info_win = None  # close info window if user clicks a new row
            d_title_index = values['main_watchlist_table']
            if d_title_index:
                wl_info_win = watchlist_array[d_title_index[0]]
                info_win = info_window(wl_info_win)
            else:
                sg.popup("Select a Title")

        #################### Make Request to Api (Search using input) ############################
        if event == 'Search' and search_win['query_title']:
            if values['query_title']:
                search_tt = search_title(values['query_title'])
                if search_tt is None:
                    sg.popup("Search Failed")
                else:
                    search_array = search_tt
                    s_tt = [d["name"] for d in search_array]
                    window['title_info_list'].update(s_tt)
            else:
                sg.popup("Please input a title")

        #################### Add Selected title to list And Save ################################
        if event == 'Add to Watchlist':
            title_selected = values['title_info_list']
            if title_selected:
                listbox_index = window['title_info_list'].get_indexes()[0]
                title_id = search_array[listbox_index]['id']
                wl_array = add_title(title_id)  # search for title using id
                watchlist_array = distinct_list(watchlist_array, wl_array)  # add dict to DISTINCT list of watchlist
                wl = [list(d.values()) for d in watchlist_array]  # turn dict into a list
                main_win['main_watchlist_table'].update(wl)  # update the main windows table with information
                save_data(DATA_FILE, watchlist_array)
            else:
                sg.popup("Input Title")
        if event == 'Clear':
            search_win['query_title'].update('')
            window['title_info_list'].update('')

    window.close()


if __name__ == '__main__':
    main()
