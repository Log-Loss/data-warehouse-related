import json
import pandas as pd
import csv
import os
import glob
import copy
import re
import shutil


def search_format(format_text, format_lists):
    if len(format_lists) < 1:
        format_lists = ['Audio CD', 'VHS Tape', 'Amazon Video', 'Blu-ray', 'DVD', '3D', '4K', 'Multi-Format',
                        'Prime Video']

    striped = format_text.replace('\n', '').replace('  ', '')
    found = []
    for item in format_lists:
        if striped.find(item) != -1:
            found.append(item)
    return found


def parse_star_views(avg_review_list):
    try:
        star, views = avg_review_list[0].split()[0], avg_review_list[1].split()[0]
        return star, views.replace(',', '')
    except:
        return None, None

def parse_title(title):
    try:
        title = title.split('\n')

        return title[0].replace(',', '_COMMA_')
    except:
        return None


def parse_runtime(runtime_list):
    try:
        if 'minutes' in runtime_list[0]:
            runtime = runtime_list[0].replace('minutes', '').replace(' ', '')
            return runtime
        if 'seconds' in runtime_list[0]:
            runtime = int( runtime_list[0].replace('seconds', '').replace(' ', '') ) / 60
            return runtime
        return runtime_list[0]
    except:
        return runtime_list[0]

def parse_Release_Date(Release_Date_list):
    try:
        release_day,release_month,release_year=Release_Date_list[0].replace(',','').split()[1],Release_Date_list[0].split()[0],Release_Date_list[0].replace(',','').split()[2]
        return release_year,release_month,release_day
    except:
        return None, None, None


def format_json(json_text, key_list, format_list):
    output = {}
    try:
        output['other-format'] = '&&'.join(search_format(json_text['other-format'], format_list))
        output['star'], output['views'] = parse_star_views(json_text['Average Customer Review:'])

    except:
        pass

    try:
        output['Run Time'] = parse_runtime(json_text['Run Time:'])
    except:
        pass

    try:
        if 'DVD Release Date:' in json_text:
            output['Release Year'], output['Release Month'], output['Release Day'] = parse_Release_Date(
                json_text['DVD Release Date:'])
        # json_text.pop('DVD Release Date:')
        else:
            output['Release Year'], output['Release Month'], output['Release Day'] = parse_Release_Date(
                json_text['VHS Release Date:'])
            #             json_text.pop('VHS Release Date:')
    except:
        pass

    if 'MPAA rating:' in json_text:
        json_text['Rated'] = json_text['MPAA rating:']


    if 'Directors:' in json_text:
        json_text['Director'] = json_text['Directors:']

    if 'Starring' in json_text:
        json_text['Actors'] = json_text['Starring']

    if 'title' in json_text:
        output['title'] = parse_title(json_text['title'])

    if len(key_list) < 1:
        key_list = ['ASIN', 'Actors', 'Director', 'Format',
                    'Genres', 'Language', 'Rated',
                    'Region', 'Studio', 'Supporting actors',
                    'Writers', 'imdb', 'img']

    for key in json_text.keys():
        if key.strip(':') not in key_list:
            continue

        content = json_text[key]
        if type(content) == list:
            output[key.strip(':')] = '&&'.join(content)
        else:
            output[key.strip(':')] = content

    return output