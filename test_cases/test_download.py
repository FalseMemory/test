import datetime
import os
from time import sleep

import pytest
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from utils.get_path import get_download_dir, get_file_dir, get_screen_dir


@pytest.fixture()
def chrome_options_driver():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": "{}".format(get_download_dir()), "safebrowsing.enabled": True}
    chrome_options.add_experimental_option("prefs", prefs)
    option_driver = webdriver.Chrome(chrome_options)
    option_driver.get("https://www.wegame.com.cn/home/")
    option_driver.maximize_window()
    return option_driver


class TestDownload:
    def __init__(self, driver):
        self.__driver = driver

    def download(self):
        pass

    # def set_download_dir(self, dir_path):
    #     driver_options = webdriver.ChromeOptions()
    #     # ”{}“.format(dir_path)
    #     prefs = {"download.default_directory": r"D:\StudyAutoTest\WeGameWebTest\file", "safebrowsing.enabled": True}
    #     driver_options.add_experimental_option("prefs", prefs)
    #     self.__driver = webdriver.Chrome(options=driver_options)


def test_download_client(chrome_options_driver, logger):
    # 已存在就删除
    if os.path.exists(get_download_dir() + "/WeGameMiniLoader.std.5.12.21.1022.exe"):
        os.remove(get_download_dir() + "/WeGameMiniLoader.std.5.12.21.1022.exe")
    chrome_options_driver.switch_to.default_content()
    chrome_options_driver.find_element(By.XPATH, "//a[@class = 'wgheader-download']").click()

    # 等待下载完毕
    sleep(10)
    try:
        assert os.path.exists(get_download_dir() + "/WeGameMiniLoader.std.5.12.21.1022.exe") is True
        raise Exception("下载客户端失败")
    except AssertionError as e:
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        screenshot_filename = r"/" + timestamp + ".png"
        chrome_options_driver.save_screenshot(get_screen_dir() + screenshot_filename)
        logger.exception("下载客户端失败：%s", str(e))
        raise
