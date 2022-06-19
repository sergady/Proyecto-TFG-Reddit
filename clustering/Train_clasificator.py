import io
import fasttext
import Prepare_clasification_sample as sample_gen
from tqdm import tqdm


texts = sample_gen.return_train_sample()
print(len(texts))

documentos_entrenamiento = []

with tqdm(total=len(texts)) as barra:
    for topic in texts:
        for post in texts[topic]:
            terminos = post.split()
            
            texto = " ".join(terminos)
            texto = "__label__" + topic +" " + texto

            documentos_entrenamiento.append(texto)
        barra.update(1)

documentos_entrenamiento = "\n".join(documentos_entrenamiento)

f = io.open("data/documentos_entrenamiento.txt", mode="w", encoding="utf-8")
f.write(documentos_entrenamiento)