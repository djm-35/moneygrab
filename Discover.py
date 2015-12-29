from selenium.webdriver.common.by import By
from getpass import getpass
import time
from Grab import Grab


class Discover(Grab):
    _content_type = 'application/vnd.intuit.QFX'

    def go(self):
        usr = str(raw_input('Enter your username: '))
        pwd = getpass('Enter your Discover password (%s): ' % usr)

        self.driver.get('https://www.discover.com/')

        user_input = self.driver.find_element_by_id('login-account')
        password_input = self.driver.find_element_by_id('login-password')
        login_btn = self.driver.find_element_by_id('login-button')

        user_input.send_keys(usr)
        password_input.send_keys(pwd)
        login_btn.click()

        # Print out cashback
        try:
            print('Cashback: ' + self._attempt(By.CSS_SELECTOR, 'div.card-rewards li.amount').text)
        except:
            print("Couldn't find Cashback")

        # Click "Recent Activity"
        self._attempt(By.CSS_SELECTOR, 'div.card-details > div.card-balances a[title="Recent Activity"]').click()

        def download(pref0, pref1):
            """ Clicks through modal and downloads the Quicken file """
            time.sleep(3)  # Cuz javascript (I hate this, wish there was a better way)
            self._attempt(By.ID, pref0 + '-download-button').click()
            self._attempt(By.ID, pref1 + '-download-options-quicken').click()
            dl_btn = self._attempt(By.CSS_SELECTOR, '#' + pref1 + '-download-options-obtrusive a.overlay-download-button')
            if dl_btn.get_attribute('innerHTML') == 'Download':
                dl_btn.click()

        # Get the recent activity (default) and the next QFX
        download('statement', 'statements')
        self._attempt(By.ID, 'statement-date').click()
        self._attempt(By.CSS_SELECTOR, '#statement-date option[value="current"]').click()
        download('recent-activity', 'recent-activity')


def main():
    ff = Discover()
    ff.go()

if __name__ == '__main__':
    main()
