from selenium import webdriver
# from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import os
from abc import ABCMeta, abstractmethod, abstractproperty


class Grab:
    __metaclass__ = ABCMeta
    __driver = None

    def __init__(self, closeonexit=False, *args, **kwargs):
        self.__closeonexit = bool(closeonexit)

    @abstractproperty
    def _content_type(self):
        return self._content_type

    @property
    def driver(self):
        if self.__driver is None:
            dl_folder_path = os.path.dirname(os.path.realpath(__file__)) + '/downloads'

            profile = webdriver.FirefoxProfile()
            profile.set_preference('browser.download.folderList', 2)  # custom location
            profile.set_preference('browser.download.manager.showWhenStarting', False)
            profile.set_preference('browser.download.dir', dl_folder_path)
            profile.set_preference('browser.helperApps.neverAsk.saveToDisk', self._content_type)

            self.__driver = webdriver.Firefox(profile)
            self.__driver.implicitly_wait(10)
        return self.__driver

    def _attempt(self, by, selector):
        try:
            return WebDriverWait(self.driver, 10).until(
                expected_conditions.visibility_of_element_located((by, selector))
            )
        except Exception as e:
            print(str(e))
            return None

    @abstractmethod
    def go(self):
        pass

    def __del__(self):
        if self.__closeonexit and self.__driver is not None:
            print('Closing browser...')
            self.__driver.quit()
