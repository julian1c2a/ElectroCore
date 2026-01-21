#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Suite para APIs de Lenguajes Formales
==========================================

Tests para:
- Alfabetos (7 endpoints)
- Lenguajes (5 endpoints)
- Análisis (3 endpoints)

Uso:
    python test_formal_languages.py
"""

import requests
import json
import sys
from urllib.parse import urljoin

BASE_URL = 'http://localhost:5000'

# Almacenar IDs creados para cleanup posterior
created_alphabet_ids = []
created_language_ids = []

def test_endpoint(method, path, data=None, expected_status=200, description=""):
    """Test a single endpoint"""
    url = urljoin(BASE_URL, path)
    
    try:
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        elif method == 'PUT':
            response = requests.put(url, json=data, headers={'Content-Type': 'application/json'})
        elif method == 'DELETE':
            response = requests.delete(url)
        else:
            return False, "Unsupported method"
        
        success = response.status_code == expected_status
        try:
            data = response.json()
        except:
            data = response.text
        
        status_icon = "✅" if success else "❌"
        print(f"  {status_icon} {method:6} {path:50} [{response.status_code}]")
        
        if description:
            print(f"     └─ {description}")
        
        if not success:
            print(f"     └─ Expected: {expected_status}, Got: {response.status_code}")
            print(f"     └─ Response: {data}")
        
        return success, data
    
    except requests.exceptions.ConnectionError:
        print(f"  ❌ {method:6} {path:50} [ERROR]")
        print(f"     └─ Connection error - is the server running?")
        return False, "Connection error"
    except Exception as e:
        print(f"  ❌ {method:6} {path:50} [ERROR]")
        print(f"     └─ {str(e)}")
        return False, str(e)


def run_tests():
    """Run all tests for Formal Languages API"""
    
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║     GeneratorFEExercises - Formal Languages API Test Suite          ║
║                                                                      ║
║     Testing 15 new endpoints:                                       ║
║     • 7 Alphabet endpoints                                          ║
║     • 5 Language endpoints                                          ║
║     • 3 Analysis endpoints                                          ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    total_tests = 0
    passed_tests = 0
    
    # ===================================================================
    # PRUEBA 1: Verificar que el servidor está funcionando
    # ===================================================================
    print("\n[1] Health Check")
    print("─" * 70)
    success, resp = test_endpoint('GET', '/api/health', description="Server is alive")
    if success:
        passed_tests += 1
    total_tests += 1
    
    # ===================================================================
    # PRUEBA 2-8: APIs de Alfabetos (7 endpoints)
    # ===================================================================
    print("\n[2-8] Alphabet APIs (7 endpoints)")
    print("─" * 70)
    
    # 2.1 Obtener alfabetos preestablecidos
    success, resp = test_endpoint('GET', '/api/alphabets/presets/list', 
                                 description="List preset alphabets")
    if success:
        passed_tests += 1
        print(f"     └─ Found {resp.get('total', 0)} preset alphabets")
    total_tests += 1
    
    # 2.2 Listar alfabetos (vacío inicialmente)
    success, resp = test_endpoint('GET', '/api/alphabets',
                                 description="List all alphabets")
    if success:
        passed_tests += 1
        print(f"     └─ Found {resp.get('total', 0)} alphabets")
    total_tests += 1
    
    # 2.3 Crear un alfabeto personalizado
    alphabet_data = {
        'name': 'Custom Base-5',
        'symbols': ['0', '1', '2', '3', '4'],
        'initial_symbol': '0'
    }
    success, resp = test_endpoint('POST', '/api/alphabets', alphabet_data,
                                 expected_status=201,
                                 description="Create custom alphabet")
    if success:
        passed_tests += 1
        alphabet_id = resp.get('alphabet', {}).get('id')
        created_alphabet_ids.append(alphabet_id)
        print(f"     └─ Created alphabet: {alphabet_id}")
    else:
        alphabet_id = None
    total_tests += 1
    
    # 2.4 Obtener el alfabeto creado
    if alphabet_id:
        success, resp = test_endpoint('GET', f'/api/alphabets/{alphabet_id}',
                                     description="Get specific alphabet")
        if success:
            passed_tests += 1
            print(f"     └─ Alphabet cardinality: {resp.get('alphabet', {}).get('cardinality', 0)}")
        total_tests += 1
        
        # 2.5 Validar el alfabeto
        success, resp = test_endpoint('POST', f'/api/alphabets/{alphabet_id}/validate',
                                     description="Validate alphabet")
        if success:
            passed_tests += 1
            print(f"     └─ Valid: {resp.get('valid', False)}")
        total_tests += 1
        
        # 2.6 Actualizar el alfabeto
        update_data = {
            'name': 'Base-5 Updated'
        }
        success, resp = test_endpoint('PUT', f'/api/alphabets/{alphabet_id}', update_data,
                                     description="Update alphabet")
        if success:
            passed_tests += 1
            print(f"     └─ Updated name: {resp.get('alphabet', {}).get('name', '')}")
        total_tests += 1
    
    # 2.7 Crear otro alfabeto para después eliminarlo
    alphabet_data_2 = {
        'name': 'Temp Alphabet',
        'symbols': ['A', 'B', 'C'],
        'initial_symbol': 'A'
    }
    success, resp = test_endpoint('POST', '/api/alphabets', alphabet_data_2,
                                 expected_status=201,
                                 description="Create second alphabet")
    if success:
        passed_tests += 1
        temp_alphabet_id = resp.get('alphabet', {}).get('id')
        created_alphabet_ids.append(temp_alphabet_id)
        
        # Eliminar el segundo alfabeto
        success, resp = test_endpoint('DELETE', f'/api/alphabets/{temp_alphabet_id}',
                                     description="Delete alphabet")
        if success:
            passed_tests += 1
            created_alphabet_ids.remove(temp_alphabet_id)
        total_tests += 1
    
    total_tests += 1
    
    # ===================================================================
    # PRUEBA 9-13: APIs de Lenguajes (5 endpoints)
    # ===================================================================
    print("\n[9-13] Language APIs (5 endpoints)")
    print("─" * 70)
    
    if not alphabet_id:
        print("  ⚠️  Skipping language tests (no alphabet created)")
        print("\n[Results]")
        print("─" * 70)
    else:
        # 3.1 Listar lenguajes (vacío inicialmente)
        success, resp = test_endpoint('GET', '/api/languages',
                                     description="List all languages")
        if success:
            passed_tests += 1
            print(f"     └─ Found {resp.get('total', 0)} languages")
        total_tests += 1
        
        # 3.2 Crear un lenguaje
        language_data = {
            'name': 'All 2-letter words',
            'alphabet_id': alphabet_id,
            'length': 2,
            'conditions': 'All words of length 2'
        }
        success, resp = test_endpoint('POST', '/api/languages', language_data,
                                     expected_status=201,
                                     description="Create language")
        if success:
            passed_tests += 1
            language_id = resp.get('language', {}).get('id')
            created_language_ids.append(language_id)
            print(f"     └─ Created language: {language_id}")
        else:
            language_id = None
        total_tests += 1
        
        # 3.3 Generar palabras del lenguaje
        if language_id:
            generate_data = {
                'condition': 'all'
            }
            success, resp = test_endpoint('POST', f'/api/languages/{language_id}/generate',
                                         generate_data,
                                         description="Generate language words")
            if success:
                passed_tests += 1
                cardinality = resp.get('cardinality', 0)
                print(f"     └─ Generated {cardinality} words")
            total_tests += 1
            
            # 3.4 Obtener el lenguaje
            success, resp = test_endpoint('GET', f'/api/languages/{language_id}',
                                         description="Get specific language")
            if success:
                passed_tests += 1
                stats = resp.get('statistics', {})
                print(f"     └─ Cardinality: {stats.get('cardinality', 0)}")
            total_tests += 1
            
            # 3.5 Crear otro lenguaje para eliminarlo
            language_data_2 = {
                'name': 'Temp Language',
                'alphabet_id': alphabet_id,
                'length': 1,
                'conditions': 'Temporary'
            }
            success, resp = test_endpoint('POST', '/api/languages', language_data_2,
                                         expected_status=201,
                                         description="Create second language")
            if success:
                passed_tests += 1
                temp_language_id = resp.get('language', {}).get('id')
                
                # Generar palabras
                test_endpoint('POST', f'/api/languages/{temp_language_id}/generate',
                            {'condition': 'all'})
                
                # Eliminar
                success, resp = test_endpoint('DELETE', f'/api/languages/{temp_language_id}',
                                             description="Delete language")
                if success:
                    passed_tests += 1
            total_tests += 1
        
        # ===================================================================
        # PRUEBA 14-16: APIs de Análisis (3 endpoints)
        # ===================================================================
        print("\n[14-16] Analysis APIs (3 endpoints)")
        print("─" * 70)
        
        # 4.1 Obtener ordenamientos
        success, resp = test_endpoint('GET', '/api/analysis/orders',
                                     description="List all orderings")
        if success:
            passed_tests += 1
            print(f"     └─ Found {resp.get('total', 0)} orderings")
        total_tests += 1
        
        # 4.2 Analizar un lenguaje
        if language_id:
            success, resp = test_endpoint('GET', f'/api/analysis/languages/{language_id}/analyze',
                                         description="Analyze language")
            if success:
                passed_tests += 1
                coverage = resp.get('coverage', {})
                print(f"     └─ Coverage: {coverage.get('coverage_percentage', 0)}%")
            total_tests += 1
        
        # 4.3 Obtener estadísticas globales
        success, resp = test_endpoint('GET', '/api/analysis/statistics',
                                     description="Get global statistics")
        if success:
            passed_tests += 1
            alphabets = resp.get('alphabets', {})
            languages = resp.get('languages', {})
            print(f"     └─ Alphabets: {alphabets.get('total', 0)}")
            print(f"     └─ Languages: {languages.get('total_languages', 0)}")
        total_tests += 1
        
        # ===================================================================
        # Cleanup
        # ===================================================================
        print("\n[Cleanup]")
        print("─" * 70)
        
        for lang_id in created_language_ids:
            test_endpoint('DELETE', f'/api/languages/{lang_id}',
                         description=f"Delete language {lang_id[:8]}...")
        
        for alpha_id in created_alphabet_ids:
            test_endpoint('DELETE', f'/api/alphabets/{alpha_id}',
                         description=f"Delete alphabet {alpha_id[:8]}...")
        
        print("\n[Results]")
        print("─" * 70)
    
    # Print summary
    print(f"\n✅ PASSED: {passed_tests}/{total_tests}")
    print(f"❌ FAILED: {total_tests - passed_tests}/{total_tests}")
    print(f"📊 Success Rate: {(passed_tests/total_tests*100):.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test(s) failed")
        return 1


if __name__ == '__main__':
    try:
        exit_code = run_tests()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)
