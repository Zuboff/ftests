from selenium.webdriver.common.by import By


class FilterSearchListLocators(object):
	MAKE = (By.ID, 'id_make1')
	MODEL = (By.ID, 'id_model1')
	YEAR_FROM = (By.ID, 'id_year_from')
	YEAR_TO = (By.ID, 'id_year_to')
	COUNTRY = (By.ID, 'id_country1')
	CITY = (By.ID, 'id_region1')
	MILEAGE_FROM = (By.ID, 'id_mileage_from')
	MILEAGE_TO = (By.ID, 'id_mileage_to')
	ENGINE_CAPACITY_FROM = (By.ID, 'id_capacity_from')
	ENGINE_CAPACITY_TO = (By.ID, 'id_capacity_to')
	PERIOD_FOR = (By.ID, 'id_period')
	COLOR = (By.ID, 'id_color_0')
	TRANSMISSION = (By.ID, 'id_gearbox_0')
	ENGINE = (By.ID, 'id_engine_0')
	PRICE_FROM = (By.ID, 'id_price_from')
	PRICE_TO = (By.ID, 'id_price_to')
	AUTOSALON_OWN = (By.ID, 'id_autosalon_own')  # продают автосалоны
	IN_CREDIT = (By.ID, 'id_in_credit')  # авто в кредите
	AFTER_DTP = (By.ID, 'id_after_dtp')  # авто после ДТП
	NO_CUSTOMS = (By.ID, 'id_no_customs')  # не растаможенные авто
	EXCHANGE = (By.ID, 'id_exchange')  # авто на обмен
	RENT = (By.ID, 'id_rent')
	FRONT_WHEEL_DRIVE = (By.ID, 'id_drive_0')  # передний привод
	BODY_TYPE_SEDAN = (By.ID, 'id_categories_0')  # тип кузова - седан
	ENGINE_GAS = (By.ID, 'id_engine_features_0')  # двигатель на -  газе
	COMPLETE_PACKAGE = (By.ID, 'id_features_0')  # авто - с полной комплектацией

	GO_BUTTON_1 = (By.CSS_SELECTOR, "div.col-xs-12  button[class*='btn-block']")  # верхняя кнопка поиск в фильтре
	GO_BUTTON_2 = (By.CSS_SELECTOR, "div  button[class*='minor-margin-top']")  # нижняя кнопка поиска в фильтре


class SearchListResultLocators(object):
	ADS_ORDINARY = (By.CSS_SELECTOR, "div[class='row advert-item']")  # обыкновенные объявления
	ADS_ORANGE = (By.CSS_SELECTOR, "div[class='row advert-item orange']")  # рекламные объявления "оранжевые"
	AD_LINK = (By.CSS_SELECTOR, "div[class='row advert-item'] * div.h4 a")  # ссылка на объявление
	PAGINATION = (By.LINK_TEXT, '%s')  # не ясно как передвать параметр/номер страницы


class SortingSectionLocators(object):
	PRICE_SORT = (By.CSS_SELECTOR, "a[data-sort='price']")
	YEAR_SORT = (By.CSS_SELECTOR, "a[data-sort='year']")
	DATE_SORT = (By.CSS_SELECTOR, "a[data-sort='date']")
	PRICE_SORT_ARROW = (By.CSS_SELECTOR, "a[data-sort='price'] i")
	YEAR_SORT_ARROW = (By.CSS_SELECTOR, "a[data-sort='year'] i")
	DATE_SORT_ARROW = (By.CSS_SELECTOR, "a[data-sort='date'] i")


class VehicleCardLocators(object):
	SPECIFICATIONS_TABLE = (By.CSS_SELECTOR, "table[class='table table-hover'] * td")  # вся таблица с характеристиками авто
	OPTIONS_TABLE = (By.CSS_SELECTOR, "div[class='col-xs-12 features clearfix'] *")  # вся таблица с опциями авто





