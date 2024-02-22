# This file is part of thymiodirect.
# Copyright 2020 ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE,
# Miniature Mobile Robots group, Switzerland
# Author: Yves Piguet
#
# SPDX-License-Identifier: BSD-3-Clause
import os
import time

from thymiodirect import Thymio
from thymiodirect.thymio_serial_ports import ThymioSerialPort

if __name__ == "__main__":
    serial_port = None
    thymio_serial_ports = ThymioSerialPort.get_ports()
    if len(thymio_serial_ports) > 0:
        serial_port = thymio_serial_ports[0].device
        print("Thymio serial ports:")
        for thymio_serial_port in thymio_serial_ports:
            print(" ", thymio_serial_port, thymio_serial_port.device)


    # connect
    use_tcp = False
    host = None
    tcp_port = None
    try:
        th = Thymio(use_tcp=use_tcp,
                    serial_port=serial_port,
                    host=host, tcp_port=tcp_port,
                    refreshing_coverage={"prox.horizontal", "button.center"},
                    )
        # constructor options: on_connect, on_disconnect, on_comm_error,
        # refreshing_rate, refreshing_coverage, discover_rate, loop
    except Exception as error:
        print(error)
        exit(1)

    def on_comm_error(error):
        # loss of connection: display error and exit
        print(error)
        os._exit(1) # forced exit despite coroutines

    th.on_comm_error = on_comm_error

    th.connect()

    # wait 2-3 sec until robots are known
    id = th.first_node()
    print(f"id: {id}")
    print(f"variables: {th.variables(id)}")
    print(f"events: {th.events(id)}")
    print(f"native functions: {th.native_functions(id)[0]}")


    print("\nROBOT ready to roll !\n")


    # set a function called after new variable values have been fetched
    prox_prev = 0
    done = False
    def obs(node_id):
        global prox_prev, done
        prox = (th[node_id]["prox.horizontal"][5] - th[node_id]["prox.horizontal"][2]) // 10
        if prox != prox_prev:
            th[node_id]["motor.left.target"] = prox
            th[node_id]["motor.right.target"] = prox
            print(prox)
            prox_prev = prox
        if th[node_id]["button.center"]:
            print("button.center")
            done = True

    th.set_variable_observer(id, obs)

    while not done:
        time.sleep(0.1)
    th.disconnect()