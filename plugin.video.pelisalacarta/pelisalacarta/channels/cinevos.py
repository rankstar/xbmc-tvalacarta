# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cinevos 
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

from core import scrapertools
from core import logger
from core.item import Item
from core import downloadtools
from servers import servertools

CHANNELNAME = "cinevos"
DEBUG = True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[cinevos.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, action="listvideos"      , title="Ultimas Peliculas Añadidas " , url="http://www.cinevos.com/"))
    #itemlist.append( Item(channel=CHANNELNAME, action="listvideos"      , title="Estrenos" , url="http://www.cinevos.com/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listbyYears"    , title="Año de estreno", url="http://www.cinevos.com/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcategorias"    , title="Categorias", url="http://www.cinevos.com/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listalfanum"    , title="Listado alfabetico", url="http://www.cinevos.com"))
    itemlist.append( Item(channel=CHANNELNAME, action="search"    , title="Buscar", url="http://www.cinevos.com"))
    return itemlist

def search(item,texto):
    logger.info("[cinevos.py] search")
    item.url = "http://www.cinevos.com/index.php?do=search&subaction=search&story=%s" % texto
    try:
        return listvideos(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def listcategorias(item):
    logger.info("[cinevos.py] listcategorias")
    
    itemlist=[]
    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    #logger.info(data)
    
    # Extrae las entradas (carpetas)
    patronvideos  = '<div class="films-category" id="cat">(.*?)<div style="clear: both;"></div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    patronvideos = '<a href="(.+?)">(.+?)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(matches[0])
    scrapertools.printMatches(matches)
    
    for match in matches:

        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item ( channel=CHANNELNAME , action="listvideos" , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot ) )

    return itemlist
        
def listbyYears(item):
    logger.info("[cinevos.py] listbyYears")
    
    itemlist=[]
    startYear = 1990
    finalYear  = 2012
    uri = "/index.php?do=search&subaction=search&story=%d"
    for i in range(finalYear-startYear+1):

        scrapedtitle = str(finalYear)
        scrapedurl = urlparse.urljoin(item.url,uri %finalYear)
        scrapedthumbnail = ""
        scrapedplot = ""
        finalYear = finalYear - 1
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item ( channel=CHANNELNAME , action="listvideos" , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot ) )

    return itemlist
    
def listalfanum(item):
    logger.info("[cinevos.py] listalfanum")
    
    BaseChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    BaseUrl   = "http://www.cinevos.com/index.php?&do=cat&catalog=%s"
    action    = "listvideos"
    itemlist = []
    #itemlist.append( Item(channel=CHANNELNAME, action=action, title="0-9" , url=BaseUrl % "0-9" , thumbnail="" , plot="" , folder=True) )
    for letra in BaseChars:
        scrapedtitle = letra
        scrapedplot = ""
        scrapedurl = BaseUrl % letra.lower()
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action=action, title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    return itemlist
    
def listvideos(item):
    logger.info("[cinevos.py] listvideos")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    logger.info(data)

    # Extrae las entradas (carpetas)
    patronvideos  = '<div class="music-news">(.*?</a>(?:&nbsp;|)</div>)'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)==0:
        patronvideos  = '<div class="standart-news">(.*?<div style="clear: both;">)</div>'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)        
    itemlist = []
    for match in matches:
        # URL
        try:
            scrapedurl = re.compile(r'href="(.+?)"').findall(match)[0]
        except:
            continue
        # Titulo
        try:
            scrapedtitle = re.compile(r'<h2>(.+?)</h2>').findall(match.replace("\n",""))[0]
            scrapedtitle = re.sub("<[^>]+>","",scrapedtitle)

        except:
            try:scrapedtitle = re.compile(r'alt="(.+?)"').findall(match)[0]
            except:scrapedtitle = "sin titulo"
        # Año 
        try:
            title1 = re.compile(r'<div class="quality">(.+?)</a>').findall(match)[0]
            title1 = re.sub("<[^>]+>","",title1)
        except:
            title1 = ""
        # Thumbnail
        try:
            scrapedthumbnail = urlparse.urljoin(item.url,re.compile(r'src="(.+?)"').findall(match)[0])
        except:
            scrapedthumbnail = ""
        # Argumento
        try:
            scrapedplot = re.compile(r'(<img src=.+?)<div style="clear: both;">').findall(match)[0]
            scrapedplot = re.sub("<[^>]+>"," ",scrapedplot).strip()
        except:
            scrapedplot = ""
        if title1:
            scrapedtitle = scrapedtitle + " (" +title1.replace("&nbsp;","") + ")"
        try:
            scrapedtitle = scrapertools.unescape(scrapedtitle)
            scrapedplot = scrapertools.unescape(scrapedplot)
        except:pass
        # Depuracion
        if (DEBUG):
            logger.info("scrapedtitle="+scrapedtitle)
            logger.info("scrapedurl="+scrapedurl)
            logger.info("scrapedthumbnail="+scrapedthumbnail)

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, extra = scrapedplot , context= "4|5"  ))
        

    # Extrae la marca de siguiente página
    
    patronvideos  = '<span class="thide pnext">(Next)</span>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "Página siguiente"
        if "search_start" in item.url:
            search_start = re.compile("search_start=(.+?)\&").findall(item.url)[0]
            scrapedurl = item.url.replace("search_start="+search_start,"search_start="+str(int(search_start)+1))
        else:
            scrapedurl = item.url+"&search_start=2&full_search=0"
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=CHANNELNAME, action="listvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot ))
        
    return itemlist

def findvideos(item):
    logger.info("[cinevos.py] findvideos")
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    logger.info(data)
    # Busca si hay subtitulo
    patronvideos  = '<a href="(http://www.cinevos.com/sub/[^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    sub = ""
    if len(matches):
        sub = matches[0]
        logger.info("con subtitulo :%s" %sub)
    # Busca la descripcion
    patronvideos  = '<p>(<div.*?</div>) </p>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    plot = ""
    if len(matches):
        plot = re.sub("<[^>]+>","",matches[0])
    # Busca los enlaces a los videos
    listavideos = servertools.findvideos(data)
    itemlist = []
    for video in listavideos:
        videotitle = scrapertools.unescape(video[0])
        #print videotitle
        url = video[1]
        server = video[2]
        if "Megaupload" in videotitle:
            videotitle = item.title + " - [Megaupload]"
        else:
            videotitle = item.title+ " - " +videotitle
        itemlist.append( Item(channel=CHANNELNAME, action="play", server=server, title=videotitle , url=url , thumbnail=item.thumbnail , plot=plot ,subtitle=sub, folder=False) )
    return itemlist

def test():
    bien = True
    
    # mainlist
    mainlist_items = mainlist(Item())
    peliculas_items = listvideos(mainlist_items[0])

    # Comprueba primero las películas "Recientes" a ver si alguna tiene mirrors    
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = findvideos(item=pelicula_item)
        if len(mirrors)>0:
            bien = True
            break
    
    return bien
