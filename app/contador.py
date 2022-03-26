from datetime import date

def dataAtual():
    data_atual = str(date.today())
    data = data_atual.split('-')
    return data[2] + '/' + data[1] + '/' + data[0]

def totPresenca(vet_presenca):
    cont = 0
    for n in vet_presenca:
        cont += int(n)
    return cont

def totFalta(vet_falta):
    cont = 0
    for n in vet_falta:
        cont += int(n)
    return cont
