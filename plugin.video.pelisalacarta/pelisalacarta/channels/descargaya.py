# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para descargaya
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "descargaya"
__category__ = "F,S"
__type__ = "generic"
__title__ = "descargaya"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[descargaya.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Series Online", action="subforos", url="http://www.descargaya.es/forumdisplay.php?f=242"))
    itemlist.append( Item(channel=__channel__, title="Películas Online", action="subforos", url="http://www.descargaya.es/forumdisplay.php?f=239"))
    
    return itemlist

def subforos(item):
    logger.info("[descargaya.py] subforos")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    patron  = '<div class="datacontainer">[^<]+'
    patron  = '<div class="titleline">[^<]+'
    patron  = '<h2 class="forumtitle"><a href="([^"]+)">([^<]+)</a></h2>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        url = urlparse.urljoin(item.url,scrapedurl)
        title = scrapedtitle
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+""+"]")
        itemlist.append( Item(channel=__channel__, action="subforos", title=title , url=url , folder=True) )

    itemlist.extend(hilos(item))

    return itemlist

def hilos(item):
    logger.info("[descargaya.py] hilos")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    patron  = '<div class="threadinfo".*?<a class="tit[^"]+" href="([^"]+)"[^>]+>([^>]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        url = urlparse.urljoin(item.url,scrapedurl)
        title = scrapedtitle
        title = unicode( title, "iso-8859-1" , errors="replace" ).encode("utf-8")
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+""+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , url=url , folder=True) )

    # Página siguiente
    patron = '<span class="prev_next"><a rel="next" href="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        itemlist.append( Item(channel=__channel__, action="hilos", title=">> Página siguiente" , url=urlparse.urljoin(item.url,matches[0].replace("&amp;","&")) , folder=True) )

    return itemlist

def findvideos(item):
    logger.info("[descargaya.py] findvideos")
    
    data = scrapertools.cache_page(item.url)
    itemlist = servertools.find_video_items(data=data)
    for videoitem in itemlist:
        videoitem.channel = __channel__
        videoitem.plot = item.plot
        videoitem.thumbnail = item.thumbnail
        videoitem.fulltitle = item.fulltitle
        
        parsed_url = urlparse.urlparse(videoitem.url)
        fichero = parsed_url.path
        partes = fichero.split("/")
        titulo = partes[ len(partes)-1 ]
        videoitem.title = titulo + " - [" + videoitem.server+"]"

    # Busca safelinking
    data = scrapertools.cachePage(item.url)
    patron  = 'https\://safelinking.net/d/[a-z0-9]+'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl in matches:
        url = scrapedurl
        title = "Enlace en safelinking"
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+""+"]")
        itemlist.append( Item(channel=__channel__, action="play", title=title , url=url , folder=True) )
        
    return itemlist

def play(item):

    if "safelinking" in item.url:
        from servers import safelinking
        new_url = safelinking.get_long_url(item.url)
        itemlist = servertools.find_video_items(data=new_url)
        item = itemlist[0]

    itemlist = [item]

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    
    # Si encuentra algún vídeo en la sección de series lo da por bueno
    subforo_series_items = subforos(mainlist_items[0])
    temporadas_completas_items = subforos(subforo_series_items[0])

    for serie_item in temporadas_completas_items:
        mirrors = findvideos( serie_item )
        if len(mirrors)>0:
            return True

    return False