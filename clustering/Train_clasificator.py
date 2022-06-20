import io
import json
from Read_and_prepare_sample import removeSymbolsAndUrls
import fasttext
import Prepare_clasification_sample as sample_gen
from tqdm import tqdm


texts = sample_gen.return_train_sample()

documentos_entrenamiento = []

with tqdm(total=len(texts)) as barra:
    for topic in texts:
        for post in texts[topic]:
            terminos = post.split()
            
            texto = " ".join(terminos)
            texto = "__label__" + topic +" " + texto

            documentos_entrenamiento.append(texto)
        barra.update(1)

control_texts = io.open("data/random_posts_control.ndjson", mode="r", encoding="utf-8").readlines()

with tqdm(total=len(control_texts)) as barra:
    for post in control_texts:
        post = json.loads(post)
        text = post["title"] + " " + post["self_text"]
        text = removeSymbolsAndUrls(text)

        terminos = text.split()
        
        texto = " ".join(terminos)
        texto = "__label__control " + texto

        documentos_entrenamiento.append(texto)
        barra.update(1)

documentos_entrenamiento = "\n".join(documentos_entrenamiento)

f = io.open("data/documentos_entrenamiento.txt", mode="w", encoding="utf-8").write(documentos_entrenamiento)