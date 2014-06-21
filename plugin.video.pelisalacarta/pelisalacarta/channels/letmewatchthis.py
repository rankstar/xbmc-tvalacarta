# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para letmewatchthis
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "letmewatchthis"
__category__ = "F,S"
__type__ = "generic"
__title__ = "LetMeWatchThis"
__language__ = "EN"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.letmewatchthis mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="showsectionsmovies" , title="Movies"   ,url="http://vodly.to/", extra="showlinks"))
    #itemlist.append( Item(channel=__channel__, action="alphabetical"    , title="Movies - Alphabetical Order" ,   url="http://vodly.to/", extra="1|showlinks"  ) )
    itemlist.append( Item(channel=__channel__, action="genre"    , title="Movies - Genre" ,   url="http://vodly.to/", extra="showlinks"  ) )
    itemlist.append( Item(channel=__channel__, action="search"    , title="Movies - Search"   ,extra="1") )
    itemlist.append( Item(channel=__channel__, action="showsectionstvshows"    , title="TV Shows" ,url="http://vodly.to/?tv", extra="tvshowepisodes"))
    #itemlist.append( Item(channel=__channel__, action="alphabetical"    , title="TV Shows - Alphabetical Order" ,   url="http://vodly.to/?tv", extra="2|tvshowepisodes"  ) )
    #itemlist.append( Item(channel=__channel__, action="genre"    , title="TV Shows - Genre" ,   url="http://vodly.to/?tv", extra="tvshowepisodes"  ) )
    itemlist.append( Item(channel=__channel__, action="search"    , title="TV Shows - Search"   ,extra="2"))
    
    return itemlist

def alphabetical(item):
    logger.info("pelisalacarta.letmewatchthis alphabetical")
    data = scrapertools.cache_page("http://vodly.to/index.php?search")
    iaction, iextra = item.extra.split('|')
    #List Movies By</td>
    #<td><a href="/?letter=123">#</a> <a href="/?letter=a">A</a> <a href="/?letter=b">B</a> <a href="/?letter=z">Z</a> |
    concat = "&sort=alphabet"
    if iaction == "2":
        concat = concat + '&tv'
        
    patron = 'List Movies By</td>(.*?)\|'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    if len(matches) == 1:
        #<a href="/?letter=123">#</a>
        patron = '<a href="([^"]+)">([^<]+)</a>'
        matches = re.compile(patron,re.DOTALL).findall(matches[0])  
        for match in matches:
            scrapedurl = urlparse.urljoin(item.url,match[0]) + concat
            scrapedtitle = match[1]
            itemlist.append( Item(channel=__channel__, action="doaction", title=scrapedtitle ,url=scrapedurl, extra=iextra))
    return itemlist

def genre(item):
    logger.info("pelisalacarta.letmewatchthis genre")
    data = scrapertools.cache_page(item.url)
    
    #<ul class="menu-genre-list"><li><a href="/?tv&genre=Action">Action</a></li><li><a href="/?tv&genre=Adventure">Adventure</a></li></ul>
    patron = '<ul class="menu-genre-list">(.*?)</ul>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    if len(matches) == 1:
        #<li><a href="/?tv&genre=Action">Action</a></li>
        patron = '<li><a href="([^"]+)">([^<]+)</a></li>'
        matches = re.compile(patron,re.DOTALL).findall(matches[0])  
        for match in matches:
            scrapedurl = urlparse.urljoin(item.url,match[0])
            scrapedtitle = match[1]
            itemlist.append( Item(channel=__channel__, action="doaction", title=scrapedtitle ,url=scrapedurl, extra=item.extra))
    return itemlist

    
def search(item,texto, categoria="*"):
    logger.info("pelisalacarta.letmewatchthis search")

    url = 'http://vodly.to/index.php'   
    
    if item.extra == "1":
        #Movies 
        key = getkey("http://vodly.to/")
        post = "search_keywords=%s&key=%s&search_section=%s" % ( texto, key, "1")
        item.url = url + "?" + post
        item.extra = "showlinks"
        return doaction(item)    
    
    if item.extra == "2":
        #TV Shows 
        key = getkey("http://vodly.to/?tv")
        post = "search_keywords=%s&key=%s&search_section=%s" % ( texto, key, "2")
        item.url = url + "?" + post
        item.extra = "tvshowepisodes"
        return doaction(item)  
      
    return []   


