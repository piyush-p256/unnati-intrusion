import pandas as pd
import requests
import time

# 1. Load the malicious traffic CSV you generated
df = pd.read_csv('C:/Users/Piyush/Desktop/iot fi/ddos_protection/core/traffic_simulator/malicious_traffic.csv')

FEATURES = [
  'dur','proto','state','spkts','dpkts','sbytes','dbytes','rate',
  'sttl','dttl','sload','dload','sloss','dloss','sinpkt','dinpkt',
  'sjit','djit','swin','stcpb','tcprtt','synack','ackdat','smean',
  'dmean','ct_srv_src','ct_state_ttl','ct_src_dport_ltm',
  'ct_dst_sport_ltm','ct_srv_dst'
]

URL = 'http://127.0.0.1:8000/attack-endpoint/'

# 2. Shuffle and send each malicious record once (then stop or loop)
for _, row in df.sample(frac=1).iterrows():
    data = {f: row[f] for f in FEATURES}
    try:
        resp = requests.post(URL, json=data)
        print("Malicious:", resp.status_code, resp.text)
    except Exception as e:
        print("Error sending malicious traffic:", e)
    time.sleep(0.3)  # adjust rate as desired
