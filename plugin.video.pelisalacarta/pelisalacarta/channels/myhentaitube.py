# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para myhentaitube
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
from servers import servertools
from core import config
from core.item import Item
from core import logger
from core import scrapertools

CHANNELNAME = "myhentaitube"
DEBUG = True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[myhentaitube.py] mainlist")
    itemlist = []
    itemlist.append( Item( channel=CHANNELNAME , title="Novedades" , action="novedades" , url="http://myhentaitube.com/" , folder=True ) )
    return itemlist

def novedades(item):
    logger.info("[myhentaitube.py] novedades")

    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las entradas
    # seccion novedades
    '''
        <a href="/index.php?option=com_content&amp;view=article&amp;id=29:ai-shimai-hentai-movie-anime-&amp;catid=1:movies&amp;Itemid=2">
        <img src="/images/stories/ai_shimai_dvd copy.gif" border="0" />
        </a>
    '''

    #patronvideos  = '<p style="text-align: center;">.*?'
    patronvideos = '<a href="(/index.php[^"]+view=article[^"]+id=[^:]([^"]+)catid=1+[^"]+)">[^<]*?'
    patronvideos += '<img src="([^"]+)".*?</a>'

    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        # Titulo
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = urlparse.urljoin(item.url,match[2]).replace(" ", "%20")
        scrapedplot = scrapertools.htmlclean(match[1].strip())
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action="capitulos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    patronvideos  = '<a href="(\/index.php\?pageNum[^"]+)">[^<]+</a></span>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=CHANNELNAME, action="novedades", title="!Página siguiente" , url=scrapedurl , folder=True) )

    return itemlist

def capitulos(item):
    logger.info("[myhentaitube.py] capitulos")
   
    title = urllib.unquote_plus( item.title )
    thumbnail = urllib.unquote_plus( item.thumbnail )
    plot = urllib.unquote_plus( item.plot )

    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    #logger.info(data)
   
    # Busca el argumento
    patronvideos  = '<div class="ficha_des">(.*?)</div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        plot = scrapertools.htmlclean(matches[0])
        logger.info("plot actualizado en detalle");
    else:
        logger.info("plot no actualizado en detalle");
   
    # Busca los enlaces a los mirrors, o a los capitulos de las series...
    '''
    <h3 style="text-align: center;">
    <a href="/index.php?option=com_content&amp;view=article&amp;id=8&amp;Itemid=2">CAPITULO 1
    </a></h3>
    '''
    patronvideos = '<a href="(/index.php[^"]+view=article[^"]+id=[^"]+)">([^<]+)<'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
   
    itemlist = listURL(matches,item.url)
    #~ for match in matches:
        #~ # Titulo
        #~ scrapedtitle = match[1]
        #~ scrapedurl = urlparse.urljoin(item.url,match[0])
        #~ scrapedthumbnail = thumbnail
        #~ scrapedplot = plot
        #~
        #~ if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
#~
        #~ # Añade al listado de XBMC
        #~ itemlist.append( Item(channel=CHANNELNAME, action="play", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=False) )

    return itemlist

def listURL(matches, url):
   logger.info("[myhentaitube.py] detail")
   
   itemlist=[]
   for match in matches:
      # Titulo
      scrapedtitle = match[1]
      scrapedurl = urlparse.urljoin(url,match[0])
   
      # Descarga la pagina
      data = scrapertools.cachePage(scrapedurl)             
      patron = "QT_WriteOBJECT_XHTML\('([^']+)'"
      matchesVideos = re.compile(patron,re.DOTALL).findall(data)
      if len(matchesVideos)>0:
         scrapedurl = matchesVideos[0]
         server="Directo"
      # Añade al listado de XBMC
      itemlist.append( Item(channel=CHANNELNAME, action="play", title=scrapedtitle , url=scrapedurl , server=server,  folder=False) )
      
   return itemlist
   
