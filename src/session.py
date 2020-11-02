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
from selenium.common.exceptions import NoSuchElementException
from explicit import waiter, XPATH
from bs4 import BeautifulSoup
from src.urls import INSTAGRAM
import itertools
import locale
from src.data import Database
from dotenv import load_dotenv
load_dotenv()

class Session:
    """A botted Instagram session.

    A session can be manipulated and controlled through various methods. 
    These methods use a selenium webdriver to execute actions needed to interact with Instagram as a service. 
    """

    def __init__(self, username, password, args=[]):
        """Initialize Session.

        Args:
            username (string): Account username.
            password (string): Account password.
            args (list, optional): Arguments. Defaults to [].
        """
        self.waiter = Waiter(6.75)
        self.username = username
        self.password = password
        self.driver = drv.make_driver()
        self.server_database = Database(self.username)
        self.login(username, password)
        
    
    def wait(self, multiplier=1):
        """Triggers an organic waiting time with an optional multiplier. 

        Args:
            multiplier (int, optional): Multiplies the organic wait. Defaults to 1.
        """
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
        """Follows a user.

        Args:
            username (string): The target's username.
        """
        try:
            self.driver.get("https://www.instagram.com/{0}/".format(username))
            self.wait()
            self.driver.find_element_by_xpath("//button[contains(.,'Follow')]").click()
        except NoSuchElementException:
            print("ERROR: Already Following")

    def unfollow(self, username):
        try:
            self.driver.get("https://www.instagram.com/{0}/".format(username))
            self.wait()
            self.driver.find_elements_by_css_selector("[aria-label=Following]")[0].click()
            self.wait(0.5)
            self.driver.find_element_by_xpath("//button[contains(.,'Unfollow')]").click()
        except NoSuchElementException:
            print("ERROR: Already Following")
    
    def get_followers(self, username):
        followers = []
        self.driver.get(INSTAGRAM.format(username))
        self.wait()
        done = 0
        while done < 3:
            done += 1
            try:
                self.wait()
                self.driver.find_element_by_css_selector("#react-root > section > main > div > header > section > ul > li:nth-child(2) > a").click()
                done = 3
            except:
                print("Retrying...")

        self.wait()

        follower_css = "ul div li:nth-child({0}) a.notranslate"
        for group in itertools.count(start = 1, step = 12):
            try:
                for follower_index in range(group, group + 12):
                    user = self.driver.find_element_by_css_selector(follower_css.format(follower_index)).text
                    if user != self.username:
                        followers.append(user)
                
                last_follower = self.driver.find_element_by_css_selector(follower_css.format(follower_index))
                self.driver.execute_script("arguments[0].scrollIntoView();", last_follower)
            except:
                break
            return followers

    def get_following(self, username):
        following = []
        self.driver.get(INSTAGRAM.format(username))
        self.wait()
        done = 0
        while done < 3:
            done += 1
            try:
                self.wait()
                self.driver.find_elements_by_class_name("-nal3 ")[2].click()
                done = 3
            except:
                print("Retrying...")

        self.wait()

        follower_css = "ul div li:nth-child({0}) a.notranslate"
        for group in itertools.count(start = 1, step = 12):
            try:
                for follower_index in range(group, group + 12):
                    user = self.driver.find_element_by_css_selector(follower_css.format(follower_index)).text
                    following.append(user)
                
                last_follower = self.driver.find_element_by_css_selector(follower_css.format(follower_index))
                self.driver.execute_script("arguments[0].scrollIntoView();", last_follower)
            except:
                break
        return following


    def get_follower_count(self, username):
        self.driver.get(INSTAGRAM.format(username))
        self.wait(0.2)
        followers_string = self.driver.find_elements_by_class_name("g47SY ")[1].text
        return int(followers_string.replace(',', ''))

    def get_following_count(self, username):
        self.driver.get(INSTAGRAM.format(username))
        self.wait(0.2)
        following_string = self.driver.find_elements_by_class_name("g47SY ")[2].text
        return int(following_string.replace(',', ''))

    def get_worth(self, username):
        #following / followers
        following = self.get_following_count(username)
        followers = self.get_follower_count(username)
        return following / followers