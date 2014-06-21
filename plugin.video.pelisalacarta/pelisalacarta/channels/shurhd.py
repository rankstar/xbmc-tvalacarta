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

__channel__ = "shurhd"
__category__ = "F"
__type__ = "generic"
__title__ = "Shurhd"
__language__ = "ES"

DEBUG = config.get_setting("debug")
SESION = config.get_setting("session","shurhd")
LOGIN = config.get_setting("login","shurhd")
PASSWORD = config.get_setting("password","shurhd")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[shurweb.py] getmainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novedades"                , action="peliculas"    , url="http://www.shurhd.com/"))
    itemlist.append( Item(channel=__channel__, title="Películas"                , action="menupeliculas"))
    itemlist.append( Item(channel=__channel__, title="Series"                   , action="series"      , url="http://series.shurhd.com/"))
#    itemlist.append( Item(channel=__channel__, title="Buscar"                   , action="search") )
    '''
    if SESION=="true":
        perform_login(LOGIN,PASSWORD)
        itemlist.append( Item(channel=__channel__, title="Cerrar sesion ("+LOGIN+")", action="logout"))
    else:
        itemlist.append( Item(channel=__channel__, title="Iniciar sesion", action="login"))
    '''

    return itemlist

def perform_login(login,password):
    # Invoca al login, y con eso se quedarán las cookies de sesión necesarias
    url="http://www.shurhd.com/wp-login.php"
    data = scrapertools.cache_page(url,post="log="+LOGIN+"&pwd="+PASSWORD+"&rememberme=forever&wp-submit=Acceder&redirect_to=http%3A%2F%2Fwww.shurhd.com%2Fwp-admin%2F&testcookie=1")

def logout(item):
    nombre_fichero_config_canal = os.path.join( config.get_data_path() , __channel__+".xml" )
    config_canal = open( nombre_fichero_config_canal , "w" )
    config_canal.write("<settings>\n<session>false</session>\n<login></login>\n<password></password>\n</settings>")
    config_canal.close();

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Sesión finalizada", action="mainlist"))
    return itemlist

def login(item):
    if config.get_platform() in ("wiimc", "rss"):
        if LOGIN<>"" and PASSWORD<>"":
            perform_login(LOGIN,PASSWORD)
            itemlist = []
            itemlist.append( Item(channel=__channel__, title="Sesión iniciada", action="mainlist"))
    else:
        import xbmc
        keyboard = xbmc.Keyboard("","Login")
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            login = keyboard.getText()

        keyboard = xbmc.Keyboard("","Password")
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            password = keyboard.getText()

        nombre_fichero_config_canal = os.path.join( config.get_data_path() , __channel__+".xml" )
        config_canal = open( nombre_fichero_config_canal , "w" )
        config_canal.write("<settings>\n<session>true</session>\n<login>"+login+"</login>\n<password>"+password+"</password>\n</settings>")
        config_canal.close();

        if LOGIN<>"" and PASSWORD<>"":
            perform_login(LOGIN,PASSWORD)
            itemlist = []
            itemlist.append( Item(channel=__channel__, title="Sesión iniciada", action="mainlist"))

    return itemlist


def menupeliculas(item):
    logger.info("[shurweb.py] menupeliculas")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Películas - HD" , action="peliculas", url="http://www.shurhd.com/calidad-hd/") )
    itemlist.append( Item(channel=__channel__, title="Películas - DVD", action="peliculas", url="http://www.shurhd.com/calidad-dvd/") )
    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto,categoria=""):
    logger.info("[shurweb.py] "+item.url+" search "+texto)
    itemlist = []
    url = item.url
    texto = texto.replace(" ","+")
    logger.info("categoria: "+categoria+" url: "+url)
    try:
        item.url = "http://www.shurweb.es/?s=%s"
        item.url = item.url % texto
        itemlist.extend(scrappingSearch(item))
        return itemlist
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def scrappingSearch(item,paginacion=True):
    logger.info("[shurweb.py] peliculas")
    url = item.url
    # Descarga la página
    data = scrapertools.cachePage(url)
    # Extrae las entradas
    patronvideos = '<a href="([^"]+)" style="display:none;" rel="nofollow"><img src="([^"]+)" width="100" height="144" border="0" alt="" /><br/><br/>[^<]+<b>([^<]+)</b></a>[^<]+<a href="([^"]+)">([^#]+)#888"><b>([^<]+)</b>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:
        if match[5] == 'Peliculas' or match[5] == 'Series':
            scrapedtitle =  match[2]
            scrapedtitle = scrapertools.entityunescape(scrapedtitle)
            fulltitle = scrapedtitle
            scrapedplot = ""
            scrapedurl = match[3]
            scrapedthumbnail = match[1]
            if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
            itemlist.append( Item(channel=__channel__, action='findvideos', title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle , context="4|5") )

    return itemlist

