# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para moviezet
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "moviezet"
__category__ = "F.S"
__type__ = "generic"
__title__ = "Moviezet"
__language__ = "ES"
__creationdate__ = "20111001"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[moviezet.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Películas"  , action="peliculas", url="http://www.moviezet.tv/movies/"))
    itemlist.append( Item(channel=__channel__, title="Series"     , action="series",    url="http://www.moviezet.tv/shows/?page_id=2853"))
    itemlist.append( Item(channel=__channel__, title="Buscar"   , action="search", url="http://www.moviezet.tv/?s="))
    
    return itemlist

def peliculas(item):
    logger.info("[moviezet.py] peliculas")
    itemlist = []
     
    itemlist.append( Item(channel=__channel__, title="Últimas películas"  , action="novedades", url="http://www.moviezet.tv/category/movies/?cat=1,-618&orderby=date&order=desc"))
    itemlist.append( Item(channel=__channel__, title="Más Populares"     , action="novedades",    url="http://www.moviezet.tv/category/movies/?cat=1,-618&orderby=meta_value_num&order=asc&meta_key=views"))
    itemlist.append( Item(channel=__channel__, title="Mejores Peliculas"     , action="novedades",    url="http://www.moviezet.tv/category/movies/?cat=1,-618&orderby=meta_value_num&order=asc&meta_key=views"))
    itemlist.append( Item(channel=__channel__, title="Generos"  , action="generos", url="http://www.moviezet.tv/category/movies/?cat=1,-618&orderby=meta_value&order=asc&meta_key=movie_genre"))
    itemlist.append( Item(channel=__channel__, title="Por Año"  , action="novedades", url="http://www.moviezet.tv/category/movies/?cat=1,-618&orderby=meta_value&order=asc&meta_key=movie_year"))
    itemlist.append( Item(channel=__channel__, title="Lista Completa"     , action="novedades",    url="http://www.moviezet.tv/category/movies/?cat=1,-618&orderby=title&order=asc"))

    return itemlist

def generos(item):
    logger.info("[moviezet.py] generos")
    itemlist = []
     
    itemlist.append( Item(channel=__channel__, title="Accion"  , action="novedades", url="http://www.moviezet.tv/movies/?cat=1&orderby=meta_value&order=asc&meta_key=movie_genre&meta_value=Acci%C3%B3n"))
    itemlist.append( Item(channel=__channel__, title="Animacion"  , action="novedades", url="http://www.moviezet.tv/movies/?cat=1&orderby=meta_value_num&order=asc&meta_key=views"))
    itemlist.append( Item(channel=__channel__, title="Aventura"  , action="novedades", url="http://www.moviezet.tv/movies/?cat=1&orderby=meta_value&order=desc&meta_key=movie_genre&meta_value=Aventura"))
    itemlist.append( Item(channel=__channel__, title="Belica"     , action="novedades",    url="http://www.moviezet.tv/movies/?cat=1&orderby=meta_value&order=asc&meta_key=movie_genre&meta_value=B%C3%A9lica"))
    itemlist.append( Item(channel=__channel__, title="Ciencia Ficcion"     , action="novedades",    url="http://www.moviezet.tv/movies/?cat=1&orderby=meta_value&order=desc&meta_key=movie_genre&meta_value=Ciencia%20Ficci%C3%B3n"))
    itemlist.append( Item(channel=__channel__, title="Comedia"     , action="novedades",    url="http://www.moviezet.tv/movies/?cat=1&orderby=meta_value&order=asc&meta_key=movie_genre&meta_value=Comedia"))
    itemlist.append( Item(channel=__channel__, title="Comedia Romantica"     , action="novedades",    url="http://www.moviezet.tv/movies/?cat=1&orderby=meta_value&order=desc&meta_key=movie_genre&meta_value=Comedia%20Rom%C3%A1ntica"))
    itemlist.append( Item(channel=__channel__, title="Crimen"     , action="novedades",    url="http://www.moviezet.tv/movies/?cat=1&orderby=meta_value&order=asc&meta_key=movie_genre&meta_value=Crimen"))
    itemlist.append( Item(channel=__channel__, title="Documental"     , action="novedades",    url="http://www.moviezet.tv/movies/?cat=1&orderby=meta_value&order=desc&meta_key=movie_genre&meta_value=Documental"))
    itemlist.append( Item(channel=__channel__, title="Drama"     , action="novedades",    url="http://www.moviezet.tv/movies/?cat=1&orderby=meta_value&order=asc&meta_key=movie_genre&meta_value=Drama"))
    itemlist.append( Item(channel=__channel__, title="Fantasia"     , action="novedades",    url="http://www.moviezet.tv/movies/?cat=1&orderby=meta_value&order=desc&meta_key=movie_genre&meta_value=Fantas%C3%ADa"))
    itemlist.append( Item(channel=__channel__, title="Musical"     , action="novedades",    url="http://www.moviezet.tv/movies/?cat=1&orderby=meta_value&order=desc&meta_key=movie_genre&meta_value=Musical"))
    itemlist.append( Item(channel=__channel__, title="Romance"     , action="novedades",    url="http://www.moviezet.tv/movies/?cat=1&orderby=meta_value&order=asc&meta_key=movie_genre&meta_value=Romance"))
    itemlist.append( Item(channel=__channel__, title="Suspense"     , action="novedades",    url="http://www.moviezet.tv/movies/?cat=1&orderby=meta_value&order=desc&meta_key=movie_genre&meta_value=Suspenso"))
    itemlist.append( Item(channel=__channel__, title="Terror"     , action="novedades",    url="http://www.moviezet.tv/movies/?cat=1&orderby=meta_value&order=asc&meta_key=movie_genre&meta_value=Terror"))
    itemlist.append( Item(channel=__channel__, title="Western"     , action="novedades",    url="http://www.moviezet.tv/movies/?cat=1&orderby=meta_value&order=desc&meta_key=movie_genre&meta_value=Western"))
    
    return itemlist

def novedades(item):
    if (DEBUG): logger.info("[moviezet.py] novedades")
    
    data = scrapertools.cache_page(item.url)
    #logger.info(data)
    # Extrae las entradas
    '''
    <td valign="top">

    <a href="http://www.moviezet.tv/movies/attack-the-block/" title="Ver Attack The Block Online"><img src="http://www.moviezet.tv/wp-content/uploads/attackblock.jpg" alt="Ver Attack The Block Online" /></a>
    '''
    patronvideos  = '<td valign="top">[^<]+<a href="(.*?)" title="(.*?)"[^<]<img src="(.*?)".*?</a>'    
    #patronvideos += "<td valign='top'><a href='([^']+)'>"
    #patronvideos += "<td valign='top'><div class='tit'><a[^>]+>([^<]+)</a></div>[^<]+"
    #patronvideos += "<div class='font11'>([^<]+)<"

    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1].replace("Ver ","").replace("Online","")
        scrapedplot = match[0]
        scrapedurl = match[0]
        scrapedthumbnail = match[2]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # AÃ±ade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    #<div class="pagination"><a href="http://www.moviezet.tv/movies/page/2/?cat=1&orderby=date&order=desc" class="next">
    patronvideos  = '<div class="pagination"><a href="(.*?)" class="next">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="novedades", title="Página siguiente" , url=scrapedurl , folder=True) )

    return itemlist

