# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para dlmore
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "dlmore"
__category__ = "S"
__type__ = "generic"
__title__ = "DL-More (FR)"
__language__ = "FR"
__creationdate__ = "20111014"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[dlmore.py] mainlist")
    
    itemlist=[]
    itemlist.append( Item(channel=__channel__, title="TV Shows - Full listing"   , action="series" , url="http://www.dl-more.eu/series.html"))

    return itemlist

def series(item):
    logger.info("[dlmore.py] series")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    patron  = '<div class="entry" id="series">[^<]+'
    patron += '<div id="name">[^<]+'
    patron += '<a href="([^"]+)" onmouseover="([^"]+)"[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for match in matches:
        scrapedtitle = match[2]
        scrapedplot = scrapertools.htmlclean(match[1])
        
        #onmouseover="Tip('<div style=\'float:left;\'><img src=\'http://images.allocine.fr/r_160_214/b_1_cfd7e1/medias/nmedia/18/74/20/27/19243939.jpg\' height=\'210\' width=\'160\' /></div> <div style=\'padding-left:180px;padding-top:10px;\'><b>Hebergeur : </b> megaupload<br><b>Langue : </b> VF<br><b>Uploadeur : </b> Skater54<br /><b>Vues : </b> 114<br><b>Telechargements : </b> 36<br /><br /><b>Resumé : </b>Nouvelles au lyc&eacute;e Padua High, les soeurs Kat et Bianca Stratford ont des temp&eacute;raments oppos&eacute;s et des objectifs bien diff&eacute;rents. Si lun est une f&eacute;ministe et une battante d&eacute;termin&eacute;e &agrave; sauver le monde et quitter l&eacute;cole au plus vite, lautre pr&eacute;f&egrave;re soigner sa popularit&eacute; et profiter de ses ann&eacute;es de lyc&eacute;e.</div>', TITLE, 'Fiche de 10 Things I Hate About You')"
        patron = "<img src='([^']+)'"
        matches2 = re.compile(patron,re.DOTALL).findall(match[1].replace("\\",""))
        if len(matches2)>0:
            scrapedthumbnail = matches2[0]
        else:
            scrapedthumbnail = ""
    
        scrapedurl = urlparse.urljoin(item.url,match[0])
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="episodios", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def episodios(item):
    logger.info("[dlmore.py] episodios")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    patron  = '<a href="(\./ajax/fiche_serie.ajax.php\?id=[^"]+)" name="lien" class="[^"]+">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin("http://www.dl-more.eu/",match[0])

        # Read episode iframe
        # http://www.dl-more.eu/ajax/fiche_serie.ajax.php?id=203&saison=1
        # http://www.dl-more.eu/series/203/ajax/fiche_serie.ajax.php?id=203&saison=1
        data = scrapertools.cachePage(scrapedurl)
        
        # Search videos in iframe
        videoitems = servertools.find_video_items(data=data)
        
        # Assigns channel name and appends season to episode title
        for videoitem in videoitems:
            videoitem.channel=__channel__
            videoitem.title = scrapedtitle + videoitem.title
        
        # All episodes from all seasons in the same list
        itemlist.extend( videoitems )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # mainlist
    mainlist_items = mainlist(Item())
    
    # Da por bueno el canal si alguno de los vídeos de las series en "Destacados" devuelve mirrors
    series_items = series(mainlist_items[0])
    episodios_items = episodios(series_items[0])
    bien = False
    for episodio_item in episodios_items:
        mirrors = servertools.find_video_items(item=episodio_item)
        if len(mirrors)>0:
            bien = True
            break
    
    return bien