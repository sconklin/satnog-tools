#!/usr/bin/env python

# Author: Steve Conklin, AI4QR <steve@conklinhouse.com>
# Copyright (C) 2015
#
# This script is distributed under the terms and conditions of the GNU General
# Public License, Version 3 or later. See http://www.gnu.org/copyleft/gpl.html
# for details.

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import json
import os
import errno
from os.path import expanduser

def get_data(url):
    response = urlopen(url)
    data = str(response.read())
    return json.loads(data)

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

class SatnogsDb:
    """Class to wrap the satnogs db."""
    def __init__(self, url = "https://db.satnogs.org/api/", cache = False):
        """Init and optionally set a URL"""
        self.baseurl = url
        self.cached = False
        load_from_satnogs = False
        if cache:
            print "Cache is True"
            cachepath = expanduser("~") + "/.cache/satnogsdb"
            if os.path.isfile(cachepath + "/transmitters"):
                with open(cachepath + "/transmitters", 'r') as jf:
                    self.cached_t = json.load(jf)
            else:
                print "transmitter cache not present"
                load_from_satnogs = True

            if (load_from_satnogs is False) and os.path.isfile(cachepath + "/satellites"):
                with open(cachepath + "/satellites", 'r') as jf:
                    self.cached_s = json.load(jf)
            else:
                print "satellite cache not present"
                load_from_satnogs = load_from_satnogs or True

        if (load_from_satnogs):
            print "Hitting Website"
            mkdir_p(cachepath)
            print "Getting data into cache"
            self.cached_t = self.transmitters()
            self.cached_s = self.satellites()
            with open(cachepath + "/transmitters", 'w') as out:
                json.dump(self.cached_t, out)
            with open(cachepath + "/satellites", 'w') as out:
                json.dump(self.cached_s, out)

        self.cached = cache


    def transmitters(self):
        """Load the transmitters from the db"""
        if self.cached:
            print "returning cached transmitter data"
            return self.cached_t

        try:
            json_data = get_data(self.baseurl + "transmitters")
            return json_data
        except:
            return False

    def satellites(self):
        """Load the satellites from the db"""
        if self.cached:
            print "returning cached satellite data"
            return self.cached_s

        try:
            json_data = get_data(self.baseurl + "satellites")
            return json_data
        except:
            return False