def peliculas(item,paginacion=True):
    logger.info("[shurweb.py] peliculas")
    url = item.url
    # Descarga la página
    data = scrapertools.cachePage(url)
    # Extrae las entradas
    '''
    <div class="afis">
    <a href="http://www.shurhd.com/invictus-dvd/" title="Invictus DVD<">
    <img src="http://www.shurhd.com/wp-content/themes/stargate spanish/stargate/timthumb.php?src=http://www.shurhd.com/wp-content/uploads/2012/04/Mr_Brooks-167323471-large.jpg&amp;w=120&amp;zc=1&amp;q=176" width="120" height="176" alt="Invictus DVD">
    <img style="position:relative; top: -176px;width:60px;height:60px;" src="/dvd.png"/><div src="" class="kucukIcon"></div></a>
    </div>
    <div class="film">
    <p><span class="kalin">Titulo:</span> <a href="http://www.shurhd.com/invictus-dvd/" title="Invictus DVD">Invictus DVD (2009)<span class="kalin"></span> </a></p>
    <p><span class="kalin">Género:</span> <a href="http://www.shurhd.com/category/otras-calidades/drama-otras-calidades/" title="Ver todas las entradas en Drama" rel="category tag">Drama</a>, <a href="http://www.shurhd.com/category/otras-calidades/" title="Ver todas las entradas en Otras calidades" rel="category tag">Otras calidades</a></p>
    <p><span class="kalin">Descripcion:</span><div style="display: none">UN:F [1.9.16_1159]</div><div class="ratingblock "><div class="ratingheader "></div><div class="ratingstars "><div id="article_rater_3347" class="ratepost gdsr-oxygen gdsr-size-20"><div class="starsbar gdsr-size-20"><div class="gdouter gdheight"><div id="gdr_vote_a3347" style="width: 100px;" class="gdinner gdheight"></div><div id="gdr_stars_a3347" class="gdsr_rating_as"><a id="gdsrX3347X5X3062XaXarticle_rater_3347Xarticle_loader_3347X10X20" title="5 / 5" class="s5" rel="nofollow"></a><a id="gdsrX3347X4X3062XaXarticle_rater_3347Xarticle_loader_3347X10X20" title="4 / 5" class="s4" rel="nofollow"></a><a id="gdsrX3347X3X3062XaXarticle_rater_3347Xarticle_loader_3347X10X20" title="3 / 5" class="s3" rel="nofollow"></a><a id="gdsrX3347X2X3062XaXarticle_rater_3347Xarticle_loader_3347X10X20" title="2 / 5" class="s2" rel="nofollow"></a><a id="gdsrX3347X1X3062XaXarticle_rater_3347Xarticle_loader_3347X10X20" title="1 / 5" class="s1" rel="nofollow"></a></div></div></div></div><div id="article_loader_3347" style="display: none; width: 100px " class="ratingloaderarticle"><div class="loader bar " style="height: 20px"><div class="loaderinner"></div></div></div></div><div class="ratingtext "><div id="gdr_text_a3347">Rating: 5.0/<strong>5</strong> (1 vote cast)</div></div></div><p>Adaptación de un libro de John Carlin (Playing the enemy). En 1990, tras ser puesto en libertad, Nelson Mandela (Morgan Freeman) llega a la Presidencia de su país y decreta la abolición del &#8220;Apartheid&#8221;. Su objetivo era llevar a cabo una política de reconciliación entre la mayoría negra y la minoría blanca. En 1995, la celebración en Sudáfrica de la Copa Mundial de Rugby fue el instrumento utilizado por el líder negro para construir la unidad nacional.</p>
    '''
    '''
    <div class="afis">
    <a href="http://www.shurhd.com/la-playa-hd/" title="La Playa HD"><img src="http://www.shurhd.com/wp-content/themes/stargate spanish/stargate/timthumb.php?src=http://www.shurhd.com/wp-content/uploads/2012/04/la-playa.jpg&amp;w=120&amp;zc=1&amp;q=176" width="120" height="176" alt="La Playa HD"><div src="" class="kucukIcon"></div></a>
    </div>
    <div class="film">
    <p><span class="kalin">Titulo:</span> <a href="http://www.shurhd.com/la-playa-hd/" title="La Playa HD">La Playa HD<span class="kalin"></span> </a></p>
    <p><span class="kalin">Genero:</span> <a href="http://www.shurhd.com/category/hd/aventuras/" title="Ver todas las entradas en Aventuras" rel="category tag">Aventuras</a>, <a href="http://www.shurhd.com/category/hd/" title="Ver todas las entradas en HD y HDRip" rel="category tag">HD y HDRip</a>, <a href="http://www.shurhd.com/category/hd/intriga/" title="Ver todas las entradas en Intriga" rel="category tag">Intriga</a></p>
    <p><span class="kalin">Descripción:</span><div style="display: none">UN:F [1.9.16_1159]</div><div class="ratingblock "><div class="ratingheader "></div><div class="ratingstars "><div id="article_rater_3283" class="ratepost gdsr-oxygen gdsr-size-20"><div class="starsbar gdsr-size-20"><div class="gdouter gdheight"><div id="gdr_vote_a3283" style="width: 85.333333333333px;" class="gdinner gdheight"></div><div id="gdr_stars_a3283" class="gdsr_rating_as"><a id="gdsrX3283X5X3062XaXarticle_rater_3283Xarticle_loader_3283X10X20" title="5 / 5" class="s5" rel="nofollow"></a><a id="gdsrX3283X4X3062XaXarticle_rater_3283Xarticle_loader_3283X10X20" title="4 / 5" class="s4" rel="nofollow"></a><a id="gdsrX3283X3X3062XaXarticle_rater_3283Xarticle_loader_3283X10X20" title="3 / 5" class="s3" rel="nofollow"></a><a id="gdsrX3283X2X3062XaXarticle_rater_3283Xarticle_loader_3283X10X20" title="2 / 5" class="s2" rel="nofollow"></a><a id="gdsrX3283X1X3062XaXarticle_rater_3283Xarticle_loader_3283X10X20" title="1 / 5" class="s1" rel="nofollow"></a></div></div></div></div><div id="article_loader_3283" style="display: none; width: 100px " class="ratingloaderarticle"><div class="loader bar " style="height: 20px"><div class="loaderinner"></div></div></div></div><div class="ratingtext "><div id="gdr_text_a3283">Rating: 4.3/<strong>5</strong> (15 votes cast)</div></div></div><p>Impulsado por el deseo de vivir experiencias y emociones apasionantes, Richard (Leonardo DiCaprio), un joven mochilero, va a Thailandia. En Bangkok, se aloja en un hotel de mala muerte, donde conoce a una pareja de franceses, Étienne (Guillaume Canet) y Françoise (Virginie Ledoyen), y a Daffy (Robert Carlyle), un viajero consumido por años de sol y drogas y que está de vuelta de todo. Daffy, un ser tortuoso y paranoico, le cuenta a Richard una historia fantástica sobre una isla paradisíaca que nunca ha sido profanada por los turistas</p>
    </p>
    '''
    patronvideos  = '<a href="([^"]+)" title="([^"]+)">[^<]*'
    patronvideos += '<img src="http\://www.shurhd.com/wp-content/themes/stargate spanish/stargate/timthumb.php\?src\=(.*?.jpg)[^"]+"[^>]+>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for url,title,thumbnail in matches:
        scrapedtitle = title
        scrapedtitle = scrapertools.entityunescape(scrapedtitle).strip()
        if scrapedtitle.endswith("<"):
            scrapedtitle = scrapedtitle[:-1]
        fulltitle = scrapedtitle
        scrapedplot = ""
        scrapedurl = url
        scrapedthumbnail = thumbnail
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='findvideos', title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle , context="4|5") )

    #<li><a class="next page-numbers" href="http://www.shurhd.com/page/2/">Siguiente</a></li>
    patronvideos  = '<li><a class="next page-numbers" href="([^"]+)">[^<]+</a></li>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = matches[0]
        pagitem = Item(channel=__channel__, action="peliculas", title="!Página siguiente" , url=scrapedurl)
        if not paginacion:
            itemlist.extend( scrapping(pagitem) )
        else:
            itemlist.append( pagitem )
    return itemlist

