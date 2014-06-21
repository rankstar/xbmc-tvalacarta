# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para watchcartoononline
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
__title__ = "Watch Cartoon Online"
__channel__ = "watchcartoononline"
__language__ = "ES"
__creationdate__ = "20121123"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[watchcartoononline.py] mainlist")
    itemlist = []

    itemlist.append( Item(channel=__channel__, action="letras" , title="Dubbed Anime"  , url="http://www.watchcartoononline.com/dubbed-anime-list"))
    itemlist.append( Item(channel=__channel__, action="letras" , title="Cartoons"      , url="http://www.watchcartoononline.com/cartoon-list"))
    itemlist.append( Item(channel=__channel__, action="letras" , title="Subbed Anime"  , url="http://www.watchcartoononline.com/subbed-anime-list"))
    itemlist.append( Item(channel=__channel__, action="letras" , title="Movies"        , url="http://www.watchcartoononline.com/movie-list"))
    itemlist.append( Item(channel=__channel__, action="letras" , title="OVA Series"    , url="http://www.watchcartoononline.com/ova-list"))

    return itemlist

def letras(item):
    logger.info("[watchcartoononline.py] letras")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<div class="letter">(.*?)</div>')
    
    patron = '<li><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="series" , title=title , url=url, thumbnail=thumbnail, plot=plot, fanart="http://pelisalacarta.mimediacenter.info/fanart/watchcartoononline.jpg"))        

    return itemlist

def series(item):
    logger.info("[watchcartoononline.py] series")
    itemlist = []
    
    letra = scrapertools.get_match(item.url,"\#(.)$")
    item.url = item.url[:-2]
    logger.info("letra="+letra)
    
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<a name="'+letra+'"></a><p[^<]+</p><ul>(.*?)</ul>')
    
    patron = '<li><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="episodios" , title=title , url=url, thumbnail=thumbnail, plot=plot, fanart="http://pelisalacarta.mimediacenter.info/fanart/watchcartoononline.jpg"))        

    return itemlist

def detalle_programa(item,data=""):
    logger.info("[watchcartoononline.py] detalle_programa")

    # Descarga la página
    url = item.url
    if data=="":
        data = scrapertools.cache_page(url)

    # Obtiene el thumbnail
    try:
        item.thumbnail = scrapertools.get_match(data,'<div class="katcont"[^<]+<div[^<]+<img src="([^"]+)"[^<]+</div>[^<]+<div class="hm">.*?</div>')
    except:
        pass

    try:
        item.plot = scrapertools.get_match(data,'<div class="katcont"[^<]+<div[^<]+<img src="[^"]+"[^<]+</div>[^<]+<div class="hm">(.*?)</div>')
        item.plot = scrapertools.htmlclean(item.plot).strip()
    except:
        pass

    return item

def episodios(item):
    logger.info("[watchcartoononline.py] episodios")

    # Descarga la pagina
    item = detalle_programa(item)
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<table[^<]+<tr[^<]+<td[^<]+<h3>Episode List</h3></td[^<]+</tr[^<]+<tr[^<]+<td[^<]+<div class="menu"[^<]+<div class="menustyle">(.*?)</ul>')
    
    patron  = '<li><a href="([^"]+)"[^>]+>([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = item.thumbnail
        plot = item.plot
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot, viewmode="movie_with_plot", fanart="http://pelisalacarta.mimediacenter.info/fanart/watchcartoononline.jpg"))

    try:
        siguiente = scrapertools.get_match(data,'<a href="([^"]+)" >\&laquo\; Previous Entries</a></div>')
        scrapedurl = urlparse.urljoin(item.url,siguiente)
        scrapedtitle = ">> Pagina Siguiente"
        scrapedthumbnail = ""
        scrapedplot = ""

        itemlist.append( Item(channel=__channel__, action="episodios", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True, fanart="http://pelisalacarta.mimediacenter.info/fanart/watchcartoononline.jpg") )
    except:
        pass
    return itemlist

def findvideos(item):
    logger.info("[watchcartoononline.py] findvideos")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,"<span class='postTabs_titles(.*?)$")
    scrapedurl = scrapertools.get_match(data,'<iframe src="([^"]+)"')
    
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="play", title=item.title, url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot, folder=False, viewmode="tvshow"))
    return itemlist

def play(item):
    logger.info("[watchcartoononline.py] play")

    # Descarga la pagina
    #http://www.cizgifilmlerizle.com/embed.php?file=httpdocs/yuke/Slugterra.S01E01.WS.XviD-err0001.flv
    #POST fuck_you=&confirm=Click+Here+to+Watch+Free%21%21
    data = scrapertools.cache_page(item.url , post="fuck_you=&confirm=Click+Here+to+Watch+Free%21%21")
    url  = scrapertools.get_match(data,'\;file=([^\&]+)&')
    url  = urllib.unquote(url)
    logger.info("url="+url)
    
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="play", title=item.title, url=url, server="directo", thumbnail=item.thumbnail, plot=item.plot, folder=False, viewmode="tvshow"))
    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # Busca algún episodio con vídeos en la primera opción de series (dubbed anime), letra "A"
    mainlist_items = mainlist(Item())
    letter_items = letras(mainlist_items[0])
    series_items = series(letter_items[1])

    # Comprueba que todas las opciones tengan algo (excepto el buscador)
    for serie_item in series_items:
        episodios_items = episodios(serie_item)

        for episodio_item in episodios_items:
            mirrors = findvideos(item=episodio_item)
            if len(mirrors)>0:
                return True

    return False