def series(item):
    logger.info("[moviezet.py] series")
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas
    #<li><a href="#" title="$#*! My Dad Says">$#*! My Dad Says</a></li>

    patron  = '<li><a href="\#" title="[^>]+>(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:
        scrapedtitle = match
        scrapedplot = ""
        code = match[0]
        scrapedurl = "http://www.moviezet.tv/category/shows/?page_id=2853&show="+(match.replace(" ","%20"))
        #scrapedurl = urllib.quote(scrapedurl)
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"] show="+scrapedtitle)

        itemlist.append( Item(channel=__channel__, action="episodios", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , show=scrapedtitle , folder=True, extra=scrapedtitle) )

    return itemlist

def temporadas(item):
    logger.info("[moviezet.py] temporadas")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    
    # Extrae las entradas
    #li><a href="#" title="1">Temporada 1</a></li>

    patron  = '<li><a href="#" title="[^>]+>(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:
        scrapedtitle = match
        temporada = scrapedtitle.replace("Temporada ","")
        scrapedtitle = match
        scrapedplot = ""
        scrapedurl = "http://www.moviezet.tv/shows/?page_id=2853&show="+(item.title.replace(" ","%20"))+"&season="+temporada
        scrapedthumbnail = item.thumbnail
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"], temporada=["+temporada+"] show="+item.show)

        itemlist.append( Item(channel=__channel__, action="episodios", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , show=item.show , folder=True, extra=item.extra + "|" + temporada) )

    return itemlist

