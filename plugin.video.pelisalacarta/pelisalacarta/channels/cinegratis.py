# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cinegratis
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "cinegratis"
__category__ = "F,S,A,D"
__type__ = "generic"
__title__ = "Cinegratis"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[cinegratis.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="peliculas"   , title="Películas - Novedades"           , url="http://www.cinegratis.net/peliculas/novedades/", extra="No+Estrenos"))
    itemlist.append( Item(channel=__channel__, action="peliculas"   , title="Películas - Estrenos"            , url="http://www.cinegratis.net/estrenos-de-cine/", extra="Estrenos+de+Cine"))
    #itemlist.append( Item(channel=__channel__, action="peliscat"   , title="Películas - Géneros"             , url="http://www.cinegratis.net/index.php?module=generos"))
    #itemlist.append( Item(channel=__channel__, action="pelisalfa"  , title="Películas - Idiomas"             , url="http://www.cinegratis.net/index.php?module=peliculas"))
    #itemlist.append( Item(channel=__channel__, action="pelisalfa"  , title="Películas - Calidades"           , url="http://www.cinegratis.net/index.php?module=peliculas"))
    itemlist.append( Item(channel=__channel__, action="search"     , title="Buscar"))

    return itemlist

def peliculas(item):
    logger.info("[cinegratis.py] peliculas")
    itemlist = []

    # Descarga la página
    if "index.php" in item.url:
        data = scrapertools.cache_page(item.url.split("?")[0],post=item.url.split("?")[1])
    else:
        data = scrapertools.cache_page(item.url)

    print data

    # Extrae los items
    patron = "<td class='asd2'[^<]+<table(.*?)</table>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for bloque in matches:
        url = scrapertools.get_match(bloque,"<a class='style1' style='[^']+' href='([^']+)'>")
        titulo = scrapertools.get_match(bloque,"<a class='style1' style='[^']+' href='[^']+'>([^<]+)</a>").strip()
        thumbnail = scrapertools.get_match(bloque,"<img src='([^']+)'")
        
        plot=""
        if not url.startswith("/"):
            url = "/"+url
        scrapedtitle = unicode(titulo,"iso-8859-1").encode("utf-8")
        scrapedurl = urlparse.urljoin(item.url,url.replace("\n",""))
        scrapedthumbnail = urlparse.urljoin(item.url,thumbnail)
        scrapedplot = scrapertools.htmlclean(plot)
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , fulltitle=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, viewmode="movie", context="4|5"))

    # Extrae la marca de siguiente página
    #<input class='boton' type='button' value='2' style='margin-left:15px;margin-right:15px;cursor:pointer; font-weight:normal;  background-color:#4B4A42; border: solid 1px #4B4A42;color:#ffffff;'>
    #<input class='boton' style='margin-left:3px;margin-right:3px;cursor:pointer;background-color:#393831;border: solid 1px #4B4A42;' type='button' value='3' onclick='document.homesearch.pag.value=3;document.homesearch.tesths.value=1;document.homesearch.submit();'><input class='boton' style='margin-left:3px;margin-right:3px;cursor:pointer;background-color:#393831;border: solid 1px #4B4A42;'type='button' value='4' onclick='document.homesearch.pag.value=4;document.homesearch.tesths.value=1;document.homesearch.submit();'><input class='boton' style='margin-left:3px;margin-right:3px;cursor:pointer;background-color:#393831;border: solid 1px #4B4A42;'type='button' value='5' onclick='document.homesearch.pag.value=5;document.homesearch.tesths.value=1;document.homesearch.submit();'>
    patron = "<input class='boton' type='button' value='[^']+' style='[^']+'><input class='boton' style='[^']+' type='button' value='[^']+' onclick='document.homesearch.pag.value\=(\d+)\;"
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "Página siguiente >>"
        if item.extra=="Estrenos+de+Cine":
            scrapedurl = "http://www.cinegratis.net/index.php?hstype=t%EDtulo&hstitle=Todos...&hscat=Todos&hslanguage=Todos&hsquality=Todas&hsestreno="+item.extra+"&hsyear1=Desde...&hsyear2=...Hasta&pag="+matches[0]+"&order1=&order2=&hsletter=&tesths=1"
        else:
            scrapedurl = "http://www.cinegratis.net/index.php?hstype=t%EDtulo&hstitle=Todos...&hscat=Todos&hslanguage=Todos&hsquality=Todas&hsestreno="+item.extra+"&hsyear1=Desde...&hsyear2=...Hasta&pag="+matches[0]+"&order1=id2&order2=desc&hsletter=&tesths=1"
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=__channel__, action="peliculas" , title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, extra=item.extra))

    return itemlist

def findvideos(item):
    logger.info("[cinegratis.py] findvideos")

    itemlist = []
    data = scrapertools.cachePage(item.url)
    '''
    <td align='center' valign='top' class='celda2'>vk.com</td>
    <td align='center' valign='top' class='celda2'>Desconocida</td>
    <td align='center' valign='top' class='celda2'>Versión Original</td>
    <td align='center' valign='top' class='celda2'>1</td>
    '''
    patron  = "<td align='center' valign='top' class='celda2'>([^<]+)</td>[^<]+"
    patron += "<td align='center' valign='top' class='celda2'>([^<]+)</td>[^<]+"
    patron += "<td align='center' valign='top' class='celda2'>([^<]+)</td>[^<]+"
    patron += "<td align='center' valign='top' class='celda2'>([^<]+)</td>[^<]+"
    patron += "<td[^<]+</td><td[^<]+<div[^<]+</div><div[^<]+</div></td></tr><tr[^<]+<td[^<]+<div[^<]+<a class='[^']+' style='[^']+' href='([^']+)"
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for servidor,calidad,idioma,partes,url in matches:
        titulo = servidor + " (" + idioma + ")"
        titulo = unicode(titulo,"iso-8859-1").encode("utf-8")
        itemlist.append( Item(channel=__channel__, action="play" , title=titulo , url=url, folder=False))

    return itemlist

def play(item):
    logger.info("[divxonline.py] play")
    itemlist=[]
    data = scrapertools.cachePage(item.url)
    #logger.info("data="+data)
    itemlist = servertools.find_video_items(data=data)
    i=1
    for videoitem in itemlist:
        videoitem.title = "Mirror %d%s" % (i,videoitem.title)
        videoitem.fulltitle = item.fulltitle
        videoitem.channel=channel=__channel__
        i=i+1

    return itemlist

def search(item,texto):
    logger.info("[cinegratis.py] search")
    if item.url=="":
        item.url="http://www.cinegratis.net/index.php?hstype=t%EDtulo&hstitle="+texto+"&hscat=Todos&hslanguage=Todos&hsquality=Todas&hsestreno=Todos&hsyear1=Desde...&hsyear2=...Hasta&pag=1&order1=&order2=&hsletter=&tesths=0"
    texto = texto.replace(" ","+")
    return peliculas(item)

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
