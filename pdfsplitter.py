#!/usr/bin/python
# -*- coding: utf-8 -*-

import shlex
import subprocess
import sys

fi = sys.argv[1] #pdf man vill dela upp
first_page = sys.argv[2] #första sida i intervallet
last_page = sys.argv[3] #sista sidan in intervallet
fo = sys.argv[4] #namn på filen man sparar till

command = shlex.split('gs -sDEVICE=pdfwrite -q -dBATCH -dNOPAUSE -dFirstPage={0} -dLastPage={1} -sOutputFile={2} {3}'.format(first_page, last_page, fo, fi))
subprocess.run(command)
