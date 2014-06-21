# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cinemax_rs
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "cinemax_rs"
__category__ = "F,S"
__type__ = "generic"
__title__ = "Filme-noi.com"
__language__ = "ES"
__creationdate__ = "20131223"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.cinemax_rs mainlist")
    item.url="http://cinemaxx.ro/newvideos.html";
    return novedades(item)

def novedades(item):
    logger.info("pelisalacarta.channels.cinemax_rs novedades")
    itemlist = []
	
    # Download page
    data = scrapertools.cachePage(item.url)

    patron  = '<li.*?'
    patron += '<a href="([^"]+)" class="pm-thumb-fix.*?'
    patron += '<img src="([^"]+)" alt="([^"]+)".*?'
    patron += '<p class="pm-video-attr-desc">(.*?)</p>'
	
    # Extract elements
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
	
    for scrapedurl,scrapedthumbnail,scrapedtitle,scrapedplot in matches:
        if (DEBUG): logger.info("url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"], title=["+scrapedtitle+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , viewmode="movie_with_plot", folder=True) )

    # Next page    
    patron  = '<li[^<]+<a href="([^"]+)">\&raquo\;</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
	
    for match in matches:
       scrapedtitle = ">> Página siguiente"
       scrapedplot = ""
       scrapedurl = urlparse.urljoin(item.url,match)
       scrapedthumbnail = ""
       if (DEBUG): logger.info("url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"], title=["+scrapedtitle+"]")
       itemlist.append( Item(channel=__channel__, action="novedades", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.channels.cinemax_rs findvideos")

    data = scrapertools.cache_page(item.url)
    #logger.info("data="+data)
    itemlist=[]
    
    #<a href="#index_panel_detailed" onClick='$("#Playerholder").load("http://www.cinemaxx.ro/ajax.php?p=custom&do=requestmirror&vid=3a20f4b86&mirror=1"
    patron = '<a href=".index_panel_detailed" onClick=\'\$\("\#Playerholder"\)\.load\("([^"]+)"[^<]+<img src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    i=1
    for url,serverthumb in matches:
        itemlist.append( Item(channel=__channel__, action="play", title="Option "+str(i) , url=url , thumbnail=serverthumb , plot=item.plot , folder=False) )
        i=i+1

    return itemlist

def play(item):
    logger.info("pelisalacarta.channels.cinemax_rs play")

    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    itemlist=[]

    from servers import servertools
    itemlist=servertools.find_video_items(data=data)
    for videoitem in itemlist:
        videoitem.channel=__channel__
        videoitem.folder=False

    return itemlist
 
# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    # mainlist
    novedades_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    bien = False
    for singleitem in novedades_items:
        mirrors_items = findvideos( item=singleitem )
        for mirror_item in mirrors_items:
            video_items = play(mirror_item)
            if len(video_items)>0:
                return True

    return False
