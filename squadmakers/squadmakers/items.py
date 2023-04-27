# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class Ruta(scrapy.Item):
    titulo = scrapy.Field()
    url = scrapy.Field()
    descripcion = scrapy.Field()
    imagen_ruta = scrapy.Field()
    rutas = scrapy.Field()
    etapas = scrapy.Field()
    distancia = scrapy.Field()
    duracion = scrapy.Field()



class DetalleRuta(scrapy.Field):
    descripcion = scrapy.Field()
    ruta = scrapy.Field()
    titulo_ruta = scrapy.Field()
    imagen_ruta = scrapy.Field()
    km_etapa = scrapy.Field()
    url_ruta = scrapy.Field()







