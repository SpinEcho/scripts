#!/usr/bin/python
# -*- coding: utf-8 -*- #

import subprocess

p1 = subprocess.Popen(['pacman', '-Qm'], stdout=subprocess.PIPE)
p2 = subprocess.run(['awk', '''{print $1}'''], stdin=p1.stdout,
                    stdout=subprocess.PIPE, text=True)
package_list = p2.stdout.splitlines()

for name in package_list:
    url = 'https://aur.archlinux.org/{0}.git'.format(name)
    dir = '/home/ulf/AUR/' + name
    subprocess.run(['mkdir', '/home/ulf/AUR/' + name])
    subprocess.run(['git', 'clone', url, dir], cwd='/home/ulf/AUR')
