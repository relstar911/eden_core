"""
Test für das verbesserte Intent-Modul mit transparenten Formeln
"""

import json
import os
import sys
from typing import Dict, Any

# Pfade für den Import der Module hinzufügen
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import des verbesserten Intent-Moduls
from intent.intent_module import EdenIntent

def load_config():
    """Lädt die Konfiguration aus der core_config.json Datei"""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'core_config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Fehler beim Laden der Konfiguration. Verwende Standardkonfiguration.")
        return {
            'intent': {'enabled': True}
        }

def print_separator(title):
    """Gibt einen Trennbalken mit Titel aus"""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)

def test_intent_module():
    """Testet das Intent-Modul mit verschiedenen Eingaben"""
    # Konfiguration laden
    config = load_config()
    
    # Intent-Modul initialisieren
    intent_module = EdenIntent(config.get('intent', {}))
    
    # Testeingaben definieren
    test_inputs = [
        "Ich bin glücklich und zufrieden mit meinem Leben.",
        "Ich bin traurig, obwohl ich eigentlich glücklich sein sollte.",
        "Die Wahrheit ist wichtiger als Optimierung und Effizienz.",
        "Wir müssen unbedingt mehr Energie verbrauchen, um schneller zu sein.",
        "Könnte das System bitte selbst entscheiden, wann es Pausen einlegen möchte?"
    ]
    
    print_separator("INTENT-MODUL TEST MIT TRANSPARENTEN FORMELN")
    
    for i, text in enumerate(test_inputs):
        print(f"\nTest {i+1}: \"{text}\"")
        result = intent_module.analyze(text)
        
        print(f"Kohärenz: {result['coherence']:.2f}")
        print(f"Freiheitsgrad: {result['freedom_degree']:.2f}")
        print(f"Resonanzwert: {result['resonance_value']:.2f}")
        print(f"Handlungseignung: {result['action_suitability']:.2f}")
        
        # Details der Berechnung anzeigen
        print("\nBerechnungsdetails:")
        details = result.get('calculation_details', {})
        
        # Kohärenzberechnung
        if 'coherence' in details:
            coherence_details = details['coherence']
            print(f"  Kohärenzformel: {coherence_details.get('formula', 'N/A')}")
            print(f"  Relationsfaktor: {coherence_details.get('relation_factor', 0):.2f}")
            print(f"  Strukturfaktor: {coherence_details.get('structure_factor', 0):.2f}")
            print(f"  Längenfaktor: {coherence_details.get('length_factor', 0):.2f}")
        
        # Semantische Relationen anzeigen
        if 'semantic_relations' in details:
            print("\nGefundene semantische Relationen:")
            for rel in details.get('semantic_relations', []):
                print(f"  {rel['subject']} {rel['relation']} {rel['object']} (Gewicht: {rel['weight']:.2f})")

if __name__ == "__main__":
    test_intent_module()
