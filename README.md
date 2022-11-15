# Pybricks-Train-Controller

** This is still work in progress (but it should already work) **

Short instruction: 
- Go to https://code.pybricks.com/
- Open the TrainController.py file or just copy and paste the content of the file into the pybricks console
- Flash your CityHub with the Pybricks Software. If you just want to run the code (without changing it) you can enable "settings -> Firmware -> Include current program", so the CityHub will be a TrainController until another firmware reflash will be done.
- If you flashed your hub including the program, just start the hub, start the program by clicking again the green button of the hub (the hub starts searching for a controller), start your controller (eventually press the controller's green button), and the two devices should pair (indicated by the same color of hub and controller). Otherwise, connect the flashed hub via bluetooth and Run the program (Connect via bluetooth and Run are both buttons inside the pybricks IDE). After running the code connect the controller as described above.

The program provides a pretty flexible way how a train can be controlled using a CityHub and a controller. By using the provided code TrainController.py, the following configuration is applied:
- The left side of the controller modifies the speed in a classical way ("+" -> increase speed, "-" decrease speed, red button -> stop)
- The right side of the controller can be used to slow down a running train slowly. Pressing the right red button starts the slow down process (which stops only if the train reaches speed 0 after some time). Within the slow down process, the current speed is changed towards speed 0. The amount per time step (100ms) can be decreased or increased by using the "+" or "-" button respectively. Note that e. g. "+" means "longer slow down time".

