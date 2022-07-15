from numpy import empty
import pygame
import subprocess
import threading 
import time
pygame.init()
import RPi.GPIO as gpio

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)

#Botao com pull-up interno
gpio.setup(3, gpio.IN) #esc0
gpio.setup(5, gpio.IN) #esc1
gpio.setup(7, gpio.IN) #esc2
gpio.setup(11, gpio.IN) #esc3
gpio.setup(13, gpio.IN) #tocar



def tocarMusica(codigo):
    global musica_Tocando , parar

    if(codigo == 1):
        print("musica ABBA")
        pygame.mixer.music.load('Abba_DancingQueen.mp3')
        pygame.mixer.music.play(0)
    elif(codigo == 2):
        print("musica CB")
        pygame.mixer.music.load('ChuckBerryJohnnyBGoode.mp3')
        pygame.mixer.music.play(0)
    elif(codigo == 3):
        print("musica AHA")
        pygame.mixer.music.load('ahaTakeOnMe.mp3')
        pygame.mixer.music.play(0)
    elif(codigo == 4):
        print("musica LZ")
        pygame.mixer.music.load('GoingToCalifornia.mp3')
        pygame.mixer.music.play(0)
    else:
        pygame.mixer.music.stop()

tocando = 0

while(1):

    start = time.time()
    if( gpio.input(3) == gpio.HIGH and gpio.input(5) == gpio.LOW and 
        gpio.input(7) == gpio.LOW and gpio.input(11) == gpio.LOW):
        codigo =1 
    elif ( gpio.input(3) == gpio.LOW and gpio.input(5) == gpio.HIGH and
        gpio.input(7) == gpio.LOW and gpio.input(11) == gpio.LOW):
        codigo =2 
    elif ( gpio.input(3) == gpio.HIGH and gpio.input(5) == gpio.HIGH and 
        gpio.input(7) == gpio.LOW and gpio.input(11) == gpio.LOW):
        codigo =3 
    elif ( gpio.input(3) == gpio.LOW and gpio.input(5) == gpio.LOW and
        gpio.input(7) == gpio.HIGH and gpio.input(11) == gpio.LOW):
        codigo =4 
    else:
        codigo = 0
    if(gpio.input(13) == gpio.HIGH):
        
        if(tocando == 0):
            tocarMusica(codigo)
            print("tocando musica ")
            print(codigo)
            tocando = 1 

    elif(gpio.input(13) == gpio.LOW):

        pygame.mixer.music.stop()
        print("musica parada")
        tocando = 0

