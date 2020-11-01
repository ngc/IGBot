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

from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
from selenium.webdriver.chrome.options import Options
import os
from time import sleep

def get_driver(args=[], url="https://www.instagram.com"):
    """Creates a webdriver based on a set of arguments and an initial URL.

    Args:
        args ([string]): Driver arguments. Defaults to an empty list (not required).
        url (str, optional): URL for the driver to start on. Defaults to "https://www.instagram.com".

    Returns:
        webdriver: A webdriver formed depending on the arguments provided.
    """
    chrome_options = Options()
    chrome_options.add_experimental_option('useAutomationExtension', False)
    if("--headless" in args): chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_dir = "/usr/lib/chromium-browser/chromedriver"

    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_dir)
    driver.get(url)
    return driver
