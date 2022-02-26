from datetime import datetime
import os
import re
import json
from unicodedata import normalize
import random
import pandas as pd
colors = {
    'verde' : '\033[92m',
    'amarillo': '\033[93m',
    'blanco' : '\033[97m',
    'ENDC' : '\033[0m'

}
def letras_colores(letra,color):
    return colors[color] + letra + colors['ENDC']

teclado = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','ñ','z','x','c','b','n','m']
salto = 0
palabrasJson = []
#leer datos de archivos txt
url = "https://raw.githubusercontent.com/javierarce/palabras/master/listado-general.txt"
data = pd.read_csv(url, on_bad_lines='skip', header= None, names = ["Palabras"])
#seleccionar las 365 palabras de manera aleatoria y que tenga tamaño 5
selecionados = data[(data.Palabras.str.len() == 5)].sample(365)
selecionados.reset_index()
#Pasar el df a una lista
palabras = selecionados["Palabras"].tolist()
fecha = str(datetime.today())
#Quitar las tildes
for i in range(len(palabras)):
    palabras[i] = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", palabras[i]), 0, re.I
    )
    palabras[i] = normalize('NFC', palabras[i])
adivino = False
palabra = random.choice(palabras)
with open('palabras_por_fecha.json', 'a') as file:
    json.dump(({'fecha':fecha,'palabras' : palabra}) , file, indent=4)
os.system('cls')
print(palabra)
board = []
intentos = 0
letrasCorrectas = []
for i in range(6):  
    #Interar 5 veces '_' para poder insertarlo en la lista
        board.append(['_' for l in range(5)])


while (not adivino) and (intentos < 6):
#Regla: No permitir palabras con una longitud diferente de 5
    palabraUsuario = input("Ingrese una palabra de 5 caracteres: ")
    palabrasJson.append(palabraUsuario)
    while len(palabraUsuario) != 5:
        print("palabra incorrecta")
        palabraUsuario = input("Ingrese una palabra de 5 caracteres: ")
        palabrasJson.append(palabraUsuario)
    os.system('cls')
    if palabra == palabraUsuario:
        adivino = True
        #iterar la palabra mientras la asigno
        board[intentos] = ["=" + letras_colores(l,'amarillo') + "=" for l in palabraUsuario]
        for i in range(len(palabraUsuario)):
            for k,j in enumerate(teclado):
                if j.find(palabraUsuario[i]) > 0:
                    teclado[k] = "=" + letras_colores(palabraUsuario[i], 'amarillo') + "="
    else:
        for i in range(5):
            if palabraUsuario[i] == palabra[i]:
                letrasCorrectas.append("="+letras_colores(palabraUsuario[i], 'amarillo')+"=")
                for k,j in enumerate(teclado):
                    if j.find(palabraUsuario[i]) >= 0:
                        teclado[k] = ("=" + letras_colores(palabraUsuario[i], 'amarillo') + "=")

            elif palabraUsuario[i] in palabra:
                letrasCorrectas.append("<"+ letras_colores(palabraUsuario[i], 'verde')+">")
                for k,j in enumerate(teclado):
                    if j.find(palabraUsuario[i]) >= 0:
                        teclado[k] = ("<" + letras_colores(palabraUsuario[i], 'verde') + ">")
            else:
                letrasCorrectas.append(">"+ letras_colores(palabraUsuario[i], 'blanco')+"<")
                for k,j in enumerate(teclado):
                    if j.find(palabraUsuario[i]) >= 0:
                         teclado[k] = (">" + letras_colores(palabraUsuario[i], 'blanco')  + "<")
        board[intentos] = letrasCorrectas
        letrasCorrectas = []

    for i in range(6):
        for k in range(5):
            print("+--", end= " ")
        print()
        print( "|" + str(" | ".join(board[i]) + "|"))
    intentos += 1
    print()

    for i in range(len(teclado)):
        if salto != 9:
            salto += 1
            print("[" + teclado[i] + "]", end ="")
        else:
            print(teclado[i])
            salto = 0
            print()
    print()


with open('partidas.json', 'a') as file:
    json.dump(({'fecha':fecha,'palabras' : palabra, 'intentos' : palabrasJson}) , file, indent=4)

print("FIN DEL JUEGO")
