from functional_tests.base import BasePage
from functional_tests.PageSection.vehicle_card import VehicleCard


class VehiclePage(BasePage):

	def __init__(self, driver):
		super(VehiclePage, self).__init__(driver)

	@property
	def card(self):
		return VehicleCard(self.driver)