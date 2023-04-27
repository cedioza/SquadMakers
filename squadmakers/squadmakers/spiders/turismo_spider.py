from squadmakers.items import Ruta, DetalleRuta

import re

import scrapy

class TurismoSpider(scrapy.Spider):
    name = "turismo"
    allowed_domains = ['turismomadrid.es']
    start_urls = ['https://turismomadrid.es/es/rutas.html']

    def get_images(self,path_image):
        url_image = re.search('url\(\'(.+?)\'\)', path_image).group(1)
        return 'https://' + self.allowed_domains[0] + url_image
        

    def start_requests(self):
        urls = [
            'https://turismomadrid.es/es/rutas.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

 # esta es el nivel  nivel1/2
    def parse(self, response):
         
         url = response.url.replace("es/rutas.html", "")
         rutas = response.xpath("//*[contains(@class, 'uk-child-width')][2]/a")
    
         for ruta in rutas:
             item = Ruta()
             item["titulo"] = ruta.xpath(".//h2/text()").get()
             path_image =  ruta.xpath('.//div[contains(@style,"background-image")]').get()
             item["imagen_ruta"] =  self.get_images(path_image)
             detalle_url = url+ruta.xpath('@href').get()
             item["url"] = detalle_url

             yield scrapy.Request(url=detalle_url, callback=self.parse_detalle, meta={'item': item})

    def parse_detalle(self, response):
        url = response.url.replace("es/rutas.html", "")
        ruta = response.meta['item']
        
        rutas_detalle = response.xpath("//a[contains(@href, 'nivel')]")
        ruta["etapas"]= len(rutas_detalle)
        detalles = []

        for detalle in rutas_detalle:
            detalle_ruta = DetalleRuta()
            detalle_ruta["ruta"] = detalle.xpath('.//h4/text()').get()
            detalle_ruta["titulo_ruta"] = detalle.xpath(".//h1/text()").get()
            path_image =  detalle.xpath('.//div[contains(@style,"background-image")]').get()
            detalle_ruta["imagen_ruta"] =  self.get_images(path_image)
            detalle_ruta["km_etapa"] = detalle.xpath(".//div[contains(@class, 'dato-etapa')]/text()").get().strip()
            detalle_url = url+detalle.xpath('@href').get()
            detalle_ruta["url_ruta"] = detalle_url
            detalles.append(detalle_ruta)

        ruta["distancia"] = detalle.xpath("//*[contains(@class, 'dato-etapa')]//span/text()").get().strip()
        ruta["duracion"] = response.xpath("//div[@class ='uk-padding-remove-left uk-padding-small']/span/text()").get().strip()
        ruta["descripcion"] = response.xpath("//div[contains(@class, 'descripcion')]/p/text()").get().strip()
        ruta["rutas"] = detalles
        yield ruta        
        # for ruta in rutas_detalle:
        #     detalle_ruta = DetalleRuta()
        #     detalle_ruta["rutas"] = ruta.xpath('.//h4/text()').get()
        #     detalle_ruta["titulo_ruta"] = ruta.xpath(".//h1/text()").get()
        #     detalle_url = url+ruta.xpath('@href').get()
        #     detalle_ruta["url_ruta"] = detalle_url
        #     ruta["detalle"]=detalle_ruta
        #     yield ruta

    #         yield scrapy.Request(url=detalle_url, callback=self.ruta_detalle, meta={'item': item})
    
    # def ruta_detalle(self,response):
    #     item = response.meta['item']
    #     item["descripcion_ruta"] = response.xpath("//div[contains(@class, 'descripcion')]/p/text()").get()
        
    #     yield item

