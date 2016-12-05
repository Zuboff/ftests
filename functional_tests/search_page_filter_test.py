# -*- encoding: utf-8 -*-
import unittest, time
from .base_test import BaseTestCase
from .Page.search_page import SearchPage


class SearchFilterTests(BaseTestCase):

	@unittest.skip("debugging code")
	def test_search_filter(self):
		search_page = SearchPage(self.driver)
		# Назначаем тестовые значения
		test_values = {'MAKE': 'ВАЗ', 'MODEL': '2106', 'YEAR_FROM': '1984',
						'YEAR_TO': '1999', 'COUNTRY': 'Украина', 'CITY': 'Киев'}
		keys_order = ['MAKE', 'MODEL', 'YEAR_FROM', 'YEAR_TO', 'COUNTRY', 'CITY']
		# Загружаем тестовые значения
		search_page.filter.search_by_category(*keys_order, **test_values)
		# Собираем результаты
		ads = search_page.result.output_ads_list('ordinary')
		# Сравниваем результаты с тестовыми значениями
		if not ads:
			print("Объявлений не найдено")
		else:
			for i in ads:
				make = i.get('cars').split()[0]
				self.assertIn(test_values['MAKE'], make)
				model = i.get('cars').split()[1]
				self.assertIn(test_values['MODEL'], model)
				year = int(i.get('year'))
				self.assertGreaterEqual(year, int(test_values['YEAR_FROM']))
				self.assertGreaterEqual(int(test_values['YEAR_TO']), year)

				city = i.get('city')
				self.assertIn(test_values['CITY'], city)
			# Выводим отчет результатов сравнения
			print("выбор <марки: %s + модели: %s + период годов : c %s по %s + город: %s> прошел тест"
									% (test_values['MAKE'], test_values['MODEL'],test_values['YEAR_FROM'],
												test_values['YEAR_TO'], test_values['CITY']))

	@unittest.skip("debugging code")
	def test_input_teh_data(self):
		search_page = SearchPage(self.driver)
		search_list = search_page.filter
		# Убираем 3 плашки которые закрываю контролы
		search_list.remove_top_bottom_cookie_plate()
		# Назначаем тестовые значения
		test_values_1 = {'MILEAGE_FROM': '10', 'MILEAGE_TO': '60'}
		test_values_2 = {'COLOR': 'черный', 'TRANSMISSION': 'Автомат', 'ENGINE': 'Бензин'}
		test_values_3 = {'ENGINE_CAPACITY_FROM': '2', 'ENGINE_CAPACITY_TO': '2.5'}
		# Загружаем тестовые значения
		search_list.input_value(**test_values_1)
		search_list.run_the_filter()
		search_list.select_checkbox(**test_values_2)
		search_list.input_value(**test_values_3)
		search_list.run_the_filter_bottom()
		# Собираем результаты из списка объявлений в словарь
		ads = search_page.result.output_ads_list('ordinary')
		# Сравниваем результаты с тестовыми значениями
		if not ads:
			print("Объявлений не найдено")
		else:
			for i in ads:
				milage = i.get('tehdata')[1]
				milage = int(milage.split()[0])
				self.assertGreaterEqual(milage, int(test_values_1['MILEAGE_FROM']))
				self.assertGreaterEqual(int(test_values_1['MILEAGE_TO']), milage)

				capacity = i.get('tehdata')[0]
				capacity = float(capacity.split()[1])
				self.assertGreaterEqual(capacity, float(test_values_3['ENGINE_CAPACITY_FROM']))
				self.assertGreaterEqual(float(test_values_3['ENGINE_CAPACITY_TO']), capacity)

				color_car = i.get('tehdata')[3]
				self.assertIn(test_values_2['COLOR'], color_car)

				transmission = i.get('tehdata')[2]
				self.assertIn(test_values_2['TRANSMISSION'], transmission)

				engine = i.get('tehdata')[0]
				engine = ''.join(engine)
				self.assertIn(test_values_2['ENGINE'], engine)
			# Выводим отчет результатов сравнения
			print("выбор <пробег: c %s по %s + КПП:%s + цвет:%s + тип_топлива:%s + "
					"объем двигателя: c %s по %s > прошел тест"
					% (test_values_1['MILEAGE_FROM'], test_values_1['MILEAGE_TO'],
					   test_values_2['TRANSMISSION'], test_values_2['COLOR'], test_values_2['ENGINE'],
					   test_values_3['ENGINE_CAPACITY_FROM'], test_values_3['ENGINE_CAPACITY_TO']))

	#@unittest.skip("debugging code")
	def test_pick_period_for(self):
		search_page = SearchPage(self.driver)
		# Убираем 3 плашки которые закрываю контролы
		search_page.filter.remove_top_bottom_cookie_plate()
		# Назначаем тестовые значения
		test_values = {'PERIOD_FOR': '2 недели'}
		# Загружаем тестовые значения
		search_page.filter.search_by_category(**test_values)
		time.sleep(3)  # FiXME
		search_page.result.crossings_between_pages('В конец')
		# Собираем результаты
		ads = search_page.result.output_ads_list('ordinary')
		period_for = ads[-1]['period_for']
		period_for = period_for.split()[0]
		# Сравниваем результаты с тестовыми значениями
		self.assertGreaterEqual(14, int(period_for))  # FIXME 2 недели ручками в 14 дней
		# Выводим отчет результатов сравнения
		print("выбор <периода просмотра объявлений %s> прошел тест"
								% test_values['PERIOD_FOR'])

	#@unittest.skip("debugging code")
	def test_input_price(self):
		search_page = SearchPage(self.driver)
		# Назначаем тестовые значения
		test_values = {'PRICE_FROM': '10000', 'PRICE_TO': '11000'}
		# Загружаем тестовые значения
		search_page.filter.input_value(**test_values)
		search_page.filter.run_the_filter()
		# Собираем результаты
		ads = search_page.result.output_ads_list('ordinary')
		# Сравниваем результаты с тестовыми значениями
		for i in ads:
			price = i.get('price_$')
			self.assertGreaterEqual(price, int(test_values['PRICE_FROM']))
			self.assertGreaterEqual(int(test_values['PRICE_TO']), price)

		print("выбор <диапазон цен с %s $ по %s $> прошел тест"
							% (test_values['PRICE_FROM'],test_values['PRICE_TO']))

	#@unittest.skip("debugging code")
	def test_diler_cars(self):
		search_page = SearchPage(self.driver)
		# Назначаем тестовые значения
		test_values = {'AUTOSALON_OWN': 'Показывать только'}
		# Загружаем тестовые значения
		search_page.filter.search_by_category(**test_values)
		# Собираем результаты
		ads = search_page.result.output_ads_list('ordinary')
		# Сравниваем результаты с тестовыми значениями
		for i in ads:
			data = i.get('firm')
			self.assertNotIn('None', data)
		print("выбор <показывать только авто автодилеров > прошел тест")

	#@unittest.skip("debugging code")
	def select_show_only(self, locator, text):
		# Хелпер по выбору  параметров и запуска из списка "Показвать только"
		search_page = SearchPage(self.driver)
		# Назначаем тестовые значения
		test_values = {locator: 'Показывать только'}
		# Загружаем тестовые значения
		search_page.filter.search_by_category(**test_values)
		# Собираем результаты
		ads = search_page.result.output_ads_list('ordinary')
		# Сравниваем результаты с тестовыми значениями
		for i in ads:
			data = ' '.join(i.get('tehdata'))
			self.assertIn(text, data)
		print("выбор <показывать только '%s' авто> прошел тест" % text)

	#@unittest.skip("debugging code")
	def test_select_rent_cars(self):
		# Проверка выдачи только арендных авто
		self.select_show_only('RENT', 'аренда')

	#@unittest.skip("debugging code")
	def test_select_credit_cars(self):
		# Проверка выдачи только кредитных авто
		self.select_show_only('IN_CREDIT', 'кредитный')

	#@unittest.skip("debugging code")
	def test_select_dtp_cars(self):
		# Проверка выдачи только авто после ДТП
		self.select_show_only('AFTER_DTP', 'после ДТП')

	#@unittest.skip("debugging code")
	def test_not_cleared_cars(self):
		# Проверка выдачи только не растаможенных авто
		self.select_show_only('NO_CUSTOMS', 'не растаможен')

	#@unittest.skip("debugging code")
	def test_car_exchange(self):
		# Проверка выдачи только авто на обмен
		self.select_show_only('EXCHANGE', 'обмен')

if __name__ == '__main__':
	unittest.main(verbosity=2)