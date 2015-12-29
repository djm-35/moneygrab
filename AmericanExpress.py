from selenium.webdriver.common.by import By
from getpass import getpass
import time
from Grab import Grab


class AA(Grab):
    _content_type = 'application/vnd.intu.qfx'

    def go(self):
        usr = str(raw_input('Enter your username: '))
        pwd = getpass('Enter American Express password (%s): ' % usr)

        self.driver.get('https://www.americanexpress.com/')

        user_input = self.driver.find_element_by_id('LabelUserID')
        password_input = self.driver.find_element_by_id('LabelPassword')
        login_btn = self.driver.find_element_by_id('loginLink')

        user_input.send_keys(usr)
        password_input.send_keys(pwd)
        login_btn.click()

        # Print out cashback
        try:
            whole = self._attempt(By.ID, 'ah-whole-loyalty').text
            decimal = self._attempt(By.ID, 'ah-decimal-loyalty').text
            print('Cashback: ' + whole + decimal)
        except:
            print("Couldn't find Cashback")

        # Click "Statements & Activity"
        self._attempt(By.ID, 'MYCA_PC_Statements2').click()

        # Click download button and "Card Activity" from menu
        self._attempt(By.ID, 'downloadMenu').click()
        time.sleep(1.5)  # wait for JS dropdown animation
        self._attempt(By.ID, 'blindCardActivity').click()

        # Download the most recent 90 days (YNAB will ignore all the extras)
        self._attempt(By.XPATH, '//*[text()[contains(.,"Most recent 90")]]/../span').click()  # rather open XPATH
        self._attempt(By.ID, 'downloadFormButton').click()


def main():
    ff = AA()
    ff.go()

if __name__ == '__main__':
    main()
