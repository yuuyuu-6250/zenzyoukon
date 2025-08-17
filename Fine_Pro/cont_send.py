import network
import espnow
from machine import I2C, Pin
import time

w0 = network.WLAN(network.STA_IF)
w0.active(True)
e = espnow.ESPNow()
e.active(True)

peer = b'\xcc\xba\x97\x16\x14(' # ここに受信側のMACアドレスを設定
try:
    e.add_peer(peer)
except OSError as err:
    if err.args and err.args[0] == -12395:
        pass
    else:
        raise

e.send(peer, b"Starting...")

i2c = I2C(0, scl=Pin(6), sda=Pin(5))
address = 0x63

def read_joystick():
    try:
        i2c.writeto(address, b'\x00')
        data = i2c.readfrom(address, 5)
        x = data[1]
        y = data[3]
        button = data[4]
        #print("X:", x, "Y:", y, "Button:", "Pressed" if button == 0 else "Released")
        return x, y, button
    except Exception as e:
        print("Read error:", e)
        return None, None, None

while True:
    x, y, button = read_joystick()
    if x is not None and y is not None:
        # CSV形式文字列で送信
        msg = "{},{},{}".format(x, y, button)
        try:
            e.send(peer, msg.encode())
            print(f"send: {msg}")
        except OSError as err:
            print("send error:", err)
            break
    time.sleep(0.5)


