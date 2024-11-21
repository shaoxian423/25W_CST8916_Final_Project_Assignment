# Tutorial: Connecting Azure IoT Hub with Azure Stream Analytics to Process Streaming Data

In this tutorial, you will learn how to connect **Azure IoT Hub** with **Azure Stream Analytics** to process real-time streaming data. We will use a Python script to simulate IoT sensor data and write a Stream Analytics query to filter and store the results in an Azure Storage Account.

---

## Step 1: Set Up Azure IoT Hub

### 1. Create an IoT Hub
1. In the Azure Portal, search for **IoT Hub** and click **Create**.
2. Provide a name for your IoT Hub and select a resource group.
3. Choose the **Free Tier** (if available) for testing purposes and create the IoT Hub.
### 2. Register a Device
1. In the IoT Hub, go to the **Devices** section and click **Add Device**.
2. Provide a Device ID (e.g., `Sensor1`) and click **Save**.
3. After the device is created, click on it to view the connection string. Copy the connection string for use in the Python script that going to simulate the sensor.
### 3. Install Required Libraries

Install the `azure-iot-device` library to simulate sensor data. Run the following command:

```bash
pip install azure-iot-device
```
### 4. Run the Python Script to Simulate Sensor Data
Use the following Python script to simulate telemetry data and send it to the IoT Hub. Replace the `CONNECTION_STRING` with the device connection string you copied earlier.

```python
import time
import random
from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "Your IoT Hub device connection string here"

def get_telemetry():
    return {
        "temperature": random.uniform(20.0, 40.0),
        "humidity": random.uniform(30.0, 70.0)
    }

def main():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    print("Sending telemetry to IoT Hub...")
    try:
        while True:
            telemetry = get_telemetry()
            message = Message(str(telemetry))
            client.send_message(message)
            print(f"Sent message: {message}")
            time.sleep(10)
    except KeyboardInterrupt:
        print("Stopped sending messages.")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
```

**Explanation:**
This Python script simulates an IoT device sending telemetry data to an Azure IoT Hub. 
It uses a connection string to authenticate and connects to the IoT Hub via the `IoTHubDeviceClient`. 
The script generates random temperature and humidity data through the `get_telemetry` function and continuously sends this data as messages to the IoT Hub every 10 seconds. 
It handles keyboard interrupts (e.g., Ctrl+C) to stop the loop gracefully and disconnects the client.

### 5. Run the Script
Execute the script to start sending telemetry data to your IoT Hub.

## Step 2: Create and Configure a Stream Analytics Job
#### 1. Create the Stream Analytics Job
1. In the Azure Portal, search for Stream Analytics jobs and click Create.
2. Provide a name for your job and select the appropriate resource group.
3. Choose Cloud as the hosting environment and create the job.
#### 2. Define Input
1. In the Stream Analytics job, go to the Inputs section and click Add.
2. Choose IoT Hub as the input source.
3. Provide the following details:
   - IoT Hub Namespace: Select your IoT Hub.
   - IoT Hub Policy Name: Use the iothubowner policy.
   - Consumer Group: Use $Default or create a new consumer group in your IoT Hub.
   - Serialization Format: Choose JSON.
#### 3. Define Output
1. Go to the Outputs section and click Add.
2. Choose Blob Storage as the output destination.
3. Provide the following details:
   - Storage Account: Select your Azure Storage Account.
   - Container: Create or choose an existing container for storing results.
   - Path Pattern: Optionally define a folder structure (e.g., output/{date}/{time}).
#### 4. Write the Stream Analytics Query
Go to the Query tab and replace the default query with the following:

```sql
SELECT
    IoTHub.ConnectionDeviceId AS DeviceId,
    AVG(temperature) AS AvgTemperature,
    AVG(humidity) AS AvgHumidity,
    System.Timestamp AS EventTime
INTO
    [output]
FROM
    [input]
GROUP BY
    IoTHub.ConnectionDeviceId, TumblingWindow(second, 60)
```
**Explanation:** This query processes streaming data in Azure Stream Analytics. 
It calculates the **average temperature and humidity** from incoming telemetry data grouped by device `IoTHub.ConnectionDeviceId` over 60-second intervals using a tumbling window. 
The results include the device ID, the computed averages, and the event timestamp `System.Timestamp`. 
The processed data is then written to an output sink specified by `output`. 
#### 5. Save and Start the Job
Save the query and click Start on the Stream Analytics job.

### Step 3: Verify the Output
1. Monitor the Stream Analytics Job
Navigate to the Monitoring tab of the job to view metrics and ensure data is being processed.

2. Check Blob Storage
   - Go to your Azure Storage Account.
   - Navigate to the container you specified in the output.
   - Verify that processed data is being stored in JSON format.

### Step 4: Clean Up Resources
To avoid unnecessary charges:

- Stop the Stream Analytics job.
- Delete resources created for this tutorial if no longer needed.
