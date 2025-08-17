import network
import espnow
from machine import Pin, PWM
import time

# LED
LED_g = Pin(7, Pin.OUT)
LED_y = Pin(8, Pin.OUT)
LED_w = Pin(9, Pin.OUT)

# DRV8835のピン設定
# モーター1
IN1_A = Pin(4, Pin.OUT)
IN2_A = Pin(3, Pin.OUT)

# モーター2
IN1_B = Pin(2, Pin.OUT)
IN2_B = Pin(1, Pin.OUT)

PWM_FREQ = 1000  # PWM周波数

# PWM設定
pwm1_A = PWM(IN1_A, freq=PWM_FREQ)
pwm2_A = PWM(IN2_A, freq=PWM_FREQ)
pwm1_B = PWM(IN1_B, freq=PWM_FREQ)
pwm2_B = PWM(IN2_B, freq=PWM_FREQ)

def left_forward(speed):
    pwm1_A.duty(speed)
    pwm2_A.duty(0)

def left_stop():
    pwm1_A.duty(0)
    pwm2_A.duty(0)

def right_forward(speed):
    pwm1_B.duty(speed)
    pwm2_B.duty(0)

def right_stop():
    pwm1_B.duty(0)
    pwm2_B.duty(0)

def motor_forward(speed):
    pwm1_A.duty(speed)
    pwm2_A.duty(0)
    pwm1_B.duty(speed)
    pwm2_B.duty(0)

def motor_stop():
    pwm1_A.duty(0)
    pwm2_A.duty(0)
    pwm1_B.duty(0)
    pwm2_B.duty(0)
    
def LED_on():
    LED_g.on()
    LED_w.on()
    
def LED_off():
    LED_g.off()
    LED_w.off()
    
LED_on()


#main
def con_motor(x, y, button):
    # --- ラジコンのジョイスティック値(x, y)を元にモーター制御 ---
    X_CENTER = 143
    Y_CENTER = 123
    X_DEAD = 30
    Y_DEAD = 30
    MOTOR_MAX = 1023
    MOTOR_MIN = 0

    x_ofs = x - X_CENTER
    y_ofs = Y_CENTER - y  # y=0が「前進」ならこう。逆なら符号調整

    # 前進・後退成分
    if abs(y_ofs) < Y_DEAD:
        y_motor = 0
    else:
        y_motor = max(min(y_ofs * 9, MOTOR_MAX), -MOTOR_MAX)

    # 左右成分
    if abs(x_ofs) < X_DEAD:
        x_motor = 0
    else:
        x_motor = max(min(x_ofs * 9, MOTOR_MAX), -MOTOR_MAX)


    if y_motor == 0 and x_motor == 0 or y_motor < 0:
        left_speed = 0
        right_speed = 0
        
    elif x_motor <= 0:
        left_speed = y_motor
        right_speed = y_motor + abs(x_motor)
        
    elif x_motor > 0:
        left_speed = y_motor + x_motor
        right_speed = y_motor
    
    left_speed = max(min(left_speed, MOTOR_MAX), MOTOR_MIN)
    right_speed = max(min(right_speed, MOTOR_MAX), MOTOR_MIN)
    
    print(f"left: {left_speed}, right: {right_speed}")
    left_forward(left_speed)
    right_forward(right_speed)

# --- WiFi/ESP-NOW初期化 ---
w0 = network.WLAN(network.STA_IF)
w0.active(True)

e = espnow.ESPNow()
e.active(True)
peer = b'\xcc\xba\x97\x15A\x8c' # ここに送信側のMACアドレスを設定

try:
    e.add_peer(peer)
except OSError as err:
    if err.args and err.args[0] == -12395:
        pass
    else:
        raise

    while True:
        host, msg = e.recv()
        if msg:
            try:
                print("raw msg:", msg)
                data = msg.decode().split(',')
                x = int(data[0])
                y = int(data[1])
                button = int(data[2])
                print(f"x: {x}, y: {y}, button: {button}")
                con_motor(x, y, button)
            except Exception as er:
                print("decode error:", er)
                
            except NameError:
                pass

        if msg == b'end':
            break

finally:
    LED_off()



