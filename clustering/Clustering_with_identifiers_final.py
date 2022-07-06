from sklearn.feature_extraction.text import TfidfVectorizer
from Read_and_prepare_sample import preprocessTexts
import sys
from datetime import datetime


def setFileOutput():
    file_name = 'results/result_' + \
        str(datetime.now().__str__().replace(
            " ", "_").replace(":", "-")[:-7])+'.txt'
    sys.stdout = open(file_name, 'w')

setFileOutput()
preprocessedTexts = preprocessTexts()  # dict {listTexts:post_ids}
preprocessedTextsIds = preprocessedTexts["post_ids"]
preprocessedTextsSubreddits = preprocessedTexts["subreddits"]
preprocessedTexts = preprocessedTexts["listTexts"]

### Solo quería ver que las listas contuviesen el mismo número de elementos
##print(len(preprocessedTexts),len(preprocessedTextsIds),len(preprocessedTextsSubreddits))

print("Texts loaded!")

"""# Clustering
Ahora con los textos preprocesados y en un único array, vamos a proceder a hacer el clustering. Así comprobaremos si es capaz de distinguir los diferentes idiomas que hay.

## Vectorizado de los textos

Antes de proceder al clustering, hay que vectorizar los datos para obterner matrices de frecuencia. Procedemos a vectorizar el corpus con la herramienta TfidfVectorizer:
"""

# Se va a usar un vectorizador que ponderará los términos mediante tf·idf,
# pasará los textos a minúsculas y usará unigramas y bigramas
# truncando, además, el vocabulario en los 15000
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
terminos = vectorizador.get_feature_names_out()

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
representative_terms = 20

print("Metodo K-means")

# Necesitamos una lista para "anotar" los clusters "interesantes", es decir,
# con un número mínimo de documentos.
#
# Además, no solo vamos a imprimir los términos sino también almacenarlos en
# otra estructura de datos...
#

num_min_docs = 5

clusters_ids_interesantes = []

clusters_vs_terminos = {}

for (cluster_id, num_docs) in docs_per_cluster.most_common(num_clusters):
    # No nos interesan clusters con menos de 5 documentos
    #
    if num_docs>=num_min_docs:
        clusters_ids_interesantes.append(cluster_id)

        clusters_vs_terminos[cluster_id] = []

        print("Cluster %d (%d documentos):" % (cluster_id, num_docs), end='')
        for term_id in indice_cluster_terminos[cluster_id, : representative_terms]:
            print('"%s"' % terminos[term_id], end=' ')
            clusters_vs_terminos[cluster_id].append(terminos[term_id])

        print()

# Vamos a crear un diccionario donde anotaremos para cada cluster los subreddits
# que aparecen, puesto que con cada documento aparecerá su subreddit sabremos
# también el número de posts de cada subreddit en cada cluster
#
clusters_vs_subreddits = {}

for i in range(len(clustering.labels_)):
    cluster_label = clustering.labels_[i]

    if cluster_label in clusters_ids_interesantes:
        subreddit = preprocessedTextsSubreddits[i]

        if cluster_label in clusters_vs_subreddits:
            if subreddit in clusters_vs_subreddits[cluster_label]:
                clusters_vs_subreddits[cluster_label][subreddit] += 1
            else:
                clusters_vs_subreddits[cluster_label][subreddit] = 1
        else:
            clusters_vs_subreddits[cluster_label]={}
            clusters_vs_subreddits[cluster_label][subreddit]=1

# Necesitamos ordenar los subreddits por cluster para que no salgan en cualquier
# orden sino de mayor a menor frecuencia de aparición
#
import operator

for cluster_label in clusters_vs_subreddits:
    current_subreddits = clusters_vs_subreddits[cluster_label]
    current_subreddits = dict(sorted(current_subreddits.items(), key=operator.itemgetter(1),reverse=True))

    print(cluster_label)
    print(clusters_vs_terminos[cluster_label])
    print(current_subreddits)
    print()

# Ejemplo de cómo obtener los identificadores *reales* del cluster al que
# pertenece cada documento.
#
# El atributo labels_ va a tener en este caso 5000 etiquetas, una por cada documento
#
def getIdentifiers():
  for i in range(len(clustering.labels_)):
      print(preprocessedTextsIds[i],clustering.labels_[i])

exit()