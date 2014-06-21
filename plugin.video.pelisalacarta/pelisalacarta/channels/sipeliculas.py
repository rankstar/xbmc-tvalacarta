# -*- coding: utf-8 -*-
#------------------------------------------------------------
# sipeliculas.com - XBMC Plugin
# Canal para sipeliculas.com by juso
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys
import base64

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "sipeliculas"
__category__ = "F"
__type__ = "generic"
__title__ = "Si peliculas"
__language__ = "ES"
__creationdate__ = "20120301"

DEBUG = config.get_setting("debug")
    
def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.sipeliculas mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Últimas películas" , action="peliculas", url="http://www.sipeliculas.com/cartelera"))
    itemlist.append( Item(channel=__channel__, title="Listado por géneros" , action="generos", url="http://www.sipeliculas.com/"))
    itemlist.append( Item(channel=__channel__, title="Listado alfabético" , action="letras", url="http://www.sipeliculas.com/"))
    itemlist.append( Item(channel=__channel__, title="Buscar..." , action="search", url=""))
 
    return itemlist

def search(item,texto):
    logger.info("pelisalacarta.sipeliculas search")
    itemlist = []

    texto = scrapertools.slugify(texto)
    item.url="http://www.sipeliculas.com/ver/"+texto    
    item.extra = ""
    itemlist.extend(lista1(item))
    
    return itemlist

def letras(item):
    logger.info("pelisalacarta.sipeliculas letras")

    itemlist=[]
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<ul class="abc">(.*?)</ul>')

    patron='<a href="([^"]+)">(.*?)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        scrapedurl=match[0]
        scrapedtitle=match[1]
        itemlist.append( Item(channel=__channel__, title=scrapedtitle , action="peliculas", url=scrapedurl)) 
    return itemlist

def generos(item):
    logger.info("pelisalacarta.sipeliculas generos")

    itemlist=[]
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<ul class="ge">(.*?)<div')

    patron='<a href="([^"]+)"[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        scrapedurl=match[0]
        scrapedtitle=unicode( match[1], "iso-8859-1" , errors="replace" ).encode("utf-8")
        itemlist.append( Item(channel=__channel__, title=scrapedtitle , action="peliculas", url=scrapedurl)) 
    return itemlist

def peliculas(item):
    logger.info("pelisalacarta.sipeliculas peliculas")

    itemlist=[]
    data = scrapertools.cachePage(item.url)   
    data = scrapertools.get_match(data,'<div id="iz">(.*?)</div[^<]+</div')
    '''
    <li>
    <a href="http://www.sipeliculas.com/detention-of-the-dead" title="Detention of the Dead (2013)"><i></i>
    <div class="img"><img src="http://img.sipeliculas.com/IMG.Mediano/detention-of-the-dead-52055048c6dcc.jpg" alt="Detention of the Dead (2013)" title="Detention of the Dead (2013)"/></div>
    <p>Detention of the Dead</p></a>
    <span>Ver Trailer</span>
    </li>
    ''' 
    patron  = '<li[^<]+'
    patron += '<a href="([^"]+)" title="([^"]+)"><i></i[^<]+'
    patron += '<div class="img"><img src="([^"]+)"'

    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        title = unicode( scrapedtitle , "iso-8859-1" , errors="replace" ).encode("utf-8")
        itemlist.append( Item(channel=__channel__, title=title , action="findvideos", url=scrapedurl, thumbnail=scrapedthumbnail))

    '''
    <div class="paginacion">
    <span>1</span><a href="http://www.sipeliculas.com/online/animacion/2/">2</a><a href="http://www.sipeliculas.com/online/animacion/3/">3</a><a href="http://www.sipeliculas.com/online/animacion/4/">4</a><a href="http://www.sipeliculas.com/online/animacion/5/">5</a><a href="http://www.sipeliculas.com/online/animacion/6/">6</a><a href="http://www.sipeliculas.com/online/animacion/2/">Siguiente &#187;</a><a href="http://www.sipeliculas.com/online/animacion/10/">Ultimo &#187;</a></div>
    '''
    try:
        data = scrapertools.get_match(data,'<div class="paginacion"(.*?)$')

        try:
            next_page_url = scrapertools.get_match(data,'<li><a href="([^"]+)" alt="Siguiente pagina"')
            itemlist.append( Item(channel=__channel__, title=">> Pagina Siguiente" , action="peliculas", url=next_page_url))
        except:
            next_page_url = scrapertools.get_match(data,'<a href="([^"]+)">Siguiente')
            itemlist.append( Item(channel=__channel__, title=">> Pagina Siguiente" , action="peliculas", url=next_page_url))

    except:
        pass

    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.sipeliculas findvideos")

    itemlist=[]
    data = scrapertools.cachePage(item.url)

    '''
    <ul class="pver">
    <li class="ver"><span class="opci">Opciones</span><span>Servidor</span><span>Idioma</span><span>Formato</span></li>
    <li class=""><a href="http://www.sipeliculas.com/turbo/24050"><span class="op">Opción 1</span><span>vimple</span><span>Latino</span><span>dvd rip</span></a></li>
    <li class=""><a href="http://www.sipeliculas.com/turbo/23458"><span class="op">Opción 2</span><span>vimple</span><span>Latino</span><span>dvd rip</span></a></li>
    <li class=""><a href="http://www.sipeliculas.com/turbo/23457"><span class="op">Opción 3</span><span>nowvideo</span><span>Latino</span><span>ts screener hq</span></a></li>
    </ul>
    '''
    patron = '<ul class="pver(.*?)</ul'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for bloque in matches:

        patron2 = '<li[^<]+<a href="([^"]+)"><span[^>]+>([^<]+)</span><span>([^<]+)</span><span>([^<]+)</span><span>([^<]+)</span>'
        matches2 = re.compile(patron2,re.DOTALL).findall(bloque)

        for scrapedurl,scrapedtitle,scrapedserver,idioma,calidad in matches2:
            title = "Ver en "+scrapedserver+" ["+idioma+"]["+calidad.upper()+"]"
            url = scrapedurl
            itemlist.append( Item(channel=__channel__, title=title , action="play", url=url, folder=False))

    return itemlist

def play(item):
    logger.info("pelisalacarta.sipeliculas play")

    itemlist=[]

    # Si es una url de la web, la descarga para buscar el enlace
    if item.url.startswith("http://www.sipeliculas"):
        data = scrapertools.cachePage(item.url)
        data = scrapertools.get_match(data,'<p class="p">(.*?)<h2 class="s">')

    # Si no es de la web, es el enlace directamente
    else:
        data = item.url

    itemlist = servertools.find_video_items(data=data)
    i=1
    for videoitem in itemlist:
        videoitem.title = "Mirror %d%s" % (i,videoitem.title)
        videoitem.fulltitle = item.fulltitle
        videoitem.channel=channel=__channel__
        i=i+1


    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    
    # Busca alguna película disponible entre las 10 primeras
    mainlist_items = mainlist(Item())
    peliculas_items = peliculas(mainlist_items[0])
    bien = False

    for i in range(0,10):
        mirrors_items = findvideos(peliculas_items[i])
        for mirror_item in mirrors_items:
            video_items = play(mirror_item)
            if len(video_items)>0:
                print "Encontrado mirror en "+video_items[0].server+" para "+peliculas_items[i].title
                return True

    return bien