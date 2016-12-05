# -*- encoding: utf-8 -*-
import unittest, time
from .base_test import BaseTestCase
from .Page.search_page import SearchPage
from .Page.vehicle_page import VehiclePage

class SearchSortTests(BaseTestCase):

	@unittest.skip("debugging code")
	def test_sorting_price_ads(self):
		search_page = SearchPage(self.driver)
		# Кликаем на сортировку по цене
		sorting_direction = search_page.sort.click_sorting_ads('PRICE_SORT')
		ads = search_page.result.output_ads_list('ordinary')
		if not ads:
			print("Объявлений не найдено")
		else:
			ls_price = search_page.result.currency_conversion(ads)
			if sorting_direction == 'ab ab-arrow-up2':
				self.assertEqual(sorted(ls_price), ls_price)
			else:
				print("Сортировка по возрастанию цены не включается, включается '%s'" % sorting_direction)

		# Кликаем еще раз на сортировку по цене
		sorting_direction = search_page.sort.click_sorting_ads('PRICE_SORT')
		ads = search_page.result.output_ads_list('ordinary')
		if not ads:
			print("Объявлений не найдено")
		else:
			ls_price = search_page.result.currency_conversion(ads)
			if sorting_direction == 'ab ab-arrow-down2':
				self.assertEqual(sorted(ls_price, reverse=True), ls_price)
			else:
				print("Сортировка по убыванию цены не включается, включается '%s'" % sorting_direction)

		print("сортировка списка объявлений по возрастанию цены и убыванию, тест прошла ")


	@unittest.skip("debugging code")
	def test_sorting_year_ads(self):
		search_page = SearchPage(self.driver)
		sorting_direction = search_page.sort.click_sorting_ads('YEAR_SORT')
		ads = search_page.result.output_ads_list('ordinary')
		if not ads:
			print("Объявлений не найдено")
		else:
			ls_year = [i.get('year') for i in ads if i.get('year') is not None]
			if sorting_direction == 'ab ab-arrow-up2':
				self.assertEqual(sorted(ls_year), ls_year)
			else:
				print("Сортировка по возрастанию года не включается, включается '%s'" % sorting_direction)

		sorting_direction = search_page.sort.click_sorting_ads('YEAR_SORT')
		ads = search_page.result.output_ads_list('ordinary')
		if not ads:
			print("Объявлений не найдено")
		else:
			ls_year = [i.get('year') for i in ads if i.get('year') is not None]
			if sorting_direction == 'ab ab-arrow-down2':
				self.assertEqual(sorted(ls_year, reverse=True), ls_year)
			else:
				print("Сортировка по убыванию года не включается, включается '%s'" % sorting_direction)

		print("сортировка списка объявлений по возрастанию и убыванию года, тест прошла ")


	@unittest.skip("debugging code")
	def test_changes_number_ads_page(self):
		search_page = SearchPage(self.driver)
		# Тестируем выдачу кол-ва объвлений на стр. согласно выбора
		NUMBER_ON_PAGE = "100"
		search_page.sort.click_dropdown_menu(NUMBER_ON_PAGE)  # надо устанавливать max размер окна, иначе click не доступен
		time.sleep(10) #FiXME
		count = search_page.result.output_link_ads_list()
		self.assertEqual(len(count), int(NUMBER_ON_PAGE))
		print("Изменения кол-ва объявлений  тест прошел, объявлений на стр.: '%s'" % NUMBER_ON_PAGE)

	#@unittest.skip("debugging code")
	def test_end_page_ads(self):
		search_page = SearchPage(self.driver)
		# Убираем 3 плашки которые закрываю контролы
		search_page.filter.remove_top_bottom_cookie_plate()
		# Назначаем тестовые значения
		test_values = {'FRONT_WHEEL_DRIVE': 'Передний', 'BODY_TYPE_SEDAN': 'Седан',
							'ENGINE_GAS': 'газ', 'COMPLETE_PACKAGE': 'Полная комлектация'}
		# кол-во открываемых объявлений для проверки
		n = 5
		# Загружаем тестовые значения
		search_page.filter.select_checkbox(**test_values)
		# Открыть отдельное объявление и собрать информацию
		link_list = search_page.result.output_link_ads_list()
		# Сравниваем результаты с тестовыми значениями
		vehicle_page = VehiclePage(self.driver)

		for i in link_list[:n]:
			self.driver.get(i)
			self.assertIn('Седан', vehicle_page.card.output_ad_teh_data()['Кузов'])
			self.assertIn('газ', vehicle_page.card.output_ad_teh_data()['Двигатель'])
			self.assertIn('Передний', vehicle_page.card.output_ad_teh_data()['Привод'])
			self.assertIn('Полная комлектация', vehicle_page.card.output_ad_options()['options'])

		print("выбор <Кузов:cедан + Топливо:газ + Привод:передний + Опции:полная комлектация> прошел тест")


if __name__ == '__main__':
	unittest.main(verbosity=2)