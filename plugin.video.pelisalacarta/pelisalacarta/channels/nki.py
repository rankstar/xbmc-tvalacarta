# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para nki
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os,sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

CHANNELNAME = "nki"
DEBUG = True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[nki.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Buscar", action="search") )
    
    return itemlist

def search(item):
    logger.info("[nki.py] search")
    
    if config.get_platform()=="xbmc" or config.get_platform()=="xbmcdharma":
        from pelisalacarta import buscador
        texto = buscador.teclado()
        item.extra = texto

    itemlist = searchresults(item)
    
    return itemlist
    
def searchresults(item):
    logger.info("[nki.py] searchresults")
    
    tecleado = item.extra.replace(" ", "+")
    item.url = "http://www.nki.cl/pelisalacarta/?search="+tecleado+"&page=1&onsite=1&type=cuevana&x=47&y=12"

    return series(item)

def series(item):
    logger.info("[nki.py] series")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las entradas
    '''
    <?xml version="1.0" encoding="UTF-8"?>
    <main>
        <node id="188"><name>Star Wars: The Clone Wars</name><year>2008</year>
            <akas>
              <node id="0">Gwiezdne wojny: Wojny klonów</node>
              <node id="1">Star Wars - A klónok háborúja</node>
              <node id="2">Star Wars: The Clone Wars - Rise of the Bounty Hunters</node>
              <node id="3">Star Wars: The Clone Wars - The Animated Series</node>
              <node id="4">Untitled Clone Wars TV Series</node>
            </akas>
            <season_list>
                <node id="1">
                    <s01ep01><cap_name>Ambush</cap_name><cap_num>s01ep01</cap_num><cap_id>8141</cap_id><download_url>http://www.nki.cl/pelisalacarta/index.php?serie_link=8141</download_url></s01ep01>
                    <s01ep02><cap_name>Rising Malevolence</cap_name><cap_num>s01ep02</cap_num><cap_id>8142</cap_id><download_url>http://www.nki.cl/pelisalacarta/index.php?serie_link=8142</download_url></s01ep02>
                    ...
                </node>
            </season_list>
        </node>
    </main>
    '''
    patron = '<node[^>]+><name>([^<]+)</name><year>([^<]+)</year><akas'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[0] + " [" + match[1] + "]"
        scrapedplot = ""
        scrapedurl = item.url
        scrapedthumbnail = ""
        # Emplea esto para volver a sacar los episodios
        extra = "<name>"+match[0]+"</name><year>"+match[1]+"</year>"

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action="episodios", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra = extra , folder=True) )

    return itemlist

def episodios(item):
    logger.info("[nki.py] episodios")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae el bloque con los capítulos de la serie
    patron  = item.extra + '<akas.*?<season_list>(.*?)</season_list>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)==0:
        return itemlist

    data = matches[0]
    patron = "<cap_name>([^<]+)</cap_name><cap_num>([^<]+)</cap_num><cap_id>[^<]+</cap_id><download_url>([^<]+)</download_url>"
    matches = re.compile(patron,re.DOTALL).findall(data)

    for match in matches:
        scrapedtitle = match[1] + " - " + match[0]
        scrapedplot = ""
        scrapedurl = match[2]
        scrapedthumbnail = ""

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action="videos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def videos(item):
    logger.info("[nki.py] videos")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    logger.info(data)

    # Busca los enlaces a los videos
    listavideos = servertools.findvideos(data)

    itemlist = []
    for video in listavideos:
        scrapedtitle = item.title.strip() + " - " + video[0]
        scrapedurl = video[1]
        server = video[2]
        
        itemlist.append( Item(channel=item.channel, title=scrapedtitle , action="play" , server=server, page=item.page, url=scrapedurl, thumbnail=item.thumbnail, show=item.show , plot=item.plot , folder=False) )

    return itemlist
