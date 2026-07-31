# -*- coding: utf-8 -*-
"""
MQTT Publisher script for IoT Sensor Node.
Supports Plaintext transmission (Port 1883) and mTLS Encrypted transmission (Port 8883).
"""

import argparse
import json
import ssl
import sys
import time
import paho.mqtt.client as mqtt

def run_publisher(host, port, topic, cafile, cert, key):
    client = mqtt.Client(client_id="sensor01_pub")
    
    if port == 8883:
        if cafile and cert and key:
            print("[+] Configuring mTLS for Port 8883...")
            client.tls_set(
                ca_certs=cafile,
                certfile=cert,
                keyfile=key,
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLSv1_2
            )
            client.tls_insecure_set(False)
        else:
            print("[!] Warning: Port 8883 requires CA certificate, client cert and private key!")

    print(f"[*] Connecting to Mosquitto Broker at {host}:{port}...")
    try:
        client.connect(host, port, 60)
        client.loop_start()
        
        for i in range(5):
            payload = {
                "device": "sensor01",
                "temperature": 30 + (i % 3),
                "humidity": 70 - (i % 3),
                "time": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            json_str = json.dumps(payload)
            res = client.publish(topic, json_str)
            if res.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"[+] [{time.strftime('%H:%M:%S')}] Published to {topic}: {json_str}")
            else:
                print(f"[X] Failed to publish message (Error code: {res.rc})")
            time.sleep(1)
            
        client.loop_stop()
        client.disconnect()
        print("[*] Publisher finished successfully.")
    except Exception as e:
        print(f"[X] Publisher error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MQTT Publisher")
    parser.add_argument("--host", default="localhost", help="Broker IP / Hostname")
    parser.add_argument("--port", type=int, default=1883, help="Port (1883 or 8883)")
    parser.add_argument("--topic", default="iot/sensor/temp", help="MQTT Topic")
    parser.add_argument("--cafile", help="CA Certificate file path")
    parser.add_argument("--cert", help="Client Certificate file path")
    parser.add_argument("--key", help="Client Key file path")
    args = parser.parse_args()

    run_publisher(args.host, args.port, args.topic, args.cafile, args.cert, args.key)
