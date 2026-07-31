# -*- coding: utf-8 -*-
"""
MQTT Subscriber script for IoT Dashboard Node.
Subscribes to topic, logs incoming messages to results/logs/mqtt_log.txt.
"""

import argparse
import json
import os
import ssl
import sys
import time
import paho.mqtt.client as mqtt

LOG_FILE = os.path.join("results", "logs", "mqtt_log.txt")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[+] Connected to Broker successfully (rc={rc})")
        client.subscribe(userdata["topic"])
        print(f"[+] Subscribed to topic: {userdata['topic']}")
    else:
        print(f"[X] Connection refused with result code {rc}")

def on_message(client, userdata, msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    mode_str = f"PORT-{userdata['port']}"
    payload_text = msg.payload.decode('utf-8')
    log_line = f"[{timestamp}] [{mode_str}] {msg.topic} : {payload_text}\n"
    
    print(f"[REC] {log_line.strip()}")
    
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_line)

def run_subscriber(host, port, topic, cafile, cert, key):
    userdata = {"topic": topic, "port": port}
    client = mqtt.Client(client_id="dashboard_sub", userdata=userdata)
    client.on_connect = on_connect
    client.on_message = on_message

    if port == 8883:
        if cafile and cert and key:
            print("[+] Configuring mTLS for Subscriber...")
            client.tls_set(
                ca_certs=cafile,
                certfile=cert,
                keyfile=key,
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLSv1_2
            )
            client.tls_insecure_set(False)

    print(f"[*] Subscriber connecting to {host}:{port}...")
    try:
        client.connect(host, port, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[*] Subscriber stopping...")
        client.disconnect()
    except Exception as e:
        print(f"[X] Subscriber error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MQTT Subscriber")
    parser.add_argument("--host", default="localhost", help="Broker IP / Hostname")
    parser.add_argument("--port", type=int, default=1883, help="Port (1883 or 8883)")
    parser.add_argument("--topic", default="iot/sensor/temp", help="MQTT Topic")
    parser.add_argument("--cafile", help="CA Certificate file path")
    parser.add_argument("--cert", help="Client Certificate file path")
    parser.add_argument("--key", help="Client Key file path")
    args = parser.parse_args()

    run_subscriber(args.host, args.port, args.topic, args.cafile, args.cert, args.key)
