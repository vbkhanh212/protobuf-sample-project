import requests
from app.proto import data_pb2 #
API_URL = "http://127.0.0.1:8000/api/data/" # Your DRF endpoint URL

# 1. Create a Protobuf message instance
user_message = data_pb2.Data(
    name="Super Khanh",
    age=25,
)

# 2. Serialize the message to a binary string (bytes)
proto_data_bytes = user_message.SerializeToString()

# 3. Define the headers for Protobuf communication
headers = {
    'Content-Type': 'application/x-protobuf',
    'Accept': 'application/x-protobuf',
}

print("Sending Protobuf request...")
response = requests.post(API_URL, data=proto_data_bytes, headers=headers)

if response.status_code == 200:
    # 4. Deserialize the binary response back into a Protobuf message
    response_message = data_pb2.Data()
    response_message.ParseFromString(response.content)

    print("--- Protobuf Response Received ---")
    print(f"Status: {response.status_code}")
    print(f"Username: {response_message.name}")
    print(f"Age: {response_message.age}")
else:
    print(f"Error {response.status_code}: {response.text}")