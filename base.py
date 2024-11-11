from machine import UART, Pin, PWM, SoftI2C # type: ignore
import time

# UARTオブジェクトの作成
uart = UART(1, baudrate=115200, tx=43, rx=44)

LED_g = Pin(7,Pin.OUT)
LED_y = Pin(8,Pin.OUT)
LED_w = Pin(9,Pin.OUT)

# DRV8835のピン設定
# モーター1
IN1_A = Pin(1, Pin.OUT)
IN2_A = Pin(2, Pin.OUT)

# モーター2
IN1_B = Pin(3, Pin.OUT)
IN2_B = Pin(4, Pin.OUT)

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
    
def LED_off():
    LED_g.off()
    LED_y.off()
    LED_w.off()
