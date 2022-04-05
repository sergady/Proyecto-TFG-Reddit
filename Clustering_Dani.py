import os
import re

"""# Obtención del dataset
Vamos a montar una unidad en drive para que el trabajo con el dataset sea más simple.
"""

"""# Preprocesamiento del dataset
Una vez que lo tenemos guardado y disponible para trabajar con él, procedemos a hacer el preprocesamiento pertinente para obtener la mayor cantidad de información de él. No obstante, no vamos a proceder con diferentes métodos sin antes pensar el por qué lo hacemos.

## Métodos de preprocesamiento
Como vemos en el fragmento de código siguiente tenemos tres métodos de preprocesado:

*   readData(): este método lee de la carpeta que contiene todos los archivos que conforman el dataset. Al leerlos mete todos los archivos excepto el readme en un array llamado listOfFiles. Desde este array será más fácil trabajar con los datos.


*   removeHeaders(listOfFiles): quita los cabeceros de los textos porque tienen información poco relevante y ,en algunos casos, palabras clave que harían demasiado específico al procesador de texto. El parámetro es la lista anteriormente mencionada que contiene todos los archivos.

*   printConsole(array): imprime el resulatado en consola en una forma más visible.

*   printToFile(array): imprime el resulatado de una forma más visible en un archivo.
"""

# Reads the files and puts them in a matrix
def readDataDani():
    with open("data/sample_file.txt","r",encoding="utf-8") as fichero:
        listOfFiles = fichero.readlines()

    return listOfFiles

# Removes the headers
def removeHeaders(listOfFiles):
    listTexts = []
    for file in listOfFiles:
        text = file.read()
        text = text.split("\n\n")[1:]
        listTexts.append(text)

    return listTexts

# Removes symbols and urls
def removeSymbolsAndUrls(listTexts):
    cleanTexts = []
    for files in listTexts:
        # We have several regular expressions to clean the texts from unuseful data
        regexpUrls = re.compile("https?://(www\.)?(\w|-)+\.\w+")
        regexpEmails = re.compile("[a-zA-Z1-9-]+@[a-zA-Z-]+\.[a-zA-Z]+")
        regexpWeb = re.compile("(http)|(www)|(http www)|(html)|(htm)|.com")
        regexpNumbers = re.compile("\d")
        regexpKeyWords = re.compile(r"(soc culture)|(basque)|(vasque)|(galiza)|(catalán)|(soc)")
        # eliminar lista de palabras: basque, galiza, catalan, .com

        completeText = "" # We create a string for each file
        for text in files:
            text = re.sub(regexpUrls,"",text) # We clean the complete urls
            text = re.sub(regexpEmails,"",text) # We clean the emails
            text = re.sub(regexpWeb,"",text) # We clean url fragments
            text = re.sub(regexpNumbers,"",text) # quitamos los números
            text = re.sub(regexpKeyWords,"",text) # quitamos las keywords
            completeText += text
        cleanTexts.append(completeText)

    return cleanTexts


# Removes symbols and urls
def removeSymbolsAndUrlsDani(text):
    # We have several regular expressions to clean the texts from unuseful data
    regexpUrls = re.compile("https?://(www\.)?(\w|-)+\.\w+")
    regexpEmails = re.compile("[a-zA-Z1-9-]+@[a-zA-Z-]+\.[a-zA-Z]+")
    regexpWeb = re.compile("(http)|(www)|(http www)|(html)|(htm)|.com")
    regexpNumbers = re.compile("\d")
    # Esto tiene que usarse para eliminar los nombres de los subreddits...
    regexpKeyWords = re.compile(r"(soc culture)|(basque)|(vasque)|(galiza)|(catalán)|(soc)")

    text = re.sub(regexpUrls,"",text) # We clean the complete urls
    text = re.sub(regexpEmails,"",text) # We clean the emails
    text = re.sub(regexpWeb,"",text) # We clean url fragments
    text = re.sub(regexpNumbers,"",text) # quitamos los números
    text = re.sub(regexpKeyWords,"",text) # quitamos las keywords

    return text

# Function to print the result on the console and to check it
def printConsole(array):
    for i in array:
      print(i)
      print("----------------------------------------------------")

