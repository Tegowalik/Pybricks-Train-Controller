from pybricks.pupdevices import DCMotor, Remote
from pybricks.parameters import Port, Direction, Button, Color
from pybricks.tools import wait

def enum(**enums):
    return type('Enum', (), enums)

RemoteMode = enum(LEFT=1, RIGHT=2, LEFT_ADVANCED=3)

class TrainRemote:
    def __init__(self, mode=RemoteMode.LEFT):
        self.remote = Remote(timeout=100000)
        self.remote.light.on(Color.BLUE)
        self.mode = mode

    def pressed(self):
        return self.remote.buttons.pressed()

    def color(self, color):
        self.remote.light.on(color)


class TrainController:
    
    SPEED_LIMIT = 100
    SPEED_INCREASE = 10

    def __init__(self, mode=RemoteMode.LEFT_ADVANCED):
        self.remote = TrainRemote(mode)
        self.motors = []
        self.power = 0
        self.slowDown = False

    def registerMotor(self, port, direction=Direction.CLOCKWISE):
        motor = DCMotor(port, direction)
        self.motors.append(motor)

    def updateMotors(self):
        for motor in self.motors:
            motor.dc(self.power)

    def updatePower(self, change):
        self.power = min(max(self.power + change, -self.SPEED_LIMIT), self.SPEED_LIMIT)
        if abs(self.power) < 20 and change < 0:
            self.power = 0

    def doSlowDown(self):
        if self.power > self.SPEED_INCREASE:
            self.updatePower(-self.SPEED_INCREASE)
        elif self.power < self.SPEED_INCREASE:
            self.updatePower(self.SPEED_INCREASE)
        else:
            self.power = 0

    def run(self, timeout=None, dt=100):
        self.remote.color(Color.GREEN)
        while True:
            buttons = self.remote.pressed()

            if len(buttons) > 0:
                if Button.CENTER in buttons:
                    break
                if self.remote.mode in [RemoteMode.LEFT, RemoteMode.LEFT_ADVANCED]:
                    if Button.LEFT in buttons:
                        self.power = 0
                    elif Button.LEFT_PLUS in buttons:
                        self.updatePower(self.SPEED_INCREASE)
                        self.slowDown = False
                    elif Button.LEFT_MINUS in buttons:
                        self.updatePower(-self.SPEED_INCREASE)
                        self.slowDown = False

                    if self.remote.mode == RemoteMode.LEFT_ADVANCED and Button.RIGHT in buttons:
                        self.slowDown = True
                        self.doSlowDown()
                elif self.remote.mode == RemoteMode.RIGHT:
                    if Button.RIGHT in buttons:
                        self.power = 0
                    elif Button.RIGHT_PLUS in buttons:
                        self.updatePower(self.SPEED_INCREASE / 2)
                        self.slowDown = False
                    elif Button.RIGHT_MINUS in buttons:
                        self.updatePower(-self.SPEED_INCREASE / 2)
                        self.slowDown = False
                self.updateMotors()
            elif self.slowDown:
                self.doSlowDown()
                self.updateMotors()

            wait(dt)
        self.remote.color(Color.RED)

while True:
    controller = TrainController()
    controller.registerMotor(Port.A, Direction.CLOCKWISE)  
    controller.registerMotor(Port.B, Direction.COUNTERCLOCKWISE)     
    controller.run()
