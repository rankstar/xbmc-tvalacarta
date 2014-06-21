# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculasid 
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "peliculasid"
__category__ = "F"
__type__ = "generic"
__title__ = "PeliculasID"
__language__ = "ES"

# Traza el inicio del canal
logger.info("[peliculasid.py] init")

DEBUG = True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[peliculasid.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="listvideos"      , title="Ultimos capítulos" , url="http://www.peliculasid.net/"))
    itemlist.append( Item(channel=__channel__, action="listvideos"      , title="Estrenos" , url="http://www.peliculasid.net/categoria/estreno"))
    itemlist.append( Item(channel=__channel__, action="listbyYears"    , title="Año de estreno", url="http://www.peliculasid.net/"))
    itemlist.append( Item(channel=__channel__, action="listcategorias"    , title="Categorias", url="http://www.peliculasid.net/"))
    itemlist.append( Item(channel=__channel__, action="listalfanum"    , title="Listado alfabetico", url="http://www.peliculasid.net/"))
    return itemlist

def listcategorias(item):
    logger.info("[peliculas.py] listcategorias")
    
    itemlist=[]
    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    #logger.info(data)
    
    # Extrae las entradas (carpetas)
    patronvideos  = '<div class="generos">(.*?)<div class="corte"></div>'
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
        itemlist.append( Item ( channel=__channel__ , action="listvideos" , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot ) )

    return itemlist
        
def listbyYears(item):
    logger.info("[peliculas.py] listbyYears")
    
    itemlist=[]
    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    #logger.info(data)
    
    # Extrae las entradas (carpetas)
    patronvideos  = '<div class="subtitulo">A.+o de estreno</div>(.*?)<div id="ano">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    patronvideos = '<option value="(/categoria.+?)">(.+?)</option>'
    matches = re.compile(patronvideos,re.DOTALL).findall(matches[0])
    scrapertools.printMatches(matches)
    
    for match in matches:

        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item ( channel=__channel__ , action="listvideos" , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot ) )

    return itemlist
    
def listalfanum(item):
    logger.info("[peliculasid.py] listalfanum")
    
    BaseChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    BaseUrl   = "http://peliculasid.net/categoria/letra/%s"
    action    = "listvideos"
    itemlist = []
    itemlist.append( Item(channel=__channel__, action=action, title="0-9" , url=BaseUrl % "0-9" , thumbnail="" , plot="" , folder=True) )
    for letra in BaseChars:
        scrapedtitle = letra
        scrapedplot = ""
        scrapedurl = BaseUrl % letra
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action=action, title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    return itemlist
    
def listvideos(item):
    logger.info("[peliculasid.py] listvideos")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    logger.info(data)

    # Extrae las entradas (carpetas)
    patronvideos  = 'id="filmga[^"]+" class="filmgal">(.*?<strong>Duraci[^<]+</strong>[^<]+</div>)'
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
            scrapedtitle = re.compile(r'<span class="titulotool">(.+?)</div>').findall(match.replace("\n",""))[0]
            scrapedtitle = re.sub("<[^>]+>","",scrapedtitle)
            try:
                scrapedtitle = scrapertools.unescape(scrapedtitle)
            except:pass
        except:
            scrapedtitle = "sin titulo"
        # Thumbnail
        try:
            scrapedthumbnail = re.compile(r'src="(.+?)"').findall(match)[0]
        except:
            scrapedthumbnail = ""
        # Argumento
        try:
            scrapedplot = re.compile(r'<div class="sinopsis">(.+?)</div>').findall(match)[0]
            scrapedplot = re.sub("<[^>]+>"," ",scrapedplot).strip()
        except:
            scrapedplot = ""

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle.strip() , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, extra = scrapedplot , context= "4|5", viewmode="movie", folder=False  ))
        

    # Extrae la marca de siguiente página
    
    patronvideos  = "<span class='current'>[^<]+</span><a href='(.+?)' class='page larger'>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "Página siguiente"
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=__channel__, action="listvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot ))
        
    return itemlist

def play(item):
    logger.info("[peliculasid.py] play")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    logger.info("data="+data)
    #so.addVariable('file','http://peliculasid.net/plugins/rip-google.php?id=pAFm6wNHwrsPmbxHWNcec9MTjNZETYmyPJy0liipFm0#.mp4');
    mediaurl = scrapertools.get_match(data,"so.addVariable\('file','([^']+)'")
    itemlist.append( Item(channel=__channel__, action="play" , title=item.title , url=mediaurl, thumbnail="", plot="", server="directo"))

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    peliculas_items = listvideos(mainlist_items[0])
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = play( item=pelicula_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien