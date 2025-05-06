# Transparente Formeln und Regelwerke für EDEN.CORE

Dieses Dokument beschreibt die transparenten Formeln und Regelwerke, die in EDEN.CORE implementiert wurden, um die Probleme von Black-Box-Scoring, oberflächlicher Resonanz und verzerrbarer Gewichtung zu beheben.

## 1. Black-Box Scoring: Transparente Formeln

### Intent-Modul (Kohärenz-Berechnung)

```
coherence = 0.4 * relation_factor + 0.3 * structure_factor + 0.3 * length_factor

Wobei:
- relation_factor = Anzahl semantischer Relationen / (Tokenanzahl * 0.2)
- structure_factor = 0.5 * hat_frage + 0.5 * connector_factor
- length_factor = 1.0 - min(1.0, abs(min(Wortanzahl, 40) - 20) / 20)
```

### Logic-Modul (Wahrheitswert-Berechnung)

```
truth_value = 0.3 * coherence + 0.2 * (1 - uncertainty) + 0.2 * temporal_confidence + 
              0.2 * emotional_depth - 0.1 * discrepancy

Wobei:
- coherence = Kohärenzwert aus dem Intent-Modul
- uncertainty = Unsicherheitsgrad im Text
- temporal_confidence = Konfidenz der zeitlichen Orientierung
- emotional_depth = Emotionale Tiefe
- discrepancy = Diskrepanz zwischen Inhalt und emotionalem Ausdruck
```

### Energy-Modul (Energiegerechtigkeits-Berechnung)

```
E_justice = (T_total * δ) / P_consumed

Wobei:
- T_total = Semantischer Wahrheitswert
- δ = Energiegerechtigkeitsfaktor (regelbasiert berechnet)
- P_consumed = Verbrauchte Energie
```

## 2. Resonanz statt Klassifikation: Emotionstiefenanalyse

### Emotionstiefe-Score

```
depth_score = 0.4 * variety + 0.3 * intensity + 0.3 * complexity

Wobei:
- variety = Anzahl erkannter Emotionen / Gesamtzahl möglicher Emotionen
- intensity = Durchschnittliche Intensität der erkannten Emotionen
- complexity = Anzahl erkannter Emotionskomplexitätsmuster / Gesamtzahl möglicher Muster
```

### Diskrepanzerkennung

```
discrepancy_score = 0.4 * detected_discrepancies_ratio + 0.3 * emotion_mismatch + 0.3 * negation_with_positive

Wobei:
- detected_discrepancies_ratio = Anzahl erkannter Diskrepanzen / Gesamtzahl möglicher Diskrepanzen
- emotion_mismatch = 1.0 wenn Diskrepanz zwischen positiven und negativen Emotionen, sonst 0.0
- negation_with_positive = 1.0 wenn Verneinung mit positiven Emotionen, sonst 0.0
```

## 3. Verzerrbare Gewichtung: Trainingsunabhängige Logikregelung

### Energiegerechtigkeitsfaktor δ

```
δ = base_delta * time_factor * load_adjustment * battery_factor * day_factor

Wobei:
- base_delta = Basiswert aus Konfiguration (standardmäßig 5.0)
- time_factor = Zeitabhängiger Faktor (1.2 nachts, 0.8 zu Spitzenzeiten, 1.0 sonst)
- load_adjustment = 1.0 - (system_load * load_factor)
- battery_factor = 1.2 wenn auf Batterie, 1.5 wenn Batterie < 30%, sonst 1.0
- day_factor = 0.9 am Wochenende, 1.0 an Werktagen
```

### Resonanzwert-Berechnung

```
resonance = weighted_sum * anti_factor * relation_factor

Wobei:
- weighted_sum = Summe(principle_scores * weights)
- anti_factor = 1.0 - (anti_matches * 0.3)
- relation_factor = 1.0 + sum(relation_weights) / len(relation_weights) * 0.2
```

## 4. Ontologie und Regelwerke

### Semantische Ontologie

Die semantische Ontologie in `data/ontology/semantic_relations.json` definiert:

- **Konzepte**: Kernkonzepte wie Wahrheit, Bedeutung, Selbstbegrenzung, etc.
- **Relationen**: Beziehungen zwischen Konzepten wie "Wahrheit ermöglicht Bedeutung"
- **Domänenspezifische Konzepte**: Fachspezifische Konzepte und deren Beziehungen

### Emotionsmuster

Die Emotionsmuster in `data/emotion_patterns.json` definieren:

- **Emotionen**: Grundemotionen mit Erkennungsmustern und Intensitätsmodifikatoren
- **Emotionale Komplexitätsmuster**: Muster für emotionale Tiefe und Komplexität
- **Diskrepanzmuster**: Muster zur Erkennung von Widersprüchen zwischen Inhalt und Emotion

## 5. Vorteile der transparenten Implementierung

1. **Nachvollziehbarkeit**: Alle Berechnungen sind transparent und nachvollziehbar
2. **Unabhängigkeit von ML-Bias**: Keine Abhängigkeit von vortrainierten Modellen
3. **Anpassbarkeit**: Parameter können direkt angepasst werden
4. **Erklärbarkeit**: Detaillierte Berechnungspfade für besseres Verständnis
5. **Stabilität**: Konsistente Ergebnisse ohne Abhängigkeit von externen Diensten

## 6. Anwendungsbeispiel

```python
# Beispiel für die Berechnung des Wahrheitswerts
text = "Ich bin glücklich, obwohl ich traurig bin."

# 1. Intent-Analyse mit transparenter Formel
intent_analysis = eden_intent.analyze(text)
coherence = intent_analysis['coherence']  # z.B. 0.75

# 2. Emotionstiefenanalyse
emotional_depth = eden_logic._analyze_emotional_depth(text)
# Erkennt sowohl "glücklich" als auch "traurig" -> hohe emotionale Komplexität

# 3. Diskrepanzerkennung
discrepancy = eden_logic._detect_discrepancy(text, semantic_context, emotional_depth)
# Erkennt Diskrepanz zwischen "glücklich" und "traurig" -> hoher Diskrepanzwert

# 4. Wahrheitswert-Berechnung mit transparenter Formel
truth_value = 0.3 * coherence + 0.2 * certainty + 0.2 * temporal_confidence + 
              0.2 * emotional_depth['depth_score'] - 0.1 * discrepancy['discrepancy_score']
```

## 7. Implementierungsdetails

Die verbesserten Module sind in folgenden Dateien implementiert:

- `intent/intent_module_enhanced.py`: Verbesserte Intent-Analyse
- `logic/logic_module_enhanced.py`: Verbesserte Logik-Evaluation mit Emotionstiefe
- `energy/adaptive_energy_enhanced.py`: Verbesserte Energieadaptivität

Alle Module verwenden die Ontologien und Regelwerke in:

- `data/ontology/semantic_relations.json`
- `data/emotion_patterns.json`
