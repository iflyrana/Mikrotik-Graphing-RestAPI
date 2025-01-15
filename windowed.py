import requests
import time

ROUTER_HOST = "[HOST]"
INTERFACE = "[INTERFACE]"
USERNAME = "[USERNAME]"
PASSWORD = "[PASSWORD]"

REQUEST_URL = f'http://{ROUTER_HOST}/rest/interface/{INTERFACE}'
CREDENTIALS = (USERNAME, PASSWORD)


def sendRequest(url, auth):
    try:
        response = requests.get(url, auth=auth)
        if response.status_code == 200:
            return (response.json())
    except requests.exceptions.RequestException:
        return None

def getInstRx_Tx():
    data = sendRequest(REQUEST_URL, CREDENTIALS)
    rx = data['rx-byte']
    tx = data['tx-byte']
    return (rx, tx)

def getInstDataRate():

    t1 = getInstRx_Tx()
    time.sleep(1)
    t2 = getInstRx_Tx()
    rx_rate = ((int(t2[0]) - int(t1[0])) * 8) / 1_000_000
    tx_rate = ((int(t2[1]) - int(t1[1])) * 8) / 1_000_000  
    return (rx_rate, tx_rate)

def graphing():
    pass

if __name__ == "__main__":
    while True:
        print(getInstDataRate())