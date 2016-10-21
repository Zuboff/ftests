# -*- encoding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import unittest, time, csv
import urllib.request

#TODO - перейти к следующе странице, если сервер не отвечает
#import socket
#timeout = 10
#socket.setdefaulttimeout(timeout)

TIMEOUT = 7
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
print("Settings: \n HOST: %s\n TIMEOUT: %s sec." % (HOST,TIMEOUT))


class SeoMetaTagTest(unittest.TestCase):

	@classmethod
	def setUp(cls):
		cls.data = list(csv.reader(the_page))
		cls.browser = webdriver.Firefox()
		cls.browser.set_page_load_timeout(TIMEOUT)

#TODO - надо функцию, которая проверяет наличие всех элементов на стр. def: check_exists_by_xpath(self, xpath)

	#def check_exists_by_xpath(self, XPATH):
	#	for i in XPATH:
	#		try:
	#			self.browser.find_element_by_xpath(i)
	#		except NoSuchElementException:
	#			return False
	#		return True

	def check_exists_by_xpath(self, xpath):
		try:
			self.browser.find_element_by_xpath(xpath)
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
				self.browser.get(url)
			except TimeoutException:
				print("Page load timeout > %s sec.!!!" % TIMEOUT)

			self.check_exists_by_xpath("//meta[@name='description']")
			self.check_exists_by_xpath("//h1")


			try:
				self.assertEqual(title.strip(), self.browser.title.strip())
			except AssertionError:
				print("%s META_TITLE - incorrect,\n  is - %s <!> must - %s " % (url, self.browser.title,title))

			if self.check_exists_by_xpath("//meta[@name='description']"):
				description = self.browser.find_element_by_xpath("//meta[@name='description']").get_attribute('content')
				description = description.strip()
				md = descr.strip()
				try:
					self.assertSequenceEqual(md, description)
				except AssertionError:
					print("%s  DESCRIPTION - incorrect,\n  is - %s <!> must - %s " % (url, description, md))
			else:
				print("META_DESCRIPTION not found \n")

			if self.check_exists_by_xpath("//h1"):
				H1 = self.browser.find_element_by_tag_name("h1").text
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
		cls.browser.quit()

if __name__ == '__main__':
	unittest.main()
	# unittest.main(warnings='ignore')



