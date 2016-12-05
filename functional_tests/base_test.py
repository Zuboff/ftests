import unittest, time
from selenium import webdriver

TIMEOUT_LOAD_PAGE = 120  # ограничение на время загрузки страницы, в сек


class BaseTestCase(unittest.TestCase):

	@classmethod
	def setUp(cls):
		cls.t_start = time.perf_counter()
		# TODO - организовать выбор различных браузеров
		#cls.driver = webdriver.Firefox("/Users/i-storenetmgx72/SeleniumLibrary/geckodriver")
		cls.driver = webdriver.Chrome('/Users/i-storenetmgx72/SeleniumLibrary/chromedriver')
		#cls.driver = webdriver.Firefox()

		cls.driver.set_page_load_timeout(TIMEOUT_LOAD_PAGE)
		cls.driver.implicitly_wait(2)
		cls.driver.maximize_window()

	@classmethod
	def tearDown(cls):
		# close the browser window
		cls.driver.quit()
		cls.t_end = time.perf_counter()
		print("test duration - %d sec." % (cls.t_end - cls.t_start))