# Transparent Formulas and Rule Sets for EDEN.CORE

This document describes the transparent formulas and rule sets implemented in EDEN.CORE to address the problems of black-box scoring, shallow resonance, and bias-prone weighting.

## 1. Black-Box Scoring: Transparent Formulas

### Intent Module (Coherence Calculation)

```
coherence = 0.4 * relation_factor + 0.3 * structure_factor + 0.3 * length_factor

Where:
- relation_factor = Number of semantic relations / (Token count * 0.2)
- structure_factor = 0.5 * question indicator + 0.5 * connector factor
- length_factor = 1.0 - min(1.0, abs(min(Word count, 40) - 20) / 20)
```

### Logic Module (Truth Value Calculation)

```
truth_value = 0.3 * coherence + 0.2 * (1 - uncertainty) + 0.2 * temporal_confidence + 
              0.2 * emotional_depth - 0.1 * discrepancy

Where:
- coherence = Coherence value from the Intent Module
- uncertainty = Uncertainty degree in the text
- temporal_confidence = Confidence of temporal orientation
- emotional_depth = Emotional depth
- discrepancy = Discrepancy between content and emotional expression
```

### Energy Module (Energy Justice Calculation)

```
E_justice = (T_total * δ) / P_consumed

Where:
- T_total = Semantic truth value
- δ = Energy justice factor (rule-based calculation)
- P_consumed = Consumed energy
```

## 2. Resonance Instead of Classification: Emotional Depth Analysis and Discrepancy Detection

### Emotional Depth Score

```
depth_score = 0.4 * variety + 0.3 * intensity + 0.3 * complexity

Where:
- variety = Number of recognized emotions / Total number of possible emotions
- intensity = Average intensity of recognized emotions
- complexity = Number of recognized emotional complexity patterns / Total number of possible patterns
```

### Discrepancy Detection

```
discrepancy_score = 0.4 * detected_discrepancies_ratio + 0.3 * emotion_mismatch + 0.3 * negation_with_positive

Where:
- detected_discrepancies_ratio = Number of detected discrepancies / Total number of possible discrepancies
- emotion_mismatch = 1.0 if discrepancy between positive and negative emotions, otherwise 0.0
- negation_with_positive = 1.0 if negation with positive emotions, otherwise 0.0
```

## 3. Bias-Prone Weighting: Training-Independent Logic Regulation (Delta Factor)

```
δ = base_delta * time_factor * load_adjustment * battery_factor * day_factor

Where:
- base_delta = Base value from configuration (default 5.0)
- time_factor = Time-dependent factor (1.2 at night, 0.8 during peak hours, 1.0 otherwise)
- load_adjustment = 1.0 - (system load * load factor)
- battery_factor = 1.2 if on battery, 1.5 if battery < 30%, otherwise 1.0
- day_factor = 0.9 on weekends, 1.0 on weekdays
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
# Example: Calculating the truth value
text = "I am happy, although I am sad."

# 1. Intent analysis with transparent formula
intent_analysis = eden_intent.analyze(text)
coherence = intent_analysis['coherence']  # e.g. 0.75

# 2. Emotional depth analysis
emotional_depth = eden_logic._analyze_emotional_depth(text)
# Detects both "happy" and "sad" -> high emotional complexity

# 3. Discrepancy detection
discrepancy = eden_logic._detect_discrepancy(text, semantic_context, emotional_depth)
# Detects discrepancy between "happy" and "sad" -> high discrepancy value

# 4. Truth value calculation with transparent formula
truth_value = 0.3 * coherence + 0.2 * certainty + 0.2 * temporal_confidence + \
    0.2 * emotional_depth['depth_score'] - 0.1 * discrepancy['discrepancy_score']
```

## 7. Implementation Details

The improved modules are implemented in the following files:

- `intent/intent_module_enhanced.py`: Enhanced intent analysis
- `logic/logic_module_enhanced.py`: Enhanced logic evaluation with emotional depth
- `energy/adaptive_energy_enhanced.py`: Enhanced adaptive energy

All modules use the ontologies and rule sets in:

- `data/ontology/semantic_relations.json`
- `data/emotion_patterns.json`
