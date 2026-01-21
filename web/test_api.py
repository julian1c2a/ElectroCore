#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for GeneratorFEExercises Web API

This script tests all API endpoints to ensure they're working correctly.
Run this after starting the Flask server.

Usage:
    python test_api.py
"""

import requests
import json
from urllib.parse import urljoin

BASE_URL = 'http://localhost:5000'

def test_endpoint(method, path, data=None, expected_status=200):
    """Test a single endpoint"""
    url = urljoin(BASE_URL, path)
    
    try:
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        else:
            return False, f"Unsupported method: {method}"
        
        success = response.status_code == expected_status
        return success, response.json() if success else response.text
    
    except requests.exceptions.ConnectionError:
        return False, "Connection error - is the server running?"
    except Exception as e:
        return False, str(e)

def run_tests():
    """Run all API tests"""
    
    print("""
╔═══════════════════════════════════════════════════════╗
║     GeneratorFEExercises - Web API Test Suite        ║
╚═══════════════════════════════════════════════════════╝
    """)
    
    tests = [
        # Health check
        {
            'name': 'Health Check',
            'method': 'GET',
            'path': '/api/health'
        },
        
        # IEEE754 encoding
        {
            'name': 'IEEE754 Encode',
            'method': 'POST',
            'path': '/api/ieee754/encode',
            'data': {'value': 5.5, 'base': 2, 'E_bits': 8, 'F_bits': 23}
        },
        
        # IEEE754 characteristics
        {
            'name': 'IEEE754 Characteristics',
            'method': 'POST',
            'path': '/api/ieee754/characteristics',
            'data': {'base': 2, 'E_bits': 8, 'F_bits': 23}
        },
        
        # IEEE754 special numbers
        {
            'name': 'IEEE754 Special Numbers',
            'method': 'POST',
            'path': '/api/ieee754/special',
            'data': {'base': 2, 'E_bits': 8, 'F_bits': 23}
        },
        
        # Base conversion
        {
            'name': 'Base Conversion',
            'method': 'POST',
            'path': '/api/convert',
            'data': {'value': '1234', 'from_base': 10, 'to_bases': [2, 8, 16]}
        },
        
        # Fixed-point distribution
        {
            'name': 'Fixed-Point Distribution',
            'method': 'POST',
            'path': '/api/distribution/fixed_point',
            'data': {'E': 4, 'F': 4, 'representation': 'unsigned'}
        },
        
        # BCD conversion
        {
            'name': 'BCD Conversion',
            'method': 'POST',
            'path': '/api/representations/bcd',
            'data': {'number': 42}
        },
        
        # Biquinario conversion
        {
            'name': 'Biquinario Conversion',
            'method': 'POST',
            'path': '/api/representations/biquinario',
            'data': {'number': 42}
        },
        
        # Compare representations
        {
            'name': 'Compare Representations',
            'method': 'POST',
            'path': '/api/representations/compare',
            'data': {'number': 42}
        },
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        name = test['name']
        method = test['method']
        path = test['path']
        data = test.get('data')
        
        print(f"\n[TEST] {name}")
        print(f"  → {method} {path}")
        
        success, response = test_endpoint(method, path, data)
        
        if success:
            print(f"  ✅ PASSED")
            if isinstance(response, dict):
                print(f"  Response: {json.dumps(response, indent=2)[:200]}...")
            passed += 1
        else:
            print(f"  ❌ FAILED")
            print(f"  Error: {response}")
            failed += 1
    
    print(f"\n{'-' * 55}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'-' * 55}\n")
    
    if failed == 0:
        print("✅ All tests passed!")
        return True
    else:
        print(f"❌ {failed} test(s) failed")
        return False

if __name__ == '__main__':
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
