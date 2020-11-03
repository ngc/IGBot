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

import os
import json
from dotenv import load_dotenv
load_dotenv()

class Database(object):

    def __init__(self, username, BASE_DIR):
        """Initializes files and database for database object on creation"""
        self.name = username
        self.BASE_DIR = BASE_DIR
        self.directory = self.init_directory()
        os.chdir(self.directory)
        if(not os.path.isfile('targets.json')):
            self.database = self.save({})
            print("DATABASE CREATED")
        else:
            self.database = self.directory + '/targets.json'
            print("EXISTING DATABASE LOCATED")
    
    def base_dir(self):
        os.chdir(self.BASE_DIR)

    def init_directory(self):
        self.base_dir()
        if(not os.path.exists("users")): os.mkdir("users/")
        os.chdir("users")
        if(not os.path.exists(self.name)): os.mkdir(self.name)
        os.chdir(self.name)
        return os.getcwd()

    def save(self, dict):
        os.chdir(self.directory)
        with open('targets.json', 'w') as fp:
            json.dump(dict, fp, sort_keys=True, indent=4)
        return self.directory + '/targets.json'

    def load(self):
        os.chdir(self.directory)
        with open('targets.json', 'r') as fp:
            return json.load(fp)



