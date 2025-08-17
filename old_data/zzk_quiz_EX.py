from machine import UART, Pin, PWM, SoftI2C
import time
import ssd1306

# UARTオブジェクトの作成
uart = UART(1, baudrate=115200, tx=43, rx=44)

# I2Cオブジェクトの作成
i2c = SoftI2C(sda=Pin(5), scl=Pin(6))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

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

# リセット
data = 0
while True:
    if uart.any():
        try:
            # バイト列を文字列に変換してから整数に変換
            data = int(uart.read().decode().strip())
            print(data)
        except ValueError:
            print("データが無効です")
            continue
    
    display.fill(0)
    display.show()
    
    diff = data * 7
    
    # デューティーサイクルを0から1023の範囲内に制限
    left_speed = max(0, min(1023, 1023 - diff))
    right_speed = max(0, min(1023, 1023 + diff))

    if data > 0:
        print('プラスの値やで')
        left_forward(left_speed)
        display.text('plus', 0, 0, 1)
        display.show()
    elif data < 0:
        print('マイナスの値やで')
        right_forward(right_speed)
        display.text('minus', 0, 0, 1)
        display.show()
    else:
        print('0やで')
        motor_stop()
        display.text('zero', 0, 0, 1)
        display.show()

    time.sleep_ms(100)
    data = 0
