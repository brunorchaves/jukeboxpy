import RPi.GPIO as gpio
import os
import time
import subprocess
import threading 
from threading import Lock
import queue
from pathlib import Path, PurePosixPath

gpio.setwarnings(False)
# Configurando como BCM
gpio.setmode(gpio.BCM)

#Botao com pull-up interno
gpio.setup(23, gpio.IN, pull_up_down = gpio.PUD_UP)
# Configurando a direcao do Pino
gpio.setup(4, gpio.OUT)#FLAG 0
gpio.setup(24, gpio.OUT)#LED vermelho
gpio.setup(17, gpio.OUT)#FLAG 1
gpio.setup(27, gpio.OUT)#FLAG 2
gpio.setup(22, gpio.OUT)#LED azul gravacao
gpio.setup(25, gpio.OUT)#LED Verde gravacao

zero = 4
vermelho = 24
um = 17
dois = 27
azul = 22
verde = 25

#Inicia os LED's apagados
gpio.output(zero, gpio.LOW)
gpio.output(um, gpio.LOW)
gpio.output(dois, gpio.LOW)

#LED RGB com PWM
blue = gpio.PWM(azul, 100)
blue.start(100)
red= gpio.PWM(vermelho, 100)
red.start(0)
green = gpio.PWM(verde, 100)
green.start(0)

# Cria vetores de retorno
global resultado
resultado = [0,0,0,0]

#Usa fila em vez de vetor
q = queue.Queue()

global mutex
mutex = Lock()

#Caminho do FW
fwbasedir = Path('/media/pi/')
fwpath = ' '


#Flag de gravacao
gravando = 0

def gravaUSB0(q,fwpath):
    output0 = subprocess.check_output([ 'lpc21isp', '-bin', '-wipe', '-control','-verify', '-try3', fwpath, '/dev/ttyUSB0', '115200', '12000'])
    #print(output0)
    out0 = str(output0)
    contain0 =  out0.rfind("Verified")#Procura a str Verified para saber se a gravacao ocorreu com sucesso
    if contain0 != -1:
        USB0done = 1
    else:
        USB0done = -1  
    print(USB0done)
    mutex.acquire()
    q.put(USB0done)
    #resultado.insert(0,USB0done)
    mutex.release()
    print('end func1')

def gravaUSB1(q,fwpath):
    output1 = subprocess.check_output([ 'lpc21isp', '-bin', '-wipe', '-control','-verify', '-try3', fwpath, '/dev/ttyUSB1', '115200', '12000'])
    #print(output1)
    out1 = str(output1)
    contain1 =  out1.rfind("Verified")#Procura a str Verified para saber se a gravacao ocorreu com sucesso
    if contain1 != -1:
        USB1done = 2
    else:
        USB1done = -2
    print(USB1done)
    mutex.acquire()
    q.put(USB1done)
    #resultado.insert(0,USB0done)
    mutex.release()
    print('end func2')

def gravaUSB2(q,fwpath):
    output2 = subprocess.check_output([ 'lpc21isp', '-bin', '-wipe', '-control','-verify', '-try3', fwpath, '/dev/ttyUSB2', '115200', '12000'])
    #print(output2)
    out2 = str(output2)
    contain2 =  out2.rfind("Verified")#Procura a str Verified para saber se a gravacao ocorreu com sucesso
    if contain2 != -1:
        USB2done = 3
    else:
        USB2done = -3
    print(USB2done)
    mutex.acquire()
    q.put(USB2done)
    #resultado.insert(0,USB0done)    
    mutex.release()
    print('end func3')    

#Implementacao do PWM

def pwmGravacao(n):   
    dutcyc = 0
    s = 1
    n *= 20
    while n != 0:
        n -= 1
        blue.ChangeDutyCycle(dutcyc)
        time.sleep(0.05)
        dutcyc = dutcyc + 10*s
        if dutcyc == 100:
            s = (-1)
        elif dutcyc == 0:
            s =(1)
     
while True:

    time.sleep(0.2)

    if gpio.input(23) == gpio.LOW & gravando == 0:
        #Limpa o vetor das flags de retorno das funcoes
        i = 0
        for i in range(4):
            resultado[i]= False

        #Apaga LED's indicadores das placas
        gpio.output(zero, gpio.LOW)
        gpio.output(um, gpio.LOW)
        gpio.output(dois, gpio.LOW) 
        red.start(0)
        green.start(0)

        # Busca arwuivo de FW
        path = list(fwbasedir.glob('**/*.bin'))

        if len(path) == 1:
            fwpath = str(PurePosixPath(path[0]))

            #Flag gravacao
            gravando = 1

            #Cria as threads
            t0 = threading.Thread(target = gravaUSB0,args = (q,fwpath))
            t1 = threading.Thread(target = gravaUSB1,args = (q,fwpath))
            t2 = threading.Thread(target = gravaUSB2,args = (q,fwpath))

            #Inicializa as threads
            start = time.time()
            t0.start()
            t1.start()
            t2.start()
            #LED azul ligado enquanto grava
            red.start(0)
            
            #Espera 5 segundos para dar o retorno das threads
            #time.sleep(25)
            #PWM efeito gravacao
            n = 25
            pwmGravacao(n)

            t0.join()
            t1.join()
            t2.join()

            end = time.time()
            elapsedTime = (end - start)
            print(elapsedTime)
            
            j = 0
            for j in range(q.qsize()):
                temp = q.get()
                resultado[abs(temp)-1]= (temp > 0)

            j = 0
            for j in range(3):
                print(resultado[j])

            i = 0
            for i in range(3):
                if resultado[i] == False:
                    if i == 0:
                        t0._stop()
                    elif i == 1:
                        t1._stop()
                    elif i == 2:
                        t2._stop()

            #Printa o retorno das funcoes depois de executadas
            flag0 = resultado[0]
            flag1 = resultado[1]
            flag2 = resultado[2]

            if flag0 == True:
                gpio.output(zero, gpio.HIGH)#LED zero ligado se gravacao ocorreu corretamente
            else:
                gpio.output(zero,gpio.LOW)
            if flag1 == True:
                gpio.output(um, gpio.HIGH)#LED um ligado se gravacao ocorreu corretamente
            else:
                gpio.output(um,gpio.LOW)
            if flag2 == True:
                gpio.output(dois, gpio.HIGH)#LED dois ligado se gravacao ocorreu corretamente
            else:
                gpio.output(dois,gpio.LOW)   

            if(flag0 & flag1 & flag2  == True):#Gravacao ocorreu corretamente
                gravando = 0
                green.start(100) 
                blue.start(0) 
                red.start(0)
            if(flag0 & flag1 & flag2  == False):#Gravacao nao ocorreu com sucesso
                gravando = 0
                red.start(100)
                blue.start(0)
        
        elif len(path) != 1:
            #Pisca laranja 
            gravando = 0
            blue.start(0)
            red.start(95)
            green.start(65) 
    else:
        gravando = 0

# Desfazendo as modificacoes do GPIO
gpio.cleanup()
