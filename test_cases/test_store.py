import datetime
import os
from time import sleep

import allure
import pytest
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from utils.get_path import get_screen_dir


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)
    driver.get("https://www.wegame.com.cn/store")
    return driver


class TestStore:

    def __init__(self, driver):
        self.__driver = driver

    def get_error_screenshot(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        screenshot_filename = r"/" + timestamp + ".png"
        file_path = get_screen_dir() + screenshot_filename
        self.__driver.save_screenshot(file_path)
        with open(file_path, "rb") as f:
            file = f.read()
            allure.attach(file, "失败截图", allure.attachment_type.PNG)
        return


@allure.title('商店推广栏')
def test_menulist(driver, logger):
    test_store = TestStore(driver)

    try:
        # //ul[@class = 'gscroll-cont-list panel-future-act-list']/li[1]//a
        # eles = driver.find_elements(By.XPATH,"//ul[@class = 'nbmodulea-menulist']//div[@class = 'we-image we-image--square']/img[@class= 'we-image-figure']")
        for i in range(0, 8):
            driver.find_elements(By.XPATH,
                                 "//ul[@class = 'nbmodulea-menulist']//div[@class = 'we-image we-image--square']/img[@class= 'we-image-figure']")[
                i].click()
            sleep(3)
            driver.get("https://www.wegame.com.cn/store")
        return
    except NoSuchElementException as e:
        test_store.get_error_screenshot()
        logger.exception("点击推荐窗口失败：%s", str(e))
        raise


@allure.title('商店新游栏')
@pytest.mark.skip(reason="模拟鼠标悬停在元素上时，报错")
def test_panel_title(driver, logger):
    test_store = TestStore(driver)
    try:
        # //ul[@class = 'gscroll-cont-list panel-future-act-list']/li[1]//a
        for i in range(0, 1):
            ele = driver.find_elements(By.XPATH,
                                       "//ul[@class = 'gscroll-cont-list panel-future-act-list']/li/div//img")[i]
            # 移动页面，显示元素
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: 'center'});",
                                  ele)
            ele.click()
            sleep(3)
            actions = ActionChains(driver)
            # 模拟鼠标悬停在元素上
            actions.move_to_element(ele).perform()
            sleep(3)
            driver.find_element(By.XPATH, '//*[@class="we-popover widget-ncardsl ani-centerscale"]//img').click()
            sleep(3)
            driver.get("https://www.wegame.com.cn/store")
        return
    except NoSuchElementException as e:
        test_store.get_error_screenshot()
        logger.exception("商店新游栏失败：%s", str(e))
        raise e


@allure.title('商店预约栏')
def test_reserve_game(driver, logger):
    test_store = TestStore(driver)
    try:
        for i in range(0, 5):

            if i > 2:
                driver.find_element(By.XPATH, "//div[@class= 'btn-next']").click()

            driver.find_elements(By.XPATH, "//ul[@class = 'we-list we-list--3']//img")[i].click()
            sleep(3)
            driver.get("https://www.wegame.com.cn/store")
        return
    except NoSuchElementException as e:
        test_store.get_error_screenshot()
        logger.exception("预约新游失败：%s", str(e))
        raise


@allure.title('商店排行榜')
def test_ranking_list(driver):
    test_store = TestStore(driver)
    try:
        for i in range(0, 32):
            driver.find_elements(By.XPATH, "//div[@class = 'rankview-subpanel-bd']/div/a")[i].click()
            sleep(3)
            driver.get("https://www.wegame.com.cn/store")
        return
    except NoSuchElementException as e:
        test_store.get_error_screenshot()
        logger.exception("排行榜失败：%s", str(e))
        raise
