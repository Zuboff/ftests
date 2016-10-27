import unittest, re, time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select


TIMEOUT_LOAD_PAGE = 120  # ограничение на время загрузки страницы, в сек
# Вводимые данные для теста
MAKE = 'BMW'
MODEL = 'X5'
FALSE_MAKE = 'Toyota'
FALSE_MODEL = 'Z3'

PRICE_FROM = ' 10000'
PRICE_TO = ' 11000'

YEAR_FROM = '2000'
YEAR_TO = '2016'

COUNTRY = 'Украина'
CITY = 'Киев'
PERIOD_FOR = 'месяц'

MILEAGE_FROM = ' 10'
MILEAGE_TO = ' 60'

ENGINE_CAPACITY_FROM = ' 2'
ENGINE_CAPACITY_TO = ' 2.5'

COLOR = 'черный'
TRANSMISSION = 'Автомат'
ENGINE = 'Бензин'


#TODO - надо обобщить использования шаблонов для regex
#TODO - обработчик "selenium.common.exceptions.TimeoutException: Message: Timed out waiting for page load."

class SearchTests(unittest.TestCase):

	@classmethod
	def setUp(cls):
		# create a new Firefox session
		cls.driver = webdriver.Firefox()
		#self.driver.implicitly_wait(5)
		cls.driver.set_page_load_timeout(TIMEOUT_LOAD_PAGE)
		#cls.driver.maximize_window()

		# navigate to the application home page
		try:
			cls.driver.get("http://avtobazar.ua/poisk/avto/?country1=1911&show_only=only_used&per-page=10")
		except TimeoutException:
			print("Page load timeout > %s sec.!!!" % TIMEOUT_LOAD_PAGE)

	def click_select_id(self, id_el, pattern):
		element = self.driver.find_element_by_id(id_el)
		select = Select(element)
		for option in select.options:
			value = option.text
			if pattern.search(value):
				option.click()
				break
		return select.first_selected_option.text

	def run_the_filter(self):
		# Нахожу кнопку Поиск1
		xpath = '//*[@id="search_form"]/div[8]/div/button'
		self.button_search = self.driver.find_element_by_xpath(xpath)
		# Запускаю фильтр
		self.button_search.submit()

	def run_the_filter_bottom(self):
		# Нахожу кнопку Поиск2
		xpath = './/*[@id="search_form"]/div[22]/button'
		self.button_search = self.driver.find_element_by_xpath(xpath)
		# Запускаю фильтр
		self.button_search.submit()

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
		# формирование словаря
		keyword = ['cars', 'city', 'price', 'milage', 'transmission', 'fuel_type', 'color_car']
		ads_list = list(zip(cars, city, price, milage, transmission, fuel_type, color_car))
		# FIXME список отображает неправильно, если один из элементов  в объявлении отсутствует

		ads = []
		for ad in ads_list:
			ad = [i.text for i in ad]
			ads.append(dict(zip(keyword, ad)))

		return ads

	def input_range_value(self, id_from , id_to, value_from, value_to):
		# TODO добавить проверку на наличие элементов и правильности ввода текста
		val_from = self.driver.find_element_by_id(id_from)
		val_from.send_keys( value_from)

		val_to = self.driver.find_element_by_id(id_to)
		val_to.send_keys(value_to)

	def selection_checkbox(self, id):
		# TODO добавить проверку на наличие элементов, видимость, enable  и правильности ввода текста
		self.driver.find_element_by_id(id).click()


	# @unittest.skip("debugging code")
	def test_input_price(self):
		# Нахожу поля установки диапазона цены на авто
		# Устанавливаю нижнюю и верхнюю цену
		self.input_range_value('id_price_from', 'id_price_to', PRICE_FROM, PRICE_TO)
		# Запускаю фильтр и собираю вывод
		self.run_the_filter()
		ads = self.output_ads_list()
		# Проверяю попадает ли результат в заданный диапазон
		for i in ads:
			st = i.get('price').split()
			price = int(st[0] + st[1])
			self.assertGreaterEqual(price, int(PRICE_FROM))
			self.assertGreaterEqual(int(PRICE_TO), price)

		print("выбор <диапазон цен> протестирован")

	# @unittest.skip("debugging code")
	def test_input_teh_data(self):
		# Убираем верхнюю плашку
		js = "var elem = document.getElementsByClassName('head-menu-wrap'); elem[0].parentNode.removeChild(elem[0]); "
		self.driver.execute_script(js)
		# Вводим Пробег/КПП/Цвет/ТипТоплива/ОбъемДвигателя
		self.input_range_value('id_mileage_from', 'id_mileage_to', MILEAGE_FROM, MILEAGE_TO)
		self.run_the_filter()
		self.selection_checkbox('id_gearbox_0')
		self.selection_checkbox('id_color_0')
		self.selection_checkbox('id_engine_0')
		self.input_range_value('id_capacity_from', 'id_capacity_to', ENGINE_CAPACITY_FROM, ENGINE_CAPACITY_TO)
		self.run_the_filter_bottom()

		# TODO - заменить time.sleep на Wait, привязаться к урлу?
		# time.sleep(10)
		# Собираем результаты из списка объявлений в словарь
		ads = self.output_ads_list()

		for i in ads:
			milage = int(i.get('milage').split()[0])
			self.assertGreaterEqual(milage, int(MILEAGE_FROM))
			self.assertGreaterEqual(int(MILEAGE_TO), milage)

			capacity = float(i.get('fuel_type').split()[1])
			self.assertGreaterEqual(capacity, float(ENGINE_CAPACITY_FROM))
			self.assertGreaterEqual(float(ENGINE_CAPACITY_TO), capacity)

			color_car = i.get('color_car')
			self.assertIn(COLOR, color_car)

			transmission = i.get('transmission')
			self.assertIn(TRANSMISSION, transmission)

			engine = i.get('fuel_type').split()[0]
			self.assertIn(ENGINE, engine)

		print("выбор <пробега + КПП + цвет + тип топлива + объем двигателя> протестирован")

	# @unittest.skip("debugging code")
	def test_search_by_category(self):
	# Нахожу поисковый блок "Поиск авто"
	# Нахожу поле выбора Марки Авто
		field_selection_name = self.driver.find_element_by_id('id_make1').text
		self.assertIn('Марка', field_selection_name)

	# Выбираю "BMW" из списка
		pattern = re.compile(MAKE + '.+')
		field_selection_make = self.click_select_id('id_make1',pattern)
	# Проверяю, что  не срабатывание на ошибочное слово слово
		self.assertNotIn(FALSE_MAKE, field_selection_make)
	# Проверяю, что срабатывание на нужное слово
		self.assertIn(MAKE, field_selection_make)

	# Выбираю "X5"
		pattern = re.compile('.+' + MODEL)
		field_selection_model = self.click_select_id('id_model1', pattern)
	# Проверяю, что  не срабатывание на ошибочное слово слово
		self.assertNotIn(FALSE_MODEL, field_selection_model)
	# Проверяю, что срабатывание на нужное слово
		self.assertIn(MODEL, field_selection_model)

	# Нахожу поля установки диапазона выпуска авто
	# Устанавливаю нижнюю границу 2000 год
		pattern = re.compile(YEAR_FROM)
		field_selection_year_from = self.click_select_id('id_year_from', pattern)
		self.assertIn(YEAR_FROM, field_selection_year_from)
	# Устанавливаю верхнюю границу 2016 год
		pattern = re.compile(YEAR_TO)
		field_selection_year_to = self.click_select_id('id_year_to', pattern)
		self.assertIn(YEAR_TO, field_selection_year_to)
