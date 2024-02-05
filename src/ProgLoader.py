from tdmclient import ClientAsync

thymio_program = """
        # reset outputs
        call sound.system(-1)
        call leds.top(0,0,0) call leds.bottom.left(0,0,0)
        call leds.bottom.right(0,0,0)
        call leds.circle(0,0,0,0,0,0,0,0)
        
        motor.left.target = 300
        motor.right.target = 300
        
        
        # if the ground sensors detects nothing Thymio becomes red otherwise he becomes green
        onevent prox
        if prox.ground.delta[0] <= 400 or prox.ground.delta[1] <= 400 then
            motor.left.target = -500
            motor.right.target = -200
            call leds.top(32,0,0)    
        
        else
            motor.left.target = 300
            motor.right.target = 300
            call leds.top(0,32,0)
        end
        
        if prox.horizontal[2] >= 800 or  prox.horizontal[0] >= 800 or  prox.horizontal[1] >= 800 then
            motor.right.target = 0
        end
        
        if prox.horizontal[3] >= 800 or  prox.horizontal[4] >= 800 then
            motor.left.target = 0
        end
"""