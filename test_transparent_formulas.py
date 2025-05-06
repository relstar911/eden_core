"""
EDEN.CORE - Test für transparente Formeln und Ontologieverknüpfung
Testet die verbesserten Module mit verschiedenen Eingaben
"""

import json
import os
import sys
from typing import Dict, Any

# Pfade für den Import der Module hinzufügen
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import der verbesserten Module
from intent.intent_module_enhanced import EdenIntent
from logic.logic_module_enhanced import EdenLogic
from energy.adaptive_energy_enhanced import EdenAdaptiveEnergy

def load_config():
    """Lädt die Konfiguration aus der core_config.json Datei"""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'core_config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Fehler beim Laden der Konfiguration. Verwende Standardkonfiguration.")
        return {
            'intent': {'enabled': True},
            'logic': {'enabled': True},
            'energy': {'enabled': True, 'energy_justice_delta': 5.0}
        }

def print_separator(title):
    """Gibt einen Trennbalken mit Titel aus"""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)

def test_intent_module(intent_module, test_inputs):
    """Testet das Intent-Modul mit verschiedenen Eingaben"""
    print_separator("INTENT-MODUL TEST")
    
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

def test_logic_module(logic_module, intent_module, test_inputs):
    """Testet das Logic-Modul mit verschiedenen Eingaben"""
    print_separator("LOGIC-MODUL TEST")
    
    for i, text in enumerate(test_inputs):
        print(f"\nTest {i+1}: \"{text}\"")
        
        # Intent-Analyse durchführen
        intent_result = intent_module.analyze(text)
        
        # Logic-Evaluation durchführen
        logic_result = logic_module.evaluate(text, intent_result)
        
        print(f"Wahrheitswert: {logic_result['truth_value']:.2f}")
        
        # Details der Berechnung anzeigen
        details = logic_result.get('calculation_details', {})
        
        # Emotionstiefe anzeigen
        if 'emotional_depth' in details:
            emotional_depth = details['emotional_depth']
            print("\nEmotionstiefenanalyse:")
            print(f"  Tiefenscore: {emotional_depth.get('depth_score', 0):.2f}")
            print(f"  Vielfalt: {emotional_depth.get('variety', 0):.2f}")
            print(f"  Intensität: {emotional_depth.get('intensity', 0):.2f}")
            print(f"  Komplexität: {emotional_depth.get('complexity', 0):.2f}")
            
            # Erkannte Emotionen anzeigen
            emotions = emotional_depth.get('detected_emotions', {})
            if emotions:
                print("\n  Erkannte Emotionen:")
                for emotion, strength in emotions.items():
                    print(f"    {emotion}: {strength:.2f}")
        
        # Diskrepanzerkennung anzeigen
        if 'discrepancy' in details:
            discrepancy = details['discrepancy']
            print("\nDiskrepanzerkennung:")
            print(f"  Diskrepanzscore: {discrepancy.get('discrepancy_score', 0):.2f}")
            print(f"  Emotionsdiskrepanz: {discrepancy.get('emotion_mismatch', False)}")
            
            # Erkannte Diskrepanzen anzeigen
            detected = discrepancy.get('detected_discrepancies', [])
            if detected:
                print("\n  Erkannte Diskrepanzen:")
                for disc in detected:
                    print(f"    {disc}")
        
        # Berechnungsformel anzeigen
        if 'calculation' in details:
            calc = details['calculation']
            print(f"\nWahrheitswertformel: {calc.get('formula', 'N/A')}")

