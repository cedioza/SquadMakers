from squadmakers.items import Ruta, DetalleRuta, Itinerario, Trayecto
import re
import scrapy

import scrapy
import re

class TurismoSpider(scrapy.Spider):
    name = "turismo"
    allowed_domains = ['turismomadrid.es']
    start_urls = ['https://turismomadrid.es/es/rutas.html']

    # Función para obtener la URL de la imagen
    def get_images(self, path_image):
        url_image = re.search('url\(\'(.+?)\'\)', path_image).group(1)
        return 'https://' + self.allowed_domains[0] + url_image
    
    # Función para obtener la URL completa
    def get_url(self, path_url):
        return 'https://' + self.allowed_domains[0] + path_url

    # Función para enviar la petición inicial
    def start_requests(self):
        urls = [
            'https://turismomadrid.es/es/rutas.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)



    def parse(self, response):
         rutas = response.xpath("//*[contains(@class, 'uk-child-width')][2]/a")
    
         for ruta in rutas:
             item = Ruta()
             item["titulo"] = ruta.xpath(".//h2/text()").get()
             path_image =  ruta.xpath('.//div[contains(@style,"background-image")]').get()
             item["imagen_ruta"] =  self.get_images(path_image)
             detalle_url = self.get_url(ruta.xpath('@href').get())
             item["url"] = detalle_url

             yield scrapy.Request(url=detalle_url, callback=self.parse_detalle, meta={'item': item},dont_filter=True)

    def parse_detalle(self, response):
        ruta = response.meta['item']
        
        rutas_detalle = response.xpath("//a[contains(@href, 'nivel')]")
        ruta["etapas"]= len(rutas_detalle)
        detalles = []

        ruta["duracion"] = response.xpath("//div[@class ='uk-padding-remove-left uk-padding-small']/span/text()").get().strip()
        ruta["descripcion"] = response.xpath("//div[contains(@class, 'descripcion')]/p/text()").get().strip()
        ruta["mapa"] = self.get_url(response.xpath("//div[contains(@class,'uk-width-2-3@m')]/img/@src").get())
        
        for detalle in rutas_detalle:
            detalle_ruta = DetalleRuta()
            ruta["distancia"] = detalle.xpath("//*[contains(@class, 'dato-etapa')]//span/text()").get().strip()
            detalle_ruta["ruta"] = detalle.xpath('.//h4/text()').get()
            detalle_ruta["titulo_ruta"] = detalle.xpath(".//h1/text()").get()
            path_image =  detalle.xpath('.//div[contains(@style,"background-image")]').get()
            detalle_ruta["imagen_ruta"] =  self.get_images(path_image)
            detalle_ruta["km_etapa"] = detalle.xpath(".//div[contains(@class, 'dato-etapa')]/text()").get().strip()
            detalle_url = self.get_url(detalle.xpath('@href').get())
            detalle_ruta["url_ruta"] = detalle_url
            detalle_ruta["itinerarios"] =yield scrapy.Request(url=detalle_url, callback=self.parse_itinerario, meta={'item_rutas': ruta,"item":detalle_ruta})
            detalles.append(detalle_ruta)
            ruta["rutas"] = detalles


         
    def parse_itinerario(self, response):
        ruta = response.meta['item_rutas']
        detalle_ruta = response.meta['item']
            
        itinerario_detalle = response.xpath('//div[@class ="uk-child-width-1-1@m uk-margin-medium-top uk-margin-remove-left uk-padding-remove-left uk-border-dotted"]')
        detalle_ruta["descripcion_itinerario"]= response.xpath('//div[contains(@class, "uk-width-1-2@m")]/p/text()').get()
        itinerarios = []
        for itenerario in itinerario_detalle:    
             itinerario_ruta = Itinerario()
             itinerario_ruta["titulo_ruta_itinerario"] = response.xpath('//h1[@class ="nivel1-titulo"]/text()').get()
             itinerario_ruta["itinerario"] = itenerario.xpath('.//h5/text()').get()
             itinerario_ruta["titulo_itinerario"] = itenerario.xpath('.//h2/text()').get()
             detalle_url = self.get_url(response.xpath('//a[contains(@href, "/nivel3")]/@href').get())
             itinerario_ruta["url_ruta"] = detalle_url
             itinerario_ruta["cronograma"] = yield scrapy.Request(url=detalle_url, callback=self.parse_cronograma_itinerarios, meta={'item_rutas': ruta,"item":detalle_ruta,"item_itirenario":itinerario_detalle})
             itinerarios.append(itinerario_ruta)
            
             detalle_ruta["itinerarios"] = itinerarios

    
    def parse_cronograma_itinerarios(self, response):
        ruta = response.meta['item_rutas']
        detalle_ruta = response.meta['item']
        detalle_itirenario = response.meta['item_itirenario']

        trayecto_detalle = response.xpath('//div[@class="uk-margin-remove-left uk-padding-remove-left uk-padding-large uk-border-dotted uk-grid"]')
        detalle_ruta["descripcion_itinerario"]= response.xpath('//div[contains(@class, "uk-width-1-2@m")]/p/text()').get()
        trayectos = []
        for trayecto in trayecto_detalle:    
             trayecto_ruta = Trayecto()
             trayecto_ruta["titulo_ruta_itinerario"] = response.xpath('//h1[@class ="nivel1-titulo"]/text()').get()
             trayecto_ruta["itinerario"] = trayecto.xpath('.//h5/text()').get()
             trayecto_ruta["titulo_itinerario"] = trayecto.xpath('.//h2/text()').get()
             trayectos.append(trayecto_ruta)
            
             detalle_itirenario["itinerarios"] = trayectos


        yield ruta  