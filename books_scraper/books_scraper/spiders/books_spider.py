import scrapy
from books_scraper.items import BooksScraperItem
from scrapy.loader import ItemLoader

class BuscalibreSpider(scrapy.Spider):
	name = "buscalibre"
	page_number = 2
	start_urls = ["https://www.buscalibre.cl/libros-envio-express-chile_t.html"]

	def parse(self, response):
		for book in  response.xpath(".//div[@class='productos pais42']/div"):
			loader = ItemLoader(item=BooksScraperItem(), selector=book)
			loader.add_xpath("name", ".//div[@class='nombre margin-top-10 text-align-left']/text()")
			loader.add_xpath("author", ".//div[@class='autor']/text()")
			yield loader.load_item()

#			name = book.xpath(".//div[@class='nombre margin-top-10 text-align-left']/text()").get()
#			author = book.xpath(".//div[@class='autor']/text()").get()
#			price = book.xpath(".//h3/text()").get()
#			if [name, author, price] != [None, None, None]:
#				yield {
#					"name": name,
#					"author": author,
#					"price": price
#				}

		next_page = "https://www.buscalibre.cl/libros-envio-express-chile_t.html?page=" + str(BuscalibreSpider.page_number)
		if BuscalibreSpider.page_number <= 2: # 134
			BuscalibreSpider.page_number += 1
			yield response.follow(url=next_page, callback=self.parse)
