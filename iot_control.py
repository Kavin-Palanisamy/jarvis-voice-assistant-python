import requests

# Example ESP32 Configuration (User can update these in .env)
ESP32_IP = "192.168.1.100" # Placeholder IP

def send_iot_command(endpoint, params=None):
    """Sends a GET request to the ESP32."""
    url = f"http://{ESP32_IP}/{endpoint}"
    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            return f"Command '{endpoint}' executed successfully on ESP32."
        else:
            return f"ESP32 returned error: {response.status_code}"
    except Exception as e:
        return f"Failed to connect to ESP32: {str(e)}"

def turn_on_light():
    """Turns on the light via ESP32."""
    return send_iot_command("light/on")

def turn_off_light():
    """Turns off the light via ESP32."""
    return send_iot_command("light/off")

def check_sensor_data():
    """Reads sensor data from the ESP32."""
    url = f"http://{ESP32_IP}/sensor"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return f"Sensor report: Temperature is {data.get('temp')}C, Humidity is {data.get('hum')}%."
        else:
            return "ESP32 sensor endpoint not found."
    except Exception as e:
        return f"Could not read sensor data: {str(e)}"

if __name__ == "__main__":
    # print(turn_on_light())
    pass