def series(item):
    logger.info("[shurweb.py] series")
    url = item.url
    # Descarga la página
    data = scrapertools.cachePage(url)
    patronvideos  = '<li class="cat-item[^<]+<div class="avhec-widget-line"><a href="([^"]+)" title="[^"]+">(.*?)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for url,title in matches:
        scrapedtitle = title
        scrapedtitle = scrapertools.entityunescape(scrapedtitle).strip()
        scrapedtitle = scrapertools.htmlclean(scrapedtitle).strip()
        if scrapedtitle.endswith("<"):
            scrapedtitle = scrapedtitle[:-1]
        fulltitle = scrapedtitle
        scrapedplot = ""
        scrapedurl = url
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+""+"]")
        itemlist.append( Item(channel=__channel__, action='episodios', title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , plot=scrapedplot , extra=scrapedtitle , show=scrapedtitle, folder=True) )

    return itemlist

def episodios(item):
    logger.info("[shurweb.py] series")
    url = item.url
    # Descarga la página
    data = scrapertools.cachePage(url)
    patronvideos  = '<li><a href="(http://series.shurhd.com/[^"]+)">(.*?)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for url,title in matches:
        title = title.replace("&#215;","x")
        scrapedtitle = title.strip()
        scrapedtitle = scrapertools.entityunescape(scrapedtitle).strip()
        scrapedtitle = scrapertools.htmlclean(scrapedtitle).strip()
        if scrapedtitle.endswith("<"):
            scrapedtitle = scrapedtitle[:-1]
        fulltitle = scrapedtitle
        scrapedplot = ""
        scrapedurl = url
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+""+"]")
        itemlist.append( Item(channel=__channel__, action='findvideos', title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , plot=scrapedplot , extra=scrapedtitle , show=item.show, context="4|5") )

    if config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee"):
        itemlist.append( Item(channel=item.channel, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())
    peliculas_items = peliculas(mainlist_items[0])
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = servertools.find_video_items(item=pelicula_item)
        if len(mirrors)>0:
            bien = True
            break

    return bien