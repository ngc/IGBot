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

from src.session import Session
import atexit
from src.core import interface

interface.print_logo()

args = {'BASE_DIR': "/home/nathan/Development/IGBot"}
main = Session('leah.g4361', 'U0luj8N6&4Ei', args)

database = main.database
following = database.load("following")

if(following == {}):
    following_list = main.get_following(main.username)
    for user in following_list:
        following[user] = {"lol":"lol"}
    database.save(following, "following")
else:
    following_list = []
    for item in following.keys():
        following_list.append(item)

for item in following_list[:50]:
    main.unfollow(item)
    following.pop(item, None)
    database.save(following, "following")