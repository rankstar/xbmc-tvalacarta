# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para voxfilme
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "voxfilme"
__category__ = "F,S"
__type__ = "generic"
__title__ = "voxfilmeonline.com"
__language__ = "RO"
__creationdate__ = "20120703"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[voxfilme.py] mainlist")
    item.url="http://voxfilmeonline.com/";
    return novedades(item)

def novedades(item):
    logger.info("[voxfilme.py] novedades")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    
    patron  = '<div class="gallery.*?" id="post-\d+">[^<]+'
    patron += '<a href="([^"]+)".*?title="([^"]+)">+<img src="([^"]+)".*?'
        
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    
    '''
    <a href="http://unsoloclic.info/page/2/" >&laquo; Peliculas anteriores</a>
    '''
    patron  = '<div id="older"[^<]+<a href="([^"]+)" >Inaninte</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = "Inainte"
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,match)
        scrapedthumbnail = ""
        if (DEBUG): logger.info("url=["+scrapedurl+"], title=["+scrapedtitle+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="novedades", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def findvideos(item):
    logger.info("[voxfilme.py] findvideos")
    data = scrapertools.cache_page(item.url)
    itemlist=[]
    
    #<a href="http://67cfb0db.linkbucks.com"><img title="billionuploads" src="http://unsoloclic.info/wp-content/uploads/2012/11/billonuploads2.png" alt="" width="380" height="50" /></a></p>
    #<a href="http://1bd02d49.linkbucks.com"><img class="colorbox-57103"  title="Freakeshare" alt="" src="http://unsoloclic.info/wp-content/uploads/2013/01/freakshare.png" width="390" height="55" /></a></p>
    patron = '<iframe href="(http.//[a-z0-9]+.linkbucks.c[^"]+)[^>]+>"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for url,servertag,serverthumb in matches:
        itemlist.append( Item(channel=__channel__, action="play", server="linkbucks", title=servertag+" [linkbucks]" , url=url , thumbnail=serverthumb , plot=item.plot , folder=False) )

    from servers import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
        if videoitem.server!="linkbucks":
            videoitem.channel=__channel__
            videoitem.action="play"
            videoitem.folder=False
            videoitem.title = "["+videoitem.server+"]"

    return itemlist

def play(item):
    logger.info("[voxfilme.py] play")
    itemlist=[]

    if item.server=="linkbucks":
        logger.info("Es linkbucks")
        
        # Averigua el enlace
        from servers import linkbucks
        location = linkbucks.get_long_url(item.url)
        logger.info("location="+location)
        
        # Extrae la URL de saltar el anuncio en adf.ly
        if location.startswith("http://adf"):
            # Averigua el enlace
            from servers import adfly
            location = adfly.get_long_url(location)
            logger.info("location="+location)

        from servers import servertools
        itemlist=servertools.find_video_items(data=location)
        for videoitem in itemlist:
            videoitem.channel=__channel__
            videoitem.folder=False

    else:
        itemlist.append(item)

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