# Function to print the result on a txt file
def printToFile(array):
    f = open("demofile.txt", "w")
    for i in array:
        f.write(i)
        f.write("------")
        f.write("\n")
    f.close()

"""Ahora, con todos los métodos necesarios para preprocesar, hacemos un método que reciba los textos y directamente saque los textos listos para usar:"""

def preprocessTexts():
    # Reads the files
    listFiles = readData()

    # Removes the headers
    listTexts = removeHeaders(listFiles)

    # Removes the unuseful symbols
    listTexts = removeSymbolsAndUrls(listTexts)

    # Last list containing all the important data from the texts
    finalList = []

    for index in range(len(listTexts)):
        if(index != None):
          finalList.append(listTexts[index])

    # Return the list of clean files
    return finalList


# Método para leer la muestra que no los archivos del directorio y dejarlo todo
# listo para el clustering
#

import json

def preprocessTextsDani():
    # Se leen los contenidos del archivo con la muestra
    #
    listFiles = readDataDani()

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

        #listTexts[identificador] = removeSymbolsAndUrlsDani(texto)
        listTexts.append(removeSymbolsAndUrlsDani(texto))
        post_ids.append(identificador)

    return {"listTexts":listTexts,"post_ids":post_ids} # Hay que retornar post_ids también...

#preprocessedTexts = preprocessTexts()

preprocessedTexts = preprocessTextsDani()

preprocessedTextsIds = preprocessedTexts["post_ids"]
preprocessedTexts = preprocessedTexts["listTexts"]


# print(printConsole(preprocessedTexts))

"""# Clustering
Ahora con los textos preprocesados y en un único array, vamos a proceder a hacer el clustering. Así comprobaremos si es capaz de distinguir los diferentes idiomas que hay.

## Vectorizado de los textos

Antes de proceder al clustering, hay que vectorizar los datos para obterner matrices de frecuencia. Procedemos a vectorizar el corpus con la herramienta TfidfVectorizer:
"""

from sklearn.feature_extraction.text import TfidfVectorizer

# Se va a usar un vectorizador que ponderará los términos mediante tf·idf,
# pasará los textos a minúsculas y usará unigramas y bigramas
# truncando, además, el vocabulario en los 1500
# términos más frecuentes.
#

vectorizador = TfidfVectorizer(encoding="utf-8", lowercase=True, ngram_range=(1,2),
                                 max_features=15000, stop_words='english')

# Se aplica el vectorizador al corpus de textos
#
matriz = vectorizador.fit_transform(preprocessedTexts)

"""## Aplicación de K-Means

Ahora vamos a aplicar k-medias (k-means). Vamos a usar un número de clusters como inicio y luego iremos probando con diferentes para ver cuál es el óptimo. Se supone que tenemos 5 lenguajes asi que usaré 6 clusters para ver si al menos encuentra los 5 lenguajes y deja algunos textos que no reconoce en el sexto grupo.
"""

from sklearn.cluster import KMeans

# El número de clusters debe fijarse y en este caso se ha establecido de manera
# empírica usando la llamada "silhouette" que varía entre -1 y 1.
# Cuanto más próximo a 1 mejor es el clustering (más diferentes son los grupos
# entre sí).
# Cuanto más próximo a cero más parecidos son los clusters entre sí.
# Si está por debajo de cero los clusters se solapan.
#
num_clusters = 250

# Se va a usar el algoritmo k-means en búsqueda de 250 clusters
#
clustering = KMeans(n_clusters=num_clusters, init='k-means++', max_iter=100, n_init=1, verbose=True)

# Se aplica el algoritmo seleccionado a la matriz que representa el corpus
#
clustering.fit(matriz)

"""### Visualización de los clusters de K-Means
Para visualizar los clusters hay que aplicar el siguiente procedimiento.
"""

from collections import Counter

from sklearn.metrics import silhouette_score


# Calculamos la puntuación de la "silueta".
#
silhouette_avg = silhouette_score(matriz, clustering.labels_)
print("Silhouette score: ", silhouette_avg)

# En el atributo labels_ tenemos el cluster al que pertenece cada documento.
# Usando un Counter podemos contar cuántos documentos hay por cluster.
#
# Sería equivalente a haber hecho docs_per_cluster = km.fit_predict(matriz)
#
docs_per_cluster = Counter(clustering.labels_)

