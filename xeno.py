#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request


def download(_data, _dirname, _bird):
        counter = 0
        for item in _data['recordings']:
            if item['type'] == 'song':
                counter += 1
                urllib.request.urlretrieve(
                    'http:{0}'.format(item['file']),
                    '{0}/{1}_{2}.mp3'.format(_dirname, _bird, counter))


def get_birds(_bird, _country):
        url = 'http://www.xeno-canto.org/api/2/recordings?'
        params = urllib.parse.urlencode(
            {'query': 'cnt:{0} {1}'.format(_country, _bird)})
        response = urllib.request.urlopen('{0}{1}'.format(url, params)).read()
        return json.loads(response)


def make_dir(_dirname):
        if not os.path.isdir(_dirname):
            subprocess.run('mkdir', '{0}'.format(_dirname))

country = sys.argv[1]
bird = sys.argv[2]
dirname = '/home/ulf/fåglar/{0}'.format(bird.replace(' ', '_'))

data = get_birds(bird, country)
make_dir(dirname)
download(data, dirname, bird)