def getkey(url):
    
    # Descarga la página
    data = scrapertools.cachePage(url)
    #logger.info(data)
    '''
      <fieldset class="search_container">
        <input type="text" id="search_term" name="search_keywords"  class="box" value="Search Title" onFocus="clearText(this)" onBlur="clearText(this)">
        <input type="hidden" name="key" value="aa68c1afe6a4d965" />
        <input type="hidden" value="2" name="search_section">
        <button class="btn" title="Submit Search" type="submit"></button>
        <span class="search_advanced_link" ><a href="http://vodly.to/index.php?search">Advanced Search</a></span>
      </fieldset>
    '''

    patronvideos  = '<fieldset class="search_container">.*?</fieldset>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches) == 1:
        patronvideos  = 'name="key".*?"([^"]+)"'    
        matches = re.compile(patronvideos,re.DOTALL).findall(matches[0])
    
    if len (matches) == 1:
        return matches[0]
    
    return ""

def showsectionsmovies(item):
    return showsections(item, item.url + "?")
def showsectionstvshows(item):
    return showsections(item, item.url + "&")

def showsections(item, url):
    logger.info("pelisalacarta.letmewatchthis showsections")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="doaction"    , title=item.title + " - Featured"      ,url=url+"sort=featured", extra=item.extra  ) )
    itemlist.append( Item(channel=__channel__, action="doaction"    , title=item.title + " - Release Date"  ,url=url+"sort=release", extra=item.extra  ) )
    itemlist.append( Item(channel=__channel__, action="doaction"    , title=item.title + " - Top Rated"     ,url=url+"sort=ratings"   , extra=item.extra  ) )
    itemlist.append( Item(channel=__channel__, action="doaction"    , title=item.title + " - Popular"       ,url=url+"sort=views"     , extra=item.extra  ) )
    itemlist.append( Item(channel=__channel__, action="doaction"    , title=item.title + " - Favorites"     ,url=url+"sort=favorites" , extra=item.extra  ) )
    itemlist.append( Item(channel=__channel__, action="doaction"    , title=item.title + " - Just Added"    ,url=url+"sort=date"      , extra=item.extra  ) )
    itemlist.append( Item(channel=__channel__, action="doaction"    , title=item.title + " - A to Z"      ,url=url+"sort=alphabet", extra=item.extra  ) )
    
    return itemlist

def doaction(item):
    logger.info("pelisalacarta.letmewatchthis doaction")
    
    
    data = scrapertools.cache_page(item.url)
    
    #<div class="index_item index_item_ie"><a href="/watch-2700449-Accused" title="Watch Accused (2010)"><img src="http://images.1channel.ch/thumbs/2700449_Accused_2010.jpg" border="0" width="150" height="225" alt="Watch Accused"><h2>Accused (2010)</h2></a><div
    patron = '<div class="index_item.*?<div'
    matches = re.compile(patron,re.DOTALL).findall(data)
        
    itemlist = []
    for match in matches:
        patron  = 'href="([^"]+)".*?src="([^"]+)".*?<h2>([^<]+)<'
        matches2 = re.compile(patron,re.DOTALL).findall(match)
        if len(matches2)==1:
            match2 = matches2[0]
            # Titulo
            scrapedtitle = scrapertools.htmlclean(match2[2])
            scrapedplot = ""
            scrapedurl = urlparse.urljoin(item.url,match2[0])
            scrapedthumbnail = match2[1]
            # Añade al listado de XBMC
            itemlist.append( Item(channel=__channel__, action=item.extra, title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, extra=scrapedtitle , plot=scrapedplot , viewmode="movie", folder=True) )


    patronvideos  = '<div class="pagination">.*?</div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    if len(matches)>0:
        patronvideos = '<span class="current">[^<]+</span>[^h]+href="([^"]+)">'        
        matches = re.compile(patronvideos,re.DOTALL).findall(matches[0])
        if len(matches)>0:
            scrapedurl = urlparse.urljoin(item.url,matches[0])
            itemlist.append( Item(channel=__channel__, action="doaction", title="!Next page >>" , url=scrapedurl , folder=True, extra= item.extra) )
    
    return itemlist

def tvshowepisodes(item):
    logger.info("pelisalacarta.letmewatchthis tvshowepisodes")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    
    #<h2><a href="http://vodly.to/tv-10395-The-Listener/season-4" title="Watch The Listener Season 4">Season 4</a></h2>
    patron = '<h2><a href="([^"]+)"[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)<=1:
        return season(item, data,"Season 1")

    for match in matches:
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedtitle = match[1]
        itemlist.append( Item(channel=__channel__, action="fillseason", title=scrapedtitle ,url=scrapedurl, extra=item.title))

    return itemlist

def fillseason(item): 
    logger.info("pelisalacarta.letmewatchthis fillseason")
    data = scrapertools.cachePage(item.url)    
    return season(item, data, item.title)
        
