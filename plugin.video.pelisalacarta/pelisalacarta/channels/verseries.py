# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os,sys,string

from core import scrapertools
from core import config
from core import logger
from core.item import Item

__channel__ = "verseries"
__category__ = "S"
__type__ = "generic"
__title__ = "Ver-Series"
__language__ = "ES"
__creationdate__ = "20111215"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[verseries.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Series - A-Z", action="letras"))
    return itemlist

def letras(item):
    logger.info("[verseries.py] letras")
    itemlist = []

    alfabeto = "abcdefghijklmnopqrstuvwxyz"
    for letra in alfabeto:
        itemlist.append( Item(channel=item.channel, action="series", title=str(letra).upper(), url = "http://www.ver-series.net/letras/"+letra+".html"))

    itemlist.append( Item(channel=item.channel, action="series", title="#", url = "http://www.ver-series.net/letras/09.html"))

    return itemlist

def series(item):
    logger.info("[verseries.py] series")

    itemlist=[]

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    '''
    <div class="bl">
    <a href="../aaron-stone-serie.html" title="Aaron Stone">
    <img src="http://www.vimagen.net/vs/im/aaron-stone.jpg" alt="Aaron Stone" width="166" height="250" border="0" class="im" />
    </a>
    '''
    patron  = '<div class="bl">[^<]+'
    patron += '<a href="([^"]+)" title="([^"]+)"[^<]+'
    patron += '<img src="([^"]+)"'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        scrapedurl = urlparse.urljoin(item.url,scrapedurl)
        scrapedtitle = unicode(scrapedtitle,"iso-8859-1").encode("utf-8").strip()
        scrapedplot = ""
        itemlist.append( Item(channel=item.channel, action="episodios", title=scrapedtitle , fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, category="series" , plot=scrapedplot, show=scrapedtitle) )

    return itemlist

def episodios(item):
    logger.info("[verseries.py] episodios")

    itemlist=[]

    # Carga las temporadas
    temporadas_itemlist=temporadas(item)
    for temporada in temporadas_itemlist:
        
        # Descarga la página de cada temporada
        data = scrapertools.cache_page(temporada.url)
        patron  = '<li class="lcc">[^<]+<a href="([^"]+)" title="([^"]+)"[^<]+</a>[^<]+</li>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)
        
        for scrapedurl,scrapedtitle in matches:
            scrapedurl = urlparse.urljoin(item.url,scrapedurl)
            scrapedtitle = unicode(scrapedtitle,"iso-8859-1").encode("utf-8").strip()
            itemlist.append( Item(channel=item.channel, action="findvideos", title=scrapedtitle , fulltitle=item.title , url=scrapedurl , thumbnail=item.thumbnail, category="series" , plot=item.plot, show=item.show) )

    if config.get_platform().startswith("xbmc"):
        itemlist.append( Item(channel=item.channel, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show) )

    return itemlist

def temporadas(item):
    logger.info("[verseries.py] temporadas")
    
    itemlist=[]

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    '''
    <li class="lcc">
    <a href="/aaron-stone/primera-temporada/" title="Aaron Stone Primera Temporada" class="lcc">Aaron Stone Primera Temporada</a>
    </li>
    '''
    patron  = '<li class="lcc">[^<]+<a href="([^"]+)" title="([^"]+)"[^<]+</a>[^<]+</li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for scrapedurl,scrapedtitle in matches:
        scrapedurl = urlparse.urljoin(item.url,scrapedurl)
        scrapedtitle = unicode(scrapedtitle,"iso-8859-1").encode("utf-8").strip()
        itemlist.append( Item(channel=item.channel, action="episodios", title=scrapedtitle , fulltitle=item.fulltitle , url=scrapedurl , thumbnail=item.thumbnail, category="series" , plot=item.plot, show=item.show) )

    return itemlist

def findvideos(item):
    logger.info("[verseries.py] findvideos")
    
    itemlist=[]

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    
    # Enlaces online
    patron  = '<li class="lcc">[^<]+<a target="repro" rel="nofollow" href="([^"]+)"[^>]+>(.*?)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for scrapedurl,scrapedtitle in matches:
        scrapedurl = urlparse.urljoin(item.url,scrapedurl)
        scrapedtitle = unicode(scrapedtitle,"iso-8859-1").encode("utf-8").strip()
        scrapedtitle = scrapertools.htmlclean(scrapedtitle)
        itemlist.append( Item(channel=item.channel, action="play", title="Online "+scrapedtitle , fulltitle=item.fulltitle , url=scrapedurl , thumbnail=item.thumbnail, category="series" , plot=item.plot, show=item.show) )
    
    # Enlaces MU
    patron  = '<li class="lcc">[^<]+<a rel="nofollow" target="blank" href="([^"]+)" class="lcc">(.*?)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for scrapedurl,scrapedtitle in matches:
        scrapedurl = urlparse.urljoin(item.url,scrapedurl)
        scrapedtitle = unicode(scrapedtitle,"iso-8859-1").encode("utf-8").strip()
        scrapedtitle = scrapertools.htmlclean(scrapedtitle)
        itemlist.append( Item(channel=item.channel, action="play", title="Descarga "+scrapedtitle , fulltitle=item.fulltitle , url=scrapedurl , thumbnail=item.thumbnail, category="series" , plot=item.plot, show=item.show) )

    return itemlist

def play(item):
    logger.info("[verseries.py] play")
    
    from servers import servertools
    itemlist = servertools.find_video_items(item)

    return itemlist

