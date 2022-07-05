import fasttext
from tqdm import tqdm
import io

def entrenar_clasificador(epoch, minCount):
    print("Entrenando.")
    return fasttext.train_supervised("data/documentos_entrenamiento.txt", epoch=epoch, minCount= minCount)

def test_clasificador(epoch, minCount): 
    clasificador = entrenar_clasificador(epoch, minCount)
    print("Entrenado.")
    test_lines = io.open("data/documentos_test.txt", mode="r", encoding="utf-8").readlines()

    resultados = list()
    aciertos = fallos = control = 0

    with tqdm(total=len(test_lines)) as barra:
        for line in test_lines[:-1]:
            # Extract label and prepare text
            text = line.split()
            label = text.pop(0)
            text = " ".join(text)

            (etiqueta, probabilidad) = clasificador.predict(text)

            etiqueta = etiqueta[0]
            
            resultados.append(label + " " + etiqueta)

            if(label == etiqueta):
                aciertos +=1
                if(label == "__label__control"):
                    control +=1
            else:
                fallos +=1

            barra.update(1)

    resultados = "\n".join(resultados)
    result = io.open("results/classifier_results/result.txt", mode="w", encoding="utf-8")
    result.write(resultados)
    result.write("Epoch = " + str(epoch) + ", minCount = " + str(minCount) + ", Aciertos = " + str(aciertos-control) + ", Fallos = " + str(fallos) + ", Control = " + str(control))
    result.write("Precisión: " + str(round( aciertos/(fallos+aciertos) ,4)*100) + " %")
    
    print()
    print("Finished!")
    print("Epoch = " + str(epoch) + ", minCount = " + str(minCount) + ", Aciertos = " + str(aciertos-control) + ", Fallos = " + str(fallos) + ", Control = " + str(control))
    print("Precisión: " + str(round( aciertos/(fallos+aciertos) ,4)*100) + " %")


test_clasificador(10, 10)