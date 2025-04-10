import time
import random
import json
from datetime import datetime, timezone
from azure.iot.device import IoTHubDeviceClient, Message

# Azure IoT Hub connection string (replace with your actual connection string)
CONNECTION_STRING = "HostName=8916RideauCanalHub.azure-devices.net;DeviceId=sensor-device-1;SharedAccessKey=Q/TlbrDq54t08W/uGr9tXDvY20nefba9EDametDr7Pc="

# Generate fake telemetry data
def get_telemetry():
    current_time_utc = datetime.now(timezone.utc).isoformat()
    return {
        "location": random.choice(["Fish Lake", "Fifth Avenue", "Patterson Creek"]),
        "temperature": round(random.uniform(-15.0, 0.0), 2),         # temperature in Celsius
        "humidity": round(random.uniform(60.0, 90.0), 2),            # humidity in %
        "ice_thickness_cm": round(random.uniform(10.0, 30.0), 2),    # ice thickness in cm
        "snow_depth_cm": round(random.uniform(0.0, 20.0), 2),        # snow depth in cm
        "event_time": current_time_utc                               # current UTC time
    }

# Main function to send telemetry to IoT Hub
def main():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    print("Sending telemetry to IoT Hub...")
    try:
        while True:
            telemetry = get_telemetry()
            message = Message(json.dumps(telemetry))
            client.send_message(message)
            print(f"Sent message: {telemetry}")
            time.sleep(10)  # Send every 10 seconds
    except KeyboardInterrupt:
        print("Stopped sending messages.")
    finally:
        client.disconnect()

# Run the program
if __name__ == "__main__":
    main()