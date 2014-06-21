# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para Terroygore
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse, urllib2,urllib,re
import sys
import xbmc
import xbmcgui
import xbmcplugin

from core import scrapertools
from core import config
from core import logger
from platformcode.xbmc import xbmctools
from core.item import Item
from servers import servertools

# Traza el inicio del canal
logger.info("[terrorygore.py] init")

__channel__ = "terrorygore"
__category__ = "F"
__type__ = "xbmc"
__title__ = "Terror y Gore"
__language__ = "ES,EN"

DEBUG = config.get_setting("debug")


def isGeneric():
    return True

def mainlist(item):
    logger.info("[terrorygore.py] mainlist")
    
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Películas de Terror"                     , action="movielist" , url="http://www.terrorygore.com/feeds/posts/default?start-index=1&max-results=50"))
    itemlist.append( Item(channel=__channel__, title="Película de Terror Asiáticas (VOSEng)"   , action="movielist" , url="http://asianmovielink.blogspot.com/feeds/posts/default/-/Horror?start-index=1&max-results=50"))
    return itemlist

def movielist(item):
    logger.info("[terrorygore.py] mainlist")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    
    start_index = "1"
    start_index_re = "start-index=(.*)&"
    url_params = item.url.split("?",1)
    url_limpia = url_params[0]
    matches = re.compile(start_index_re,re.DOTALL).findall(item.url)

    if len(matches)>0:
        start_index = matches[0]
        new_start = int(start_index) + 50

    #Para evitar problemas cuando el XML no esta completo o bien estructurado (que por desgracia pasa)
    entrada_blog_re = "<entry>(.*?)</entry>"

    # Expresion Regular para extraer la info
    patronvideos  = "<title.*?>(.*?)</title>.*?"
    patronvideos += "<summary type=['\"]text['\"]>(.*?)</summary>.*?"
    patronvideos += "<link rel=['\"]alternate['\"].*?href=['\"](.*?)['\"].*?"
    patronvideos += "<media:thumbnail.*?url=['\"](.*?)['\"]"
    
    matches = re.compile(entrada_blog_re,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    #Procesamos cada coincidencia 
    for match in matches:
        entrada_blog = match
        matches_entradas = re.compile(patronvideos,re.DOTALL).findall(entrada_blog)
        for match2 in matches_entradas:

            # Titulo
            scrapedtitle = match2[0]

            # URL
            scrapedurl = match2[2]
        
            # Thumbnail
        
            scrapedthumbnail = match2[3]
            
            #Queremos la caratula con una calida mejor. Este cambio devuelve una imagen de 200px en vez de 72px
            scrapedthumbnail = scrapedthumbnail.replace("s72-c","s200")
            # Argumento
            scrapedplot = match2[1]

            # Depuracion
            if (DEBUG):
                logger.info("scrapedtitle="+scrapedtitle)
                logger.info("scrapedurl="+scrapedurl)
                logger.info("scrapedthumbnail="+scrapedthumbnail)

            # Añade al listado de XBMC
            itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , fulltitle=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, extra = "" , context="4|5" ))
        
    if len(matches)>45:
        scrapedurl = url_limpia+"?start-index="+str(new_start)+"&max-results=50"
        itemlist.append( Item(channel=__channel__, title="Página Siguiente", action="movielist" , url=scrapedurl))
    
    return itemlist


