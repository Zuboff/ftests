import unittest, re
from .search_list_page import SearchPageElements
from selenium.common.exceptions import TimeoutException

# Вводимые данные для теста
MAKE = 'ВАЗ'
MODEL = '2106'
FALSE_MAKE = 'Toyota'
FALSE_MODEL = 'Z3'

PRICE_FROM = '10000'
PRICE_TO = '11000'

YEAR_FROM = '1984'
YEAR_TO = '1999'

COUNTRY = 'Украина'
CITY = 'Киев'
PERIOD_FOR = '2 недели'

MILEAGE_FROM = '10'
MILEAGE_TO = '60'

ENGINE_CAPACITY_FROM = '2'
ENGINE_CAPACITY_TO = '2.5'

COLOR = 'черный'
TRANSMISSION = 'Автомат'
ENGINE = 'Бензин'

NUMBER_ON_PAGE = "100"

# TODO - обработчик "selenium.common.exceptions.TimeoutException: Message: Timed out waiting for page load."
# TODO - сортировка по времени размещения оъявлений - ?
# TODO - показывать только новые объявления
# TODO - проверка работы "Умных фильтров" - ?
# TODO - проверить диапазоны для мощности л.с.
# TODO проверка добавления дополнительной марки/модели
# TODO проверка работы плашки с указателями фильтров

