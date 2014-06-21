# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para piratestreaming
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "instreaming"
__category__ = "F"
__type__ = "generic"
__title__ = "instreaming"
__language__ = "IT"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[instreaming.py] mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novità"     , action="peliculas", url="http://www.instreaming.tv/"))
    itemlist.append( Item(channel=__channel__, title="Prime visioni"     , action="peliculas", url="http://www.instreaming.tv/category/film/prime-visioni"))
    itemlist.append( Item(channel=__channel__, title="Dvd RIP" , action="peliculas", url="http://www.instreaming.tv/category/film/alta-qualita"))
    itemlist.append( Item(channel=__channel__, title="Serie Tv" , action="peliculas", url="http://www.instreaming.tv/category/serie-tv"))
    itemlist.append( Item(channel=__channel__, title="Cerca", action="search"))
    return itemlist
    
def search(item,texto):
    logger.info("[instreaming.py] search "+texto)
    itemlist = []
    texto = texto.replace(" ","%20")
    item.url = "http://www.instreaming.tv/search/"+texto
    item.extra = ""

    try:
        return peliculas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def categorias(item):
    '''
    <select name="linkIole2" size="1" onchange="location.href=this.value">
    <option value="#">Categorie Film</option>
	<option value="http://instreaming.tv/category/animazione/">Animazione</option>
	<option value="http://instreaming.tv/category/avventura/">Avventura</option>
	<option value="http://instreaming.tv/category/azione/">Azione</option>
	<option value="http://instreaming.tv/category/biografico/">Biografico</option>
	<option value="http://instreaming.tv/category/comico/">Comico</option>
	</select>
	<td><tr>
	</td></tr>
	<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<tr>
	<select name="linkIole2" size="1" onchange="location.href=this.value">
	<option value="#">Serie Tv</option>
	<option value="http://instreaming.tv/category/serie-tv/0-9/">0-9</option>
	<option value="http://instreaming.tv/category/serie-tv/a-f/">A-F</option>
	<option value="http://instreaming.tv/category/serie-tv/g-l/">G-L</option>
	<option value="http://instreaming.tv/category/serie-tv/m-r/">M-R</option>
	<option value="http://instreaming.tv/category/serie-tv/s-z/">S-Z</option>
	</select></td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<td><select name="linkIole2" size="1" onchange="location.href=this.value">
	<option value="#">Anime Cartoon</option>
	<option value="http://instreaming.tv/category/anime-cartoon-italiani/">Anime Cartoon ITA</option>
	<option value="http://instreaming.tv/category/anime-cartoon-sub-ita/">Anime Cartoon Sub-ITA</option>
	</select>
    '''
    url=item.url.split("|")[0]
    cat=item.url.split("|")[1]
    itemlist = []
    data = scrapertools.cache_page(url)
    if cat=="film":
    	data = scrapertools.get_match(data,'<option value="#">Categorie Film</option>(.*?)</select>' )
    else:
    	if cat=="serie":
    		data = scrapertools.get_match(data,'<option value="#">Serie Tv</option>(.*?)</select>' )
    	else:
    		data = scrapertools.get_match(data,'<option value="#">Anime Cartoon</option>(.*?)</select>' )
    patron  = '<option value="([^"]+)">([^<]+)</option>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def peliculas(item):
    logger.info("[instreaming.py] peliculas url:" + item.url)
    itemlist = []

    # Descarga la p�gina
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas (carpetas)
    '''
    <a href="http://www.instreaming.tv/film/silent-hill-revelation.html">
	<img src="http://img.instreaming.tv/images/n/701a50f46ef30c29fdb6be2947926679669a38a6.jpg" alt="Silent Hill: Revelation" width="70" height="99">
	</a>
    '''
    patron  = '<a[^>]*href="(http://www.instreaming.tv/film/[^>"]+)">\s*'
    patron += '<img src="([^>"]+)" alt="([^>"]+)"'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        scrapedplot = ""
        scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle.replace("Streaming",""))
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    '''
    <a rel="bookmark" href="/film/ballata-dellodio-e-dellamore.html">
	<img src="http://img.instreaming.tv/images/n/701a50f46ef30c29fdb6be2947926679669a38a6.jpg" alt="Silent Hill: Revelation" width="70" height="99">
	</a>
    '''
    patron  = '<a rel="bookmark" href="(/film/[^>"]+)">\s*'
    patron += '<img src="([^>"]+)" alt="([^>"]+)"'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        scrapedurl="http://www.instreaming.tv" + scrapedurl
        scrapedplot = ""
        scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle.replace("Streaming",""))
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
	'''
	<a href="http://www.instreaming.tv/serie-tv/15love-film-in-streaming-megavideo-megaupload-film-gratis-in-italiano-warez-ita-rapidshare-serie-tv.html" target="_blank">15/love</a>
	'''
    patron  = '<a href="(http://www.instreaming.tv/serie-tv/[^>"]+)"[^>]*>([^>"]+)</a>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
    
        scrapedthumbnail=""
        scrapedplot = ""
        scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle.replace("Streaming",""))
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )


    # Extrae el paginador
    #<a href="http://www.instreaming.tv/category/film/alta-qualita/page/2">&nbsp;Successiva»&nbsp;</a>
    patronvideos  = '<a href="([^"]+)"\s*>&nbsp;Successiva&raquo;&nbsp;</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="Next Page >>" , url=scrapedurl , folder=True) )

    return itemlist

# Verificaci�n autom�tica de canales: Esta funci�n debe devolver "True" si est� ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los v�deos de "Novedades" devuelve mirrors
    novedades_items = peliculas(mainlist_items[0])
    bien = False
    for novedades_item in novedades_items:
        mirrors = servertools.find_video_items( item=novedades_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien