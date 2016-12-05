from functional_tests.base import BasePage
from functional_tests.locators import SortingSectionLocators
from selenium.webdriver.common.by import By

class SortingSection(BasePage):
	# Сортировать объявления
	def click_sorting_ads(self, key):

		locator = getattr(SortingSectionLocators, key)

		element = self.find_element(*locator)
		element.click()

		_map = {'PRICE_SORT': 'PRICE_SORT_ARROW', 'YEAR_SORT': 'YEAR_SORT_ARROW',
										'DATE_SORT': 'DATE_SORT_ARROW'}
		locator_arrow = getattr(SortingSectionLocators,_map[key])
		attr = self.find_element(*locator_arrow).get_attribute('class')
		return attr

	# Для работы с выпадающим меню, который определяет кол-во объявлений на стр.
	def click_dropdown_menu(self, count):
		self.driver.find_element_by_id('countValue').click()
		css = "ul[class*='results-count'] * a[data-count='%s']" % count
		element = self.driver.find_element(By.CSS_SELECTOR, css)
		element.click()

