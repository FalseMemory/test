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

from test_cases.test_login import test_login_pwd
from utils.get_path import get_screen_dir


# @pytest.fixture(scope="module")
# def driver():
#     driver = webdriver.Chrome()
#     driver.maximize_window()
#     driver.implicitly_wait(5)
#     driver.get("https://www.wegame.com.cn/store/2000004/Don_t_Starve_Together")
#     return driver
@allure.title('单次购买流程')
def test_purchase(driver, logger, get_error_screenshot):
    # 首先登录
    key = {"username": "1183839611", "password": "z1187689110"}
    test_login_pwd(driver, key)
    driver.get("https://www.wegame.com.cn/store/2000004/Don_t_Starve_Together")
    # 点购买
    driver.find_element(By.XPATH,
                        '//*[@id="app"]/div[1]/div/div/div[1]/div/div[2]/div/div[2]/div[3]/div[2]/div/span/a[1]').click()
    sleep(3)
    # 选择版本
    driver.find_element(By.XPATH, "//div[@class = 'widget-gcard widget-gcard--list widget-gcard--list-xs']").click()
    driver.find_element(By.XPATH, "//a[@class = 'we-button we-button--primary']").click()
    # 切换到支付iframe
    # driver.switch_to.frame(0)
    iframe_locator = (By.XPATH, "//iframe[@class = 'wegame-pay-frame']")
    iframe_element = driver.find_element(*iframe_locator)
    driver.switch_to.frame(iframe_element)  # 切换到指定的iframe
    try:
        img = driver.find_element(By.XPATH, "//div[@class= 'qr-code-container wx']/img")
        assert img is not None
        return
    except NoSuchElementException as e:
        get_error_screenshot()
        logger.exception("加载支付二维码失败：%s", str(e))
        raise
