from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from getpass import getpass
import time
import os


class Discover():
    __driver = None

    def __init__(self, closeonexit=False, *args, **kwargs):
        self.__closeonexit = bool(closeonexit)

    @property
    def driver(self):
        if self.__driver is None:
            dl_folder_path = os.path.dirname(os.path.realpath(__file__)) + '/downloads'

            profile = webdriver.FirefoxProfile()
            profile.set_preference('browser.download.folderList', 2)  # custom location
            profile.set_preference('browser.download.manager.showWhenStarting', False)
            profile.set_preference('browser.download.dir', dl_folder_path)
            profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/vnd.intuit.QFX')

            self.__driver = webdriver.Firefox(profile)
            self.__driver.implicitly_wait(10)
        return self.__driver

    def __attempt(self, by, selector):
        try:
            return WebDriverWait(self.driver, 10).until(
                expected_conditions.visibility_of_element_located((by, selector))
            )
        except Exception as e:
            print(str(e))
            return None

    def go(self):
        usr = str(raw_input('Enter your username: '))
        pwd = getpass('Enter discover password (%s): ' % usr)

        self.driver.get('https://www.discover.com/')

        user_input = self.driver.find_element_by_id('login-account')
        password_input = self.driver.find_element_by_id('login-password')
        login_btn = self.driver.find_element_by_id('login-button')

        user_input.send_keys(usr)
        password_input.send_keys(pwd)
        login_btn.click()

        # Click "Recent Activity"
        self.__attempt(By.CSS_SELECTOR, 'div.card-details > div.card-balances a[title="Recent Activity"]').click()

        def download(pref0, pref1):
            """ Clicks through modal and downloads the Quicken file """
            time.sleep(3)  # Cuz javascript (I hate this, wish there was a better way)
            self.__attempt(By.ID, pref0 + '-download-button').click()
            self.__attempt(By.ID, pref1 + '-download-options-quicken').click()
            dl_btn = self.__attempt(By.CSS_SELECTOR, '#' + pref1 + '-download-options-obtrusive a.overlay-download-button')
            if dl_btn.get_attribute('innerHTML') == 'Download':
                dl_btn.click()

        # Get the recent activity (default) and the next QFX
        download('statement', 'statements')
        self.__attempt(By.ID, 'statement-date').click()
        self.__attempt(By.CSS_SELECTOR, '#statement-date option[value="current"]').click()
        download('recent-activity', 'recent-activity')

    def __del__(self):
        if self.__closeonexit and self.__driver is not None:
            print('Closing browser...')
            self.__driver.quit()


def main():
    ff = Discover()
    ff.go()

if __name__ == '__main__':
    main()
