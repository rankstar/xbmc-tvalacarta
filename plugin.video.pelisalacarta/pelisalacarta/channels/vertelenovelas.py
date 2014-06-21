# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para vertelenovelas
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "vertelenovelas"
__category__ = "S"
__type__ = "generic"
__title__ = "Ver Telenovelas"
__language__ = "ES"
__creationdate__ = "20121015"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[vertelenovelas.py] mainlist")
    
    itemlist = []

    itemlist.append( Item(channel=__channel__, action="novedades_episodios" , title="Últimos capítulos agregados"    , url="http://vertelenovelas.net/"))
    itemlist.append( Item(channel=__channel__, action="series"              , title="Últimas telenovelas agregadas"  , url="http://vertelenovelas.net/"))
    itemlist.append( Item(channel=__channel__, action="emision"             , title="Lista de telenovelas en emisión", url="http://vertelenovelas.net/"))
    itemlist.append( Item(channel=__channel__, action="todas"               , title="Lista completa"                 , url="http://vertelenovelas.net/"))
    itemlist.append( Item(channel=__channel__, action="letras"              , title="Lista alfabética"               , url="http://vertelenovelas.net/"))

    return itemlist

def novedades_episodios(item):
    logger.info("[vertelenovelas.py] novedades_episodios")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    patron  = '<div class="not"><div class="tova"></div><a href="([^"]+)" title="([^"]+)"[^<]+'
    patron += '<img class="[^"]+" src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        title = scrapedtitle.strip()
        title = unicode( title, "iso-8859-1" , errors="replace" ).encode("utf-8")
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = scrapedthumbnail
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , url=url , thumbnail=thumbnail, viewmode="movie", folder=True) )

    return itemlist

def series(item):
    logger.info("[vertelenovelas.py] series")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    patron  = '<div class="not1"><a href="([^"]+)" title="([^"]+)"[^<]+'
    patron += '<img class="[^"]+" src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        title = scrapedtitle.strip()
        title = unicode( title, "iso-8859-1" , errors="replace" ).encode("utf-8")
        url = urlparse.urljoin("http://vertelenovelas.net",scrapedurl)
        thumbnail = scrapedthumbnail
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
        itemlist.append( Item(channel=__channel__, action="episodios", title=title , url=url , thumbnail=thumbnail, viewmode="movie", folder=True) )

    if len(itemlist)==0:
        patron  = '<article[^<]+'
        patron += '<a href="([^"]+)"[^<]+'
        patron += '<header>([^<]+)</header[^<]+'
        patron += '<figure><img src="([^"]+)"'

        matches = re.compile(patron,re.DOTALL).findall(data)
        if DEBUG: scrapertools.printMatches(matches)

        for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
            title = scrapedtitle.strip()
            title = unicode( title, "iso-8859-1" , errors="replace" ).encode("utf-8")
            url = urlparse.urljoin("http://vertelenovelas.net",scrapedurl)
            thumbnail = scrapedthumbnail
            if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
            itemlist.append( Item(channel=__channel__, action="episodios", title=title , url=url , thumbnail=thumbnail, viewmode="movie", folder=True) )

    return itemlist

def canales(item):
    logger.info("[vertelenovelas.py] canales")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    data = scrapertools.get_match(data,'<div class="ctit">TELENOVELAS POR CANALAES DE TELEVISION(.*?)</ul>')
    patron  = '<li><a href="([^"]+)[^>]+>([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
        itemlist.append( Item(channel=__channel__, action="series", title=title , url=url , folder=True) )
    
    return itemlist

def letras(item):
    logger.info("[vertelenovelas.py] letras")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    patron  = '<li class="menu-gen"><a href="(letra[^"]+)[^>]+>([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
        itemlist.append( Item(channel=__channel__, action="series", title=title , url=url , folder=True) )
    
    return itemlist

def episodios(item):
    logger.info("[vertelenovelas.py] episodios")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<ul class="anime_episodios"(.*?)</ul>')
    #<li><a href="ver/rafaela-119.html">Capitulo 119</a></li>
    patron  = '<li><a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        title = scrapertools.htmlclean(scrapedtitle)
        plot = ""
        thumbnail = ""
        url = urlparse.urljoin(item.url,scrapedurl)

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=True) )
    
    return itemlist

