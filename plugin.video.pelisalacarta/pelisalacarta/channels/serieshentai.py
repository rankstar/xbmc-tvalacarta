# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para serieshentai
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import cookielib
import urlparse,urllib2,urllib,re
import os
import sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "serieshentai"
__category__ = "F"
__type__ = "generic"
__title__ = "Series Hentai"
__language__ = "ES"
__adult__ = "true"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[serieshentai.py] mainlist")

    item.url="http://series-hentai.net/hentai-online"
    return series(item)

def series(item):
    logger.info("[serieshentai.py] series")

    itemlist = []

    data = scrapertools.cache_page(item.url)
    patron = '<td class="tijav"  ><a href="([^"]+)">([^<]+)</a></td>[^<]+<td> xxx </td>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle in matches:
        itemlist.append( Item( channel=item.channel, action="findvideos", title=scrapedtitle, url=scrapedurl, folder=True))

    return itemlist


# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():

    # Da por bueno el canal si alguno de las series devuelve mirrors
    from servers import servertools
    series_items = mainlist(Item())
    bien = False
    for serie_item in series_items:
        mirrors = servertools.find_video_items( item=serie_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien