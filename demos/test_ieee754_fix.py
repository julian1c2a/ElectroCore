#!/usr/bin/env python3
"""Test para IEEE754 encode endpoint"""

import requests
import json
import time
import subprocess
import sys
import os

# Change to web directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("Iniciando servidor Flask...")
server = subprocess.Popen([sys.executable, "web/app.py"], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)

# Esperar a que el servidor inicie
time.sleep(3)

try:
    print("Probando endpoint /api/ieee754/encode...")
    
    test_cases = [
        {'value': 1.5, 'E_bits': 8, 'F_bits': 23},
        {'value': 3.14},
        {'value': 0.0},
        {'value': float('inf')},
    ]
    
    for i, test_data in enumerate(test_cases):
        print(f"\nTest {i+1}: {test_data}")
        response = requests.post('http://localhost:5000/api/ieee754/encode', 
                               json=test_data,
                               timeout=2)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✓ Status: {response.status_code}")
            print(f"    Valor: {data['value']}")
            print(f"    Bits: {data['bits']}")
            print(f"    Decodificado: {data['decoded']}")
        else:
            print(f"  ✗ Status: {response.status_code}")
            print(f"    Response: {response.text[:200]}")
            
finally:
    print("\nDeteniendo servidor...")
    server.terminate()
    server.wait()
    print("✓ Servidor detenido")
