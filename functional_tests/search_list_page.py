import unittest, re, time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

TIMEOUT_LOAD_PAGE = 40  # ограничение на время загрузки страницы, в сек
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
		# web elements list ads(dic)
		xpath = '//*[@id="items-list"]/*/div/div[1]/div/a'
		cars = self.driver.find_elements_by_xpath(xpath)

		xpath = '//*[@id="items-list"]/*/*/div[4]/div[1]/a[3]'
		city = self.driver.find_elements_by_xpath(xpath)

		xpath = './/*[@id="items-list"]/*/*/div[3]/div[1]/p[1]/span'
		price = self.driver.find_elements_by_xpath(xpath)

		xpath = './/*[@id= "items-list"]/*/*/div[1]/ul/li[1]'
		fuel_type = self.driver.find_elements_by_xpath(xpath)

		xpath = './/*[@id= "items-list"]/*/*/div[1]/ul/li[2]'
		milage = self.driver.find_elements_by_xpath(xpath)

		xpath = './/*[@id= "items-list"]/*/*/div[1]/ul/li[3]'
		transmission = self.driver.find_elements_by_xpath(xpath)

		xpath = './/*[@id= "items-list"]/*/*/div[1]/ul/li[4]'
		color_car = self.driver.find_elements_by_xpath(xpath)

		xpath = './/*[@id="items-list"]/*/*/div[4]/div[2]'
		period_for = self.driver.find_elements_by_xpath(xpath)

		# формирование словаря
		keyword = ['cars', 'city', 'price', 'milage',
						'transmission', 'fuel_type', 'color_car','period_for']
		ads_list = list(zip(cars, city, price, milage,
						transmission, fuel_type, color_car, period_for))
		# FIXME список отображает неправильно, если один из элементов  в объявлении отсутствует

		ads = []
		for ad in ads_list:
			ad = [i.text for i in ad]
			ads.append(dict(zip(keyword, ad)))

		return ads

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

