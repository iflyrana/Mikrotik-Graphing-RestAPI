import requests
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
            return response.json()
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
    rx_rates = []
    tx_rates = []
    timestamps = []

    start_time = time.time()

    # Function to update the graph dynamically
    def update(frame):
        nonlocal rx_rates, tx_rates, timestamps

        # Get the current data rate
        rx_rate, tx_rate = getInstDataRate()

        # Add new data to the lists
        current_time = time.time() - start_time
        rx_rates.append(rx_rate)
        tx_rates.append(tx_rate)
        timestamps.append(current_time)

        # Keep only the last 60 points (1 minute of data)
        if len(timestamps) > 60:
            rx_rates = rx_rates[-60:]
            tx_rates = tx_rates[-60:]
            timestamps = timestamps[-60:]

        # Clear the current plot and re-plot with updated data
        ax.clear()
        ax.plot(timestamps, rx_rates, label="RX Rate (Mbps)", color="blue")
        ax.plot(timestamps, tx_rates, label="TX Rate (Mbps)", color="red")
        ax.set_title("Live Data Rate (Mbps)")
        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("Rate (Mbps)")
        ax.legend()
        ax.grid(True)

    fig, ax = plt.subplots(figsize=(10, 6))


    ani = animation.FuncAnimation(fig, update, interval=1000)

    plt.show()

if __name__ == "__main__":
    graphing()