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
from bs4 import BeautifulSoup
from src.urls import INSTAGRAM
import itertools
import locale
import requests
from src.data import Database
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
load_dotenv()

class Session:
    """A botted Instagram session.

    A session can be manipulated and controlled through various methods. 
    These methods use a selenium webdriver to execute actions needed to interact with Instagram as a service. 
    """

    def __init__(self, username, password, args={}):
        """Initialize Session.

        Args:
            username (string): Account username.
            password (string): Account password.
            args (list, optional): Arguments. Defaults to [].
        """
        self.waiter = Waiter(23)
        self.username = username
        self.password = password
        self.driver = drv.make_driver()
        self.database = Database(self.username, args["BASE_DIR"])
        self.login(username, password)
        
        #Data Dictionaries
        self.follows_data = self.database.load("follows")
        
    
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

            self.follows_data[username] = {'timestamp': time.time(), 'followed_back': False}
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
        following_count = self.get_followers_following(username)[0]
        following = []
        self.driver.get(INSTAGRAM.format(username))
        # Click the 'Follower(s)' link
        self.driver.find_element_by_partial_link_text("follower").click()

        # Wait for the followers modal to load
        xpath = "/html/body/div[4]/div/div/div[2]/div/div[2]"
        self.wait()

        SCROLL_PAUSE = 0.5  # Pause to allow loading of content
        self.driver.execute_script("followersbox = document.getElementsByClassName('isgrP')[0];")
        last_height = self.driver.execute_script("return followersbox.scrollHeight;")

        # We need to scroll the followers modal to ensure that all followers are loaded
        while True:
            self.driver.execute_script("followersbox.scrollTo(0, followersbox.scrollHeight);")

            # Wait for page to load
            time.sleep(2.5)

            # Calculate new scrollHeight and compare with the previous
            new_height = self.driver.execute_script("return followersbox.scrollHeight;")
            if new_height == last_height:
                break
            last_height = new_height

        # Finally, scrape the followers
        source = self.driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        user_elements = soup.findAll("a", {"class": "FPmhX"})

        for element in user_elements:
            following.append(element.text)
            
        return following

    def get_following(self, username):
        following_count = self.get_followers_following(username)[0]
        following = []
        self.driver.get(INSTAGRAM.format(username))
        # Click the 'Follower(s)' link
        self.driver.find_element_by_partial_link_text("following").click()

        # Wait for the followers modal to load
        xpath = "/html/body/div[4]/div/div/div[2]/div/div[2]"
        self.wait()

        SCROLL_PAUSE = 0.5  # Pause to allow loading of content
        self.driver.execute_script("followersbox = document.getElementsByClassName('isgrP')[0];")
        last_height = self.driver.execute_script("return followersbox.scrollHeight;")

        # We need to scroll the followers modal to ensure that all followers are loaded
        while True:
            self.driver.execute_script("followersbox.scrollTo(0, followersbox.scrollHeight);")

            # Wait for page to load
            time.sleep(2.5)

            # Calculate new scrollHeight and compare with the previous
            new_height = self.driver.execute_script("return followersbox.scrollHeight;")
            if new_height == last_height:
                break
            last_height = new_height

        # Finally, scrape the followers
        source = self.driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        user_elements = soup.findAll("a", {"class": "FPmhX"})

        for element in user_elements:
            following.append(element.text)
            
        return following


    def get_followers_following(self, username):
        try:
            page = requests.get(INSTAGRAM.format(username))

            soup = BeautifulSoup(page.text, 'html.parser')
            results = soup.find("meta", property="og:description")
            meta_string = results["content"]

            number_string = ""
            index = 0
            for char in meta_string:
                if(char == ' '): break
                number_string += char
                index += 1
            followers = max(int(number_string.replace(',', '')), 1)

            number_string = ""
            index = meta_string.find(', ') + 2
            for char in meta_string[index:]:
                if(char == ' '): break
                number_string += char
            following = max(int(number_string.replace(',', '')), 1)

            return (followers, following)
        except:
            return (1, 1)

    def get_worth(self, username):
        #following / followers
        followers, following = self.get_followers_following(username)
        return following / followers

    def close(self):
        self.database.save(self.follows_data, "follows")