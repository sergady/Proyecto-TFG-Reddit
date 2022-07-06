import csv
import io
from Train_clasificator import entrenar_clasificador
from Read_and_prepare_sample import removeSymbolsAndUrls

def tag_file():
    # opening the CSV file
    with open('data/expert_posts.csv', mode ='r', encoding="utf-8")as file:
        # reading the CSV file
        csvFile = csv.reader(file)
        clasificador = entrenar_clasificador(10, 10)
        results = list()

        # displaying the contents of the CSV file
        for line in csvFile[1:]:
            text = line[4] + " " + line[5]
            (etiqueta, probabilidad) = clasificador.predict(text)
            results.append(etiqueta[0] + "\t" + str(probabilidad[0]) + "\t" + text)
        

    results = "\n".join(results)
    io.open("results/classifier_results/result_maryland.txt", mode="w", encoding="utf-8").write(results)

def tag_file_by_user():
    # opening the CSV file
    with open('data/expert_posts.csv', mode ='r', encoding="utf-8")as file:
        # reading the CSV file
        csvFile = csv.reader(file)
        clasificador = entrenar_clasificador(10, 10)
        users = dict()

        # displaying the contents of the CSV file
        for line in csvFile:
            text = line[4] + " " + line[5]
            removeSymbolsAndUrls(text)
            (etiqueta, probabilidad) = clasificador.predict(text)
            
            if(users.get(line[0]) == None):
                users[line[0]] = [etiqueta[0]]
            else:
                users[line[0]].append(etiqueta[0])

    f = io.open("results/classifier_results/result_users_maryland.txt", mode="w", encoding="utf-8")
    for item in users.items():
        f.write(str(item))
        f.write("\n")

tag_file_by_user()