import serial
import time


ser = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)

def decide_speed(ir_l, ir_r, dist):
  
    if ir_l == 0 or ir_r == 0:
        return 'X', "EMERGENCY STOP (IR)"

    if dist == 0:
        return 'X', "NO DIST DATA"

    elif dist < 10:
        return 'X', "STOP"

    elif dist < 25:
        return 'S', "SLOW"

    else:
        return 'F', "FAST"


while True:
    try:
        if ser.in_waiting:
            raw = ser.readline().decode().strip()

      
            parts = raw.split(',')

            if len(parts) != 3:
                continue

            ir_l = int(parts[0])
            ir_r = int(parts[1])
            dist = float(parts[2])

            cmd, state = decide_speed(ir_l, ir_r, dist)

            print(f"IR_L:{ir_l} IR_R:{ir_r} Dist:{dist:.1f} -> {state}")

            ser.write(cmd.encode())

    except Exception as e:
        print("Error:", e)