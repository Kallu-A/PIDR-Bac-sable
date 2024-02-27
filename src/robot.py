import os

from thymiodirect import Thymio
from thymiodirect.thymio_serial_ports import ThymioSerialPort


# Adapter pattern of the thymio direct library
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

    # Disconnect the robot
    def disconnet(self):
        print("robot disconnection: ", end='')
        self.thymioPanel.disconnect()
        print("DONE")


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