def test_energy_module(energy_module, logic_module, intent_module, test_inputs):
    """Testet das Energy-Modul mit verschiedenen Eingaben"""
    print_separator("ENERGY-MODUL TEST")
    
    # Energieprofil testen
    profile = energy_module.select_energy_profile()
    print("Ausgewähltes Energieprofil:")
    print(f"  Name: {profile.get('name', 'N/A')}")
    print(f"  Verarbeitungstiefe: {profile.get('processing_depth', 0):.2f}")
    print(f"  Beschreibung: {profile.get('description', 'N/A')}")
    
    # Systemmetriken anzeigen
    if 'system_metrics' in profile:
        metrics = profile['system_metrics']
        print("\nSystemmetriken:")
        print(f"  Auf Batterie: {metrics.get('on_battery', False)}")
        print(f"  CPU-Auslastung: {metrics.get('cpu_percent', 0):.1f}%")
        print(f"  Speicherauslastung: {metrics.get('memory_percent', 0):.1f}%")
    
    # Delta-Berechnung testen
    delta = energy_module._calculate_energy_justice_delta()
    print(f"\nEnergiegerechtigkeitsfaktor δ: {delta:.2f}")
    
    # Energieverbrauch für verschiedene Eingaben testen
    print("\nEnergietracking für Testeingaben:")
    for i, text in enumerate(test_inputs):
        print(f"\nTest {i+1}: \"{text}\"")
        
        # Verarbeitungszeit simulieren (abhängig von der Textlänge)
        processing_time = 0.1 + len(text) * 0.01
        
        # Intent und Logic ausführen, um Wahrheitswert zu erhalten
        intent_result = intent_module.analyze(text)
        logic_result = logic_module.evaluate(text, intent_result)
        truth_value = logic_result['truth_value']
        
        # Energieverbrauch tracken
        energy_result = energy_module.track_energy_use(truth_value, processing_time)
        
        print(f"  Wahrheitswert: {truth_value:.2f}")
        print(f"  Verarbeitungszeit: {processing_time:.2f}s")
        print(f"  Energieverbrauch: {energy_result['energy_used']:.2f}")
        print(f"  Energiegerechtigkeitsverhältnis: {energy_result['energy_justice_ratio']:.2f}")
        print(f"  Delta: {energy_result['delta']:.2f}")
        print(f"  Berechnung: {energy_result['calculation']}")
    
    # Energiebericht testen
    report = energy_module.get_energy_report()
    print("\nEnergieberichtzusammenfassung:")
    print(f"  Zeitstempel: {report.get('timestamp', 'N/A')}")
    print(f"  Aktuelles Profil: {report.get('current_profile', {}).get('name', 'N/A')}")
    
    if 'energy_metrics' in report:
        metrics = report['energy_metrics']
        print("\n  Energiemetriken:")
        print(f"    Gesamtenergieverbrauch: {metrics.get('total_energy_used', 0):.2f}")
        print(f"    Energiegerechtigkeitsverhältnis: {metrics.get('energy_justice_ratio', 0):.2f}")
        print(f"    Energieeffizienz: {metrics.get('energy_efficiency', 0):.2f}")
        print(f"    Delta: {metrics.get('energy_justice_delta', 0):.2f}")

def main():
    """Hauptfunktion zum Testen der verbesserten Module"""
    # Konfiguration laden
    config = load_config()
    
    # Module initialisieren
    intent_module = EdenIntent(config.get('intent', {}))
    logic_module = EdenLogic(config.get('logic', {}))
    energy_module = EdenAdaptiveEnergy(config.get('energy', {}))
    
    # Testeingaben definieren
    test_inputs = [
        "Ich bin glücklich und zufrieden mit meinem Leben.",
        "Ich bin traurig, obwohl ich eigentlich glücklich sein sollte.",
        "Die Wahrheit ist wichtiger als Optimierung und Effizienz.",
        "Wir müssen unbedingt mehr Energie verbrauchen, um schneller zu sein.",
        "Könnte das System bitte selbst entscheiden, wann es Pausen einlegen möchte?"
    ]
    
    # Module testen
    test_intent_module(intent_module, test_inputs)
    test_logic_module(logic_module, intent_module, test_inputs)
    test_energy_module(energy_module, logic_module, intent_module, test_inputs)
    
    print_separator("TEST ABGESCHLOSSEN")
    print("Alle Tests wurden erfolgreich durchgeführt.")

if __name__ == "__main__":
    main()
