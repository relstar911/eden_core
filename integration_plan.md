# Integration Plan for Transparent Formulas in EDEN.CORE

## 1. Directory Structure

The following files must be integrated into the main structure:

- `data/ontology/semantic_relations.json` → keep
- `data/emotion_patterns.json` → keep
- `intent/intent_module_enhanced.py` → integrate into `intent/intent_module.py`
- `logic/logic_module_enhanced.py` → integrate into `logic/logic_module.py`
- `energy/adaptive_energy_enhanced.py` → integrate into `energy/adaptive_energy.py`

## 2. Integration Steps

### 2.1 Intent Module

1. Transfer ontology-linking methods from `intent_module_enhanced.py` into `intent_module.py`
2. Implement transparent formulas for coherence, degree of freedom, and resonance
3. Integrate calculation details into the return values

### 2.2 Logic Module

1. Integrate emotional depth analysis from `logic_module_enhanced.py` into `logic_module.py`
2. Implement discrepancy detection
3. Adopt transparent truth value calculation

### 2.3 Energy Module

1. Integrate training-independent calculation of the energy justice factor δ
2. Adopt transparent formulas for energy consumption and justice
3. Integrate detailed calculation information into the return values

## 3. Test Plan

After integration, the following tests should be performed:

1. Unit tests for each module with various inputs
2. Integration tests for module interaction
3. Performance tests to verify efficiency

## 4. Documentation

Documentation should be updated to explain the transparent formulas and their benefits:

1. Update README.md
2. Maintain documentation in `docs/transparent_formulas.md`
3. Update inline documentation in the modules

## 5. Timeline

1. Module integration: 1-2 hours
2. Testing: 1 hour
3. Documentation: 1 hour

Total duration: 3-4 hours
