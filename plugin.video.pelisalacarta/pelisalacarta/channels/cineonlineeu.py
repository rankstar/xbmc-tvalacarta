# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cineonlineeu
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "cineonlineeu"
__category__ = "F"
__type__ = "generic"
__title__ = "cineonlineeu"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[cineonlineeu.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__ , action="peliculas" , title="Novedades"      , url="http://www.cine-online.eu/" ))
    itemlist.append( Item(channel=__channel__ , action="generos"   , title="Por categorías" , url="http://www.cine-online.eu/" ))
    itemlist.append( Item(channel=__channel__ , action="search"    , title="Buscar" ))

    return itemlist

def search(item,texto):
    logger.info("[cineonlineeu.py] search")
    if item.url=="":
        item.url="http://www.cine-online.eu/search?q="
    texto = texto.replace(" ","+")
    item.url = item.url+texto
    try:
        return peliculas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def generos(item):
    logger.info("[cineonlineeu.py] mainlist")
    itemlist = []
    
    '''
    <li><a href='#'>Peliculas por Genero</a>
    <ul>
    <li><a href='http://www.cine-online.eu/search/label/accion'>Acción</a></li>
    <li><a href='http://www.cine-online.eu/search/label/Animaci%C3%B3n'>Animacion</a></li>
    <li><a href='http://www.cine-online.eu/search/label/aventuras'>Aventuras</a></li>
    <li><a href='http://www.cine-online.eu/search/label/Belica'>Belica</a></li>
    <li><a href='http://www.cine-online.eu/search/label/ficcion'>Ficcion</a></li>
    <li><a href='http://www.cine-online.eu/search/label/Comedia'>Comedia</a></li>
    <li><a href='http://www.cine-online.eu/search/label/cine%20espa%C3%B1ol'>Cine Español</a></li>
    <li><a href='http://www.cine-online.eu/search/label/Documental'>Documental</a></li>
    <li><a href='http://www.cine-online.eu/search/label/Drama'>Drama</a></li>
    <li><a href='http://adultos.cine-online.eu/'>Eroticas</a></li>
    <li><a href='http://www.cine-online.eu/search/label/Fantastico'>Fantastico</a></li>
    <li><a href='http://www.cine-online.eu/search/label/Infantil'>Infantil</a></li>
    <li><a href='http://www.cine-online.eu/search/label/romance'>Romance</a></li>
    <li><a href='http://www.cine-online.eu/search/label/terror'>Terror</a></li>
    <li><a href='http://www.cine-online.eu/search/label/Thriller'>Thriller</a></li>
    <li><a href='http://www.cine-online.eu/search/label/Western'>Western</a></li>
    </ul>
    </li>
    '''
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,"<li><a href='#'>Peliculas por Genero</a>[^<]+<ul>(.*?)</ul>" )
    patron  = "<li><a href='([^']+)'>([^<]+)</a></li>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist


def peliculas(item):
    logger.info("[cineonlineeu.py] peliculas")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas (carpetas)
    patron  = "<div class='post bar hentry'>[^<]+"
    patron += "<a name='[^']+'></a>[^<]+"
    patron += "<h3 class='post-title entry-title'>[^<]+"
    patron += "<a href='([^']+)'>([^<]+)</a>[^<]+"
    patron += '</h3>.*?<img.*?src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        plot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , fanart = scrapedthumbnail , plot=plot , viewmode="movie", folder=True) )

    patron  = "<div class='item-content'>[^<]+"
    patron += "<div class='item-thumbnail'>[^<]+"
    patron += "<a href='([^']+)'[^<]+"
    patron += "<img.*?src='([^']+)'[^<]+"
    patron += "</a>[^<]+"
    patron += "</div>[^<]+"
    patron += "<div class='item-title'><a[^>]+>([^<]+)</a></div>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        plot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , fanart = scrapedthumbnail , plot=plot , folder=True) )

    # Extrae el paginador
    patronvideos  = "<a class='blog-pager-older-link' href='([^']+)'"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="Página siguiente >>" , url=scrapedurl , folder=True) )

    return itemlist

def findvideos(item):
    logger.info("[cineonlineeu.py] findvideos")
    data = scrapertools.cache_page(item.url)
    itemlist=[]

    #<a href="http://6dc55dcb.linkbucks.com/"
    patron = '(http://[a-z0-9]+.linkbucks.com)'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for url in matches:
        itemlist.append( Item(channel=__channel__, action="play", server="linkbucks", title="Ver enlace [linkbucks]" , url=url , thumbnail="" , plot=item.plot , folder=False) )

    #<a href="http://6dc55dcb.linkbucks.com/"
    patron = '(http://adf.ly/[a-zA-Z0-9]+)'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for url in matches:
        itemlist.append( Item(channel=__channel__, action="play", server="adfly", title="Ver enlace [adf.ly]" , url=url , thumbnail="" , plot=item.plot , folder=False) )

    from servers import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
        if videoitem.server!="linkbucks" and videoitem.server!="adfly":
            videoitem.channel=__channel__
            videoitem.action="play"
            videoitem.folder=False
            videoitem.title = "["+videoitem.server+"]"

    return itemlist

def play(item):
    logger.info("[cineonlineeu.py] play")
    itemlist=[]

    if item.server=="linkbucks":
        from servers import linkbucks
        location = linkbucks.get_long_url(item.url)
    elif item.server=="adfly":
        from servers import adfly
        location = adfly.get_long_url(item.url)
    else:
        location = item.url
        
    from servers import servertools
    itemlist=servertools.find_video_items(data=location)
    for videoitem in itemlist:
        videoitem.channel=__channel__
        videoitem.folder=False

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # mainlist
    mainlist_items = mainlist(Item())
    
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    peliculas_items = peliculas(mainlist_items[0])
    
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = findvideos(pelicula_item)
        if len(mirrors)>0 and len( play(mirrors[0]) )>0:
            bien = True
            break

    return bien