def episodios(item):
    logger.info("[moviezet.py] episodios")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    
    # Extrae las temporadas

    temporadas_itemlist = temporadas(item)
    
    for temporada_item in temporadas_itemlist:
        id_temporada = temporada_item.extra.split("|")[1]
        data = scrapertools.cache_page(temporada_item.url)

        # Extrae las entradas
        #http://www.moviezet.tv/category/shows/?page_id=2853&show=Continuum&season=1&episode=1
        #<li><a href="#7685" title="1"><b>1.</b> Pilot</a></li>
        patron  = '<li><a href="(.*?)" title="(.*?)"><b>.*?</b>(.*?)</a></li>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)
        
        for match in matches:
            code = match[0]
            episodio = match[1]
            if len(episodio)==1:
                episodio = "0" + episodio
            scrapedtitle = temporada_item.title + "x" + episodio + " "+match[2].strip()
            scrapedplot = ""
            scrapedurl = "http://www.moviezet.tv/category/shows/?page_id=2853&show="+(item.show.replace(" ","%20"))+"&season="+id_temporada+"&episode="+match[1]
            scrapedthumbnail = item.thumbnail
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"] show="+item.show)
    
            itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , show = item.show , folder=True) )

    if config.get_platform().startswith("xbmc"):
        itemlist.append( Item(channel=item.channel, title="Añadir estos episodios a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show) )

    return itemlist

def findvideos(item):
    logger.info("[moviezet.py] findvideos")

    # True es Serie, False es Pelicula
    serieOpelicula = True
    code =""
    if (item.url.startswith("http://www.moviezet.tv/shows/")):
        data = scrapertools.cachePage(item.url)
        #<a class="watch-show" href="http://www.moviezet.tv/shows/dexter-pilot/">
        patron = '<a class="watch-show" href="(.*?)">'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if len(matches)>0:
            code = matches[0]
        logger.info("code="+code)
        url = matches[0]
        serieOpelicula = True
    else:
        # http://www.cuevana.tv/peliculas/2553/la-cienaga/
        logger.info("url1="+item.url)
        url = item.url
        serieOpelicula = False
    
    logger.info("url2="+url)
    data = scrapertools.cachePage(url)
    logger.info("data="+data)
    
    # Si es una serie tendrá ese enlace "watch-show"
    try:
        url = scrapertools.get_match(data,'<a class="watch-show" href="([^"]+)">')
        data = scrapertools.cachePage(url)
    # Si no lo tiene puede seguir tranquilamente
    except:
        pass
    logger.info("data="+data)

    patron = "&mubs=(.*?)&"
    matches = re.compile(patron,re.DOTALL).findall(data)
    code = matches[0]
    logger.info("code="+code)
    

    # Subtitulos
    #http://www.moviezet.tv/files/s/sub/18962_ES.srt
    #suburl = "http://www.moviezet.tv/files/s/sub/"+code
    suburl = "http://www.moviezet.tv/files/s/sub/"+code+"_ES.srt"
    logger.info("suburl="+suburl)
    
    # Elimina el archivo subtitulo.srt de alguna reproduccion anterior
    ficherosubtitulo = os.path.join( config.get_data_path(), 'subtitulo.srt' )
    if os.path.exists(ficherosubtitulo):
        try:
          os.remove(ficherosubtitulo)
        except IOError:
          logger.info("Error al eliminar el archivo subtitulo.srt "+ficherosubtitulo)
          raise

    listavideos = servertools.findvideos(data)
    
    itemlist = []
    
    for video in listavideos:
        server = video[2]
        scrapedtitle = item.title + " [" + server + "]"
        scrapedurl = video[1]
        
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot, server=server, subtitle=suburl, folder=False))

    return itemlist
  

# Al llamarse "search" la funciÃ³n, el launcher pide un texto a buscar y lo aÃ±ade como parÃ¡metro
def search(item,texto):
    logger.info("[moviezet.py] search")
    
    try:
        # La URL puede venir vacÃ­a, por ejemplo desde el buscador global
        if item.url=="":
            item.url="http://www.moviezet.tv/?s=Search.."
    
        # Reemplaza el texto en la cadena de bÃºsqueda
        item.url = item.url + texto
        
        

        # Devuelve los resultados
        return listar(item)
        
    # Se captura la excepciÃ³n, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []
    
def listar(item):
    logger.info("[moviezet.py] listar")
    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    logger.info(data)
    #<a href="http://www.moviezet.tv/movies/terminator-salvation/" title="Ver Terminator: La Salvación Online"><img src="http://moviezet.tv/wp-content/uploads/30.jpg" alt="Ver Terminator: La Salvación Online" /></a>
    patronvideos  = '<div class="movie-thumb">.*?<a href="(.*?)" title="(.*?)"[^<]<img src="(.*?)".*?</a>'


    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1].replace("Ver","").replace("Online","")
        scrapedplot = match[2]
        scrapedurl = match[0]
        scrapedthumbnail = match[2]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # AÃ±ade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    patronvideos  = "<a class='next' href='([^']+)' title='Siguiente'>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="listar", title="PÃ¡gina siguiente" , url=scrapedurl , folder=True) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    peliculas_items = peliculas(mainlist_items[0])
    novedades_items = novedades(peliculas_items[0])
    bien = False
    for pelicula_item in novedades_items:
        mirrors = findvideos( item=pelicula_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien