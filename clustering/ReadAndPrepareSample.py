import json
import re

from Constants import SAMPLE_FILE_NAME


# Reads the files and puts them in a matrix
def readSampleFile():
    with open(SAMPLE_FILE_NAME, "r", encoding="utf-8") as sample_file:
        text = sample_file.readlines()
    return text


# Removes symbols and urls
def removeSymbolsAndUrls(text):
    # We have several regular expressions to clean the texts from unuseful data
    regexpUrls = re.compile("https?://(www\.)?(\w|-)+\.\w+")
    regexpEmails = re.compile("[a-zA-Z1-9-]+@[a-zA-Z-]+\.[a-zA-Z]+")
    regexpWeb = re.compile("(http)|(www)|(http www)|(html)|(htm)|.com")
    regexpNumbers = re.compile("\d")

    text = re.sub(regexpUrls, "", text)  # We clean the complete urls
    text = re.sub(regexpEmails, "", text)  # We clean the emails
    text = re.sub(regexpWeb, "", text)  # We clean url fragments
    text = re.sub(regexpNumbers, "", text)  # quitamos los números

    return text

def preprocessTexts():
    # Se leen los contenidos del archivo con la muestra
    listFiles = readSampleFile()

    # No es necesario eliminar las cabeceras puesto que no hay tal cosa en nuestros datos
    #
    # Sí es necesario no obstante tener por un lado el identificador del documento
    # y por otro el texto del mismo (title + selftext)
    #

    listTexts = []
    post_ids = []
    subreddit_post = []

    for entrada in listFiles[1:]:
        # entrada es una cadena y con json.loads la parseamos en un diccionario
        #
        entrada = json.loads(entrada)

        titulo = entrada["title"].strip()
        contenido = entrada["self_text"].strip()
        texto = titulo + " " + contenido
        texto = texto.strip()

        listTexts.append(removeSymbolsAndUrls(texto))
        post_ids.append(entrada["post_id"])
        subreddit_post.append(entrada["subreddit"])

    # Se devuelve la lista de textos, sus ids y el subreddit al que pertenecen
    return {"listTexts":listTexts,"post_ids":post_ids, "subreddits": subreddit_post} 


def storeTextsInArray():
    posts_array = readSampleFile()
    texts = []
    for i in range(len(posts_array)-1):
        try:  # Used to avoid exceptions for empty lines in the end
            text = json.loads(posts_array[i])
            texts.append(text)
        except json.decoder.JSONDecodeError:
            continue

    return [texts, posts_array[0]]
