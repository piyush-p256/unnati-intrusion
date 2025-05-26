import pandas as pd
import requests
import time

# 1. Load the normal traffic CSV you generated
df = pd.read_csv('C:/Users/Piyush/Desktop/iot fi/ddos_protection/core/traffic_simulator/normal_traffic.csv')

# 2. The exact same FEATURES list used by your model
FEATURES = [
  'dur','proto','state','spkts','dpkts','sbytes','dbytes','rate',
  'sttl','dttl','sload','dload','sloss','dloss','sinpkt','dinpkt',
  'sjit','djit','swin','stcpb','tcprtt','synack','ackdat','smean',
  'dmean','ct_srv_src','ct_state_ttl','ct_src_dport_ltm',
  'ct_dst_sport_ltm','ct_srv_dst'
]

URL = 'http://127.0.0.1:8000/attack-endpoint/'

# 3. Stream rows continuously (loop over and over)
while True:
    for _, row in df.iterrows():
        data = {f: row[f] for f in FEATURES}
        try:
            resp = requests.post(URL, json=data)
            print("Normal:", resp.status_code, resp.json())
        except Exception as e:
            print("Error sending normal traffic:", e)
        time.sleep(0.5)  # adjust rate as desired
