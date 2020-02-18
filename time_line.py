#!/usr/bin/env python3
#
# подключаем модуль для работы с EV3
from ev3dev.ev3 import *
# подключаем библиотеку работы со временем
import time
from os import system
#большой шрифт для LCD EV3
os.system('setfont Lat15-TerminusBold32x16')

# объект для работы с кнопками на блоке
btn = Button()

# список портов для просмотра
input_ports = ['in1','in2','in3','in4']

# IR = InfraredSensor("in4")

for port in  input_ports:
    try:
        US = UltrasonicSensor(port)
        test = US.value()
    except Exception:
        # print( port, " no" )
        pass
    else:
        print( port, " USonic " )
        break

# print( "port :",port,"-", US.value() )

# переменная для мерцания (смены яркости диодов)
i=0

print("loaded")

#пока не нажата кнопка "назад"
while not btn.backspace:

    Sound.tone([(500,1000,40)]).wait()
    Sound.speak("ready to Start").wait()

    #
    #  Первый режим:
    #  Ожидаем появление робота в зоне старта
    #  ( в зоне действия ультра-звукового датчика )
    #
    #  бопьше 30см  отсекаем      (300мм)
    while US.value()>=300:
        time.sleep(0.01)
        # ждем старта - мерцаем зеленым
        Leds.set_color(Leds.RIGHT, Leds.GREEN,i/255)
        Leds.set_color(Leds.LEFT, Leds.GREEN,i/255)
        i += 5
        if i > 255:
            i = 0
    #
    #  Второй режим: Страт
    #  Запоминаем время старта
    st=time.time()
    #  Сигнализируем, что увидели стартующего
    Sound.tone([(800,100,40)]).wait()

    # меньше 1 секунда не засекаем
    time.sleep(2)
    #
    #  Ждем пока стартующий покинет зону действия датчика
    while  US.value()<300:
        time.sleep(0.1)
    #
    # Режим третий:
    # Ожидаем робота на финише
    while US.value()>=300:
        time.sleep(0.01)
        # идет Замер времени - мерцаем оранжевым
        Leds.set_color(Leds.RIGHT, Leds.ORANGE,i/255)
        Leds.set_color(Leds.LEFT, Leds.ORANGE,(255-i)/255)
        i +=  5
        if i > 255:
            i = 0
    #
    #  Режим четвертый: Финиш
    #  Запоминаем Время финиша
    ft=time.time()
    # Сигнализируем что увидели финишируемого
    Sound.beep()

    # Ждем пока робот покинет зону Датчика на финише
    while  US.value()<300:
        time.sleep(0.1)

    #округпяеь до 1000-ных
    tt = round ( ft - st , 3 )
    print( tt )
    Sound.speak( tt ).wait()