def season(item, data, season):    
    logger.info("pelisalacarta.letmewatchthis season("+season+")")
    itemlist = []  
    seasonnumber = season
    patron = '([0-9]+)'
    matches = re.compile(patron,re.DOTALL).findall(season)
    if len(matches)==1:
        seasonnumber = matches[0]
    #<div class="tv_episode_item"> <a href="/tv-2700449-Accused/season-1-episode-3">Episode 3
    #<span class="tv_episode_name"> - Helen's Story</span>        </a> </div>  
    #<div class="tv_episode_item"> <a href="/tv-13098-The-Game/season-5-episode-4">Episode 4                              </a> </div>
    '''
    <div class="tv_episode_item">
    <a href="http://vodly.to/tv-10395-The-Listener/season-4-episode-10" title="Watch The Listener Season 4 Episode 10 - The Long Con">Episode 10
    <span class="tv_episode_name"> - The Long Con</span>
    </a>
    </div>
    '''
    patron = '<div class="tv_episode_item">(.*?)</div>'
    matches2 = re.compile(patron,re.DOTALL).findall(data)
    for match2 in matches2: 
        #There are chapters without "TITLE"
        patron = '<a href="([^"]+)"[^>]*>([^<]+)<'
        matches3 = re.compile(patron,re.DOTALL).findall(match2)
        patron = '<span class="tv_episode_name">([^<]+)</span>'
        matches4 = re.compile(patron,re.DOTALL).findall(match2)
        if len(matches3) ==1:
            title = ""
            if len(matches4)==1:
                title = scrapertools.htmlclean(matches4[0])           
            
            chapternumber= matches3[0][1].strip()  
            patron = '([0-9]+)'
            matches = re.compile(patron,re.DOTALL).findall(chapternumber)
            if len(matches)==1:
                chapternumber =  "%02d" % (int(matches[0]))    
                        
            scrapedtitle = seasonnumber + "x" + chapternumber + title
            scrapedextra = seasonnumber + "x" + chapternumber + " " +item.extra
            scrapedthumbnail = item.thumbnail
            scrapedurl = urlparse.urljoin(item.url,matches3[0][0])
            scrapedplot = ""
            itemlist.append( Item(channel=__channel__, action="showlinks", title=scrapedtitle , url=scrapedurl , extra= scrapedextra, thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
             
        
    return itemlist        
        
def showlinks(item):
    logger.info("pelisalacarta.letmewatchthis showlinks")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)
    '''
    <a href="/external0" onClick="return  addHit('1889692257', '1')" rel="nofollow" title="Watch Version 3 of Accused" target="_blank">Version 3</a>
    </span></td>
    <td align="center" width="115" valign="middle"><span class="version_host"><script type="text/javascript">document.writeln('veehd.com');</script></span>
    '''
    
    patronvideos  = 'movie_version_link">.*?<a href="(/external[^"]+)".*?title="[^>]+>([^<]+)</a>.*?'
    patronvideos += '<span class="version_host">[^\']+\'([^\']+)\''

    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        # Servidor
        servidor = match[2].strip()
        # Titulo
        scrapedtitle = item.extra + " [" + servidor + "]"#  " + scrapertools.htmlclean(match[1])
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = item.thumbnail
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, extra="", category=item.category, fanart=item.thumbnail, folder=False))

          
    return itemlist

def play(item):
    logger.info("pelisalacarta.letmewatchthis play")
    
    location = scrapertools.get_header_from_response(item.url.replace(" ","%20"),header_to_get="location")
    logger.info("pelisalacarta.letmewatchthis location="+location)
    
    if location!="":
        itemlist = servertools.find_video_items(data=location)
    else:
        item.url = item.url.replace(" ","%20")
        itemlist = servertools.find_video_items(item) 
        if len(itemlist) == 0:  
            try:
                count = 0
                exit = False
                while(not exit and count < 5):
                    #A veces da error al intentar acceder
                    try:
                        page = urllib2.urlopen(item.url)
                        urlvideo = page.geturl() 
                        exit = True
                    except:
                        count = count + 1
                if(exit):
                        listavideos = servertools.findvideos(urlvideo)
                        for video in listavideos:
                            scrapedtitle = item.title.strip() + " - " + video[0].strip()
                            scrapedurl = video[1]
                            server = video[2]
                            
                            itemlist.append( Item(channel=item.channel, title=scrapedtitle , action="play" , server=server, page=item.page, url=scrapedurl, thumbnail=item.thumbnail, show=item.show , plot=item.plot , folder=False) )
    
            except:  
                import sys
                for line in sys.exc_info():
                    logger.error( "%s" % line ) 
                     
        for videoitem in itemlist:
            try:
                videoitem.title = scrapertools.get_match(item.title,"Watch Version \d+ of (.*)\(")
            except:
                videoitem.title = item.title
        
    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    peliculas_items = doaction(mainlist_items[0])
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = showlinks( item=pelicula_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien
