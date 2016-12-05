from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
TIMEOUT_LOAD_PAGE = 120

class BasePage(object):
	""" All page objects inherit from this """

	def __init__(self, driver, base_url='https://avtobazar.ua/'):
		self.base_url = base_url
		self.driver = driver

	def find_element(self, *locator):
		WebDriverWait(self.driver, 100).until(
			lambda s: s.find_element(*locator).get_attribute('disabled') is None)
		return self.driver.find_element(*locator)

	def open(self,url):
		url = self.base_url + url
		try:
			self.driver.get(url)
		except TimeoutException:
			print("Page load timeout > %s sec.!!!" % TIMEOUT_LOAD_PAGE)


	def get_title(self):
		return self.driver.title

	def get_url(self):
		return self.driver.current_url

	def get_text(self, *locator):
		return self.find_element(*locator).text

	def click_element(self,*locator):
		return self.find_element(*locator).click

	# Выбираем из селектов
	def select_option(self, pattern, *locator):
		element = self.find_element(*locator)
		#element = self.driver.find_element(*locator)
		select = Select(element)
		for option in select.options:
			value = option.text
			if pattern.search(value):
				option.click()
				break
		return select.first_selected_option.text

	# Убираем верхнюю навигационную плашку
	def remove_top_plate(self):
		js = "var elem = document.getElementsByClassName('head-menu-wrap'); elem[0].parentNode.removeChild(elem[0]); "
		self.driver.execute_script(js)
	# Убираем сообщение о разрешении сбора куков
	def remove_cookie_plate(self):
		js = "var elem = document.getElementsByClassName('container row'); elem[0].parentNode.removeChild(elem[0]); "
		self.driver.execute_script(js)
	def remove_bottom_plate(self):
		js = "var elem = document.getElementsByClassName('navbar navbar-default navbar-fixed-bottom hidden-xs'); elem[0].parentNode.removeChild(elem[0]); "
		self.driver.execute_script(js)

	def remove_top_bottom_cookie_plate(self):
		self.remove_top_plate()
		self.remove_cookie_plate()
		self.remove_bottom_plate()

