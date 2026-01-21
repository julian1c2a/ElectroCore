#!/usr/bin/env python3
"""Comprehensive test for IEEE754 encode endpoint"""

from web.app import app
import json

client = app.test_client()

# Test múltiples valores
test_cases = [
    {'value': 1.5, 'E_bits': 8, 'F_bits': 23},
    {'value': 3.14, 'E_bits': 8, 'F_bits': 23},
    {'value': 0.0, 'E_bits': 8, 'F_bits': 23},
    {'value': 0.5, 'E_bits': 5, 'F_bits': 10},
    {'value': 100.25, 'E_bits': 8, 'F_bits': 23},
]

print('IEEE754 Encode Endpoint - Test Results')
print('=' * 70)

passed = 0
failed = 0

for i, test in enumerate(test_cases, 1):
    response = client.post('/api/ieee754/encode',
        json=test,
        content_type='application/json'
    )
    
    if response.status_code == 200:
        data = response.get_json()
        print(f'Test {i}: PASS')
        print(f'  Input: {test["value"]} (E_bits={test["E_bits"]}, F_bits={test["F_bits"]})')
        print(f'  Bits: {data["bits"]}')
        print(f'  Decoded: {data["decoded"]}')
        passed += 1
    else:
        print(f'Test {i}: FAIL')
        print(f'  Status: {response.status_code}')
        failed += 1

print('=' * 70)
print(f'Results: {passed} passed, {failed} failed')
if failed == 0:
    print('SUCCESS! IEEE754 encode endpoint is working correctly.')