# De este modo obtenemos de nuevo el texto asociado a los términos (recordemos
# que con el vectorizador obtenemos una "traducción" totalmente numérica de los
# documentos).
#
terminos = vectorizador.get_feature_names()

# El atributo cluster_centers_ es un array n-dimensional (realmente bidimensional)
# que contiene el centroide de cada cluster en una matriz de clusters x términos
# definido por pesos flotantes obviamente
#
# El método argsort de numpy *no* ordena el array, retorna *otro* array de las
# mismas dimensiones que contiene *índices* en el orden en que deberían estar
# para que los *valores* del array (en este caso cluster_centers_) estuviera
# ordenado
#
indice_cluster_terminos = clustering.cluster_centers_.argsort()[:, ::-1]

# Nos quedamos con los num_clusters clusters y mostramos los 20
# términos más representativos de los mismos.
#
print("Método K-means")
for (cluster_id, num_docs) in docs_per_cluster.most_common(num_clusters):
  print("Cluster %d (%d documentos):" % (cluster_id, num_docs), end='')
  for term_id in indice_cluster_terminos[cluster_id, :20]:
    print('"%s"' % terminos[term_id], end=' ')
  print()

# Ejemplo de cómo obtener los identificadores *reales* del cluster al que
# pertenece cada documento.
#
# El atributo labels_ va a tener en este caso 5000 etiquetas, una por cada documento
#
#for i in range(len(clustering.labels_)):
#    print(preprocessedTextsIds[i],clustering.labels_[i])

exit()

"""## Aplicación de Afinnity Propagation

Ahora vamos a usar el método de affinity propagation.
La mayor ventaja de este frente a K-means es que no hay que especificar el número de clusters que se espera recibir.
"""

from sklearn.cluster import AffinityPropagation

# Obsérvese que no es preciso indicar el número de clusters
#
clustering = AffinityPropagation(max_iter=100, verbose=True)

# Se aplica el algoritmo seleccionado a la matriz que representa el corpus
#
clustering.fit(matriz)

"""Ahora para observar los resultados procedemos a hacer la silueta igual que con k-means."""

# Calculamos la puntuación de la "silueta".
#
silhouette_avg = silhouette_score(matriz, clustering.labels_)
print("Silhouette score: ", silhouette_avg)

# En el atributo labels_ tenemos el cluster al que pertenece cada documento.
# Usando un Counter podemos contar cuántos documentos hay por cluster.
#
# Sería equivalente a haber hecho docs_per_cluster = km.fit_predict(matriz)
#
docs_per_cluster = Counter(clustering.labels_)
print("Número de clusters descubiertos: %d" % len(docs_per_cluster))

# De este modo obtenemos de nuevo el texto asociado a los términos (recordemos
# que con el vectorizador obtenemos una "traducción" totalmente numérica de los
# documentos).
#
terminos = vectorizador.get_feature_names()

# El atributo cluster_centers_ debería ser según la documentación un array
# n-dimensional (realmente bidimensional) pero por alguna razón retorna
# una matriz dispersa comprimida.
#
# Afortunadamente se puede convertir en un array n-dimensional
#
# El método argsort de numpy *no* ordena el array, retorna *otro* array de las
# mismas dimensiones que contiene *índices* en el orden en que deberían estar
# para que los *valores* del array (en este caso cluster_centers_) estuviera
# ordenado
#
#pprint.pprint(type(clustering.cluster_centers_))
cluster_centers = clustering.cluster_centers_.toarray()
#pprint.pprint(type(cluster_centers))

#indice_cluster_terminos = clustering.cluster_centers_.argsort()[:, ::-1]
indice_cluster_terminos = cluster_centers.argsort()[:, ::-1]

# Nos quedamos con los 50 clusters con más documentos y mostramos los 20
# términos más representativos de los mismos.
#
for (cluster_id, num_docs) in docs_per_cluster.most_common(50):
  print("Cluster %d (%d documentos):" % (cluster_id, num_docs), end='')
  for term_id in indice_cluster_terminos[cluster_id, :20]:
    print('"%s"' % terminos[term_id], end=' ')
  print()

"""Problemas:
* Affinity no funciona
"""