#!/usr/bin/env python
"""Test script for distribution visualizer API."""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_fixed_point_unsigned():
    """Test fixed point unsigned."""
    print("\n=== Testing Fixed Point Unsigned ===")
    payload = {
        'tipo_numero': 'fixed_point',
        'E': 4,
        'F': 4,
        'representation': 'unsigned',
        'base': 2
    }
    response = requests.post(f"{BASE_URL}/api/distribution/chart-data", json=payload)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Success: {data.get('success')}")
    if data.get('success'):
        print(f"Min: {data['statistics']['min']}, Max: {data['statistics']['max']}")
    else:
        print(f"Error: {data.get('error')}")
    return response.status_code == 200

def test_fixed_point_signed_magnitude():
    """Test fixed point signed magnitude."""
    print("\n=== Testing Fixed Point Signed Magnitude ===")
    payload = {
        'tipo_numero': 'fixed_point',
        'E': 4,
        'F': 4,
        'representation': 'signed_magnitude',
        'base': 2
    }
    response = requests.post(f"{BASE_URL}/api/distribution/chart-data", json=payload)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Success: {data.get('success')}")
    if data.get('success'):
        print(f"Min: {data['statistics']['min']}, Max: {data['statistics']['max']}")
    else:
        print(f"Error: {data.get('error')}")
    return response.status_code == 200

def test_fixed_point_twos_complement():
    """Test fixed point two's complement."""
    print("\n=== Testing Fixed Point Two's Complement ===")
    payload = {
        'tipo_numero': 'fixed_point',
        'E': 4,
        'F': 4,
        'representation': 'twos_complement',
        'base': 2
    }
    response = requests.post(f"{BASE_URL}/api/distribution/chart-data", json=payload)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Success: {data.get('success')}")
    if data.get('success'):
        print(f"Min: {data['statistics']['min']}, Max: {data['statistics']['max']}")
    else:
        print(f"Error: {data.get('error')}")
    return response.status_code == 200

def test_fixed_point_ones_complement():
    """Test fixed point one's complement."""
    print("\n=== Testing Fixed Point One's Complement ===")
    payload = {
        'tipo_numero': 'fixed_point',
        'E': 4,
        'F': 4,
        'representation': 'ones_complement',
        'base': 2
    }
    response = requests.post(f"{BASE_URL}/api/distribution/chart-data", json=payload)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Success: {data.get('success')}")
    if data.get('success'):
        print(f"Min: {data['statistics']['min']}, Max: {data['statistics']['max']}")
    else:
        print(f"Error: {data.get('error')}")
    return response.status_code == 200

def test_floating_point():
    """Test floating point."""
    print("\n=== Testing Floating Point ===")
    payload = {
        'tipo_numero': 'floating_point',
        'E': 8,
        'F': 23,
        'base': 2
    }
    response = requests.post(f"{BASE_URL}/api/distribution/chart-data", json=payload)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Success: {data.get('success')}")
    if data.get('success'):
        print(f"Min: {data['statistics']['min']}, Max: {data['statistics']['max']}")
    else:
        print(f"Error: {data.get('error')}")
    return response.status_code == 200

def test_floating_point_base10():
    """Test floating point with base 10."""
    print("\n=== Testing Floating Point Base 10 ===")
    payload = {
        'tipo_numero': 'floating_point',
        'E': 4,
        'F': 8,
        'base': 10
    }
    response = requests.post(f"{BASE_URL}/api/distribution/chart-data", json=payload)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Success: {data.get('success')}")
    if data.get('success'):
        print(f"Min: {data['statistics']['min']}, Max: {data['statistics']['max']}")
    else:
        print(f"Error: {data.get('error')}")
    return response.status_code == 200

def test_fixed_point_base8():
    """Test fixed point with base 8."""
    print("\n=== Testing Fixed Point Base 8 ===")
    payload = {
        'tipo_numero': 'fixed_point',
        'E': 3,
        'F': 3,
        'representation': 'unsigned',
        'base': 8
    }
    response = requests.post(f"{BASE_URL}/api/distribution/chart-data", json=payload)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Success: {data.get('success')}")
    if data.get('success'):
        print(f"Min: {data['statistics']['min']}, Max: {data['statistics']['max']}")
    else:
        print(f"Error: {data.get('error')}")
    return response.status_code == 200

if __name__ == "__main__":
    print("Testing Distribution Visualizer API")
    print("=" * 50)
    
    results = {
        'Fixed Point Unsigned': test_fixed_point_unsigned(),
        'Fixed Point Signed Magnitude': test_fixed_point_signed_magnitude(),
        'Fixed Point Two\'s Complement': test_fixed_point_twos_complement(),
        'Fixed Point One\'s Complement': test_fixed_point_ones_complement(),
        'Floating Point': test_floating_point(),
        'Floating Point Base 10': test_floating_point_base10(),
        'Fixed Point Base 8': test_fixed_point_base8(),
    }
    
    print("\n" + "=" * 50)
    print("Summary:")
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"  {test_name}: {status}")
