# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculashdpro
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

__category__ = "A"
__type__ = "generic"
__title__ = "peliculashd.pro"
__channel__ = "peliculashdpro"
__language__ = "ES"
__creationdate__ = "20121112"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[peliculashdpro.py] mainlist")
    itemlist=[]
    itemlist.append( Item(channel=__channel__, action="listado", title="Novedades"  , url="http://www.peliculashd.pro/" ))
    itemlist.append( Item(channel=__channel__, action="generos", title="Por géneros", url="http://www.peliculashd.pro/" ))
    itemlist.append( Item(channel=__channel__, action="listado", title="HD"         , url="http://www.peliculashd.pro/hd/" ))
    itemlist.append( Item(channel=__channel__, action="listado", title="Latino"     , url="http://www.peliculashd.pro/latino/" ))
    return itemlist

def generos(item):
    logger.info("[peliculashdpro.py] generos")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<ul class="genres">(.*?)</ul>')
    
    patron = '<li><a title="[^"]+" href="([^"]+)"><span>([^<]+)</span>'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="listado" , title=title , url=url, thumbnail=thumbnail, plot=plot))        

    return itemlist

def listado(item):
    logger.info("[peliculashdpro.py] listado")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    '''
    <div class="leftpane">
    <div class="movieposter" title="Watch Movie Sin retorno (2010)">
    <a href="http://www.peliculashd.pro/drama/13935-sin-retorno-2010.html"><img src="http://img.newdivx.net/pictures/Sin_retorno-891476241-large.jpg" width="110" height="150" alt="Watch Movie Sin retorno (2010)" title="Watch Movie Sin retorno (2010)" /></a>    
    <div class="shortname">Sin retorno (2010)</div>
    </div>
    </div>
    <div class="rightpane">
    <div style="display:block;overflow:hidden;">
    <h2 class="title" title="Sin retorno (2010)"><a href="http://www.peliculashd.pro/drama/13935-sin-retorno-2010.html">Sin retorno (2010)</a></h2>    
    <div style="height:105px; overflow:hidden;">
    <div class="small">
    <div id="news-id-13935" style="display:inline;">Un joven ciclista muere atropellado por un automóvil. El culpable huye sin dejar rastro. Pero el padre de la víctima, con el apoyo der los medios de comunicación, exige que se encuentre al responsable y se haga justicia. Una serie de hechos fortuitos y unos magistrados contaminados por la opinión pública harán que un hombre inocente se siente en el banquillo de los acusados.</div>
    </div>
    </div>
    <div class="clear" style="height:2px;"></div>
    '''
    patron = '<div class="leftpane">[^<]+'
    patron += '<div class="movieposter"[^<]+'
    patron += '<a href="([^"]+)"><img src="([^"]+)"[^<]+</a>[^<]+'
    patron += '<div class="shortname">([^<]+)</div>.*?<div class="small">[^<]+'
    patron += '<div[^>]+>(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl,scrapedthumbnail,scrapedtitle,scrapedplot in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = scrapedthumbnail
        plot = scrapertools.htmlclean(scrapedplot)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, fanart=thumbnail, plot=plot, viewmode="movie_with_plot"))

    try:
        siguiente = scrapertools.get_match(data,'<a href="([^"]+)">Next \&\#8594\;</a>')
        scrapedurl = urlparse.urljoin(item.url,siguiente)
        scrapedtitle = ">> Pagina Siguiente"
        scrapedthumbnail = ""
        scrapedplot = ""

        itemlist.append( Item(channel=__channel__, action="listado", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    except:
        pass
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
                mirrors = findvideos(item=itemlist[0])
                if len(mirrors)>0:
                    return True

    return False