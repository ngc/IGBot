# Copyright (C) 2020 Nathan Coulas
# 
# This file is part of IGBot.
# 
# IGBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# IGBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with IGBot.  If not, see <http://www.gnu.org/licenses/>.

import time
import datetime
import math
import random

class Waiter:

    def __init__(self, peak_hour=3600, multiplier=25):
        self.peak_hour = peak_hour
        self.multiplier = multiplier
        self.loglist = []
        self.activity = 1 #Ranges from 0 - 1

    def add(self, timestamp, magnitude):
        self.loglist.append({'timestamp': timestamp, 'magnitude': magnitude})

    def calculate_activity(self):
        now = datetime.datetime.now()
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        timestamp = (now - midnight).seconds
        k = -0.4
        d = 6.3
        r = 1
        c = 3600
        r = r/4.6211
        self.activity = -(1 + k) * math.sin((((d*c)/(24*c)) * (timestamp/3600) - r - 7.9)) - k
        self.activity = 1 - self.activity

    def get_noise(self):
        return random.random() * self.activity * self.multiplier

    def wait(self):
        """Organic waiting function that avoids rate-limiting"""
        self.calculate_activity()
        magnitude = self.activity * self.multiplier + self.get_noise()

        timestamp = time.time
        print("Waiting for {0} seconds.".format(magnitude))
        time.sleep(magnitude)
        self.add(timestamp, magnitude)