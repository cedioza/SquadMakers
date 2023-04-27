
﻿
# Repositorio prueba técnica de Squadmakers en Python


### Librerías :
- Scrapy: [scrapy](https://scrapy.org)


## Instalación

Instalar con pip:

```
$ pip install -r requirements.txt
```

## Estructura 
```
.
|──────squadmakers/
| |────spiders/
| | |────items.py
| |────middlewares/
| | |────pipelines.py
| |────utils/
| | |────settings.py


```
## Paso a Paso

activar el entorno virtual 

./squadmakers/venv/Scripts/Activate

ubicarnos en la carmeta spiders.py y ejecutar el siguiente comando 

scrapy runspider turismo_spider.py -o resultados.json


## Requisito 

El reto consiste en comprobar tu pericia para extraer información de páginas
web y en construir base de datos. Para el reto vamos a extraer la
información del siguiente link, que nos ofrecen itinerarios para hacer turismo
por Madrid. El objetivo es realizar un script para descargar la información y
almacenarla en una base de datos a tu elección