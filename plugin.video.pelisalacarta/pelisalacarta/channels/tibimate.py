# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para Tibimate
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "tibimate"
__category__ = "F,D"
__type__ = "generic"
__title__ = "Tibimate"
__language__ = "ES"
__adult__ = "true"

DEBUG = config.get_setting("debug")

UrlLogin = "http://tibimate.li/xbtit/index.php?page=login"

TituloCompleto = False


def isGeneric():
    return True

def login():

    LOGIN = config.get_setting("tibimateuser")
    PASSWORD = config.get_setting("tibimatepassword")

    data = scrapertools.cache_page(UrlLogin)
    #No estas logado : <title>TibiMate Tracker .::. Index->Login</title>
    #Si estas Logado : <title>TibiMate Tracker .::. Inicio</title>

    patron = "<title>TibiMate Tracker \.::\. Index->Login</title>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
       # Hace el submit del login Solo si no estas logeado
       post = "uid="+LOGIN+"&pwd="+PASSWORD
       logger.info("post="+post)
       data = scrapertools.cache_page(UrlLogin , post=post)

       patron = "<title>TibiMate Tracker \.::\. Inicio</title>"
       matches = re.compile(patron,re.DOTALL).findall(data)
       if len(matches)==0:
         return False

    return True

def mainlist(item):
    logger.info("[Tibimate.py] mainlist")
    itemlist = []
    
    if config.get_setting("tibimateaccount")!="true":
        itemlist.append( Item( channel=__channel__ , title="Habilita tu cuenta en la configuración..." , action="openconfig" , url="" , folder=False ) )
    else:
        if login():
            itemlist.append( Item( channel=__channel__ , title="Estrenos" , action="Browser" , url="http://tibimate.li/xbtit/index.php?page=streams&cat=1&pages=1" , folder=True ) )
            itemlist.append( Item( channel=__channel__ , title="Peliculas" , action="Browser" , url="http://tibimate.li/xbtit/index.php?page=streams&cat=2&pages=1" , folder=True ) )
            itemlist.append( Item( channel=__channel__ , title="PeliculasHD" , action="Browser" , url="http://tibimate.li/xbtit/index.php?page=streams&cat=3&pages=1" , folder=True ) )
            if config.get_setting("enableadultmode")=="true":
                itemlist.append( Item( channel=__channel__ , title="XXX" , action="Browser" , url="http://tibimate.li/xbtit/index.php?page=streams&cat=4&pages=1" , folder=True ) )
                itemlist.append( Item( channel=__channel__ , title="XXX HD" , action="Browser" , url="http://tibimate.li/xbtit/index.php?page=streams&cat=5&pages=1" , folder=True ) )
        else:
            itemlist.append( Item( channel=__channel__ , title="Cuenta incorrecta, revisa la configuración..." , action="openconfig" , url="" , folder=False ) )
    return itemlist

def openconfig(item):
    if "xbmc" in config.get_platform() or "boxee" in config.get_platform():
        config.open_settings( )
    return []

