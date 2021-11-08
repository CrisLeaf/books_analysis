import scrapy
from books_scraper.items import BooksScraperItem
from scrapy.loader import ItemLoader

class BuscalibreSpider(scrapy.Spider):
	name = "buscalibre"
	page_number = 2
	start_urls = ["https://www.buscalibre.cl/libros-envio-express-chile_t.html"]

	def parse(self, response):
		for book in response.xpath(".//div[@class='productos pais42']/div"):
			loader = ItemLoader(item=BooksScraperItem(), selector=book)
			loader.add_xpath("name", ".//div[@class='nombre margin-top-10 text-align-left']")
			loader.add_xpath("author", ".//div[@class='autor']")
			loader.add_xpath("link", ".//a/@href")
			loader.add_xpath("price", ".//h3")
			loader.add_value("website", "buscalibre")
			yield loader.load_item()
		next_page = "https://www.buscalibre.cl/libros-envio-express-chile_t.html?page=" + str(BuscalibreSpider.page_number)
		if BuscalibreSpider.page_number <= 134:
			BuscalibreSpider.page_number += 1
			yield response.follow(url=next_page, callback=self.parse)

class AntarticaSpider(scrapy.Spider):
	name = "antartica"
	start_urls = ["https://www.antartica.cl/libros.html", "https://www.antartica.cl/libros/infantil-y-juvenil.html"]

	def parse(self, response):
		for category in response.xpath(".//ul[@class='static-search--links']/li/a"):
			category_link = category.xpath("@href").get()
			yield response.follow(url=category_link, callback=self.parse_item)

	def parse_item(self, response):
		for book in response.xpath(".//div[@class='product details product-item-details']"):
			loader = ItemLoader(item=BooksScraperItem(), selector=book)
			loader.add_xpath("name", ".//strong/a")
			loader.add_xpath("author", ".//div/a")
			loader.add_xpath("link", ".//strong/a/@href")
			loader.add_xpath("price", ".//span/span/span/span")
			loader.add_value("website", "antartica")
			yield loader.load_item()
		try:
			next_page = response.xpath(".//a[@class='next-page']/@href").get()
		except:
			next_page = None
		if next_page is not None:
			print(next_page)
			yield response.follow(url=next_page, callback=self.parse_item)

class FeriachilenaSpider(scrapy.Spider):
	name = "feriachilena"
	start_urls = [
		"https://feriachilenadellibro.cl/categoria-producto/agendas-y-calendarios/",
		"https://feriachilenadellibro.cl/categoria-producto/arquitectura-y-urbanismo/",
		"https://feriachilenadellibro.cl/categoria-producto/arte-y-diseno/",
		"https://feriachilenadellibro.cl/categoria-producto/autoayuda-y-esoterismo/autoayuda/",
		"https://feriachilenadellibro.cl/categoria-producto/books-about-chile/",
		"https://feriachilenadellibro.cl/categoria-producto/ciencia-y-naturaleza/",
		"https://feriachilenadellibro.cl/categoria-producto/ciencias-sociales/",
		"https://feriachilenadellibro.cl/categoria-producto/deportes/",
		"https://feriachilenadellibro.cl/categoria-producto/derecho/",
		"https://feriachilenadellibro.cl/categoria-producto/diccionarios-y-enciclopedias/",
		"https://feriachilenadellibro.cl/categoria-producto/economia-y-negocios/",
		"https://feriachilenadellibro.cl/categoria-producto/ensayos-y-biografias/",
		"https://feriachilenadellibro.cl/categoria-producto/esoterismo/",
		"https://feriachilenadellibro.cl/categoria-producto/entretencion/",
		"https://feriachilenadellibro.cl/categoria-producto/filosofia/",
		"https://feriachilenadellibro.cl/categoria-producto/gastronomia-cocina-vinos/",
		"https://feriachilenadellibro.cl/categoria-producto/geografia-2/",
		"https://feriachilenadellibro.cl/categoria-producto/historia/",
		"https://feriachilenadellibro.cl/categoria-producto/hogar-y-familia/",
		"https://feriachilenadellibro.cl/categoria-producto/informatica-e-internet/",
		"https://feriachilenadellibro.cl/categoria-producto/ingenieria/",
		"https://feriachilenadellibro.cl/categoria-producto/libros-infantiles/",
		"https://feriachilenadellibro.cl/categoria-producto/libros-juveniles/",
		"https://feriachilenadellibro.cl/categoria-producto/literatura/",
		"https://feriachilenadellibro.cl/categoria-producto/literatura-escolar/",
		"https://feriachilenadellibro.cl/categoria-producto/medicina/",
		"https://feriachilenadellibro.cl/categoria-producto/medicina-alternativa/",
		"https://feriachilenadellibro.cl/categoria-producto/musica-cine-ballet-teatro/",
		"https://feriachilenadellibro.cl/categoria-producto/ocio-y-hobbies/",
		"https://feriachilenadellibro.cl/categoria-producto/politica-2/",
		"https://feriachilenadellibro.cl/categoria-producto/religion/",
		"https://feriachilenadellibro.cl/categoria-producto/sexologia/",
		"https://feriachilenadellibro.cl/categoria-producto/tecnologia/",
		"https://feriachilenadellibro.cl/categoria-producto/textos-de-estudio/",
		"https://feriachilenadellibro.cl/categoria-producto/turismo-y-viajes/"
	]

	def parse(self, response):
		for book in response.xpath(".//div[@class='astra-shop-summary-wrap']"):
			item_link = book.xpath(".//a[@class='ast-loop-product__link']/@href").get()
			yield response.follow(url=item_link, callback=self.parse_item)
		try:
			next_page = response.xpath(".//a[@class='next page-numbers']/@href").get()
		except:
			next_page = None
		if next_page is not None:
			yield response.follow(url=next_page, callback=self.parse)

	def parse_item(self, response):
		loader = ItemLoader(item=BooksScraperItem(), selector=response)
		loader.add_xpath("name", ".//h1[@class='product_title entry-title']/text()")
		loader.add_xpath("author", ".//div[@class='woocommerce-product-details__short-description']/p")
		loader.add_xpath("link", "head/link[@rel='canonical']/@href")
		loader.add_xpath("price", ".//p[@class='price']/span/bdi/text()")
		loader.add_value("website", "feriachilena")
		yield loader.load_item()