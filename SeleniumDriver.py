from selenium import webdriver


class SeleniumDriver:
    __instance = None

    @staticmethod
    def get_instance():
        if SeleniumDriver.__instance is None:
            SeleniumDriver()
        return SeleniumDriver.__instance

    def __init__(self):
        if SeleniumDriver.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            option = webdriver.ChromeOptions()
            option.add_argument('headless')
            browser = webdriver.Chrome(executable_path='./chromedriver/chromedriver', chrome_options=option)
            SeleniumDriver.__instance = browser
