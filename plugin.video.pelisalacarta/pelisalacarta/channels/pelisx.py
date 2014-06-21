# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para PelisX (por ZeDinis)
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "pelisx"
__category__ = "F"
__type__ = "generic"
__title__ = "PelisX"
__language__ = "ES"

# Traza el inicio del canal
logger.info("[pelisx.py] init")

DEBUG = True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[pelisx.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Ver Todas" , url="http://www.pelisx.net/ver-todos/"))
    itemlist.append( Item(channel=__channel__, action="listcategorias"      , title="Categorias" , url="http://www.pelisx.net/ver-todos/"))
    itemlist.append( Item(channel=__channel__, action="listactrices"    , title="Actrices y Tags", url="http://www.pelisx.net/actrices-porno/"))
    itemlist.append( Item(channel=__channel__, action="search"    , title="Buscar...", url=""))
    return itemlist

def listcategorias(item):
    logger.info("[pelisx.py] listcategorias")
    itemlist=[]

    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Amateur" , url="http://www.pelisx.net/amateur/"))
    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Anal" , url="http://www.pelisx.net/anal/"))
    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Asiaticas" , url="http://www.pelisx.net/asiaticas/"))
    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Grupos" , url="http://www.pelisx.net/grupos/"))
    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Hentai" , url="http://www.pelisx.net/hentai/"))
    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Interracial" , url="http://www.pelisx.net/interracial/"))
    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Jovencitas" , url="http://www.pelisx.net/jovencitas-peliculas-online/"))
    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Lesbianas" , url="http://www.pelisx.net/lesbianas/"))
    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Maduritas" , url="http://www.pelisx.net/maduritas/"))
    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Oral" , url="http://www.pelisx.net/oral-peliculas-online/"))
    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Pornstars" , url="http://www.pelisx.net/pornstars/"))
    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Tetonas" , url="http://www.pelisx.net/tetonas/"))    

    return itemlist
        
def listactrices(item):
    logger.info("[pelisx.py] listactrices")
    
    itemlist=[]
    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    logger.info(data)
    
    # Extrae las entradas (carpetas)
    patronvideos = "<a href='(.+?)'[^<]+>(.+?)</a>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    scrapertools.printMatches(matches)
    
    for match in matches:

        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item ( channel=__channel__ , action="listapelis" , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot ) )

    return itemlist

def search(item,texto):
    logger.info("[pelisx.py] search")
    itemlist = []

    texto = texto.replace(" ","+")
    item.url="http://www.pelisx.net/?s=" + texto    
    itemlist.extend(listapelis(item))
    
    return itemlist

def listapelis(item):
    logger.info("[pelisx.py] listapelis")

    itemlist=[]
    '''
    GET /ver-todos/ HTTP/1.1
    Host: www.pelisx.net
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:20.0) Gecko/20100101 Firefox/20.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    Accept-Language: es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3
    Accept-Encoding: gzip, deflate
    Cookie: 720planBAK=R3744889740; 720plan=R1791155563; __utma=187995689.514298305.1366385595.1366385595.1366385595.1; __utmb=187995689.2.10.1366385595; __utmc=187995689; __utmz=187995689.1366385595.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)
    Connection: keep-alive
    If-Modified-Since: Fri, 19 Apr 2013 15:22:21 GMT
    Cache-Control: max-age=0
    '''
    # Descarga la página
    headers=[]
    headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:20.0) Gecko/20100101 Firefox/20.0"])
    headers.append(["Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"])
    headers.append(["Accept-Language","es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"])
    headers.append(["Accept-Encoding","gzip, deflate"])
    data = scrapertools.cachePage(item.url,headers=headers)
    #logger.info(data)

    # Extrae las entradas 
    #<img src="http://www.pelisx.net/wp-content/themes/twenten/thumb.php?src=http://www.pelisx.net/wp-content/uploads/2013/04/13.png&amp;h=200&amp;w=140&amp;zc=1&q=100" alt="Rump Raiders 2" />                <h2><a href="http://www.pelisx.net/pelicula-porno/rump-raiders-2/">Rump Raiders 2</a></h2>        <span><a href="http://www.pelisx.net/anal/">Anal</a></span>       </div>              <div class="contenedor_wallpaper_img  f_left">                      <img src="http://www.pelisx.net/wp-content/themes/twenten/thumb.php?src=http://www.pelisx.net/wp-content/uploads/2013/04/12.png&amp;h=200&amp;w=140&amp;zc=1&q=100" alt="Teens vs Mamas
    patronvideos  = '<img src="http://www.pelisx.net/wp-content/themes/twenten/thumb.php\?src\=(http\://[^\&]+)[^<]+<h2[^<]+<a href="([^"]+)">([^<]+)</a></h2>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    scrapertools.printMatches(matches)

    for match in matches:
        scrapedurl = urlparse.urljoin(item.url,match[1])     
        scrapedtitle = match[2]
        scrapedthumbnail = match[0]
        scrapedplot = ""
        
        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle.strip(), url=scrapedurl, thumbnail=scrapedthumbnail))
        

    # Extrae la marca de siguiente página
    
    patronvideos  = '<a href="([^"]+)" class="nextpostslink">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "Siguiente página >>"
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=__channel__, action="listapelis" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail))
        
    return itemlist

def findvideos(item):
    logger.info("[pelisx.py] findvideos")

    itemlist=[]
    # Descarga la página
    headers=[]
    headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:20.0) Gecko/20100101 Firefox/20.0"])
    headers.append(["Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"])
    headers.append(["Accept-Language","es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"])
    headers.append(["Accept-Encoding","gzip, deflate"])
    data = scrapertools.cachePage(item.url,headers=headers)
    logger.info(data)

    from servers import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
        videoitem.channel=__channel__
        videoitem.action="play"
        videoitem.folder=False
        videoitem.title = "["+videoitem.server+"]"

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools

    # mainlist
    mainlist_items = mainlist(Item())
    listapelis_items = listapelis(mainlist_items[0])

    return bien
