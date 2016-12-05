from functional_tests.base import BasePage
from functional_tests.PageSection.filter_section_list import FilterListRegion
from functional_tests.PageSection.search_list_result import SearchListResult
from functional_tests.PageSection.sorting_section import SortingSection


class SearchPage(BasePage):

	def __init__(self, driver):
		super(SearchPage, self).__init__(driver)
		self.url = 'poisk/avto/?country1=1911&show_only=only_used&per-page=10'
		self.open(self.url)

	@property
	def filter(self):
		return FilterListRegion(self.driver)

	@property
	def result(self):
		return SearchListResult(self.driver)

	@property
	def sort(self):
		return SortingSection(self.driver)


