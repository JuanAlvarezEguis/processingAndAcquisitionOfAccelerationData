# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 20:10:20 2021

@author: Juan José Álvarez Eguis
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

class ATIVD:
    """
    ATIVD (Analysis, transformation and illustration of vibration data). En 
    esta clase se realizan las transformadas necesarias para realizar los
    procesos de análisis y se grafican sus resultados. Los análisis que se 
    realizan son enfocados al desarrollo de labores de monitoreo de condición. 
    
    Nota: Los datos deben seguir el modelo de almacenamiento de ASDSC.
    """
    
    def __init__(self,nombreDocumento,FrecuenciaMuestreo,VentanaMedicion,ciclo):
        self.nombre=nombreDocumento
        self.fm=FrecuenciaMuestreo                       #En Hz
        self.vm=VentanaMedicion                          #En segundos
        self.data=[]
        self.ac=[]                                       #En m/s^2
        self.ts=1/self.fm
        self.time=[]
        self.ciclo=ciclo
        self.fft=[]
        self.fftMag=[]
        self.frq=[]
        self.velfft=[]
        self.velfftMag=[]
        self.ceps=[]
        
    #EXTRACCION
        
    #Extraer datos de archivo .txt
    def extraerDatosTxt (self):
        try:
            file= open(self.nombre,'r')
            self.data=file.readlines()
        except FileNotFoundError:
            print(self.nombre + ': ¡ARCHIVO INEXISTENTE!')
        file.close()

    #Se organizan los datos de cada acelerometro por ciclo en un diccionario
    def acondicionamientoDatos(self):
    
        ac1={}
        ac2={}
        d1=[]
        d2=[]
        flagMed=False
        cont=0
        n=0
        for i in self.data:
            label=i.split(':')[0]
            if label=='Ciclo':
                n=float(i.split(':')[1].rstrip().split(' ')[1])
                flagMed=False
                cont=1
                if n>1:
                    ac1[n-1]=d1
                    ac2[n-1]=d2
                    d1=[]
                    d2=[]
            else:
                if cont==2:
                    flagMed=True
                    cont=0
                
                if cont==1:
                    cont=2
            if flagMed:
                Med=i.split(';')
                d1.append(float(Med[0]))
                d2.append(float(Med[1]))
        ac1[n]=d1
        ac2[n]=d2
        self.ac=[ac1,ac2]


    #TRANSFORMADAS

    #Se calcula la FFt de los datos solo la magnitud
    def dataFFt(self,acelerometro):
        fft=np.fft.fft(self.ac[acelerometro][self.ciclo])
        fftMag=abs(fft)
        self.fft=fft
        self.fftMag=fftMag
        
    #Se calcula la integral de la señal
    def integral(self):
        vel=[]
        velMag=[]
        for i in range(1,len(self.frq)):
            vel.append(self.fft[i]/(2*np.pi*1j*self.frq[i]))
            velMag.append(abs(self.fft[i]/(2*np.pi*1j*self.frq[i])))
            print('frq: '+str(round(self.frq[i],2))+'; vel: '+str(abs(self.fft[i]/(2*np.pi*1j*self.frq[i]))))
        self.velfft=vel
        self.velfftMag=velMag
    
    #Análisis cepstrum
    def cepstrumR(self):
        fftReal=[]
        for i in self.fft:
            fftReal.append(np.log(abs(i)))
        ceps=abs(np.fft.ifft(fftReal))
        for i in range(0,len(ceps)-1):
            print('Time: '+str(round(1000*self.time[i],4))+' Quefrency: '+str(abs(ceps[i])))
        self.ceps=ceps
    
    #GRAFICAS

    #Se grafica en el dominio del tiempo los datos 
    def gDataTime(self,acelerometro):
        self.time=np.arange(0,len(self.ac[acelerometro][self.ciclo])/self.fm,self.ts)
        plt.plot(self.time,self.ac[acelerometro][self.ciclo])
        plt.xlabel('Time [s]')
        plt.ylabel('Aceleration [m/s^2]')
        plt.title('Comportamiento temporal')
        plt.grid()
        plt.show

    #Se grafica la FFT en magnitud
    def gDataFrec(self,limF):
        #n= len(self.fftMag)
        #k= np.arange(n)
        #self.frq=self.fm*k/n
        
        frqTry=self.fm*(np.arange(50000)/50000)
        self.frq=frqTry[:len(self.fftMag)]
        
        plt.plot(self.frq,self.fftMag)
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Magnitude')
        plt.title('Comportamiento frecuencial')
        plt.xlim(-10,limF)
        plt.grid()
        plt.show

    #Se grafica la FFT en magnitud de la velocidad
    def gDataFrecVel(self,limFMin,limFMax,limFMiny,limFMaxy,lin,frecInte,frecInte2):
        n= len(self.velfftMag)
    
        plt.plot(self.frq[1:],self.velfftMag)
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Magnitude')
        plt.title('Comportamiento frecuencial')
        plt.xlim(limFMin,limFMax)
        plt.ylim(limFMiny,limFMaxy)
        if lin:
            for i in range(0,8):  
                plt.axvline(x=i*frecInte2,ymin=0,ymax=max(self.velfftMag),linewidth=1,linestyle='--',color='red')
                plt.axvline(x=i*frecInte,ymin=0,ymax=max(self.velfftMag),linewidth=1,linestyle='--',color='orange')
        plt.grid()
        plt.show
    
    def gCepstrum(self,limFMin,limFMax,limFMiny,limFMaxy,lin,frecInte,frecInte2):
        plt.plot(1000*self.time[2:],self.ceps[2:])
        plt.xlabel('Time [ms]')
        plt.ylabel('Spectral Variation [dB]')
        plt.title('Análisis Cepstrum ')
        plt.xlim(limFMin,limFMax)
        plt.ylim(limFMiny,limFMaxy)
        plt.grid()
        plt.show



