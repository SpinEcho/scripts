#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import shlex
import sys

fi = sys.argv[1] #MIDI-fil att konvertera
fo = fi.split(".")[0] + ".ogg"

command = shlex.split('timidity {0} -Ov -o {1}'.format(fi, fo))
subprocess.run(command)