def Browser(item):
    logger.info("[tibimate.py] Browser")
    itemlist=[]


    #patron = '(.*?)pages=(.*?)\Z'
    #matches = re.compile(patron,re.DOTALL).findall(item.url)
    #scrapertools.printMatches(matches)
    #if len(matches) > 0: 
    #  BasePag = matches[0][0]+"pages="
    #  PaginaAct = int(matches[0][1])

    #logger.info("BasePag" + BasePag + "----"+str(PaginaAct))
    #if PaginaAct > 1 : itemlist.append( Item(channel=__channel__, action="Browser", title="<<- Pagina Anterior" , url=BasePag+str(PaginaAct-1) , folder=True) )

    data = scrapertools.cache_page(item.url)

    #logger.info("data= "+data)

    #patron = '<span class="pagercurrent"><b>([^"]+)</b></span>'#<div class="pagelinks">Páginas:.*?\[<strong>[^<]+</strong>\].*?<a class="navPages" href="(?!\#bot)([^"]+)">[^<]+</a>.*?</div>'
    #matches = re.compile(patron,re.DOTALL).findall(data)
    #if len(matches) > 0: PaginaAct = matches[0]

	
    #<div style="width:150px;height:260px;background-color:#aaa;padding:8px;float:left;margin:15px 5px;">
    # Aqui comienza el enlace con su portada
    # <div style="width:148px;height:200px;border:1px solid #333">
    # <a href="index.php?page=pelison&id=0db906dbcb65a08fc2687f6a041b4137ef0d457c" onclick="_gaq.push(['_trackEvent', 'streams_page', 'stream-0db906dbcb65a08fc2687f6a041b4137ef0d457c'])"><img src="http://tibimate.li/xbtit/Portadas/pztRR7iGXqHR.jpg" style="width:148px;height:200px"></a>
    # </div>
    # Aqui acaba el enlace con su portada
    # <div style="width:148px;height:50px;word-wrap:break-word">
    #   <p style="color:#545dab;font-family:'Comic Sans MS', cursive;font-size:13px;line-height:.8">Her.DVDSCR.MiC</p>
    #   <p style="color:#333;font-family:'Comic Sans MS', cursive;font-size:10px;line-height:.3">Categoria: Estrenos XVID</p>
    #   <p style="color:#333;font-family:'Comic Sans MS', cursive;font-size:10px;line-height:.3">Visto: 32 veces</p>
    # </div>
    #
    #</div>

    UrlParcial = "index.php\?page=pelison&id="
    UrlBase = "http://tibimate.li/xbtit/"
    
    patron = '<a href="' + UrlParcial + '([^"]+)".*?<img src="([^"]+)" style="width:148px;height:200px">.*?<p style="color:#545dab;font-family:.*?, cursive;font-size:13px;line-height:.8">([^<]+)</p>'
    action = "findvideos"
    #logger.info("patron= "+patron)

    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    #logger.info("matches= "+str(len(matches)))
    for Id, Cartel,Titulo in matches:
    # for Id in matches:
        url = UrlBase + UrlParcial.replace("\?","?") + Id
        title = Limpia(Titulo)
        if TituloCompleto :
          dataTitu = scrapertools.cache_page(url)
          #<center><h3>Her.DVDSCR.MiC</h3></center>
          patronimage = "<center><h3>(.*?)</h3></center>"
          matchesTit = re.compile(patronimage,re.DOTALL).findall(dataTitu)
          if len(matchesTit)>0:
            title = Limpia(matchesTit[0])

        thumbnail = Cartel
        plot = ""
        # Añade al listado
        itemlist.append( Item(channel=__channel__, action=action, title= title, url=url , thumbnail=thumbnail , plot=plot , folder=True) )
    
    # EXTREA EL LINK DE LA SIGUIENTE PAGINA
    #Extracto de la paginacion
    #<form name="change_page1pages" method="post" action="index.php">
    #<label class="custom-select"><select  name="pages" onchange="location=document.change_page1pages.pages.options[document.change_page1pages.pages.selectedIndex].value" size="1">
    #<option selected="selected"value="index.php?page=streams&amp;cat=1&pages=1">1</option>
    #<option value="index.php?page=streams&amp;cat=1&pages=2">2</option>
    #<option value="index.php?page=streams&amp;cat=1&pages=3">3</option>
    #<option value="index.php?page=streams&amp;cat=1&pages=4">4</option>
    #</select></label>
    #&nbsp;<span class="pagercurrent"><b>1</b></span>
    #&nbsp;<span class="pager"><a href="index.php?page=streams&amp;cat=1&pages=2">2</a></span>
    #&nbsp;<span class="pager"><a href="index.php?page=streams&amp;cat=1&pages=3">3</a></span>
    #&nbsp;<span class="pager"><a href="index.php?page=streams&amp;cat=1&pages=2">&nbsp;&gt;</a></span>
    #&nbsp;<span class="pager"><a href="index.php?page=streams&amp;cat=1&pages=4">&nbsp;&raquo;</a></span>
    #</form>


    #    url = match
    #    title = ">> Página Siguiente"
    #    thumbnail = ""
    #    plot = ""
    #    # Añade al listado
    #    itemlist.append( Item(channel=__channel__, action="Browse", title=title , url=url , folder=True) )
	
    #<span class="pager"><a href="index.php?page=streams&amp;cat=1&pages=2">&nbsp;&gt;</a></span>
    patron = '<span class="pager"><a href="([^"]+)">&nbsp;&gt;</a></span>'#<div class="pagelinks">Páginas:.*?\[<strong>[^<]+</strong>\].*?<a class="navPages" href="(?!\#bot)([^"]+)">[^<]+</a>.*?</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    #if len(matches) > 0: itemlist.append( Item(channel=__channel__, action="Browser", title="Pagina Siguiente -->" , url=BasePag+str(PaginaAct+1) , folder=True) )
    if len(matches) > 0: itemlist.append( Item(channel=__channel__, action="Browser", title="Pagina Siguiente -->" , url=UrlBase+Limpia(matches[0]), folder=True) )

    return itemlist

    
def findvideos(item):
    logger.info("[Tibimate.py] findvideos"+item.url)
    data = scrapertools.cache_page(item.url)

    itemlist=[]

    #logger.info("data="+data)

    Titulo = 'NoSe' 
    #<center><h3>Her.DVDSCR.MiC</h3></center>
    patronimage = "<center><h3>(.*?)</h3></center>"
    matches = re.compile(patronimage,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    if len(matches)>0:
      Titulo = Limpia(matches[0])

    #<script type="text/javascript">
    #		jwplayer("mediaplayer").setup({
    #		flashplayer: "jwplayer/player.swf",
    #		skin: "reproductor/ruby.zip",
    #       'width': "930",
    #		'height': "506",
    #		'provider': 'http',
    #                 
    #		'image': "http://tibimate.li/xbtit/Portadas/pztRR7iGXqHR.jpg",
    #		file: "http://5.135.164.142/v/izY682I2Z339.mp4"
    #		});
    #</script>

    #logger.info("data="+data)
    patronimage = 'jwplayer\("mediaplayer"\)' + "\.setup.*?skin:.*?'image': " + '"([^"]+)",.*?file: "([^"]+)"'
    #logger.info("patron="+patronimage)
    matches = re.compile(patronimage,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    #if len(matches)>0:
    for Poster, Url in matches:
      thumbnail = Poster
      thumbnail = scrapertools.htmlclean(thumbnail)
      thumbnail = unicode( thumbnail, "iso-8859-1" , errors="replace" ).encode("utf-8")
      item.thumbnail = thumbnail
      itemlist.append( Item(channel=__channel__, action="play", title=Titulo , url=Url , thumbnail=thumbnail, folder=False) )

    return itemlist   

def Limpia(cadena):
    cadena = cadena.replace('&amp;','&')
    return cadena

