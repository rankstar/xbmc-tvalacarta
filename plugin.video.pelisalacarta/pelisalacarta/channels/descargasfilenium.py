# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal Descargas Filenium
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import json

from core import scrapertools
from core import downloadtools
from core import config
from core import logger
from core.item import Item

__channel__ = "descargasfilenium"
__category__ = "F,S"
__type__ = "generic"
__title__ = "Descargas Torrent en Filenium"
__language__ = "ES"

DEBUG = config.get_setting("debug")
TIMEOUT=30

def isGeneric():
    return True

def mainlist(item):
    logger.info("[descargasfilenium.py] mainlist")
    itemlist=[]

    itemlist.append( Item(channel=__channel__ , action="completados" , title="Torrents completados" , url="http://filenium.com/xbmc_json"))
    itemlist.append( Item(channel=__channel__ , action="pendientes"  , title="Torrents en curso"    , url="http://filenium.com/xbmc_json"))

    return itemlist

def completados(item):
    logger.info("[descargasfilenium.py] completados")

    url = item.url

    datas = scrapertools.cachePage(url, timeout=TIMEOUT)
    logger.info(datas)
    data = json.loads(datas)
    logger.info(str(data))

    repes = set()

    itemlist = []
    for match in data:
        if match['status'] == "COMPLETED" and match['filename'] not in repes:
            #logger.info(match['download_url'])
            title = downloadtools.limpia_nombre_excepto_1(match['filename'])
            itemlist.append( Item(channel=__channel__ , category="filenium torrent", action="play", server="filenium", title=title , url=match['download_url'] + "?.torrent" , thumbnail=match['screenshot'], plot="Filenium torrent" , folder=False))
            repes.add(match['filename'])

    return itemlist

def pendientes(item):
    logger.info("[descargasfilenium.py] pendientes")

    url = item.url
                
    datas = scrapertools.cachePage(url, timeout=TIMEOUT)
    logger.info(datas)
    data = json.loads(datas)
    logger.info(str(data))

    itemlist = []
    for match in data:
        if match['status'] != "COMPLETED":
            porcentaje = str(match['percent_done'])
            title = downloadtools.limpia_nombre_excepto_1(match['name'])
            try:
                tiempo = int(match['estimated_time'])
                if tiempo<60:
                    estimado = "%ds" % tiempo
                elif tiempo>60 and tiempo<60*60:
                    estimado = "%dm %ds" % ( tiempo / 60 , tiempo % 60)
                else:
                    horas = tiempo / (60*60)
                    tiempo = tiempo - (horas*60*60)
                    minutos = tiempo / 60
                    tiempo = tiempo - (minutos * 60)
                    segundos = tiempo
                    estimado = "%dh %dm %ds" % ( horas , minutos , segundos)
            except:
                estimado="???"
            #{"status":"DOWNLOADING","down_speed":5000,"peers_connected":12,"percent_done":0,"estimated_time":67475,"error_message":null,"size":337513018,"name":"Ladron De Guante Blanco - Temp1 [HDTV][Cap.107][Spanish]","id":2996823}
            itemlist.append( Item(channel=item.channel , action="pendientes"   , title="("+porcentaje+"%) (Estimado "+estimado+") "+title , url="http://filenium.com/xbmc_json" , thumbnail="", plot="Downloading to Filenium", folder=False )) 
    
    return itemlist
