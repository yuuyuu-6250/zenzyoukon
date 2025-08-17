import sensor
import image
import lcd
import math
import time  # 追加
from machine import UART
from fpioa_manager import fm

# 初期設定
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
lcd.init()

# UART設定
fm.register(35, fm.fpioa.UART1_RX, force=True)
fm.register(34, fm.fpioa.UART1_TX, force=True)
uart = UART(UART.UART1, 115200)  # 初期化追加[2][4]

# 赤色検出用LAB閾値
red_threshold = (0, 100, 22, 69, -8, 55)  # L_min, L_max, A_min, A_max, B_min, B_max[2][4]

# 画像中心座標
center_x = 180  # VGA対応[2][4]
center_y = 120  # VGA対応[2][4]

while True:
    img = sensor.snapshot().rotation_corr(x_rotation=0, y_rotation=0, z_rotation=90)

    # 赤色ブロブ検出
    blobs = img.find_blobs([red_threshold],
                          pixels_threshold=200,
                          area_threshold=200)

    if blobs:
        # 最大面積のブロブを選択
        largest = max(blobs, key=lambda b: b.pixels())

        # バウンディングボックス描画
        img.draw_rectangle(largest.x(), largest.y(),
                         largest.w(), largest.h(),
                         color=(255, 0, 0))

        # 中心座標取得
        obj_x = largest.cx()
        obj_y = largest.cy()
        img.draw_cross(obj_x, obj_y, color=(0, 255, 0), size=10)

        # 偏差計算
        dx = obj_x - center_x
        dy = obj_y - center_y
        distance = math.sqrt(dx**2 + dy**2)

        # UART送信
        data = "{}\r\n".format(dx)  # 両座標送信[2][4]
        print(data)
        uart.write(data)

        # デバッグ表示
        img.draw_string(0, 0, "DX:{} DY:{}".format(dx, dy),
                       color=(255, 255, 255))
    else:
        uart.write("0\r\n")  # オブジェクトなし時[2][4]

    time.sleep_ms(10)
