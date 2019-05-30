#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import json
import shlex
import subprocess
import urllib.parse
import urllib.request
from sys import exit

# Huvudfunktioner

def download(name):
    get_result('info', name, False)
    subprocess.run(['mkdir', '/home/ulf/AUR/{}'.format(name)])
    subprocess.run(['git', 'clone', 'https://aur.archlinux.org/{}.git'.format(name), '/home/ulf/AUR/{}'.format(name)])


def install(package):
    command = shlex.split('makepkg -ci')
    subprocess.run(command,cwd='/home/ulf/AUR/{}'.format(package))

def list_packages():
    results = pacman_search_foreign()
    print()
    print('Installerade paket:')
    print('-------------------')
    for line in results:
        print(line)


def query(name):
    info_list = pacman_query_package(name)
    headings_of_interest = ['Namn', 'Beroende för', 'Beskrivning',
                            'Installerades', 'Orsak', 'Version']
    sorted_list = [line for heading in headings_of_interest
                   for line in info_list if heading in line]
    for line in (sorted_list):
        print(line)


def search(_search_type, name):
    result = get_result(_search_type, name, True)
    number_hits(result)
    fields = result['results']
    swe_translate = {'Description': 'Beskrivning',
                     'Name': 'Namn',
                     'URL': 'Hemsida',
                     'Version': 'Version'}

# Om exakt sökning ger träff får man ensam dictionary, flytta till lista
    if _search_type == 'info':
        fields = [fields]

    print()
    for field in fields:
        for key, swe_values in swe_translate.items():
            print(swe_values, ':', field[key])
        print('Senast uppdaterad: ' + conversion(field['LastModified']))


def update():
    name_list = pacman_search_foreign()
    update_list = []

    for name in name_list:
        git_pull = subprocess.run(['git', 'pull', 'https://aur.archlinux.org/{}.git'.format(name)],
                                  cwd='/home/ulf/AUR/{}'.format(name), stdout=subprocess.PIPE, text=True).stdout
        if 'Redan' in git_pull:
            print('Uppdaterad')
        if 'Uppdaterar' in git_pull:
            update_list.append(name)
        
        print()

    if update_list:
        print('Uppdaterat:')
        for update in update_list:
            print(update)

# Hjälpfunktioner


def check_error(_result):
    if _result['type'] == 'error':
        print('Felmeddelande: ' + _result['results'])
        exit()

    elif _result['resultcount'] == 0:
        print('Sökningen gav inga resultat')
        exit()


def conversion(seconds):
    return subprocess.run(['date', '--date', '@' + str(seconds), '+%Y-%m-%d %X'],
                          stdout=subprocess.PIPE, text=True).stdout


def get_result(_search_type, name, output):
    url = 'https://aur.archlinux.org/rpc/'
    params = urllib.parse.urlencode({'type': _search_type, 'arg': name})
    response = urllib.request.urlopen('{0}?{1}'.format(url, params)).read()
    check_error(json.loads(response))
    if output:
        return json.loads(response)


def number_hits(results):
    if results['resultcount'] > 1:
        while True:
            cont_search = input('Sökningen gav {} träffar. Vill du forsätta? (j/n) '.format(results['resultcount']))

            if cont_search.startswith('n'):
                exit()

            if cont_search.startswith('j'):
                break


def pacman_query_package(name):
    return subprocess.run(['pacman', '-Qi', name], stdout=subprocess.PIPE, text=True).stdout.splitlines()


def pacman_search_foreign():
    p1 = subprocess.Popen(['pacman', '-Qm'], stdout=subprocess.PIPE)
    return subprocess.run(['awk', '{print $1}'], stdin=p1.stdout, stdout=subprocess.PIPE, text=True).stdout.splitlines()


ap = argparse.ArgumentParser()
ap.add_argument('-u', '--update', action='store_true',
                help='Kollar om installerade paket behöver uppdateras')

ap.add_argument('-s', '--search',
                help='Söker efter paket i AUR')

ap.add_argument('-i', '--install',
                help='Installerar paket från AUR')

ap.add_argument('-ss', '--searchexact',
                help='Söker efter paket i AUR med exakt matchning')

ap.add_argument('-d', '--download',
                help='Laddar ner paket från AUR')

ap.add_argument('-q', '--query',
                help='Kort beskrivning av installerat paket')

ap.add_argument('-l', '--list_packages', action='store_true',
                help='Listar installerade paket')

args = ap.parse_args()
# options = vars(args)

if args.download:
    download(args.download)

if args.install:
    install(args.install)

if args.list_packages:
    list_packages()

if args.query:
    query(args.query)

if args.search:
    search_type = 'search'
    search(search_type, args.search)

if args.searchexact:
    search_type = 'info'
    search(search_type, args.searchexact)

if args.update:
    update()
