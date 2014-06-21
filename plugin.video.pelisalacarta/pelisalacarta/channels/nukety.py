# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para nukety
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "nukety"
__category__ = "F"
__type__ = "generic"
__title__ = "nukety"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[nukety.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__ , action="lista"    , title="Series TV"      , url="http://nukety.wordpress.com/category/series-tv/" ))
    itemlist.append( Item(channel=__channel__ , action="lista"    , title="OnAir | SD"     , url="http://nukety.wordpress.com/category/series-tv/en-curso-sd/" ))
    itemlist.append( Item(channel=__channel__ , action="lista"    , title="Completas | SD" , url="http://nukety.wordpress.com/category/series-tv/completas-sd/" ))
    itemlist.append( Item(channel=__channel__ , action="lista"    , title="OnAir | HD"     , url="http://nukety.wordpress.com/category/series-tv/en-curso-hd/" ))
    itemlist.append( Item(channel=__channel__ , action="lista"    , title="Completas | HD" , url="http://nukety.wordpress.com/category/series-tv/completas-hd/" ))
    itemlist.append( Item(channel=__channel__ , action="lista"    , title="Cine 480p"      , url="http://nukety.wordpress.com/cine-480p/" ))

    return itemlist

def lista(item):
    logger.info("[nukety.py] lista")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas (carpetas)
    patron  = '<div class="entry-content"[^<]+'
    patron += '<p><strong>([^<]+)</strong></p>[^<]+'
    patron += '<p><img class="[^"]+" src="([^"]+)" alt="[^"]+" /></p>[^<]+'
    patron += '<p[^<]+<a href="([^\#]+)'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedtitle,scrapedthumbnail,scrapedurl in matches:
        title=scrapedtitle.strip()
        url=urlparse.urljoin(item.url,scrapedurl)
        thumbnail=urlparse.urljoin(item.url,scrapedthumbnail)
        plot=""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , url=url , thumbnail=thumbnail , plot=plot , viewmode="movies_with_plot", folder=True) )

    try:
        current_page = scrapertools.get_match(item.url,"page/(\d+)")
        next_page = str( int(current_page)+1 )
        next_page_url = item.url.replace("page/"+current_page,"page/"+next_page)
    except:
        current_page = "1"
        next_page = "2"
        next_page_url = urlparse.urljoin(item.url,"page/2")
    
    itemlist.append( Item(channel=__channel__, action="lista", title=">> Página siguiente" , url=next_page_url , folder=True) )

    return itemlist

def findvideos(item):
    logger.info("[nukety.py] findvideos")

    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    itemlist=[]
    
    from servers import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
        videoitem.channel=__channel__
        videoitem.action="play"
        videoitem.folder=False
        videoitem.title = "["+videoitem.server+"]"

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    return False
