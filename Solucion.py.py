#!/usr/bin/env python
# coding: utf-8

# In[107]:


import csv, json, math
##FUNCIONES PARA ARCHIVO CSV
#funcion para saber si sube o baja la accion diaramente
def comportamiento(str_open, str_close):
    close = eval(str_close)
    open = eval(str_open)
    if close - open > 0:
        comportamiento = "SUBE"
    if close - open < 0:
        comportamiento = "BAJA"
    if close - open == 0:
        comportamiento = "ESTABLE"
    return comportamiento
#funcion para calcular la diferencia absoluta renglon a renglon
def diferencia(str_open, str_high):
    high = eval(str_high)
    open = eval(str_open)
    comportamiento = abs(open - high)
    return comportamiento

##FUNCIONES PARA ARCHIVO JSON
#Exportar el archivo json:
def creador_json(lista_valores):
    #aca se van a definir las claves de el diccionario
    claves = ["date_lowest_close","lowest_close","date_highest_open","highest_open","mean_volume", "date_smallest_difference", "smallest_difference"]
    #crear un diccionario vacio 
    diccionario_json = {}
    #hacer una combinacion de renglon por renglon para generar el diccionario
    for tupla in zip(claves, lista_valores):
        #colocar los renglones del diccionario uno para cada clave
        diccionario_json[tupla[0]] = tupla[1]
    #convertir los datos del diccionario en datos compatibles con json    
    objeto_json = json.dumps(diccionario_json)
    #escribir el archivo con los datos
    with open("detalles.json", "w") as archivo_json:
        archivo_json.write(objeto_json)
        
#tomar cada renglon e irlo midiendo para encontrar los datos solicitados:
#el resultado sale de esta tabla:
#lista_valores = [0-fecha_close_bajo, 1-str_close_bajo, 2-fecha_open_alto, 3-str_open_alto, 4-prom_vol, 5-fecha_dif_menor, 6-dif_menor]
#linea         = [0-Date, 1-Open, 2-High, 3-Low, 4-Close, 5-Adj Close, 6-Volume]
def valores_json(linea, lista_valores):
    #print(linea, values_list)
    #"date_lowest_close"
    #Close más bajo y la fecha
    if eval(linea[4]) < lista_valores[1]:
        lista_valores[0] = linea[0]
        lista_valores[1] = eval(linea[4])
    #Open más alto y su fecha
    if eval(linea[1]) > lista_valores[3]:
        lista_valores[2] = linea[0]
        lista_valores[3] = eval(linea[1])
    #Sumar los volumenes para calcular el promedio:
    lista_valores[4] = lista_valores[4] + eval(linea[6])
    #Diferencia absoluta menor y su fecha
    open = eval(linea[1])
    high = eval(linea[2])
    diferencia_absoluta = abs(open - high)
    #print(diferencia_absoluta)
    if diferencia_absoluta < lista_valores[6]:
        lista_valores[5] = linea[0]
        lista_valores[6] = diferencia_absoluta
    #retorno final del las operaciones para el archivo json
    return lista_valores
    
with open("TWITTER.csv","r") as archivo, open("analisis_archivo.csv","w", newline = '') as archivo_nuevo:
    archivo_leido = csv.reader(archivo)
    #codigo para evitar la lectura del encabezado:
    next(archivo_leido) 
    #for row in archivo_leido:
    #    print(row)
    archivo_exportar = csv.writer(archivo_nuevo, delimiter = " ")
    #redaccion del encabezado nuevo
    encabezado_nuevo_csv = ["Fecha", "Comportamiento_de_la_accion", "Diferencia_absoluta_open-high"]
    #Agregar el encabezado nuevo a la fila 1 del archivo nuevo
    archivo_exportar.writerow(encabezado_nuevo_csv)
    #valores iniciales para que la funcion valores_json tenga de donde comparar:
    values_list = ["2022-06-29", 111.11, "2022-06-29", 11.11, 0, "2022-06-29", 100000000000]
    #contador para el promedio
    contador = 0
    for renglon in archivo_leido:
        #Leer renglon por renglon
        renglon_a_escribir = [renglon[0], comportamiento(renglon[1], renglon[4]), diferencia(renglon[1], renglon[2])]       
        #exportar el renglon al csv
        archivo_exportar.writerow(renglon_a_escribir)
        #Leer cada renglon para las comparaciones y hacer el json (Values_list es una funcion)
        values_list = valores_json(renglon, values_list)
        contador += 1
        #Exportar archivo json
    #para calcular el promedio
    #print(contador)
    values_list[4] = values_list[4] / contador
    creador_json(values_list)
