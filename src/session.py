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
from src.core.wait import Waiter
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *

class Session:
    """A botted Instagram session.

    A session can be manipulated and controlled through various methods. 
    These methods use a selenium webdriver to execute actions needed to interact with Instagram as a service. 
    Routines can also be defined 

    """

    def __init__(self, username, password, args=[]):
        """

        Args:
            username (string): Account username.
            password (string): Account password.
            args (list, optional): Arguments. Defaults to [].
        """
        self.waiter = Waiter()
        self.username = username
        self.password = password
        self.driver = drv.make_driver()
        self.login(username, password)
        
    
    def wait(self, multiplier=1):
        self.waiter.wait(multiplier)

    def login(self, username, password, args=[]):
        """Logs into the Instagram account for the session.

        Args:
            username ([type]): Account username.
            password ([type]): Account password.
            args (list, optional): The arguments. Defaults to [].
        """
        self.driver.get("https://www.instagram.com/")
        self.wait()
        self.driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
        self.driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
        self.driver.find_element_by_xpath("//button[contains(.,'Log In')]").click()
        self.wait(2)

    def follow(self, username):
        try:
            self.driver.get("https://www.instagram.com/{0}/".format(username))
            self.wait()
            self.driver.find_element_by_xpath("//button[contains(.,'Follow')]").click()
        except NoSuchElementException:
            print("ERROR: Already Following")