# TODO проверить что объявления загрузились для указанного периода

	# Нахожу регион в которой продается автомобиль
	# Выбираю страну "Украина"
		pattern = re.compile(COUNTRY)
		field_selection_country = self.click_select_id('id_country1', pattern)
		self.assertIn(COUNTRY, field_selection_country)
	# Выбираю город "Киев"
		pattern = re.compile(r'Киев\b') #FIXME - работает нормально, но шаблон вроде кривой
		field_selection_city = self.click_select_id('id_region1', pattern)
		self.assertIn(CITY, field_selection_city)

	# Добавить дополнительный регион
	# Добавить страну "Украина"
	# Добавить город "Харьков"

	# Нахожу возможно ограничить дату поступления объявления
	# Выбираю объявления за последний месяц
		pattern = re.compile(PERIOD_FOR)
		field_selection_period_for = self.click_select_id('id_period', pattern)
		self.assertIn(PERIOD_FOR, field_selection_period_for)
#TODO проверить что объявления загрузились за "последний месяц" - перейти на последнюю страницу списка?
	# Запускаю фильтр
		self.run_the_filter()

	# Нахожу список объявлений удовлетворяющих всем требованиям фильтра
		ads = self.output_ads_list()

		for i in ads:
			make = i.get('cars').split()[0]
			self.assertIn(MAKE, make)

			model = i.get('cars').split()[1]
			self.assertIn(MODEL, model)

			year = int(i.get('cars').split()[2])
			self.assertGreaterEqual(year, int(YEAR_FROM))
			self.assertGreaterEqual(int(YEAR_TO), year)

			city = i.get('city')
			self.assertIn(CITY, city)

		print("выбор <марки + модели + период годов + город> протестирован")


	@classmethod
	def tearDown(cls):
		# close the browser window
		cls.driver.quit()

if __name__ == '__main__':
	unittest.main(verbosity=2)