def findvideos(item):
    logger.info("[vertelenovelas.py] findvideos")
    data = scrapertools.cache_page(item.url)
    itemlist=[]

    #<embed type="application/x-shockwave-flash" src="http://vertelenovelas.net/player.swf" width="680" height="430" id="mpl" name="mpl" quality="high" allowscriptaccess="always" allowfullscreen="true" wmode="transparent" flashvars="&file=http://content1.catalog.video.msn.com/e2/ds/4eeea8b3-6228-492b-a2be-e8b920cf4d4e.flv&backcolor=fd4bc5&frontcolor=fc9dde&lightcolor=ffffff&controlbar=over&volume=100&autostart=false&image=">
    #<embed type="application/x-shockwave-flash" src="http://vertelenovelas.net/player.swf" width="680" height="430" id="mpl" name="mpl" quality="high" allowscriptaccess="always" allowfullscreen="true" wmode="transparent" flashvars="&file=http://content1.catalog.video.msn.com/e2/ds/4eeea8b3-6228-492b-a2be-e8b920cf4d4e.flv&backcolor=fd4bc5&frontcolor=fc9dde&lightcolor=ffffff&controlbar=over&volume=100&autostart=false&image="></embed></d
    patron = '<embed type="application/x-shockwave-flash" src="http://vertelenovelas.net/player.swf".*?file=([^\&]+)&'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        itemlist.append( Item(channel=__channel__, action="play", server="directo", title=item.title , url=match , thumbnail=item.thumbnail , plot=item.plot , folder=False) )

    #<embed width="680" height="450" flashvars="file=mp4:p/459791/sp/45979100/serveFlavor/flavorId/0_0pacv7kr/forceproxy/true&amp;image=&amp;skin=&amp;abouttext=&amp;dock=false&amp;streamer=rtmp://rtmpakmi.kaltura.com/ondemand/&amp;
    patron = '<embed width="[^"]+" height="[^"]+" flashvars="file=([^\&]+)&.*?streamer=(rtmp[^\&]+)&'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for final,principio in matches:
        itemlist.append( Item(channel=__channel__, action="play", server="directo", title=item.title , url=principio+final , thumbnail=item.thumbnail , plot=item.plot , folder=False) )

    #file=mp4:/c/g1MjYyYjpCnH8dRolOZ2G7u1KsleMuDS/DOcJ-FxaFrRg4gtDIwOjkzOjBrO8N_l0&streamer=rtmp://cp96275.edgefcs.net/ondemand&
    patron = 'file=([^\&]+)&streamer=(rtmp[^\&]+)&'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for final,principio in matches:
        itemlist.append( Item(channel=__channel__, action="play", server="directo", title=item.title , url=principio+"/"+final , thumbnail=item.thumbnail , plot=item.plot , folder=False) )


    from servers import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
        videoitem.channel=__channel__
        videoitem.action="play"
        videoitem.folder=False
        videoitem.title = "["+videoitem.server+"]"

    return itemlist

def todas(item):
    logger.info("[vertelenovelas.py] todas")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<h2 class="title">Lista de Telenovelas</h2>(.*?)</ul>')
    #<li><a href="abrazame-muy-fuerte.html" title="Abrazame muy fuerte" class="     El Canal de las es">Abrazame muy fuerte</a></li><li><a href="acorralada.html" title="Acorralada" class="Estados Unidos">Acorralada</a></li><li><a href="al-diablo-con-los-
    patron  = '<li><a href="([^"]+)[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
        itemlist.append( Item(channel=__channel__, action="episodios", title=title , url=url , folder=True) )
    
    return itemlist

def emision(item):
    logger.info("[vertelenovelas.py] emision")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<h2 class="title">Telenovelas en Emision</h2>(.*?)</ul>')
    patron  = '<li><a href="([^"]+)[^>]+>([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
        itemlist.append( Item(channel=__channel__, action="episodios", title=title , url=url , folder=True) )
    
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