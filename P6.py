# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 09:00:16 2021

@author: Juan José Álvarez Eguis
"""

import ASDSC 

"""
En este código se realiza una ciclos de medición con una cantidad de 
mediciones determinada. El objetivo de este código es el realizar una prueba del algoritmo 
de la clase ASDS con la tarjeta MM2. 
"""

while True:
    if __name__=="__main__":
        #Inicialización
        puerto='COM3'
        direccion="C:/Users/Asus/OneDrive - Universidad EIA/Trabajo de grado/Laboratorios/Sistemas mecánicos 2/Data/"
        nombreDoc="PruebaVelocidad.txt"
        velocidad=115200
        frec = 10000
        ventana = 5
        acMed=ASDSC.ASDSC(frec,ventana,puerto,3,direccion,100007,velocidad,nombreDoc)
        #Toma de datos
        acMed.MM2()
        break
        