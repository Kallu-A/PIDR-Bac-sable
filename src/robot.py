import os

from thymiodirect import Thymio
from thymiodirect.thymio_serial_ports import ThymioSerialPort


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


# Adapter pattern of the thymio direct library and work as a singleton to easily get the robot
@singleton
class Robot:

    def __init__(self):
        thymio_serial_ports = ThymioSerialPort.get_ports()
        if len(thymio_serial_ports) > 0:
            serial_port = thymio_serial_ports[0].device
            print("Thymio serial ports:")
            for thymio_serial_port in thymio_serial_ports:
                print(" ", thymio_serial_port, thymio_serial_port.device)

        try:
            self.thymioPanel = Thymio(use_tcp=False,
                        serial_port=serial_port,
                        host=None, tcp_port=None,
                        refreshing_coverage={"prox.horizontal", "button.center"},
                        )
            # constructor options: on_connect, on_disconnect, on_comm_error,
            # refreshing_rate, refreshing_coverage, discover_rate, loop
        except Exception as error:
            print(error)
            exit(1)

        # Function called if connection to thymio is lost
        def on_comm_error(error):
            # loss of connection: display error and exit
            print("Connectin loss with the robot: exit of the program")
            print(error)
            os._exit(1) # forced exit despite coroutines

        self.thymioPanel.on_comm_error = on_comm_error
        self.thymioPanel.connect()
        self.id = self.thymioPanel.first_node()
        self.thymio = self.thymioPanel[self.id]

        print(f"Robot n°{self.id} is ready to roll !")

        self.alive = True

        pass

    # Disconnect the robot
    def disconnet(self):
        print("robot disconnection: ", end='')
        self.thymioPanel.disconnect()
        self._instance = None
        print("DONE")

    def stop(self):
        self.move_robot(0, 0)

    # Add a observer
    def add_obs(self, obs):
        self.thymioPanel.set_variable_observer(self.id, obs)

    # methode to add to the obs added to handle disconnection with the center button
    def disconnect_button_center(self):
        if self.thymio["button.center"]:
            print("button.center")
            self.disconnet()

    #print the document of the robot dev purpose
    def documentation(self):
        print(f"id: {self.id}")
        print(f"variables: {self.thymioPanel.variables(self.id)}")
        print(f"events: {self.thymioPanel.events(self.id)}")
        print(f"native functions: {self.thymioPanel.native_functions(self.id)[0]}")


    # call to make the robot move
    def move_robot(self, left, right):
        self.thymio["motor.left.target"] = left
        self.thymio["motor.right.target"] = right

    # call to stop the robot
    def stop_robot(self):
        self.move_robot(0, 0)
        
    
    # get the initial orientation of the robot with the nearby obstacles
    def get_initial_orientation(self):
        # we need to activate the sensors
        self.thymio["prox.horizontal"][0].enable = True
        self.thymio["prox.horizontal"][1].enable = True
        
        prox_values = self.thymio["prox.horizontal"].get()
        
        # allows us to see with sensor is closer to the obstacles
        if prox_values[0] > 0 or prox_values[1] > 0:
            if prox_values[0] > prox_values[1]:
                initial_orientation = 90
            else:
                initial_orientation = -90
        
        else:
            initial_orientation = 0 
            # in this case, the orientation is unknown
            
        return initial_orientation
        # must be defined with the orientation of the obstacle
        # could be easier to put a fixed value and stuck to it 