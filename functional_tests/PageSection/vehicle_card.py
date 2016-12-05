from functional_tests.base import BasePage
from functional_tests.locators import VehicleCardLocators
from selenium.webdriver.common.by import By


class VehicleCard(BasePage):
	# Сбор на конечном объявлении технических данных автомобиля
	def output_ad_teh_data(self):
		locator = VehicleCardLocators.SPECIFICATIONS_TABLE
		li = [i.text for i in self.driver.find_elements(*locator)]
		ad_teh_data = dict(zip(li[::2], li[1::2]))

		return ad_teh_data

	# Сбор на конечном объявлении опций автомобиля
	def output_ad_options(self):
		locator = VehicleCardLocators.OPTIONS_TABLE
		options = self.driver.find_elements(*locator)
		options = [i.text.replace('\n', ', ') for i in options]
		ad_options = {'options': ', '.join(options)}

		return ad_options
