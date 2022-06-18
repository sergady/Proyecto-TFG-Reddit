from cgitb import text
import json
import random
from Read_and_prepare_sample import removeSymbolsAndUrls

PERCENTAGES_DICT = {"abuse":2147,"anxiety":519,"bodyimage":139,"depression":93,"eating":87,"familyissues":94,"friendissues":63,"grief":457,"healthconcerns":31,"lgbtqissues":26, "loneliness":17, "relationshipissues":20, "selfharm":11, "substanceabuse": 8}

# Reads the files and puts them in a matrix
def readSampleFile(topic, month, percentage):
    with open("data/data_"+ topic +"/" + topic +"_"+ month +".ndjson", "r", encoding="utf-8") as sample_file:
        text = sample_file.readlines()
        if(percentage >= 100):
            return text
        else:
            return percentage_text(text, percentage)

def percentage_text(text, percentage):
    number_texts = round(len(text) * percentage / 100)
    percentage_text = list()

    while(len(percentage_text) < number_texts):
        percentage_text.append(text.pop(random.randrange(len(text))))

    return percentage_text

def preprocess_texts(topic, month, percentage):
    # Se leen los contenidos del archivo con la muestra
    listFiles = readSampleFile(topic, month, percentage)

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
        texto = removeSymbolsAndUrls(texto)
        texto = texto.strip()

        listTexts.append(texto)
        post_ids.append(entrada["post_id"])
        subreddit_post.append(entrada["subreddit"])

    # Se devuelve la lista de textos, sus ids y el subreddit al que pertenecen
    return {"listTexts":listTexts,"post_ids":post_ids, "subreddits": subreddit_post} 

def retrieve_texts(topic):
    months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    texts = list()
    for month in months:
        texts.extend(preprocess_texts(topic, month, PERCENTAGES_DICT.get(topic, 100))["listTexts"])
        
    return texts

def return_train_sample():
    topics = PERCENTAGES_DICT.keys()
    texts = list()
    for topic in topics:
        texts.extend(retrieve_texts(topic))

    return texts