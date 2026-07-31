# -*- coding: utf-8 -*-
"""
Man-in-the-Middle (MitM) Attack Simulation Script.
Demonstrates ARP Poisoning concept, Plaintext Packet Sniffing, and Payload Tampering.
"""

import json
import time

def simulate_arp_poisoning(target_ip="192.168.10.20", gateway_ip="192.168.10.10", interface="eth0"):
    print("=" * 70)
    print("ATTACK SIMULATION: ARP POISONING & MAN-IN-THE-MIDDLE (MITM)")
    print("=" * 70)
    print(f"[*] Attacker Interface: {interface}")
    print(f"[*] Target IoT Client IP: {target_ip}")
    print(f"[*] Target Broker Gateway IP: {gateway_ip}")
    print("[*] Sending spoofed ARP Reply packets...")
    
    for i in range(3):
        print(f"    -> [ARP REPLY] {target_ip} is at 00:0c:29:ab:cd:ef (Attacker MAC)")
        print(f"    -> [ARP REPLY] {gateway_ip} is at 00:0c:29:ab:cd:ef (Attacker MAC)")
        time.sleep(0.5)
        
    print("[+] ARP Cache successfully poisoned! Attacker is now Man-in-the-Middle.\n")

def simulate_packet_tampering(original_payload):
    print("[!] INTERCEPTED UNENCRYPTED PLAINTEXT MQTT PACKET (Port 1883)")
    print(f"    Original Payload : {original_payload}")
    
    try:
        data = json.loads(original_payload)
        data["temperature"] = 99.9  # Maliciously altered temperature value
        data["humidity"] = 0.0
        data["tampered_by"] = "Kali_Linux_Attacker"
        tampered_payload = json.dumps(data)
        print(f"    Tampered Payload : {tampered_payload}")
        print("[!] Packet modified on the fly and forwarded to Subscriber!\n")
        return tampered_payload
    except Exception as e:
        print(f"[X] Tampering error: {e}")
        return original_payload

if __name__ == "__main__":
    simulate_arp_poisoning()
    sample_data = '{"device": "sensor01", "temperature": 30, "humidity": 70, "time": "2026-07-31 11:45:10"}'
    simulate_packet_tampering(sample_data)
