# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para Shurweb
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os,sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools


__channel__ = "seriesid"
__category__ = "S"
__type__ = "generic"
__title__ = "Seriesid"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[seriesid.py] getmainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Últimos episodios" , action="ultimos" , url="http://seriesid.com/ultimos-episodios/", fanart="http://pelisalacarta.mimediacenter.info/fanart/seriesid.jpg"))
    itemlist.append( Item(channel=__channel__, title="Todas"             , action="series"  , url="http://seriesid.com/", fanart="http://pelisalacarta.mimediacenter.info/fanart/seriesid.jpg"))
    itemlist.append( Item(channel=__channel__, title="Buscar"            , action="search"  , fanart="http://pelisalacarta.mimediacenter.info/fanart/seriesid.jpg") )
    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto,categoria=""):
    logger.info("[seriesid.py] "+item.url+" search "+texto)
    itemlist = []
    url = item.url
    texto = texto.replace(" ","+")
    logger.info("categoria: "+categoria+" url: "+url)
    try:
        item.url = "http://seriesid.com/search/%s"
        item.url = item.url % texto
        itemlist.extend(series(item))
        return itemlist
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def ultimos(item):
    logger.info("[seriesid.py] ultimos")
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<div id="main"(.*?)</ul>')
    
    # Extrae las entradas
    '''
    <div class="thumbnail">
    <a href="http://www.seriesid.tv/vicious-1x06/"><img pagespeed_high_res_src="http://1-ps.googleusercontent.com/h/www.seriesid.tv/wp-content/uploads/xVicious_Serie_de_TV-621455088-large1-166x250.jpg.pagespeed.ic.HS26zzzapg.jpg" title="Vicious 1x06 - Episode 6" src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAFA3PEY8MlBGQUZaVVBfeMiCeG5uePWvuZHI////////////////////////////////////////////////////2wBDAVVaWnhpeOuCguv/////////////////////////////////////////////////////////////////////////wAARCAD6AKYDASIAAhEBAxEB/8QAGAABAQEBAQAAAAAAAAAAAAAAAAECAwT/xAApEAEBAAIBBAEDBAIDAAAAAAAAAQIRMQMSIUFRIjJxE0JhkQSBM6HB/8QAFwEBAQEBAAAAAAAAAAAAAAAAAAECA//EABoRAQEBAQEBAQAAAAAAAAAAAAABEQIxEkH/2gAMAwEAAhEDEQA/APMukVHQFNIqGlAAAAABUAAATSgIKaBE0uxUQAFNml0igAAoKAAAAAAAAgKCUXSCCKaBABBSKKACgLJcrqcgg7/o4z7rbf4S9LH9t/sTY4jWXTyx5nj5ZFAAAAAAAAQUBkARVRRQAB6Ojj24915rhOXouXnUGempNn6cXu0uWUnrkZZyxk12uHVx15k18t552WbmmMsu7C0WesIN9LDvz1/Y2YdPLP7Z/tu/4+c4srvr6e3HxE7de6rH082fSyw82eGHs1vxfMrz9Xp9l/i8I1K5gCmk2oCACKAKAAPT0/PTleZ16Oevp+RK73HG+bIz1bjqW2Nyf7cupjL5vTGWerjjJ49uMusbG+rda/Dj3boN7dv8b7svw88dellrP8jXseqZJnnMbrmrrG+bNsd0vU1q8e4rCd/1z/xOtd9K/leprHHxHHO3XN0isBAbAAQUAABUDuDYrp0MZ3+fjw49123MrLLPS4xenpuX6fM8OefX6evHmu+NnUwl+Xl6vQs6nicmJrjnncr5ZXOdudx+EBY3LpmNI3HswtuO4lme+Z/Tj0urZ9OjPr5TxMbtWa11tfLz55buvSZZ5ZVudK3Df7jE1nas+2kdIqKgAADUZa4Vnqs5fJovBOFYTTSGgduh1Ljbjzvhjrd/dvObvyy31Or+phJefYjhle7LuvNEvi6X1sWVqRSR1wxk81HS3HL7eeWsupcvTHUy3ndfhO2z+Wsc7W+nj3XddUwx7cf5XkQ8Xnyx2y8eGrqTScC7jNx17ZXK6m6zjds2NTpQEbIqKrn0lMftS8JhfpVG0AFTjIMuAc8p9Sw35JyI307vL8O29Y15+nfrdcrrp5KOeM8N4TeTM4dMJqflr8RrZcpjjv259bLtx1PbjJde9Mq67lk1d7bvDjlda03Mt4gZTcc8dy10YvKLPVE2MujRSJtpzTK+KY8RMuFx4EaEBVTYCM8WpOYuXKewXDxm65/Zk54/8jpn5wv4UZnl2jlh5re1omWMzynxGM8Z68N7YyqDnZY3079DN8r07zEG2MmmclEggy1rdqaJUs3zVRMr5ajGtVoRrYAAAM58bZtaz8YsA3v6pXbmPPb4jtLqbUMfpxX1/KY7y81qgzaxWmQZpj4rVjNQbnn2XhnDVXLwozsBBfKm00CZc7anDOXnxpYC72bUAQPQM58Mrn6ZBr4dpw4/Dr6BrZUlSqHpD0gF4Zq00gY8Jol1S3YAzQGlt+EWf9iprX5TTUNCJ5i72nBNg0JtMqDNu6gArr6cvTpOAanJUi1RLwzFvCYg1U9FPSDOSbWsgAAoqcCrLpZds4/d5W/IjSaTabBbWbRAAUBufaw1+wG4VJSqJeDEpigtZWoAy1GbyAADSKiKk5XZORUTYqAIACgAv7ULwDeHCsY1oEpCkAqKArF5atZAFgKogAAAioIIAKioAsRYCluhKBurEX0AnlUBFEBqCAqgAACIFAQAFRUBQAUogEVFARUARUBQAf/Z" onload="var elem=this;setTimeout(function(){elem.onload = null;elem.src=elem.getAttribute('pagespeed_high_res_src');}, 0);"></a>
    <div class="caption">
    <h2><a title="Ver Episodio Vicious 1x06 - Episode 6" href="http://www.seriesid.tv/vicious-1x06/">Vicious 1x06 - Episode 6</a></h2>
    <a href="http://www.seriesid.tv/vicious-1x06/" class="btn btn-primary btn-block">Ver Episodio</a>
    </div>
    </div>
    '''
    patron  = '<div class="thumbnail"[^<]+<a href="([^"]+)"><img pagespeed[^=]+="([^"]+)" title="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot=""
        if DEBUG: logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , fulltitle=title , url=url , thumbnail=thumbnail , plot=plot , fanart="http://pelisalacarta.mimediacenter.info/fanart/seriesid.jpg") )

    return itemlist

