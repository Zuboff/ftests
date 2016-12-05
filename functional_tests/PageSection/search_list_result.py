from functional_tests.base import BasePage
from selenium.webdriver.common.by import By
from functional_tests.locators import *
import re, time
from selenium.webdriver.support.ui import WebDriverWait

EXCHANGE_RATES = 1.12


class SearchListResult(BasePage):

	# Хелпер, для обработки совпадений для regex
	def displaymatch(self, text):
		valid_year = re.compile(r"([2][0][0-1]\d|[1][9]\d\d)")  # Находим только "правильные года"
		year = valid_year.match(text)
		if year is None:
			return None
		return (int(year.group()))

	def output_ads_list(self, *type_ads):
		driver = self.driver
		_map = {'ordinary': SearchListResultLocators.ADS_ORDINARY, 'orange': SearchListResultLocators.ADS_ORANGE}
		ads = []
		for key in type_ads:
			locator = _map[key]

			#WebDriverWait(self.driver, 100).until(
			#	lambda s: s.find_element(*locator).get_attribute('class') is not None)
			time.sleep(5) #FIXME

			ad_div = driver.find_elements(*locator)
			for i in ad_div:

				adr = i.text.split('сохранить сравнить\n')
				if adr[1].count('\n') == 1:
					adr[1] = 'None\nNone\n' + adr[1]
				elif adr[1].count('\n') == 2:
					adr[1] = 'None\n' + adr[1]

				adr[1] = 'сохранить сравнить\n' + adr[1]
				adr = (adr[0] + adr[1]).split('\n')

				cars, *tehdata, price, _, _, salon, firm, city, period_for = adr
				ad = {'cars': ' '.join(cars.split()[:-1]), 'tehdata': tehdata,
						'year':  self.displaymatch(cars.split()[-1]),
						'price_$': int(''.join(price.split()[:-1])),
						'currency': price.split()[-1],
						'salon': salon, 'firm': firm,
						'city': city.split('/')[-1].strip(), 'period_for': period_for}

				ads.append(ad)
		return ads

	# Собираем линки на конечные страницы объявлений
	def output_link_ads_list(self):
		driver = self.driver #TODO поставить задержку
		ad_div = driver.find_elements(*SearchListResultLocators.AD_LINK)
		link_list = [i.get_attribute('href') for i in ad_div]
		return link_list

	# Переход по пагинатору
	def crossings_between_pages(self, n_page):
		element = self.find_element(By.LINK_TEXT, '%s' % n_page)
		# TODO - не использую локатор, тк не знаю как передать в него номер страницы
		element.click()

	# Сбор на конечном объявлении технических данных автомобиля
	def output_ad_teh_data(self):
		xpath = '//table[@class="table table-hover"]/tbody/tr/child::*'
		li = [i.text for i in self.driver.find_elements_by_xpath(xpath)]
		ad_teh_data = dict(zip(li[::2], li[1::2]))
		return ad_teh_data

	#  Привести цены евро в доллары
	def currency_conversion(self, ads):
		ls_currency = [i.get('currency') for i in ads]
		ls_price = [i.get('price_$', 'currency') for i in ads]
		e = []
		for i, val in enumerate(ls_currency):
			if val == '€':
				e.append(i)
		for i in e:
			ls_price[i] = int(ls_price[i] * EXCHANGE_RATES)

		return ls_price
