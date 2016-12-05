from functional_tests.base import BasePage
from functional_tests.locators import FilterSearchListLocators
import re, time
from selenium.webdriver.support.ui import WebDriverWait


class FilterListRegion(BasePage):
	# Клик на Поиск верхнего блока
	def run_the_filter(self):
		# Нахожу кнопку Поиск1
		self.button_search = self.driver.find_element(*FilterSearchListLocators.GO_BUTTON_1)
		# Запускаю фильтр
		self.button_search.submit()

	# Клик на Поиск нижнего блока
	def run_the_filter_bottom(self):
		# Нахожу кнопку Поиск2
		self.button_search = self.driver.find_element(*FilterSearchListLocators.GO_BUTTON_2)
		# Запускаю фильтр
		self.button_search.submit()

	# Функция которая выбирает в фильтре передаваемые значения, возвращает значение
	def search_by_category(self, *args, **kwargs):

		if not args:
			args = kwargs

		for key in args:
			locator = getattr(FilterSearchListLocators, key)

			if key == 'MAKE':
				pattern = re.compile(kwargs[key] + '.+')
			elif key == 'MODEL':
				pattern = re.compile('(.+)?' + kwargs[key])
			elif key == 'CITY':
				pattern = re.compile(kwargs[key] + '$' + '|' + kwargs[key] + '\s')
			else:
				pattern = re.compile(kwargs[key])

			self.select_option(pattern, *locator)

		self.run_the_filter()

	def input_value(self, **kwargs):
		for key in kwargs:
			locator = getattr(FilterSearchListLocators, key)
			#WebDriverWait(self.driver, 100).until(
			#	lambda s: s.find_element(*locator).get_attribute('disabled') is None)
			self.find_element(*locator).send_keys(kwargs[key])

	def select_checkbox(self, **kwargs):
		for key in kwargs:
			locator = getattr(FilterSearchListLocators, key)
			#WebDriverWait(self.driver, 100).until(
			#	lambda s: s.find_element(*locator).get_attribute('disabled') is None)
			element = self.find_element(*locator)
			element.click()