def series(item):
    logger.info("[seriesid.py] series")
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<li class="active"><a>Series</a></li>(.*?)</ul')
    
    # Extrae las entradas
    patron  = '<li><a href="([^"]+)"[^<]+<i[^<]+</i>([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail=""
        plot=""
        if DEBUG: logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="episodios", title=title , fulltitle=title , url=url , thumbnail=thumbnail , plot=plot , fanart="http://pelisalacarta.mimediacenter.info/fanart/seriesid.jpg") )

    itemlist = sorted(itemlist, key=lambda item: item.title)

    return itemlist

def episodios(item):
    logger.info("[seriesid.py] episodios")
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    
    '''
    <div class="entry-content">
    <img class="entry-img" src="http://seriesid.com/wp-content/uploads/once-upon-a-time-temporada-2-dvdripvosesubtitulos-espanol-capitulo-51-166x250.jpg" alt="Once Upon a Time">
    <p>La serie se basa en la teoría de que existe un universo alterno donde todos los personajes de los clásicos cuentos de hadas existen -un mundo que tiene una conexión perdida con nuestro mundo- por lo que se centra en los personajes del Bosque Encantado y la conspiración de la Reina Malvada para perturbar la vida de los demás habitantes. Mediante una maldición la Bruja envía a los personajes de los cuentos al pueblo de Storybrooke, Maine, donde todos se encuentran sin saber quiénes son en realidad, siendo ella la única con un final feliz.</p>
    <h2>Cuarta Temporada</h2>
    <ul class="links_category"><li><a href="http://seriesid.com/once-upon-a-time-2x06/" title="Once Upon a Time 2x06 - Tallahassee">Once Upon a Time 2x06 - Tallahassee</a></li><li><a href="http://seriesid.com/once-upon-a-time-2x05/" title="Once Upon a Time 2x05 - The Doctor">Once Upon a Time 2x05 - The Doctor</a></li><li><a href="http://seriesid.com/once-upon-a-time-2x04/" title="Once Upon a Time 2x04 - The Crocodile">Once Upon a Time 2x04 - The Crocodile</a></li><li><a href="http://seriesid.com/once-upon-a-time-2x03/" title="Once Upon a Time 2x03 - Lady of the Lake">Once Upon a Time 2x03 - Lady of the Lake</a></li><li><a href="http://seriesid.com/once-upon-a-time-2x02/" title="Once Upon a Time 2x02 - We Are Both">Once Upon a Time 2x02 - We Are Both</a></li><li><a href="http://seriesid.com/once-upon-a-time-2x01/" title="Once Upon a Time 2x01 - Broken">Once Upon a Time 2x01 - Broken</a></li><li><a href="http://seriesid.com/once-upon-a-time-2x00/" title="Once Upon a Time 2x00 - Magic Is Coming">Once Upon a Time 2x00 - Magic Is Coming</a></li><li><a href="http://seriesid.com/once-upon-a-time-2x09/" title="Once Upon a Time 2x09 - Queen of Hearts">Once Upon a Time 2x09 - Queen of Hearts</a></li><li><a href="http://seriesid.com/once-upon-a-time-2x08/" title="Once Upon a Time 2x08 - Into the Deep">Once Upon a Time 2x08 - Into the Deep</a></li><li><a href="http://seriesid.com/once-upon-a-time-2x07/" title="Once Upon a Time 2x07 - Child of the Moon">Once Upon a Time 2x07 - Child of the Moon</a></li></ul>
    <div class="addth">
    <h3>Compartir</h3>
    '''
    # Extrae argumento y thumbnail
    scrapedplot = scrapertools.get_match(data,'<div class="entry-content"[^<]+<img.*?<p>(.*?)<h2>')
    scrapedthumbnail = scrapertools.get_match(data,'<div class="entry-content"[^<]+<img class="[^"]+" pagespeed[^=]+="([^"]+)"')
    
    data = scrapertools.get_match(data,'<ul class="links_category">(.*?)</ul>')
    
    # Extrae las entradas
    patron  = '<li><a href="([^"]+)" title="[^"]+">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail=scrapedthumbnail
        plot=scrapedplot
        if DEBUG: logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , fulltitle=title , url=url , thumbnail=thumbnail , plot=plot , viewmode="movie_with_plot" , fanart="http://pelisalacarta.mimediacenter.info/fanart/seriesid.jpg") )

    itemlist = sorted(itemlist, key=lambda item: item.title)

    return itemlist

