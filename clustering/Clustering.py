from numpy import empty_like
from Read_and_prepare_sample import storeTextsInArray
import sys
from datetime import datetime

file_name = 'results/result_'+str(datetime.now().__str__().replace(" ", "_").replace(":","-")[:-7])+'.txt'
sys.stdout = open(file_name, 'w')

stop_words_file = "static_data/stopWords.txt"

[preprocessedTexts, sample_seed] = storeTextsInArray()
print("Texts loaded!")
print("Semilla de sample_file.txt: " + sample_seed)

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
vectorizador = TfidfVectorizer(encoding="iso-8859-1", lowercase=True, ngram_range=(1, 1), max_features=1500)

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
num_clusters = 30

# Se va a usar el algoritmo k-means en búsqueda de 6 clusters
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

# Creates the dictionary of stop words we not need
# Usamos el diccionario para sacar las palabras vacías
def createStopWordsDictionary(words_file):
    with open(words_file) as stop_words:
        stop_words_list = stop_words.read().split("\n")
        stop_words_dictionary = {}
        for stop_word in stop_words_list:
            stop_words_dictionary.update({stop_word: True})
    return stop_words_dictionary

stop_words_dictionary = createStopWordsDictionary(stop_words_file) #stopwords

# Nos quedamos con los num_clusters clusters y mostramos los 25
# términos más representativos de los mismos.
#
terminos_representativos = 25

print("Método K-means")
for (cluster_id, num_docs) in docs_per_cluster.most_common(num_clusters):
  print("Cluster %d (%d documentos):" % (cluster_id, num_docs), end='')
  i = cluster_id
  while i < len(indice_cluster_terminos):
    if( not stop_words_dictionary.get(terminos[i], False)): # Check if it is an empty word
      print('"%s"' % terminos[i], end=' ')
      i += 1
      
  print()

sys.stdout.close()
"""## Aplicación de Afinnity Propagation

Ahora vamos a usar el método de affinity propagation.
La mayor ventaja de este frente a K-means es que no hay que especificar el número de clusters que se espera recibir.


from sklearn.cluster import AffinityPropagation

# Obsérvese que no es preciso indicar el número de clusters
#
clustering = AffinityPropagation(max_iter=100, verbose=True)

# Se aplica el algoritmo seleccionado a la matriz que representa el corpus
#
clustering.fit(matriz)

#Ahora para observar los resultados procedemos a hacer la silueta igual que con k-means.

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

# Nos quedamos con los 25 clusters con más documentos y mostramos los 10
# términos más representativos de los mismos.
#
for (cluster_id, num_docs) in docs_per_cluster.most_common(25):
  print("Cluster %d (%d documentos):" % (cluster_id, num_docs), end='')
  for term_id in indice_cluster_terminos[cluster_id, :10]:
    print('"%s"' % terminos[term_id], end=' ')
  print()
"""