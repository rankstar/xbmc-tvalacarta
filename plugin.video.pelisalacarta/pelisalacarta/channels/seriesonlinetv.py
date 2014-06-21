# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para seriesonlinetv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys
import base64

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

__category__ = "A"
__type__ = "generic"
__title__ = "Series Online TV"
__channel__ = "seriesonlinetv"
__language__ = "ES"
__creationdate__ = "20121112"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[seriesonlinetv.py] mainlist")
    itemlist=[]
    itemlist.append( Item(channel=__channel__, action="series" , title="Series"          , url="http://www.seriesonlinetv.com/", extra="listaseries" ))
    itemlist.append( Item(channel=__channel__, action="series" , title="Series Españolas", url="http://www.seriesonlinetv.com/", extra="listaseries-espana" ))
    itemlist.append( Item(channel=__channel__, action="series" , title="Miniseries"      , url="http://www.seriesonlinetv.com/", extra="listaseries-miniseries" ))
    itemlist.append( Item(channel=__channel__, action="series" , title="Dibujos animados", url="http://www.seriesonlinetv.com/", extra="listaseries-dibujos" ))
    itemlist.append( Item(channel=__channel__, action="series" , title="Anime"           , url="http://www.seriesonlinetv.com/", extra="listaseries-anime" ))
    return itemlist

def series(item):
    logger.info("[seriesonlinetv.py] series")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<div id="'+item.extra+'"><dl class="list">(.*?)</dl>')
    patron = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="episodios" , title=title , url=url, thumbnail=thumbnail, plot=plot))        

    return itemlist

def episodios(item):
    logger.info("[seriesonlinetv.py] episodios")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    patron  = '<div class="fechaCapitulo">([^<]+)</div>[^<]+'
    patron += '<div class="idiomaCapitulo">(.*?)</div>[^<]+'
    patron += '<div class="nombreCapitulo">[^<]+'
    patron += '<b><a href ="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for fecha,numidioma,scrapedurl,scrapedtitle in matches:
        idioma = ""
        if "3.png" in numidioma:
            idioma=" (sub)"
        elif "1.png" in numidioma:
            idioma=" (español)"
        elif "2.png" in numidioma:
            idioma=" (latino)"

        title = scrapedtitle.strip()+idioma
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, fanart=thumbnail, plot=plot, viewmode="movie_with_plot"))

    if len(itemlist)==0:
        itemlist.append( Item(channel=__channel__, action="" , title="No hay episodios de esta serie en la web"))
    
    return itemlist

def findvideos(item):
    logger.info("[seriesonlinetv.py] findvideos(%s)" % item.tostring())
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    patron = '<table class="parrillaDescargas">(.*?)</table>'
    data = scrapertools.get_match(data,patron)
    
    '''
    <td class="numMirror"><img src="http://webs.ono.com/divx/img/filmes1.png" align="middle" alt="Ver online" title="Ver online" /> <a target="_blank" href="/video/40-putlocker/82381-007-Al-servicio-secreto-de-su-Majestad-1969.html"> <b>1</ b> <img src="http://webs.ono.com/divx/img/flecha.png" align="middle" /></a></td>
    <td class="hostParrilla"><a target="_blank" href="/video/40-putlocker/82381-007-Al-servicio-secreto-de-su-Majestad-1969.html"><img src="http://imagenes.divxonline.info/logos_servers/40.jpg" height="23" alt="Host" title="Host" /></a></td>
    <td class="idiomaParrilla"><a target="_blank" href="/video/40-putlocker/82381-007-Al-servicio-secreto-de-su-Majestad-1969.html"><img src="http://imagenes.divxonline.info/idiomas/1.png" alt="Audio" title="Audio" /></a></td>
    <td class="partesParrilla"><a target="_blank" href="/video/40-putlocker/82381-007-Al-servicio-secreto-de-su-Majestad-1969.html">1</a></td>
    <td class="uploaderParrilla"><a target="_blank" href="/video/40-putlocker/82381-007-Al-servicio-secreto-de-su-Majestad-1969.html">anonimo</a></td>
    '''
    patron  = '<td class="numMirror">.*?</td>[^<]+'
    patron += '<td class="hostParrilla"><a target="_blank" href="([^"]+)"><img src="([^"]+)"'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    for url,thumbnail in matches:
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedtitle = url
        try:
            scrapedtitle = scrapedtitle.split("/")[2]
        except:
            pass
        
        scrapedtitle = "Ver online "+scrapedtitle
        itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle , fulltitle=item.title , url=scrapedurl , thumbnail=thumbnail , plot=item.plot , folder=False) )

    # Descarga la página
    data = scrapertools.cachePage(item.url.replace("/serie/","/descarga-directa/"))
    patron = '<table class="parrillaDescargas">(.*?)</table>'
    data = scrapertools.get_match(data,patron)
    
    patron  = '<td class="numMirror">.*?</td>[^<]+'
    patron += '<td class="hostParrilla"><a target="_blank" href="([^"]+)"><img src="([^"]+)"'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    for url,thumbnail in matches:
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedtitle = url
        try:
            scrapedtitle = scrapedtitle.split("/")[2]
        except:
            pass
        
        scrapedtitle = "Descarga directa "+scrapedtitle
        itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle , fulltitle=item.title , url=scrapedurl , thumbnail=thumbnail , plot=item.plot , folder=False) )

    return itemlist

def play(item):
    logger.info("[seriesonlinetv.py] play")
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    logger.info("data1="+data)
    data = scrapertools.get_match(data,"(<script type=\"text/javascript\">decodeBase64\('[^']+'\))")
    logger.info("data2="+data)

    import divxonline
    data = divxonline.decryptinks(data)
    logger.info("data3="+data)

    itemlist = servertools.find_video_items(data=data)
    i=1
    for videoitem in itemlist:
        videoitem.title = videoitem.title
        videoitem.fulltitle = item.fulltitle
        videoitem.channel=channel=__channel__
        i=i+1

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # mainlist
    mainlist_items = mainlist(Item())
    
    # Comprueba que todas las opciones tengan algo (excepto el buscador)
    for mainlist_item in mainlist_items:

        if mainlist_item.action!="search":
            exec "itemlist = "+mainlist_item.action+"(mainlist_item)"
            if len(itemlist)==0:
                print "La sección '"+mainlist_item.title+"' no tiene series"
                return False

    # Busca episodios en alguna de las 10 primeras series
    series_itemlist = series(mainlist_items[0])

    for i in range(0,10):
        episodios_itemlist = episodios(series_itemlist[0])
        if len(episodios_itemlist)>0:
            return True

    return False
