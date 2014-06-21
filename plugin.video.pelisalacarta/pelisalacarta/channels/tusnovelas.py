# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para tusnovelas.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "tusnovelas"
__category__ = "S"
__type__ = "generic"
__title__ = "Tus novelas"
__language__ = "ES"
__creationdate__ = "20120703"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[tusnovelas.py] mainlist")
    
    itemlist = []

    itemlist.append( Item(channel=__channel__, action="novedades"           , title="Últimas telenovelas"           , url="http://www.tusnovelas.com/"))
    itemlist.append( Item(channel=__channel__, action="novedades_episodios" , title="Últimos episodios"             , url="http://www.tusnovelas.com/"))
    itemlist.append( Item(channel=__channel__, action="todas"               , title="Lista completa de telenovelas" , url="http://www.tusnovelas.com/"))

    return itemlist

def novedades_episodios(item):
    logger.info("[tusnovelas.py] novedades_episodios")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    '''
    <div class="dia">
    <img src="http://img.tusnovelas.com/por-ella-soy-eva.jpg" width="70px" height="105px" align="right"/>
    <div class="dia-titulo"><a href="http://www.tusnovelas.com/capitulo/por-ella-soy-eva-95.html" class="tts">Por ella soy eva 95</a></div>
    <div class="dia-lista"><a href="por-ella-soy-eva.html">Lista de capítulos</a></div>
    30/06/2012<br /><br />
    '''
    patron  = '<div class="dia">[^<]+'
    patron += '<img src="([^"]+)"[^<]+'
    patron += '<div class="dia-titulo"><a href="([^"]+)"[^>]+>([^<]+)</a></div>'    
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedthumbnail,url,scrapedtitle in matches:
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,url)
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    
    return itemlist

def novedades(item):
    logger.info("[tusnovelas.py] novedades")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    '''
    <div class="imagelist">
    <div align="center">
    <div class="gallery">
    <div class="picture">
    <a href="primera-dama-chile.html" title="Primera dama Chile" >
    <img src="http://img.tusnovelas.com/primera-dama-chile.jpg" width="160px" height="240px" alt="Primera dama Chile" /></a>
    </div>
    <div class="ttt">
    <a href="primera-dama-chile.html" rel="bookmark" title="Primera dama Chile">Primera dama Chile</a>
    </div>
    <div class="clear">
    </div>
    </div>
    </div>
    </div>
    </div><div>
    '''
    patron  = '<div class="imagelist">[^<]+'
    patron += '<div align="center">[^<]+'
    patron += '<div class="gallery">[^<]+'
    patron += '<div class="picture">[^<]+'
    patron += '<a href="([^"]+)" title="([^"]+)"[^<]+'
    patron += '<img src="([^"]+)"'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for url,scrapedtitle,scrapedthumbnail in matches:
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,url)
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="episodios", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    
    '''
    <li ><a href="ultimas/p/14" title="&Uacute;ltima">&raquo;&raquo;</a></li>
    '''
    patron  = '<a href="([^"]+)" title="\&Uacute\;ltima">\&raquo\;\&raquo\;</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = ">> Página siguiente"
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,match)
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="novedades", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def episodios(item):
    logger.info("[tusnovelas.py] episodios")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    patron  = '<li class="lc"><a href="([^"]+)" class="lcc">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for url,scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedurl = urlparse.urljoin(item.url,url)

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    
    return itemlist

def findvideos(item):
    logger.info("[tusnovelas.py] findvideos")
    data = scrapertools.cache_page(item.url)
    itemlist=[]

    patron = '<embed type="application/x-shockwave-flash" src="http://www.todoanimes.com/reproductor/player.swf".*?file=([^\&]+)&'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        itemlist.append( Item(channel=__channel__, action="play", server="directo", title=item.title , url=match , thumbnail=item.thumbnail , plot=item.plot , folder=False) )

    #<embed width="680" height="450" flashvars="file=mp4:p/459791/sp/45979100/serveFlavor/flavorId/0_0pacv7kr/forceproxy/true&amp;image=&amp;skin=&amp;abouttext=&amp;dock=false&amp;streamer=rtmp://rtmpakmi.kaltura.com/ondemand/&amp;
    patron = '<embed width="[^"]+" height="[^"]+" flashvars="file=([^\&]+)&.*?streamer=(rtmp[^\&]+)&'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for final,principio in matches:
        itemlist.append( Item(channel=__channel__, action="play", server="directo", title=item.title , url=principio+final , thumbnail=item.thumbnail , plot=item.plot , folder=False) )


    from servers import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
        videoitem.channel=__channel__
        videoitem.action="play"
        videoitem.folder=False
        videoitem.title = "["+videoitem.server+"]"

    return itemlist

def todas(item):
    logger.info("[tusnovelas.py] todas")
    itemlist=[]

    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<div id="noti-titulo">Lista de Telenovelas</div>[^<]+<div class="dm">(.*?)</div>')
    
    patron = '<li><a href="([^"]+)"[^>]+>([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for url,title in matches:
        scrapedurl = urlparse.urljoin(item.url,url)
        itemlist.append( Item(channel=__channel__, action="episodios", title=title , url=scrapedurl , folder=True) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():

    # mainlist
    mainlist_items = mainlist(Item())
    novedades_items = novedades_episodios(mainlist_items[1])
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    bien = False
    for singleitem in novedades_items:
        mirrors = findvideos( item=singleitem )
        if len(mirrors)>0:
            bien = True
            break

    return bien