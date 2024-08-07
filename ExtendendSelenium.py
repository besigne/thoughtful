from RPA.Browser.Selenium import Selenium
from selenium.webdriver.firefox.options import Options
from webdrivermanager import ChromeDriverManager
from SeleniumLibrary.base import keyword
import logging


class ExtendedSelenium(Selenium):

    def __init__(self, *args, **kwargs):
        Selenium.__init__(self, *args, **kwargs)
        cdm = ChromeDriverManager(link_path="AUTO")
        cdm.download_and_install()
        
    @keyword
    def looking_at_element(self, locator):
        element = self.get_webelement(locator)
        self.logger.warn(dir(element))

    @keyword
    def open_site(self, url, **kwargs):
        logging.basicConfig(level=logging.DEBUG)
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        self.open_browser(
            url=url,
            browser="chrome",
            options=options,
            **kwargs
        )

    @keyword
    def print_webdriver_log(self, logtype):
        print(f"\n{logtype.capitalize()} Log")
        return self.driver.get_log(logtype)
        