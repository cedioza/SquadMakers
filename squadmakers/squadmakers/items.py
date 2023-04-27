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
    mapa = scrapy.Field()
    etapas = scrapy.Field()
    distancia = scrapy.Field()
    duracion = scrapy.Field()
    itinerario = scrapy.Field()


class DetalleRuta(scrapy.Field):
    descripcion = scrapy.Field()
    ruta = scrapy.Field()
    titulo_ruta_itinerario = scrapy.Field()
    imagen_ruta = scrapy.Field()
    km_etapa = scrapy.Field()
    url_ruta = scrapy.Field()
    itinerarios = scrapy.Field()
    descripcion_itinerario = scrapy.Field()

class Itinerario(scrapy.Field):
    titulo_ruta = scrapy.Field()
    titulo_itinerario = scrapy.Field()
    cronograma = scrapy.Field()
    ruta = scrapy.Field()
    url_ruta = scrapy.Field()
    mapa_gpx = scrapy.Field()
    mapa_kmz = scrapy.Field()
    itinerario = scrapy.Field()

class Trayecto(scrapy.Field):
    pass


    
    







