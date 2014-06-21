# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para internapoli
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "internapoli"
__category__ = "F"
__type__ = "generic"
__title__ = "Internapoli City (IT)"
__language__ = "IT"
__creationdate__ = "20110516"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[internapoli.py] mainlist")
    item.url = "http://www.internapoli-city.org/"
    return novedades(item)

def novedades(item):
    logger.info("[internapoli.py] novedades")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    '''
    <div class='post bar hentry'>
    <a name='1873478727340052815'></a>
    <h3 class='post-title entry-title'>
    <a href='http://www.internapoli-city.org/2011/11/yes-man-megaupload-ita.html'>Yes Man Film Streaming (2008)</a>
    </h3>
    <div class='post-header-line-1'></div>
    <div class='post-body entry-content'>
    <div id='summary1873478727340052815'><div dir="ltr" style="text-align: left;" trbidi="on">
    <div class="separator" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em; text-align: center;">
    <img border="0" height="200" src="http://1.bp.blogspot.com/-FmPLmbLHyso/Tr1BN8koSGI/AAAAAAAAAos/o_2dDVDchxE/s200/yes+man.jpg" width="141" /></div>
    <br />
    <div>
    Yes Man è un film del 2008, diretto da Peyton Reed. La pellicola racconta la storia di Carl Allen, interpretato da Jim Carrey, un uomo apatico e insoddisfatto della sua vita. Un giorno Carl incontra un suo ex collega che lo obbliga a partecipare ad un seminario sull&#8217;autostima, in cui viene spiegato un sistema per dare una svolta alla propria esistenza, che consiste nel dire sempre e a qualunque costo &#8220;sì&#8221; a tutto quello che ci viene richiesto.</div>
    </div>
    <br />
    <div style="text-align: center;">
    <b>Link.. (<a href="http://rapidgator.net/file/45405741/yes.man.2008.italian.dvdrip.xvid_p92.avi.html" target="_blank">Rapidgator</a>)-(<a href="http://www.putlocker.com/file/57077A323E5B3972" target="_blank">Putlocker</a>)-(<a href="http://www.nowvideo.co/video/08a947be1e980" target="_blank">Nowvideo</a>)-(<a href="http://www.nowdownload.co/dl/b1837f9f2f78b" target="_blank">Nowdownload</a>)</b></div>
    <div style="text-align: center;">
    <b>Qualità: Dvdrip - Anno: 2008</b></div>
    <br />
    <center>
    <iframe allowfullscreen="allowfullscreen" frameborder="0" height="315" src="http://www.youtube.com/embed/FVI78YxlWGw" width="560"></iframe></center>
    </div>
    <script type='text/javascript'>
    masSummaryAndThumb("summary1873478727340052815","http://www.internapoli-city.org/2011/11/yes-man-megaupload-ita.html");
    </script>
    <div class='readmorecontent'><a href='http://www.internapoli-city.org/2011/11/yes-man-megaupload-ita.html'>Vai al Film &#187;</a></div>
    <div style='clear: both;'></div>
    </div>
    <div class='post-footer'><span class='post-labels'>
    Etichette:
    <a href='http://www.internapoli-city.org/search/label/Commedia' rel='tag'>Commedia</a>,
    <a href='http://www.internapoli-city.org/search/label/DvdRip' rel='tag'>DvdRip</a>
    </span>
    </div>
    </div>
    '''
    patronvideos  = "<div class='post bar hentry'>[^<]+"
    patronvideos += "<a name='[^']+'></a>[^<]+"
    patronvideos += "<h3 class='post-title entry-title'>[^<]+"
    patronvideos += "<a href='([^']+)'>([^<]+)</a>.*?"
    patronvideos += '<img border="[^"]+" height="[^"]+" src="([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , viewmode="movie", folder=True) )

    #<a class='blog-pager-older-link' href='http://www.internapoli-city.org/search?updated-max=2012-05-15T23:54:00%2B02:00&amp;max-results=10' id='Blog1_blog-pager-older-link' title='Post più vecchi'><img height='38' src='http://1.bp.blogspot.com/-duUmcoXvqN8/T3uMWNT32hI/AAAAAAAAD4Q/EJ7MUmU1F90/s1600/desno.png' width='50'/></a>
    patron = "<a class='blog-pager-older-link' href='([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = ">> Página siguiente"
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,match)
        scrapedthumbnail = match[2]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="novedades", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def findvideos(item):
    logger.info("[internapoly.py] findvideos")

    data = scrapertools.cache_page(item.url)
    item.url = scrapertools.get_match(data,'<div class="separator"[^<]+<img[^<]+</div[^<]+.*?<a href="([^"]+)"')
    data = scrapertools.cache_page(item.url)
    
    itemlist = servertools.find_video_items(data=data)
        
    for videoitem in itemlist:
        videoitem.channel = __channel__

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools

    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    peliculas_items = mainlist(Item())
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = servertools.find_video_items( item=pelicula_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien