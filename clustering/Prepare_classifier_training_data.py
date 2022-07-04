import io
import json
from Read_and_prepare_sample import removeSymbolsAndUrls
import Prepare_clasification_sample as sample_gen
from tqdm import tqdm


def load_post_control(post):
    post = json.loads(post)
    text = post["title"] + " " + post["self_text"]
    text = removeSymbolsAndUrls(text)

    terminos = text.split()
    
    texto = " ".join(terminos)
    texto = "__label__control " + texto
    return texto

def load_post_label(post):
    terminos = post.split()
    texto = " ".join(terminos)
    texto = "__label__" + topic +" " + texto
    return texto

[texts,tests] = sample_gen.return_train_sample()

documentos_entrenamiento = list()
documentos_test = list()

with tqdm(total=len(texts)) as barra:
    for topic in texts:
        for post in texts[topic]:
            documentos_entrenamiento.append(load_post_label(post))
        barra.update(1)

control_texts = io.open("data/random_posts_control.ndjson", mode="r", encoding="utf-8").readlines()

with tqdm(total=len(control_texts)) as barra:
    for post in control_texts:
        documentos_entrenamiento.append(load_post_control(post))
        barra.update(1)

documentos_entrenamiento = "\n".join(documentos_entrenamiento)

io.open("data/documentos_entrenamiento.txt", mode="w", encoding="utf-8").write(documentos_entrenamiento)

with tqdm(total=len(tests)) as barra:
    for topic in tests:
        for post in tests[topic]:
            documentos_test.append(load_post_label(post))
        barra.update(1)

control_test_texts = io.open("data/random_posts_control_test.ndjson", mode="r", encoding="utf-8").readlines()

with tqdm(total=len(control_test_texts)) as barra:
    for post in control_test_texts:
        documentos_test.append(load_post_control(post))
        barra.update(1)

documentos_test = "\n".join(documentos_test)
io.open("data/documentos_test.txt", mode="w", encoding="utf-8").write(documentos_test)