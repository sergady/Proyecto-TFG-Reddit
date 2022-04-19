from numpy import empty_like
from ReadSample import storeTextsInArray
import sys
from datetime import datetime
import re
import json

def setFileOutput():
    file_name = 'results/result_'+str(datetime.now().__str__().replace(" ", "_").replace(":","-")[:-7])+'.txt'
    sys.stdout = open(file_name, 'w')

# Removes symbols and urls
def removeSymbolsAndUrlsDani(text):
    # We have several regular expressions to clean the texts from unuseful data
    regexpUrls = re.compile("https?://(www\.)?(\w|-)+\.\w+")
    regexpEmails = re.compile("[a-zA-Z1-9-]+@[a-zA-Z-]+\.[a-zA-Z]+")
    regexpWeb = re.compile("(http)|(www)|(http www)|(html)|(htm)|.com")
    regexpNumbers = re.compile("\d")
    # Esto tiene que usarse para eliminar los nombres de los subreddits... Si es depression, anxiety,... no quitara palabras útiles?
    # regexpKeyWords = re.compile(r"(soc culture)|(basque)|(vasque)|(galiza)|(catalán)|(soc)")

    text = re.sub(regexpUrls,"",text) # We clean the complete urls
    text = re.sub(regexpEmails,"",text) # We clean the emails
    text = re.sub(regexpWeb,"",text) # We clean url fragments
    text = re.sub(regexpNumbers,"",text) # We clean numbers
    # text = re.sub(regexpKeyWords,"",text) # quitamos las keywords

    return text

def preprocessTextsDani():
    # Se leen los contenidos del archivo con la muestra
    with open("data/sample_file.txt","r",encoding="utf-8") as fichero:
        listFiles = fichero.readlines()

    # listFiles
    # No es necesario eliminar las cabeceras puesto que no hay tal cosa en nuestros datos
    #
    # Sí es necesario no obstante tener por un lado el identificador del documento
    # y por otro el texto del mismo (title + selftext)
    #

    listTexts = list()
    post_ids = list()

    for entrada in listFiles[1:]:
        # entrada es una cadena y con json.loads la parseamos en un diccionario
        #
        entrada = json.loads(entrada)

        titulo = entrada["title"].strip()
        contenido = entrada["self_text"].strip()
        texto = titulo + " " + contenido
        texto = texto.strip()
        identificador = entrada["post_id"]

        listTexts.append(texto)
        post_ids.append(identificador)

    return {"listTexts":listTexts,"post_ids":post_ids} # Hay que retornar post_ids también...


[preprocessedTexts, sample_seed] = storeTextsInArray()
print("Texts loaded!")
print("Semilla de sample_file.txt: " + sample_seed)
preprocessTextsDani()