def findvideos(item):
    logger.info("[seriesid.py] findvideos")
    itemlist = []

    data = scrapertools.cache_page(item.url)
    patron = '"(http://www.seriesid.tv/.*?player.php[^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedurl in matches:
        sitio = scrapertools.get_match(scrapedurl,"sitio\=([^\&]+)")
        title = "Ver en "+sitio
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail=""
        plot=""
        if DEBUG: logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="play", title=title , fulltitle=title , url=url , thumbnail=thumbnail , plot=plot , viewmode="movie_with_plot" , fanart="http://pelisalacarta.mimediacenter.info/fanart/seriesid.jpg", folder=False) )

    return itemlist

def play(item):
    logger.info("[seriesid.py] play")
    itemlist = []
    
    #http://seriesid.com/iframe-player.php?sitio=videobam&id=KIuBs
    #http://seriesid.com/player.php?sitio=videobam&id=KIuBs
    data = scrapertools.cache_page(item.url.replace("iframe-player","player"))
    logger.info("data="+data)
    
    itemlist = servertools.find_video_items(data=data)
        
    for videoitem in itemlist:
        videoitem.channel = __channel__
        
    try:
        url = scrapertools.get_match(data,"so.addVariable\('file','(http://peliculasid.net/plugins/rip-google.php[^']+)'")
        itemlist.append( Item(channel=__channel__, action="play", title=item.title , url=url , server="directo", folder=False) )
    except:
        pass

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguna de las series "En emisión" devuelve mirrors
    episodios_items = ultimos(mainlist_items[0])
    bien = False
    
    for episodio_item in episodios_items:
        mirrors = findvideos( item=episodio_item )
        if len(mirrors)>0:
            return True

    return False