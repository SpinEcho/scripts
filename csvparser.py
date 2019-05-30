#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import csv
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def year_change(_pop_list, _years, _index):
    slice_start = (_years[0] - 1950) + 1
    slice_end = (_years[-1] - 1950) + 2
    number_years = _years[-1] - _years[1]

    x_data = [str(year) for year in _years]
    y_data = _pop_list[_index][slice_start:slice_end]
    pop_mean = np.mean(y_data)

    ax = plt.subplot()
    plt.title(_pop_list[_index][0])
    plt.xlabel('Årtal')
    ax.bar(x_data, y_data)
    xticks = ax.get_xticks()
    ax.set_xticks(xticks[::5])
    ax.hlines(y=pop_mean, xmin=0, xmax=number_years,
                color='dimgray', linestyle='--')
    plt.show()


def pop_sort(_poplist, _start, _stop, _year):
    _poplist.sort(key=lambda x: x[(_year-1950)+1])
    _poplist.reverse()

    x_data = [row[0] for row in _poplist[_start-1:_stop]]
    y_data = [row[(_year-1950)+1] for row in _poplist[_start-1:_stop]]

    ax = plt.subplot()
    plt.title('Sveriges kommuner på plats {0}-{1} år {2}'.format(_start, _stop, _year))
    plt.xlabel('Kommuner')
    ax.bar(x_data, y_data)
    plt.show()


def change_to_int(temp_list):
    for i in range(len(temp_list)):
        for j in range(1, len(temp_list[i])):
            temp_list[i][j] = int(temp_list[i][j])
    return temp_list


def csv_read(_file):
    with open(_file, newline='') as csv_file:
        temp_list = []
        out = csv.reader(csv_file, delimiter=' ', quotechar='|')
        for row in out:
            if len(row) == 2:
                row[0] = ' '.join([row[0], row[1]])
                del(row[1])
            temp_str = row[0].replace('\xa0', '')
            temp_list.append(temp_str.split(','))
    return temp_list

ap = argparse.ArgumentParser()
ap.add_argument('-s', '--sort', nargs=3, help='Sorterar kommuner i befolkningsordning')
ap.add_argument('-k', '--kommun', nargs=3, help='Visar kommunens befolkning')
args = ap.parse_args()

csv_file = '/home/ulf/bef.csv'
input_list = csv_read(csv_file)
year_list = input_list[0]
pop_list = change_to_int(input_list[1:])
name_list = [row[0] for row in pop_list]

if args.kommun:
    try:
        name_index = name_list.index(args.kommun[0])
    except ValueError:
        print('Ingen giltig kommun')
        sys.exit()

    start_year = int(args.kommun[1])
    end_year = int(args.kommun[2])
    if start_year not in range(1950, 2018) or end_year not in range(1950, 2018):
        print('Felaktigt årtal')
        sys.exit()

    years = [year for year in range(start_year,
             end_year+1)]
    year_change(pop_list, years, name_index)

if args.sort:
    start = int(args.sort[0])
    stop = int(args.sort[1])
    year = int(args.sort[2])
    pop_sort(pop_list, start, stop, year)
# options = vars(args)
