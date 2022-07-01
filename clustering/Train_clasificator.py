import fasttext

clasificador = fasttext.train_supervised("documentos_entrenamiento.txt")

print("Entrenado.")