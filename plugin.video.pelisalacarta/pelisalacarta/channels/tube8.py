# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para tube8
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import time
from datetime import date, datetime
from servers import servertools
#from platform.xbmc import xbmctools
from core import config
from core.item import Item
from core import logger
#from pelisalacarta import buscador

from core import scrapertools

__channel__ = "tube8"
__category__ = "F"
__type__ = "generic"
__title__ = "Tube 8"
__language__ = "EN"
__working__ = "true"
__adult__ = "true"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[tube8.py] mainlist")
    
    itemlist = []
    itemlist.append( Item( channel=__channel__ , title="Destacados" , action="getList" , url="http://www.tube8.com/latest.html" , folder=True ) )
    itemlist.append( Item( channel=__channel__ , title="Categorias" , action="getCategory" , url="http://www.tube8.com/categories.html" , folder=True ) )
    itemlist.append( Item( channel=__channel__ , title="Videos Recientes" , action="getList" , url="http://www.tube8.com/newest.html" , folder=True ) )
    itemlist.append( Item(channel=__channel__, action="search"    , title="Buscar", url="http://www.tube8.com/search.html?q="))
    
    return itemlist

def getList(item):
    logger.info("[tube8.py] novedades")
    url = item.url
    # ------------------------------------------------------
    # Descarga la página
    # ------------------------------------------------------
    data = scrapertools.cachePage(url)
    #logger.info(data)
    
    # ------------------------------------------------------
    # Extrae las entradas
    # ------------------------------------------------------
    '''
			<div id="video_i1820621">
				<a href="http://www.tube8.com/latina/brazilian-facials-talita/1820621/"><img width="190" height="143" class="videoThumbs" id="i1820621" category="e" thumb_src="http://cdn1.image.tube8.phncdn.com/1110/17/4e9cc6b7bde22/190x143/" src="http://cdn1.image.tube8.phncdn.com/1110/17/4e9cc6b7bde22/190x143/14.jpg" alt="Brazilian Facials  Talita" /></a>
				<h2><a href="http://www.tube8.com/latina/brazilian-facials-talita/1820621/" title="Brazilian Facials  Talita">Brazilian Facials  Talita</a></h2>

				<div class="video-cont-wrapper">
					<div class="video-left-text">							
						<div class="float-left" style="padding:2px 0 0 0; color:green;">96%</div>
						<div class="float-left main-sprite-img thumb up"></div>
					</div>
					<div class="video-right-text float-right"><strong>35:43</strong></div>
				</div>
			</div>
    '''
    patronvideos  = '<div id="video_.*?">.*?<a href="([^"]+)"><img.*? src="([^"]+)".*?<a.*?title="([^"]+)"'
    
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    
    itemlist = []
    for match in matches:
        itemlist.append( Item(channel=__channel__, action="getVideo", title=match[2], url=match[0] , thumbnail=match[1] , folder=True) )

    return itemlist

def getVideo(item):
    logger.info("[tube8.py] getVideo")
    # ------------------------------------------------------
    # Descarga la página
    # ------------------------------------------------------
 
    matches = re.compile('(\d+)/').findall(item.url)
    if DEBUG: scrapertools.printMatches(matches)
    idvideo= matches[0]

    data = scrapertools.cachePage(item.url)
    matches = re.compile('var hash = "([a-z0-9]+)"').findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    hash= matches[0]

    url = "http://www.tube8.com/ajax/getVideoDownloadURL.php?_=" + str(int(time.time()*1000)) + "&hash=" + hash + "&video=" + idvideo
    logger.debug("[tube8.py] url " + url)

    MAIN_HEADERS = []
    MAIN_HEADERS.append(["Host","www.tube8.com"] )
    MAIN_HEADERS.append(['User-Agent', 'Mozilla/5.0 (Windows NT 5.1; rv:8.0) Gecko/20100101 Firefox/8.0'])
    MAIN_HEADERS.append(['Connection', 'keep-alive'])
    MAIN_HEADERS.append(['Referer', item.url])
    MAIN_HEADERS.append(['X-Requested-With', 'XMLHttpRequest'])
    MAIN_HEADERS.append(['Accept','*/*'])
    MAIN_HEADERS.append(['Accept-Language', 'es-es,es;q=0.8,en-us;q=0.5,en;q=0.3'])
    MAIN_HEADERS.append(['Content-Type', 'application/x-www-form-urlencoded'])

    data = scrapertools.cache_page(url,headers=MAIN_HEADERS)
    logger.debug("[tube8.py] data " + data)

    matches = re.compile('"standard_url":"(http.*?)"').findall(data)
    if not matches:
        matches = re.compile('"(http://cdn\d+\.public\.tube8\.com/.*?)"').findall(data)

	logger.debug("[tube8.py] URL  " + matches[0].replace("\\",""))
    
    itemlist = []
    item.action="play"
    item.server="Directo"
    item.Folder=False   
    item.url=matches[0].replace("\\","")
    # Añade al listado de XBMC
    itemlist.append(item)

    return itemlist

