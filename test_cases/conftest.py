import datetime

import allure
import pytest
from selenium import webdriver
import logging

from utils.get_path import get_screen_dir


@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)
    driver.get("https://www.wegame.com.cn/home/")
    return driver


@pytest.fixture(scope="session", autouse=True)
def logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    logger = logging.getLogger(__name__)
    return logger

@pytest.fixture(scope="session")
def get_error_screenshot(driver):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    screenshot_filename = r"/" + timestamp + ".png"
    file_path = get_screen_dir() + screenshot_filename
    driver.save_screenshot(file_path)
    with open(file_path, "rb") as f:
        file = f.read()
        allure.attach(file, "失败截图", allure.attachment_type.PNG)
    return