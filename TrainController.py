from pybricks.hubs import CityHub
from pybricks.pupdevices import DCMotor, Remote
from pybricks.parameters import Port, Direction, Button, Color
from pybricks.tools import wait
from urandom import choice

def enum(**enums):
    return type('Enum', (), enums)

# Defines the available remote modi
# LEFT: Standard control with (only) the left buttons
# RIGHT: Standard control with (only) the right buttons
# LEFT_ADVANCED: Standard control with the left buttons and the right buttons can be used to start and modify a slowdown of the train
RemoteMode = enum(LEFT=1, RIGHT=2, LEFT_ADVANCED=3)

class TrainRemote:
    def __init__(self, mode=RemoteMode.LEFT, color=Color.GREEN):
        print("Start connecting remote...")
        self.remote = Remote(timeout=10000)
        print("Successfully connected to remote " + self.remote.name())
        self.remote.light.on(color)
        self.mode = mode

    def pressed(self):
        return self.remote.buttons.pressed()

    def color(self, color):
        self.remote.light.on(color)

class TrainController:
    
    SPEED_LIMIT = 100 # The maximum speed limit in % (100 means up to maximum speed)
    SPEED_INCREASE = 10 # The speed increase/ decrease per button click
    CUT_OFF_SPEED = 20 # The speed level once s.t. speeds below that speed will cut off to zero to avoid annoying squeaking.
    SLOWDOWN_SPEED = SPEED_INCREASE / 2 # The speed to use per time step for the automatic slow down. Can be adjusted in LEFT_ADVANCED mode 

    def __init__(self, mode=RemoteMode.LEFT_ADVANCED, color=Color.GREEN):
        if color == 'random':
            color = choice([Color.YELLOW, Color.GREEN, Color.CYAN, Color.BLUE, Color.RED])
        self.hub = CityHub()
        self.remote = TrainRemote(mode, color=color)     
        self.hub.light.on(color)      
        self.motors = []
        self.power = 0
        self.slowDown = False

    def registerMotor(self, port, direction=Direction.CLOCKWISE):
        motor = DCMotor(port, direction)
        self.motors.append(motor)

    def updateMotors(self):
        if self.power == 0:
            for motor in self.motors:
                motor.stop()
            self.slowDown = False
        else: 
            for motor in self.motors:
                motor.dc(self.power)

    def updatePower(self, change):
        oldPower = self.power
        sum = oldPower + change
        if oldPower != 0 and sum * oldPower <= 0:
            self.power = 0
        else:           
            self.power = min(max(oldPower + change, -self.SPEED_LIMIT), self.SPEED_LIMIT)
            if abs(self.power) < self.CUT_OFF_SPEED and abs(oldPower) >= self.CUT_OFF_SPEED:
                self.power = 0

    def doSlowDown(self):
        if self.power > self.SPEED_INCREASE:
            self.updatePower(-self.SLOWDOWN_SPEED)
        elif self.power < self.SPEED_INCREASE:
            self.updatePower(self.SLOWDOWN_SPEED)
        else:
            self.power = 0

    def run(self, dt=100):
        while True:
            buttons = self.remote.pressed()

            if len(buttons) > 0:
                if self.remote.mode in [RemoteMode.LEFT, RemoteMode.LEFT_ADVANCED]:
                    if Button.LEFT in buttons:
                        self.power = 0
                    elif Button.LEFT_PLUS in buttons:
                        self.updatePower(self.SPEED_INCREASE)
                        self.slowDown = False
                    elif Button.LEFT_MINUS in buttons:
                        self.updatePower(-self.SPEED_INCREASE)
                        self.slowDown = False

                    if self.remote.mode == RemoteMode.LEFT_ADVANCED:
                        if Button.RIGHT in buttons:
                            self.slowDown = True
                            self.doSlowDown()
                        elif Button.RIGHT_PLUS in buttons:
                            # Increase the total slow down time i. e. the train stops slower
                            self.SLOWDOWN_SPEED = max(1, self.SLOWDOWN_SPEED - 1)
                        elif Button.RIGHT_MINUS in buttons:
                            # Decrease the total slow down time i. e. the train stops faster
                            # Note that the "4" just means that the at least four time steps are
                            # required to stop a full speed train.
                            self.SLOWDOWN_SPEED = min(self.SPEED_LIMIT / 4, self.SLOWDOWN_SPEED + 1)
                elif self.remote.mode == RemoteMode.RIGHT:
                    if Button.RIGHT in buttons:
                        self.power = 0
                    elif Button.RIGHT_PLUS in buttons:
                        self.updatePower(self.SPEED_INCREASE / 2)
                        self.slowDown = False
                    elif Button.RIGHT_MINUS in buttons:
                        self.updatePower(-self.SPEED_INCREASE / 2)
                        self.slowDown = False
            elif self.slowDown:
                self.doSlowDown()
            self.updateMotors()

            wait(dt)

# create train controller with random color s.t. multiple controller-hub-pairs can be distinguished
controller = TrainController(mode=RemoteMode.LEFT_ADVANCED, color='random')
controller.registerMotor(Port.A, Direction.CLOCKWISE)  
controller.registerMotor(Port.B, Direction.COUNTERCLOCKWISE)     
controller.run()
