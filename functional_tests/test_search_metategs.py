# -*- encoding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import unittest, time, csv, socket
import urllib.request

#TODO - перейти к следующе странице, если сервер не отвечает

TIMEOUT_RESPONSE_TIME = 10 # ограничение на время отклика сервера
TIMEOUT_LOAD_PAGE = 6  # ограничение на время загрузки страницы, в сек
HOST = 'http://avtobazar.ua'
#HOST = 'http://old.avtobazar.ua:8000'
URL = 'https://docs.google.com/spreadsheet/ccc?key=1XIlpiHQqKA_hRAdWporzDapY2TYKJZZVp-duOnpmbx8&output=csv'
XPATH = ["//meta[@name='description']","//h1"]


req = urllib.request.Request(URL)
with urllib.request.urlopen(req) as response:
	the_page = response.read()
the_page = the_page.decode('utf-8').splitlines()

t_start = time.perf_counter()

print("Validation tags to SEO: 'META_TITLE, META_DESCRIPTION, H1 ")
print("Settings: \n HOST: %s\n TIMEOUT_RESPONSE_TIME: %s sec.\n TIMEOUT: %s sec." % (HOST,TIMEOUT_RESPONSE_TIME,TIMEOUT_LOAD_PAGE))


class SeoMetaTagTest(unittest.TestCase):


	@classmethod
	def setUp(cls):
		cls.data = list(csv.reader(the_page))

		cls.firefoxProfile = webdriver.FirefoxProfile()
		cls.firefoxProfile.set_preference("http.response.timeout", 10)
		cls.driver = webdriver.Firefox(cls.firefoxProfile)
		cls.driver.set_page_load_timeout(TIMEOUT_LOAD_PAGE)
		#socket.setdefaulttimeout(TIMEOUT_RESPONSE_TIME)

		

#TODO - надо функцию, которая проверяет наличие всех элементов на стр. def: check_exists_by_xpath(self, xpath)

	def check_exists_by_xpath(self, xpath):
		try:
			self.driver.find_element_by_xpath(xpath)
		except NoSuchElementException:
			return False
		return True

	def test_check_spelling_meta_tag(self):

		i = 0
		for url,title,descr,h1 in self.data[1:]:
			start = time.perf_counter()
			url = HOST + url
			i += 1
			print(("\n %s. test > " + url) % i)

			try:
				try:
					#socket.setdefaulttimeout(TIMEOUT_RESPONSE_TIME)
					self.driver.get(url)
				except socket.timeout:
					print("Response server timeout > %s sec.!!!" % TIMEOUT_RESPONSE_TIME)
					continue
			except TimeoutException:
				print("Page load timeout > %s sec.!!!" % TIMEOUT_LOAD_PAGE)

			#socket.setdefaulttimeout(None)
			try:
				self.assertEqual(title.strip(), self.driver.title.strip()) #FIXME -  срабатывает исключение socket.timeout old.avtobazar.ua
			except AssertionError:
				print("%s META_TITLE - incorrect,\n  is - %s <!> must - %s " % (url, self.driver.title,title))
				#print("!!!!!!!!!!!!!Exception - %s" % e)

			if self.check_exists_by_xpath("//meta[@name='description']"):
				description = self.driver.find_element_by_xpath("//meta[@name='description']").get_attribute('content')
				description = description.strip()
				md = descr.strip()
				try:
					self.assertSequenceEqual(md, description)
				except AssertionError:
					print("%s  DESCRIPTION - incorrect,\n  is - %s <!> must - %s " % (url, description, md))
			else:
				print("META_DESCRIPTION not found \n")

			if self.check_exists_by_xpath("//h1"):
				H1 = self.driver.find_element_by_tag_name("h1").text
				H1 = H1.strip()
				mh = h1.strip()
				try:
					self.assertSequenceEqual(h1, H1)
				except AssertionError:
					print("%s H1 - incorrect,\n  is - %s <!> must - %s " % (url, H1, mh))
			else:
				print("H1 not found")

			end = time.perf_counter()
			duration = end - start
			print("test duration - %s is - %d sec." % (url,duration))

		t_end = time.perf_counter()
		print("Tests Ended, total duration - %d sec." %(t_end - t_start))

	@classmethod
	def tearDown(cls):
		cls.driver.quit()

if __name__ == '__main__':
	unittest.main()
	# unittest.main(warnings='ignore')



