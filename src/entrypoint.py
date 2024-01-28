from thymiodirect import Thymio

from thymioserialports import ThymioSerialPort

port = ThymioSerialPort.default_device()

print(port)
th = Thymio(serial_port=port,
            on_connect=lambda node_id:print(f"{node_id} is connected"))
th.connect()


id = th.first_node()
th[id]["leds.top"] = [0, 0, 32]