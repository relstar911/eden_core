# Integrationsplan für transparente Formeln in EDEN.CORE

## 1. Ordnerstruktur

Die folgenden Dateien müssen in die Hauptstruktur integriert werden:

- `data/ontology/semantic_relations.json` → beibehalten
- `data/emotion_patterns.json` → beibehalten
- `intent/intent_module_enhanced.py` → in `intent/intent_module.py` integrieren
- `logic/logic_module_enhanced.py` → in `logic/logic_module.py` integrieren
- `energy/adaptive_energy_enhanced.py` → in `energy/adaptive_energy.py` integrieren

## 2. Integrationsschritte

### 2.1 Intent-Modul

1. Die Methoden zur Ontologieverknüpfung aus `intent_module_enhanced.py` in `intent_module.py` übernehmen
2. Die transparenten Formeln für Kohärenz, Freiheitsgrad und Resonanz implementieren
3. Die Berechnungsdetails in die Rückgabewerte integrieren

### 2.2 Logic-Modul

1. Die Emotionstiefenanalyse aus `logic_module_enhanced.py` in `logic_module.py` integrieren
2. Die Diskrepanzerkennung implementieren
3. Die transparente Wahrheitswertberechnung übernehmen

### 2.3 Energy-Modul

1. Die trainingsunabhängige Berechnung des Energiegerechtigkeitsfaktors δ integrieren
2. Die transparenten Formeln für Energieverbrauch und -gerechtigkeit übernehmen
3. Die detaillierten Berechnungsinformationen in die Rückgabewerte integrieren

## 3. Testplan

Nach der Integration sollten folgende Tests durchgeführt werden:

1. Einzeltests für jedes Modul mit verschiedenen Eingaben
2. Integrationstests für das Zusammenspiel der Module
3. Leistungstests zur Überprüfung der Effizienz

## 4. Dokumentation

Die Dokumentation sollte aktualisiert werden, um die transparenten Formeln und deren Vorteile zu erklären:

1. README.md aktualisieren
2. Dokumentation in `docs/transparent_formulas.md` beibehalten
3. Inline-Dokumentation in den Modulen aktualisieren

## 5. Zeitplan

1. Integration der Module: 1-2 Stunden
2. Tests: 1 Stunde
3. Dokumentation: 1 Stunde

Gesamtdauer: 3-4 Stunden
