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

from src.core import driver as drv
from src.core import wait

class Session:
    """A botted Instagram session.

    A session can be manipulated and controlled through various methods. 
    These methods use a selenium webdriver to execute actions needed to interact with Instagram as a service. 
    Routines can also be defined 

    """

    def __init__(self, username, password, args=[]):
        """

        Args:
            username ([type]): [description]
            password ([type]): [description]
            args (list, optional): [description]. Defaults to [].
        """
        self.username = username
        self.password = password


    def start(username, password, args=[], routine):
        """Starts a botted Instagram session.

        Args:
            username (string): username for account session.
            password (string): password for account session
            args (list, optional): Arguments. Defaults to an empty list (not required).
        """
        driver = drv.get_driver()
        driver.get("https://www.google.com")
    
