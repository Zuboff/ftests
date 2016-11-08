import unittest, re, time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

TIMEOUT_LOAD_PAGE = 20  # ограничение на время загрузки страницы, в сек
URL = "http://avtobazar.ua/poisk/avto/?country1=1911&show_only=only_used&per-page=10"


class SearchPageElements(unittest.TestCase):


	@classmethod
	def setUp(cls):
		cls.t_start = time.perf_counter()
		# TODO - организовать выбор различных браузеров
		cls.driver = webdriver.Firefox()
		cls.driver.set_page_load_timeout(TIMEOUT_LOAD_PAGE)

		# navigate to the application home page
		try:
			cls.driver.get(URL)
		except TimeoutException:
			print("Page load timeout > %s sec.!!!" % TIMEOUT_LOAD_PAGE)

	@classmethod
	def tearDown(cls):
		# close the browser window
		cls.driver.quit()
		cls.t_end = time.perf_counter()
		print("test duration - %d sec." % (cls.t_end - cls.t_start))

	# Клик на Поиск верхнего блока
	def run_the_filter(self):
		# Нахожу кнопку Поиск1
		xpath = '//*[@id="search_form"]/div[8]/div/button'
		self.button_search = self.driver.find_element_by_xpath(xpath)
		# Запускаю фильтр
		self.button_search.submit()

	# Клик на Поиск нижнего блока
	def run_the_filter_bottom(self):
		# Нахожу кнопку Поиск2
		xpath = './/*[@id="search_form"]/div[22]/button'
		self.button_search = self.driver.find_element_by_xpath(xpath)
		# Запускаю фильтр
		self.button_search.submit()

	# Сбор данных в списке объявлений в словарь
	def output_ads_list(self):
		driver = self.driver

		xpath = "//div[@class='row advert-item'] | //div[@class='row advert-item orange']"
		ad_div = driver.find_elements_by_xpath(xpath)
		ads = []
		for i in ad_div:

			adr = i.text.split('сохранить сравнить\n')
			if adr[1].count('\n') == 1:
				adr[1] = 'None\nNone\n' + adr[1]
			elif adr[1].count('\n') == 2:
				adr[1] = 'None\n' + adr[1]

			adr[1] = 'сохранить сравнить\n' + adr[1]
			adr = (adr[0] + adr[1]).split('\n')

			cars, *tehdata, price, _, _, salon, firm, city, period_for = adr
			ad = {'cars': ' '.join(cars.split()[:-1]), 'year': cars.split()[-1], 'tehdata': tehdata, 'price': price, 'salon': salon,
			       'firm': firm, 'city': city.split('/')[-1].strip(), 'period_for': period_for}

			ads.append(ad)
		return ads

	# Собираем линки на конечные страницы объявлений
	def output_link_ads_list(self):
		driver = self.driver

		xpath = "//div[@class='row advert-item']/div[1]/div/a"
		ad_div = driver.find_elements_by_xpath(xpath)
		link_list = [i.get_attribute('href') for i in ad_div]
		return link_list

	# Установка диапазона велечин
	def input_range_value(self, id_from, id_to, value_from, value_to):
		# TODO добавить проверку на наличие элементов и правильности ввода текста
		val_from = self.driver.find_element_by_id(id_from)
		val_from.send_keys(value_from)

		val_to = self.driver.find_element_by_id(id_to)
		val_to.send_keys(value_to)

	# Выбор чекбокса
	def selection_checkbox(self, id):
		# TODO добавить проверку на наличие элементов, видимость, enable  и правильности ввода текста
		self.driver.find_element_by_id(id).click()

	# Выбор из выпадающего спсика поиск по шаблону
	def click_select_id(self, id_el, pattern):
		element = self.driver.find_element_by_id(id_el)
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

	# Переход по пагинатору
	def crossings_between_pages(self, n_page):
		xpath = './/*[@id="pagination"]/div/ul/li[' + n_page + ']/a'  # выбираем в пагинаторе последниюю стр.
		self.driver.find_element_by_xpath(xpath).click()
		# TODO - надо обобщить переход по другим стр

	# Сбор на конечном объявлении технических данных автомобиля
	def output_ad_teh_data(self):
		xpath = '//table[@class="table table-hover"]/tbody/tr/child::*'
		li = [i.text for i in self.driver.find_elements_by_xpath(xpath)]
		ad_teh_data = dict(zip(li[::2], li[1::2]))

		return ad_teh_data

	# Сбор на конечном объявлении опций автомобиля
	def output_ad_options(self):
		xpath = '//div[@class="col-xs-12 features clearfix"]/child::*'
		options = self.driver.find_elements_by_xpath(xpath)
		options = [i.text.replace('\n',', ') for i in options]
		ad_options = {'options': ', '.join(options)}

		return ad_options