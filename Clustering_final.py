from sklearn.feature_extraction.text import TfidfVectorizer
from numpy import empty_like
from ReadAndPrepareSample import preprocessTexts
import sys
from datetime import datetime


def setFileOutput():
    file_name = 'results/result_' + \
        str(datetime.now().__str__().replace(
            " ", "_").replace(":", "-")[:-7])+'.txt'
    sys.stdout = open(file_name, 'w')


preprocessedTexts = preprocessTexts()  # dict {listTexts:post_ids}
preprocessedTextsIds = preprocessedTexts["post_ids"]
preprocessedTexts = preprocessedTexts["listTexts"]
print("Texts loaded!")


"""# Clustering
Ahora con los textos preprocesados y en un único array, vamos a proceder a hacer el clustering. Así comprobaremos si es capaz de distinguir los diferentes idiomas que hay.

## Vectorizado de los textos

Antes de proceder al clustering, hay que vectorizar los datos para obterner matrices de frecuencia. Procedemos a vectorizar el corpus con la herramienta TfidfVectorizer:
"""

# Se va a usar un vectorizador que ponderará los términos mediante tf·idf,
# pasará los textos a minúsculas y usará unigramas y bigramas
# truncando, además, el vocabulario en los 1500
# términos más frecuentes.
#
vectorizador = TfidfVectorizer(encoding="utf-8", lowercase=True, ngram_range=(1, 2),
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
# No entiendo el outcome??
def getIdentifiers(): 
  for i in range(len(clustering.labels_)):
      print(preprocessedTextsIds[i],clustering.labels_[i])

exit()