def getCategory(item):
    logger.info("[tube8.py] getCategory")
    url = item.url
    # ------------------------------------------------------
    # Descarga la página
    # ------------------------------------------------------
    data = scrapertools.cachePage(url)
    #logger.info(data)
    
    # ------------------------------------------------------
    # Extrae las entradas
    # ------------------------------------------------------
    '''
	<div class="menu-category-wrapper" style="text-align: left;">
		<h1 class="main-title main-sprite-img">Categories</h1>
		<div class="box-flex box-cat-wrapper-left">
		<div class="box-flex box-cat-wrapper-right"><ul class="categories-menu"><li class="first-link"><a href="http://www.tube8.com/cat/amateur/6/" onclick="pageTracker._trackEvent('Header', 'ChosenSort category Amateur in straight');">Amateur</a></li>
			<li><a href="http://www.tube8.com/cat/anal/13/" onclick="pageTracker._trackEvent('Header', 'ChosenSort category Anal in straight');">Anal</a></li>
			<li><a href="http://www.tube8.com/cat/asian/12/" onclick="pageTracker._trackEvent('Header', 'ChosenSort category Asian in straight');">Asian</a></li>
			<li><a href="http://www.tube8.com/cat/blowjob/7/" onclick="pageTracker._trackEvent('Header', 'ChosenSort category Blowjob in straight');">Blowjob</a></li>

			<li><a href="http://www.tube8.com/cat/ebony/4/" onclick="pageTracker._trackEvent('Header', 'ChosenSort category Ebony in straight');">Ebony</a></li>
			<li><a href="http://www.tube8.com/cat/erotic/11/" onclick="pageTracker._trackEvent('Header', 'ChosenSort category Erotic in straight');">Erotic</a></li>
			<li><a href="http://www.tube8.com/cat/fetish/5/" onclick="pageTracker._trackEvent('Header', 'ChosenSort category Fetish in straight');">Fetish</a></li>
			<li><a href="http://www.tube8.com/cat/hardcore/1/" onclick="pageTracker._trackEvent('Header', 'ChosenSort category Hardcore in straight');">Hardcore</a></li>
			<li><a href="http://www.tube8.com/cat/latina/14/" onclick="pageTracker._trackEvent('Header', 'ChosenSort category Latina in straight');">Latina</a></li>
			<li><a href="http://www.tube8.com/cat/lesbian/8/" onclick="pageTracker._trackEvent('Header', 'ChosenSort category Lesbian in straight');">Lesbian</a></li>
			<li><a href="http://www.tube8.com/cat/mature/2/" onclick="pageTracker._trackEvent('Header', 'ChosenSort category Mature in straight');">Mature</a></li>
			<li><a href="http://www.tube8.com/cat/strip/10/" onclick="pageTracker._trackEvent('Header', 'ChosenSort category Strip in straight');">Strip</a></li>
			<li><a href="http://www.tube8.com/cat/teen/3/" onclick="pageTracker._trackEvent('Header', 'ChosenSort category Teen in straight');">Teen</a></li>

			<li><a href="http://www.tube8.com/gay/" onclick="pageTracker._trackEvent('Header', 'ChosenSort gay in straight ');segmentCookie(1);">Gay</a></li><li><a href="http://www.tube8.com/shemale/" onclick="pageTracker._trackEvent('Header', 'ChosenSort shemale in straight ');segmentCookie(2);">Shemale</a></li><li><a href="http://enter.t8premium.com/track/MTI2NDU6MjU6MzQ/" rel="nofollow">HD</a></li></ul></div>
		</div>
	</div>
    '''
    patron = '<ul class="categories-menu">(.*?)</ul>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    data=matches[0]
    if DEBUG: scrapertools.printMatches(matches)
    patron = '<a href=[\'"](.*?)[\'"].*?>(.*?)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    
    itemlist = []
    for match in matches:
        itemlist.append( Item( channel=__channel__ , title=match[1] , action="getList" , url=match[0] , folder=True ) )

    return itemlist

def search(item,texto, categoria="*"):
    logger.info("[tube8.py] search")
    item.url=item.url+texto
    itemlist = getList(item)

    return itemlist

