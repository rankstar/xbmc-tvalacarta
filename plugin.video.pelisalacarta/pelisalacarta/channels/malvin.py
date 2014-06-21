# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para malvin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "malvin"
__category__ = "F,D"
__type__ = "generic"
__title__ = "Malvin.tv"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[malvin.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Portada"   , action="portada", url="http://www.malvin.biz/"))
    itemlist.append( Item(channel=__channel__, title="Películas" , action="lista",     url="http://www.malvin.biz/search"))
    #itemlist.append( Item(channel=__channel__, title="Series"    , action="lista",     url="http://www.malvin.biz/search/label/Serie%20Completa"))
    itemlist.append( Item(channel=__channel__, title="Anime"     , action="lista",     url="http://www.malvin.biz/search/label/Anime%20Completo"))
    itemlist.append( Item(channel=__channel__, title="Estrenos"  , action="lista",     url="http://www.malvin.biz/search/label/Estrenos"))
    itemlist.append( Item(channel=__channel__, title="Generos"   , action="generos",   url="http://www.malvin.biz/"))

    return itemlist

def portada(item):
    logger.info("[malvin.py] portada")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas (carpetas)
    patronvideos  = '<div id="item-estrenos"><a class="tolon" title="([^"]+)" href="([^"]+)"><div class="play"></div><img alt="[^"]+" src="([^"]+)"'    
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapedtitle = ""
    scrapedurl = ""
    scrapedthumbnail = ""
    
    for scrapedtitle,scrapedurl, scrapedthumbnail in matches:
        title = scrapedtitle
        thumbnail = scrapedthumbnail
        url = scrapedurl
        plot = ""

        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=True) )

    return itemlist

def lista(item):
    logger.info("[malvin.py] lista")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas (carpetas)
    patronvideos  = 'document.write\(thumbnails\("([^"]+)","([^"]+)","([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        title = scrapedtitle
        thumbnail = scrapedthumbnail
        url = scrapedurl
        plot = ""
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=True) )

    return itemlist

def generos(item):
    logger.info("[malvin.py] generos")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match( data , "<div id='article'[^<]+<div class='menu'[^<]+<ul>(.*?)</ul>")

    # Extrae las entradas (carpetas)
    patronvideos  = "<li><a href='([^']+)'>([^<]+)</a></li>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:        
        title = scrapedtitle
        thumbnail = ""
        url = urlparse.urljoin(item.url,scrapedurl)
        plot = ""
        itemlist.append( Item(channel=__channel__, action="lista", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=True) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    # mainlist
    mainlist_items = mainlist(Item())
    portada_items = portada(mainlist_items[0])
    if len(portada_items)==0:
        print "No hay elementos en la portada"
        return False

    lista_items = lista(mainlist_items[1])
    if len(lista_items)==0:
        print "No hay elementos en la sección de películas"
        return False

    for portada_item in portada_items:
        from servers import servertools
        mirrors = servertools.find_video_items(item=portada_item)
        if len(mirrors)>0:
            bien = True
            break

    return bien
