from numpy import empty
import pygame
import subprocess
import threading 
import time
pygame.init()


Iniciar = 0
B_coletar = 0
B_moeda = str(empty)
Dinheiro = 0
RESET = 0

Estado_iniciar = 0
Estado_coleta = 1
Estado_compara = 2
Estado_escolheMusica = 3
Estado_reproduzir = 4
Estado_pause = 5

estado  = 0

codigoMusica = 0
musica_Tocando = 0
# def escolhaAcao(coringa):
#     if(coringa = 'R' ):
#         RESET = 1
#     elif(coringa = 'M'):
#         B_Moeda = 'M'



def tocarMusica(codigo):
    global musica_Tocando , parar

    if(codigo == '1'):
        pygame.mixer.music.load('Cochise.mp3')
        pygame.mixer.music.play(0)
    elif(codigo == '2'):
        pygame.mixer.music.load('Cochise.mp3')
        pygame.mixer.music.play(0)
    elif(codigo == '3'):
        pygame.mixer.music.load('Cochise.mp3')
        pygame.mixer.music.play(0)
    elif(codigo == '4'):
        pygame.mixer.music.load('GoingToCalifornia.mp3')
        pygame.mixer.music.play(0)

while(1):

    start = time.time()

    if estado == Estado_iniciar: 
        Iniciar  = int(input("Iniciar?"))
        if(Iniciar == 1):
            estado = Estado_coleta

    elif estado == Estado_coleta:
        B_coletar  = int(input("Coletar dinheiro?")) 
        if(B_coletar == 1):
            B_Moeda = input("Aperte M para colocar a moeda ") 
            if(B_Moeda == 'M'):
                Dinheiro += 1
                B_Moeda = ' '
                
        if(B_coletar == 0):
            estado = Estado_compara

    elif estado == Estado_compara: 
        if(Dinheiro>=2):
            print("Você colocou dinheiro suficiente ")
            estado = Estado_escolheMusica 
        else:
            print("Coloque mais dinheiro ")
            estado = Estado_coleta


    elif estado == Estado_escolheMusica: 
        print("Escolha a musica: ") 
        print("1- Alive Pearl Jam ") 
        print("2 - Stairway to heaven - LZ: ") 
        print("3 - Aqualung JT ") 
        print("4 - Cochise audioslave ") 
        codigo = input("Codigo Musica ") 
        t0 = threading.Thread(target = tocarMusica,args = (codigo, ))
        # tocarMusica(codigo)
        t0.start()
        estado = Estado_pause

    elif estado == Estado_pause: 
        print("tocando musica")
        parar = 0
        parar = input("parar?")
        if(parar == '1'):
            pygame.mixer.music.stop()
            RESET = 1 
            


    if(RESET):
        estado = Estado_iniciar
        #resetar todas as variaveis
        musica_Tocando = 0
        RESET = 0
        codigoMusica = 0
        parar = 0
