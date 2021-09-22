# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 10:33:02 2021

@author: Juan José Álvarez Eguis
"""

import serial
from time import time

class ASDSC:
    """
    A2DSC (Acquisition and storage of data by serial communication). Esta clase se encargar 
    de adquirir, guardar y mostrar los datos provenientes de una comunicación serial. 
    """
    
    #Constructor
    def __init__(self,frec,ventana,puerto,ciclos,direccion,numeroDatos,velocidadTransmisionDatos=57600,nombre='Data.txt'):
        self.__puerto=puerto
        self.__velocidadTransmisionDatos=velocidadTransmisionDatos
        self.serialPort=0.0
        self.message=""
        self.date=0.0
        self.data=[]
        self.countCiclos=0.0
        self.ciclos=ciclos
        self.__direccion=direccion
        self.nombre=nombre
        self.runTime=0
        self.nDatos=numeroDatos
        self.nDatosMuestra = ventana*frec
        
        
        
    #Inicializar puesto serial
    def initPuertoSerial(self):
        ser= serial.Serial(self.__puerto,self.__velocidadTransmisionDatos)
        ser.flushInput()
        self.serialPort=ser
        
    #Funcion para enviar dato por puerto serial
    def sendDataSerial(self,data,prefijo,sufijo):	
	    #Se envia el mensaje
        m=prefijo+ str(data) + sufijo
        m=m.encode('latin-1')
        self.serialPort.write(m)
    
    #Recibir datos por puerto serial
    def receiveDataSerial(self):
        LineBytes=self.serialPort.readline()
        line=LineBytes.decode('latin-1').strip()
        self.message=line
    
    
    #Acondicionamiento de senal
    def acondMensaje(dato1,dato2):
    	mensaje=dato1 + ";" + dato2
    	return mensaje
    
    #Recibir fecha
    def getFecha(self,fecha):
        for i in range(6):
            self.receiveDataSerial()
            fecha.append(self.message)
        return fecha
        
    
    #Acondicionar fecha con CSV
    def genFecha(self,fecha):
        date=fecha[0] + ";" + fecha[1] + ";" + fecha[2] + ";" + fecha[3] + ";" + fecha[4] + ";" + fecha[5]
        self.date=date
    
    	
    #Acondicionamiento de datos posterior al guardado
    def acondData(self,dato1,dato2):
        
        l1=len(dato1)
        l2=len(dato2)
        data=[]
        if l1<l2:
            l=l1
        else:
            l=l2
        for i in range(l):
		
            d=dato1[i][0:len(dato1[i])-2] + ";" + dato2[i][0:len(dato2[i])-2] + ";"
            data.append(d)
		
        self.data=data
    

    # Escribir en TXT conjunto de datos
    def writeTXT(self):
    	if self.countCiclos==1:
    		ref="w"
    	else:
    		ref="a"
    	file=open(self.__direccion + self.nombre,ref)
    	file.write("Ciclo: "+str(self.countCiclos)+"\n")
    	#file.write(self.date + "\n")
    	for i in self.data:
    		file.write(i +"\n")
    	file.close()
    
    #Actualizar nombre de archivo de datos
    def updateName(self,newName):
        self.nombre=newName
        
    #Proceso de A2DSC para tarjeta MM2
    def MM2(self):
        
        #Variables necesarias
        prefijo="HDTAC+"
        sufijo="\r\n"
        
        #Inicialización de tarjeta MM2
        self.initPuertoSerial()
        self.sendDataSerial('CYC='+str(self.ciclos),prefijo,sufijo)
        for i in range(2):
            self.receiveDataSerial()
        start_time = time()
        mainFlag=True
        print("Inicio del proceso de medición")
        self.sendDataSerial('STR',prefijo,sufijo)
        #Ejecución de ciclos
        while mainFlag:
            dataFlag=False
            self.receiveDataSerial()
            if self.message=="MM2>> OK: Modo de operación offline iniciado." or (self.countCiclos>0):
                self.countCiclos=self.countCiclos+1
                print("Ciclo: " + str(self.countCiclos))
                
                while not dataFlag:
                    if self.countCiclos==1:
                        self.receiveDataSerial()
                        print(self.message)
                    if self.message == "Envio de datos":
                        
                        #fecha=[]
                        #self.genFecha(self.getFecha(fecha))
                        dato1=[]
                        dato2=[]
                        count = 1
                        while  not dataFlag:
                            self.receiveDataSerial()
                            if self.message == "Envio de datos finalizado":
                                dataFlag=True
                                
                                
                            else:
                                
                                if len(self.message)>1:
                                    if self.message[-1]=="0":
                                        dato1.append(self.message)
                                    if self.message[-1]=="1":
                                        dato2.append(self.message)
                self.acondData(dato1,dato2)
                self.writeTXT()
                if self.countCiclos==self.ciclos:
                    mainFlag=False
                    self.countCiclos=0
                    self.serialPort.close()
                    self.runTime = time() - start_time
                    print("Tiempo de ejecucion: " + str(self.runTime) + " segundos")
                    print("Tiempo promedio por ciclo: "+str(self.runTime/self.ciclos)+" segundos")
                
                
        
    
        
        
        
    