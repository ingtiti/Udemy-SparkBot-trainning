from itty import *
import urllib2
import json

def sendSparkGET(url):
    """
    ESTA FUNCION NOS SERVIRA PARA SOLICITAR EL MENSAJE DEL USUARIO QUE FUNCIONARA
    COMO trigger DE NUESTO bot, A LA VEZ QUE OBTENEMOS EL username DE QUIEN
    ENVIA LA PETICION O MENSAJE
    """
    request = urllib2.Request(url,
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    contents = urllib2.urlopen(request).read()
    return contents

def sendSparkPOST(url, data):
    """
    ESTA FUNCION NOS SERVIRA PARA CONFIRMAR LA RECEPCION DEL COMANDO O MENSAJE
    SOLICITADO A CISCO SPARK
    """
    request = urllib2.Request(url, json.dumps(data),
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    contents = urllib2.urlopen(request).read()
    return contents


@post('/')
def index(request):
    """
    CUANDO UN MENSAJE PROVENGA DESDE EL webhook SERA PROCESADO EN ESTE METODO.
    EL MENSAJE SE OBTIENE POR LA FUNCION sendSparkGet(). EL MENSAJE SERA 'PARSEADO'.
    SI SE ENCUENTRA UN TEXTO ESPERADO EN EL MENSAJE, ENTONCES SE EJECUTA UNA ACCION:
    /batman    - CONTESTA EN EL MISMO room MAS UN MENSAJE
    /batcave   - REPLICA EL MISMO MENSAJE
    /batsignal - CONTESTA CON UNA IMGEN
    """
    webhook = json.loads(request.body)
    print webhook['data']['id']
    result = sendSparkGET('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
    result = json.loads(result)
    msg = None
    if webhook['data']['personEmail'] != bot_email:
        in_message = result.get('text', '').lower()
        in_message = in_message.replace(bot_name, '')
        if 'batman' in in_message or "whoareyou" in in_message:
            msg = "I'm Batman!"
        elif 'batcave' in in_message:
            message = result.get('text').split('batcave')[1].strip(" ")
            if len(message) > 0:
                msg = "The Batcave echoes, '{0}'".format(message)
            else:
                msg = "The Batcave is silent..."
        elif 'batsignal' in in_message:
            print "NANA NANA NANA NANA"
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "files": bat_signal})
        if msg != None:
            print msg
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
    return "true"

####CAMBIA ESTOS VALORES#####
bot_email = "yourbot@sparkbot.io"
bot_name = "yourBotDisplayName"
bearer = "BOT BEARER TOKEN HERE"
bat_signal  = "https://upload.wikimedia.org/wikipedia/en/c/c6/Bat-signal_1989_film.jpg"
run_itty(server='wsgiref', host='0.0.0.0', port=10010)
