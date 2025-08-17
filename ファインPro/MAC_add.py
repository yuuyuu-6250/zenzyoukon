import network

# ステーションインターフェース（通常はこちらで十分）
sta = network.WLAN(network.STA_IF)
sta.active(True)
print(sta.config('mac'))
