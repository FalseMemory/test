import datetime
from time import sleep

import allure
import pytest
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from utils.get_path import get_screen_dir
from utils.read_data import read_json_data


@allure.story("登录功能")
class LoginPage:
    def __init__(self, driver, username=None, password=None):
        self.__driver = driver
        self.__username = username
        self.__password = password

    def set_username(self, username):
        self.__username = username

    def set_password(self, password):
        self.__password = password

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def login_by_pwd(self):
        if self.__username is None or self.__password is None:
            raise NoSuchElementException("no username or password")
        self.__driver.find_element(By.ID, 'u').send_keys(self.__username)
        self.__driver.find_element(By.ID, 'p').send_keys(self.__password)
        self.__driver.find_element(By.ID, 'login_button').click()

    def is_logged_in(self, driver):
        try:
            cookies = driver.get_cookies()
            for cookie in cookies:
                if cookie.get("value") is not None:
                    if cookie.get("value").startswith('o'):
                        return True
        except NoSuchElementException:
            return False
        return False

    #
    def logout(self, driver):
        if self.is_logged_in(driver):
            driver.find_element(By.XPATH, '//span[@class ="wglogin-btn"]').click()
        return

    def switch_to_login_page(self, driver):
        driver.switch_to.default_content()
        iframe_locator = (By.XPATH, "//iframe[@frameborder= '0']")
        iframe_element = driver.find_element(*iframe_locator)
        driver.switch_to.frame(iframe_element)  # 切换到指定的iframe

    def get_error_screenshot(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        screenshot_filename = r"/" + timestamp + ".png"
        file_path = get_screen_dir() + screenshot_filename
        self.__driver.save_screenshot(file_path)
        with open(file_path, "rb") as f:
            file = f.read()
            allure.attach(file, "失败截图", allure.attachment_type.PNG)
        return


# @pytest.fixture(scope="session")
def enter_login_window(driver):
    # driver.get("https://www.wegame.com.cn/home/")
    # 如果已登录，则退出登录
    login = LoginPage(driver)
    if login.is_logged_in(driver) is True:
        login.logout(driver)
    # 点击右上角登录按钮
    driver.find_element(By.XPATH, "//span[@class = 'btn-wglogin-text']").click()
    # 进入登录iframe
    driver.switch_to.frame(0)
    return


@allure.title('QQ扫码登录')
def test_QRcode(driver):
    img = driver.find_element(By.XPATH, '//img[@class = "qrImg"]')
    assert img is not None


@pytest.mark.skip(reason="waste too much time")
def test_QRcode_timeout(driver):
    img = driver.find_element(By.XPATH, '//img[@class = "qrImg"]')
    sleep(600)
    time_out = driver.find_element(By.ID, 'qr_invalid')
    assert time_out.get_attribute("style") is not "display: none"


@allure.title('QQ快速登录')
# 如果已登录，则退出登录，如果没快速登录窗口，则用例失败
def test_quick_login(driver):
    login_page = LoginPage(driver)
    login_page.logout(driver)
    enter_login_window(driver)
    try:
        quick_window = driver.find_element(By.XPATH, '//a[@tabindex="2"]')
    except NoSuchElementException:
        assert "没有登录QQ" == "已登录QQ"
        return
    href = quick_window.get_attribute("href")
    if href is not None:
        quick_window.click()
    driver.switch_to.default_content()
    assert driver.find_element(By.XPATH, "//div[@id = 'wglogin-box']/p/img") is not None


@allure.title('QQ密码登录')
@pytest.mark.parametrize("key", read_json_data()["test_login"])
def test_login_pwd(driver, key):
    # username  = "1183839611"
    # password = "z1187689110"
    # driver = webdriver.Chrome()
    # driver.maximize_window()
    # driver.implicitly_wait(5)
    driver.get("https://www.wegame.com.cn/home/")
    enter_login_window(driver)
    driver.find_element(By.ID, "switcher_plogin").click()
    login_page = LoginPage(driver)
    login_page.set_username(key["username"])
    login_page.set_password(key["password"])
    login_page.login_by_pwd()
    WebDriverWait(driver, 5)
    driver.switch_to.default_content()
    # 登录成功
    if login_page.is_logged_in(driver):
        return
    else:
        # error message
        driver.switch_to.frame(0)
        err_m = driver.find_element(By.ID, "err_m")
        login_page.get_error_screenshot()
    return

@allure.title('微信扫描登录')
def test_login_wechat(driver):
    enter_login_window(driver)
    driver.switch_to.default_content()
    # 切换到微信登录页面
    driver.find_element(By.XPATH, "/html/body/div[5]/div/div/div[1]/ul/li[2]/a").click()
    iframe_locator = (By.XPATH, "//iframe[@frameborder= '0']")
    iframe_element = driver.find_element(*iframe_locator)
    driver.switch_to.frame(iframe_element)  # 切换到指定的iframe
    # driver.switch_to.frame(0)
    # 查看二维码是否显示正常
    img = driver.find_element(By.XPATH, "//div[@class = 'wrp_code']/img")
    assert img.get_attribute("src") is not None
