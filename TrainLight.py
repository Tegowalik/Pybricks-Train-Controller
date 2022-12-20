from pybricks.hubs import CityHub
from pybricks.pupdevices import Light
from pybricks.parameters import Color, Port
from pybricks.tools import wait

hub = CityHub()
hub.light.on(Color.GREEN)
light = Light(Port.A)
light.on()
while True:
    wait(10000)
    