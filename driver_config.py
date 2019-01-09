import os

from pyvirtualdisplay import Display

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver


class FlaurologicalDriver:

    DIR_PATH = 'pages'

    def __init__(self, logger=None):
        self.logger = logger
        self.pages = []
        self.data = []

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

    def run(self, url: str, save_mode=False) -> None:
        """
        Starting point parser
        :param url: <str> web-url to scrape
        :param save_mode: <bool> default=False. If true then it will run the save_pages method
        :return: None
        """
        if save_mode:
            self.save_pages(url)
        self.parser(url)

    def parser(self, url: str) -> None:
        """
        Parse whole the data from the url
        :param url: <str> web-url to scrape
        :return: None
        """
        self.driver.get(url)
        while True:
            btn = self.driver.find_element_by_xpath('//*[@id="FUS1808_next"]')
            if btn.get_attribute("class").split(' ')[-1] == 'next':
                self._specific_page()
                btn.click()
            else:
                self._specific_page()
                break

    def save_pages(self, url: str) -> None:
        """
        Save every page from the web-url
        :param url: <str> web-url to scrape
        :return: None
        """
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

    def quit(self) -> None:
        """
        Stop the driver. Quit the browser
        :return: None
        """
        self.driver.quit()

    # PROTECTED
    def _specific_first_page(self) -> None:
        """
        Parse only first page, which contains only 1 required row
        :return: None
        """
        data = {}
        data['session-title'] = self.__xpath_text('//*[@id="FUS1808"]/tbody/tr[10]/td[3]/div[1]')
        data['speakerType'] = self.__xpath_text('//*[@id="FUS1808"]/tbody/tr[10]/td[3]/div[2]/div[1]')
        data['speakerDetails'] = {}
        elem = self.__xpath_text('//*[@id="FUS1808"]/tbody/tr[10]/td[3]/div[2]/div[2]')
        data['speakerDetails']['name'], data['speakerDetails']['Workplace'] = elem.split('\n')
        self.data.append(data)

    def _specific_page(self) -> None:
        """
        Parse every page
        :return: None
        """
        table = self.driver.find_element_by_xpath('//*[@id="FUS1808"]/tbody')
        elements = table.find_elements(By.TAG_NAME, 'tr')
        for element in elements:
            try:
                self.data.append(self._gen_data(element))
            except Exception as _er:
                if self.logger:
                    self.logger.error(_er)

    def _gen_data(self, element) -> dict:
        """
        Gen data from the page to dict format
        :return: None
        """
        data = {}
        data['session-title'] = element.find_elements(By.TAG_NAME, 'td')[2].find_elements(By.TAG_NAME, 'div')[0].text
        data['speakerType'] = element.find_elements(
            By.TAG_NAME, 'td'
        )[2].find_elements(By.TAG_NAME, 'div')[1].find_elements(By.TAG_NAME, 'div')[0].text
        data['speakerDetails'] = {}
        elem = element.find_elements(
            By.TAG_NAME, 'td'
        )[2].find_elements(By.TAG_NAME, 'div')[1].find_elements(By.TAG_NAME, 'div')[1].text
        elem = elem.split('\n')
        if len(elem) > 2:
            names = []
            workplaces = []
            elem = list(filter(lambda x: x, elem))
            for i in range(len(elem)):
                if i % 2 == 0:
                    names.append(elem[i])
                else:
                    workplaces.append(elem[i])
            data['speakerDetails']['names'], data['speakerDetails']['Workplaces'] = names, workplaces
        else:
            data['speakerDetails']['names'], data['speakerDetails']['Workplaces'] = [elem[0]], [elem[-1]]
        return data

    # PRIVATE
    def __xpath_text(self, xpath: str, elem=None) -> str:
        """
        Get the text from the `self.driver` element or `elem` if was received.
        Find the element via `xpath`
        :param xpath: <str>
        :param elem: selenium-object
            if elem is not None:
                return elem.find_element_by_xpath(xpath).text
        :return: <str> text of the selenium-element
        """
        if elem:
            return elem.find_element_by_xpath(xpath).text
        return self.driver.find_element_by_xpath(xpath).text

    def __download_page(self, i: int) -> None:
        """
        load page from the url
        :param i: <int> number of the page. It will be the specific name of '.html' document
        :return: None
        """
        page = self.driver.page_source
        filepath = os.path.join(self.DIR_PATH, str(i) + '.html')
        with open(filepath, 'w') as f:
            f.write(page)
            self.pages.append(filepath)