class SearchTests(SearchPageElements):

	def test_changes_number_ads_page(self):
		# Тестируем выдачу кол-ва объвлений на стр. согласно выбора
		self.click_dropdown_menu(NUMBER_ON_PAGE) # надо устанавливать max размер окна, иначе click не доступен
		count = self.output_link_ads_list()
		self.assertEqual(len(count), int(NUMBER_ON_PAGE))
		print("Изменения кол-ва объявлений  тест прошел, объявлений на стр.: '%s'" % NUMBER_ON_PAGE)


	#@unittest.skip("debugging code")
	def test_sorting_year_ads(self):
		# Тестируем сортировку по году
		sorting_direction = self.click_sorting_ads('year')
		ads = self.output_ads_list('ordinary')
		ls_year = [i.get('year') for i in ads if i.get('year') is not None]

		if sorting_direction == 'ab ab-arrow-up2':
			self.assertEqual(sorted(ls_year), ls_year)
		else:
			print("Сортировка по возрастанию года не включается, включается '%s'" % sorting_direction)

		sorting_direction = self.click_sorting_ads('year')
		ads = self.output_ads_list('ordinary')
		ls_year = [i.get('year') for i in ads if i.get('year') is not None]

		if sorting_direction == 'ab ab-arrow-down2':
			self.assertEqual(sorted(ls_year, reverse=True), ls_year)
		else:
			print("Сортировка по убыванию года не включается, включается '%s'" % sorting_direction)

		print("сортировка списка объявлений по возрастанию и убыванию года, тест прошла ")


	#@unittest.skip("debugging code")
	def test_sorting_price_ads(self):
		# Тестируем  сортировку по цене
		# Кликаем на сортировку по цене
		sorting_direction = self.click_sorting_ads('price')
		ads = self.output_ads_list('ordinary')
		ls_price = self.currency_conversion(ads)
		if sorting_direction == 'ab ab-arrow-up2':
			self.assertEqual(sorted(ls_price), ls_price)
		else:
			print("Сортировка по возрастанию цены не включается, включается '%s'" % sorting_direction)

		# Кликаем еще раз на сортировку по цене
		sorting_direction = self.click_sorting_ads('price')
		ads = self.output_ads_list('ordinary')
		ls_price = self.currency_conversion(ads)
		if sorting_direction == 'ab ab-arrow-down2':
			self.assertEqual(sorted(ls_price, reverse=True), ls_price)
		else:
			print("Сортировка по убыванию цены не включается, включается '%s'" % sorting_direction)

		print("сортировка списка объявлений по возрастанию цены и убыванию, тест прошла ")



	def select_show_only(self, id, text):
		# Хелпер по выбору  параметров и запуска из списка "Показвать только"
		pattern = re.compile('Показывать только')
		self.click_select_id(id, pattern)
		self.run_the_filter_bottom()

		ads = self.output_ads_list('ordinary', 'orange')
		for i in ads:
			data = ' '.join(i.get('tehdata'))
			self.assertIn(text, data)
		print("выбор <показывать только '%s' авто> прошел тест" % text)


	#@unittest.skip("debugging code")
	def test_select_rent_cars(self):
		# Проверка выдачи только арендных авто
		self.select_show_only('id_rent', 'аренда')

	#@unittest.skip("debugging code")
	def test_select_credit_cars(self):
		# Проверка выдачи только кредитных авто
		self.select_show_only('id_in_credit', 'кредитный')

	#@unittest.skip("debugging code")
	def test_select_dtp_cars(self):
		# Проверка выдачи только авто после ДТП
		self.select_show_only('id_after_dtp', 'после ДТП')

	#@unittest.skip("debugging code")
	def test_not_cleared_cars(self):
		# Проверка выдачи только не растаможенных авто
		self.select_show_only('id_no_customs', 'не растаможен')

	#@unittest.skip("debugging code")
	def test_car_exchange(self):
		# Проверка выдачи только авто на обмен
		self.select_show_only('id_exchange', 'обмен')

	#@unittest.skip("debugging code")
	def test_diler_cars(self):
		# Проверка выдачи только авто дилеров
		self.driver.implicitly_wait(10) # TODO - Explicit Waits надо установить
		pattern = re.compile('Показывать только')
		self.click_select_id('id_autosalon_own', pattern)
		self.run_the_filter_bottom()

		ads = self.output_ads_list('ordinary', 'orange')
		for i in ads:
			data = i.get('firm')
			self.assertNotIn('None', data)
		print("выбор <показывать только авто автодилеров > прошел тест")


	#@unittest.skip("debugging code")
	def test_end_page_ads(self):
		self.remove_top_plate()
		# Выбрали авто с передним приводом
		self.selection_checkbox('id_drive_0')
		# Выбрали авто с типом кузова "Седан"
		self.selection_checkbox('id_categories_0')
		# Выбрали авто на "Газе"
		self.selection_checkbox('id_engine_features_0')
		# Выбрали авто с полной компектации
		self.selection_checkbox('id_features_0')
		# Открыть отдельное объявление и собрать информацию
		n = 5  # кол-во открываемых объявлений

		link_list = self.output_link_ads_list()
		for i in link_list[:n]:
			self.driver.get(i)
			self.assertIn('Седан', self.output_ad_teh_data()['Кузов'])
			self.assertIn('газ', self.output_ad_teh_data()['Двигатель'])
			self.assertIn('Передний', self.output_ad_teh_data()['Привод'])
			self.assertIn('Полная комлектация', self.output_ad_options()['options'])

		print("выбор <Кузов:cедан + Топливо:газ + Привод:передний + Опции:полная комлектация> прошел тест")

	#@unittest.skip("debugging code")
	def test_input_price(self):
		# Нахожу поля установки диапазона цены на авто
		# Устанавливаю нижнюю и верхнюю цену
		self.input_range_value('id_price_from', 'id_price_to', PRICE_FROM, PRICE_TO)
		# Запускаю фильтр и собираю вывод
		self.run_the_filter()
		ads = self.output_ads_list('ordinary', 'orange')
		# Проверяю попадает ли результат в заданный диапазон
		for i in ads:
			price = i.get('price_$')
			self.assertGreaterEqual(price, int(PRICE_FROM))
			self.assertGreaterEqual(int(PRICE_TO), price)

		print("выбор <диапазон цен с %s $ по %s $> прошел тест" % (PRICE_FROM, PRICE_TO))

	#@unittest.skip("debugging code")
	def test_pick_period_for(self):
		# TODO - обработать ситуацию, когда на последней стр нет списка объявлений
		pattern = re.compile(PERIOD_FOR)
		field_selection_period_for = self.click_select_id('id_period', pattern)
		self.assertIn(PERIOD_FOR, field_selection_period_for)

		self.run_the_filter()

		self.remove_top_plate()
		self.crossings_between_pages('last()') # переход на последнюю стр

		xpath = './/*[@id="items-list"]/div[last()]/*/div[4]/div[2]'  # выбираем в списке  последнее объявление
		period_for = self.driver.find_element_by_xpath(xpath)
		#print("1" + period_for.text)
		period_for = period_for.text.split()[0]
		#print("2" + period_for)
		self.assertGreaterEqual(14, int(period_for)) #FIXME 2 недели ручками в 14 дней

		print("выбор <периода просмотра объявлений %s> прошел тест" % PERIOD_FOR)

	#@unittest.skip("debugging code")
	def test_input_teh_data(self):
		# Убираем верхнюю плашку
		self.remove_top_plate()
		# Вводим Пробег/КПП/Цвет/ТипТоплива/ОбъемДвигателя
		self.input_range_value('id_mileage_from', 'id_mileage_to', MILEAGE_FROM, MILEAGE_TO)
		self.run_the_filter()
		self.selection_checkbox('id_gearbox_0')
		self.selection_checkbox('id_color_0')
		self.selection_checkbox('id_engine_0')
		self.input_range_value('id_capacity_from', 'id_capacity_to', ENGINE_CAPACITY_FROM, ENGINE_CAPACITY_TO)
		self.run_the_filter_bottom()

		# time.sleep(10)
		# Собираем результаты из списка объявлений в словарь
		ads = self.output_ads_list('ordinary', 'orange')
		for i in ads:
			milage = i.get('tehdata')[1]
			milage = int(milage.split()[0])
			self.assertGreaterEqual(milage, int(MILEAGE_FROM))
			self.assertGreaterEqual(int(MILEAGE_TO), milage)

			capacity = i.get('tehdata')[0]
			capacity = float(capacity.split()[1])
			self.assertGreaterEqual(capacity, float(ENGINE_CAPACITY_FROM))
			self.assertGreaterEqual(float(ENGINE_CAPACITY_TO), capacity)

			color_car = i.get('tehdata')[3]
			self.assertIn(COLOR, color_car)

			transmission = i.get('tehdata')[2]
			self.assertIn(TRANSMISSION, transmission)

			engine = i.get('tehdata')[0]
			engine = ''.join(engine)
			self.assertIn(ENGINE, engine)

		print("выбор <пробег: c %s по %s + КПП:%s + цвет:%s + тип_топлива:%s + "
				"объем двигателя: c %s по %s > прошел тест"
				%(MILEAGE_FROM, MILEAGE_TO, TRANSMISSION, COLOR,ENGINE,ENGINE_CAPACITY_FROM,ENGINE_CAPACITY_TO))

	#@unittest.skip("debugging code")
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

	# Выбираю MODEL
		pattern = re.compile('(.+)?' + MODEL)
		field_selection_model = self.click_select_id('id_model1', pattern)
	# Проверяю, что  не срабатывание на ошибочное слово слово
		self.assertNotIn(FALSE_MODEL, field_selection_model)
	# Проверяю, что срабатывание на нужное слово
		self.assertIn(MODEL, field_selection_model)

	# Устанавливаю нижнюю границу YEAR_FROM
		pattern = re.compile(YEAR_FROM)
		field_selection_year_from = self.click_select_id('id_year_from', pattern)
		self.assertIn(YEAR_FROM, field_selection_year_from)
	# Устанавливаю верхнюю границу YEAR_TO
		pattern = re.compile(YEAR_TO)
		field_selection_year_to = self.click_select_id('id_year_to', pattern)
		self.assertIn(YEAR_TO, field_selection_year_to)

	# Выбираю страну "Украина"
		pattern = re.compile(COUNTRY)
		field_selection_country = self.click_select_id('id_country1', pattern)
		self.assertIn(COUNTRY, field_selection_country)
	# Выбираю город "Киев"
		pattern = re.compile(CITY + '$' + '|' + CITY + '\s')
		field_selection_city = self.click_select_id('id_region1', pattern)
		self.assertIn(CITY, field_selection_city)

	# TODO проверка добавления дополнительного региона

	# Запускаю фильтр
		self.run_the_filter()

	# Нахожу список объявлений удовлетворяющих всем требованиям фильтра
		ads = self.output_ads_list('ordinary', 'orange')
		for i in ads:
			make = i.get('cars').split()[0]
			self.assertIn(MAKE, make)

			model = i.get('cars').split()[1]
			self.assertIn(MODEL, model)

			year = int(i.get('year'))
			self.assertGreaterEqual(year, int(YEAR_FROM))
			self.assertGreaterEqual(int(YEAR_TO), year)

			city = i.get('city')
			self.assertIn(CITY, city)

		print("выбор <марки: %s + модели: %s + период годов : c %s по %s + город: %s> прошел тест"
				%(MAKE, MODEL, YEAR_FROM, YEAR_TO, CITY))


if __name__ == '__main__':
	unittest.main(verbosity=2)
