from pyvirtualdisplay import Display

from selenium.webdriver.common.keys import Keys
from selenium import webdriver

import os


class FlaurologicalDriver:

    DIR_PATH = 'pages'

    def __init__(self, logger=None):
        try:
            display = Display(visible=0, size=(800, 600))
            display.start()

            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')

            self.driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', chrome_options=options)
        except Exception as _er:
            if logger:
                logger.error(_er)
            self.driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')

        self.pages = []
        self.data = []

    def run(self, url):
        self.parser(url)
        # self.save_pages(url)

    def parser(self, url):
        self.driver.get(url)
        # self._specific_first_page()  # not really need
        while True:
            btn = self.driver.find_element_by_xpath('//*[@id="FUS1808_next"]')
            if btn.get_attribute("class").split(' ')[-1] == 'next':
                self._specific_page()
                btn.click()
            else:
                self._specific_page()
                break
        # self._specific_last_page()  # not really need
        print(self.data)

    def save_pages(self, url):
        self.driver.get(url)
        counter = 0
        while True:
            btn = self.driver.find_element_by_xpath('//*[@id="FUS1808_next"]')
            if btn.get_attribute("class").split(' ')[-1] == 'next':
                counter += 1
                self.__download_page(counter)
                btn.click()
            else:
                counter += 1
                self.__download_page(counter)
                break

    def quit(self):
        self.driver.quit()

    # PROTECTED
    def _specific_first_page(self):
        data = {}
        data['session-title'] = self.__xpath_text('//*[@id="FUS1808"]/tbody/tr[10]/td[3]/div[1]')
        data['speakerType'] = self.__xpath_text('//*[@id="FUS1808"]/tbody/tr[10]/td[3]/div[2]/div[1]')
        data['speakerDetails'] = {}
        elem = self.__xpath_text('//*[@id="FUS1808"]/tbody/tr[10]/td[3]/div[2]/div[2]')
        data['speakerDetails']['name'], data['speakerDetails']['Workplace'] = elem.split('\n')
        # print(data)
        self.data.append(data)

    def _specific_page(self):
        elements = self.driver.find_elements_by_xpath('//*[@id="FUS1808"]/tbody/tr')
        for element in elements:
            data = {}
            try:
                data['session-title'] = self.__xpath_text('//*[@id="FUS1808"]/tbody/tr[10]/td[3]/div[1]', element)
                data['speakerType'] = self.__xpath_text('//*[@id="FUS1808"]/tbody/tr[10]/td[3]/div[2]/div[1]', element)
                data['speakerDetails'] = {}
                elem = self.__xpath_text('//*[@id="FUS1808"]/tbody/tr[10]/td[3]/div[2]/div[2]', element)
                data['speakerDetails']['name'], data['speakerDetails']['Workplace'] = elem.split('\n')
                self.data.append(data)
            except:
                pass

    def _specific_last_page(self):
        pass

    # PRIVATE
    def __xpath_text(self, xpath, elem=None):
        if elem:
            return elem.find_element_by_xpath(xpath).text
        return self.driver.find_element_by_xpath(xpath).text

    def __download_page(self, i):
        page = self.driver.page_source
        filepath = os.path.join(self.DIR_PATH, str(i) + '.html')
        with open(filepath, 'w') as f:
            f.write(page)
            self.pages.append(filepath)
