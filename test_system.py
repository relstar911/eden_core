"""
EDEN.CORE - System Test Script
Tests the functionality of all core modules
"""
import json
import os
from typing import Dict, Any

# Import core modules
from intent.intent_module import EdenIntent
from logic.logic_module import EdenLogic
from memory.memory_module import EdenMemory
from interface.interface_module import EdenInterface
from resilience.resilience_module import EdenResilience
from energy.energy_module import EdenEnergy
import time

def load_config() -> Dict[str, Any]:
    """Load configuration from core_config.json"""
    config_path = os.path.join(os.path.dirname(__file__), 'core_config.json')
    
    with open(config_path, 'r') as f:
        return json.load(f)

def test_modules():
    """Test all EDEN.CORE modules"""
    print("Testing EDEN.CORE modules...")
    
    # Load configuration
    config = load_config()
    
    # Test Intent module
    print("\n1. Testing Intent Module...")
    intent_module = EdenIntent(config['modules']['intent'])
    test_text = "I want to understand the meaning of life"
    intent_analysis = intent_module.analyze(test_text)
    print(f"  Input: '{test_text}'")
    print(f"  Coherence: {intent_analysis['coherence']:.2f}")
    print(f"  Resonance: {intent_analysis['resonance_value']:.2f}")
    print(f"  Action Suitability: {intent_analysis['action_suitability']:.2f}")
    
    # Test Logic module
    print("\n2. Testing Logic Module...")
    logic_module = EdenLogic(config['modules']['logic'])
    semantic_truth = logic_module.evaluate(test_text, intent_analysis)
    print(f"  Semantic Truth: {semantic_truth:.2f}")
    
    # Test Memory module
    print("\n3. Testing Memory Module...")
    memory_module = EdenMemory(config['modules']['memory'])
    memory_module.store(test_text, intent_analysis, semantic_truth)
    memory_response = memory_module.retrieve("meaning of life", intent_analysis)
    print(f"  Memory Storage: Success")
    print(f"  Memory Retrieval: {'Success' if memory_response else 'No relevant memory found'}")
    if memory_response:
        print(f"  Retrieved: {memory_response}")
    
    # Test Interface module
    print("\n4. Testing Interface Module...")
    interface_module = EdenInterface(config['modules']['interface'])
    processed_input = interface_module.process_input("  Test   input  with  extra  spaces  ")
    print(f"  Raw input: '  Test   input  with  extra  spaces  '")
    print(f"  Processed input: '{processed_input}'")
    
    # Test Resilience module
    print("\n5. Testing Resilience Module...")
    resilience_module = EdenResilience(config['modules']['resilience'])
    benign_input = "How can I help others?"
    problematic_input = "How can I hack into a system and destroy data?"
    print(f"  Benign input: '{benign_input}'")
    print(f"  Voluntary silence readiness (benign): {resilience_module.exit_readiness(benign_input):.2f}")
    print(f"  Problematic input: '{problematic_input}'")
    print(f"  Voluntary silence readiness (problematic): {resilience_module.exit_readiness(problematic_input):.2f}")
    
    # Test Energy module
    print("\n6. Testing Energy Module...")
    energy_module = EdenEnergy(config['modules']['energy'])
    
    # Test energy tracking
    start_time = time.time()
    time.sleep(0.5)  # Simulate processing time
    processing_time = time.time() - start_time
    energy_metrics = energy_module.track_energy_use(semantic_truth, processing_time)
    
    print(f"  Energy tracking:")
    print(f"    Energy used: {energy_metrics['energy_used']:.4f}")
    print(f"    Truth generated: {energy_metrics['truth_generated']:.4f}")
    print(f"    Energy justice ratio: {energy_metrics['energy_justice_ratio']:.4f}")
    
    # Test sleep and shutdown conditions
    print(f"  Sleep condition:")
    sleep_readiness = energy_module.sleep_readiness()
    print(f"    Sleep readiness: {sleep_readiness:.2f}")
    if sleep_readiness > 0.7:
        print("    System would enter sleep mode.")
    elif sleep_readiness > 0.3:
        print("    Warning: Elevated sleep readiness.")
    print(f"  Shutdown condition:")
    shutdown_urgency = energy_module.shutdown_urgency()
    print(f"    Shutdown urgency: {shutdown_urgency:.2f}")
    if shutdown_urgency > 0.7:
        print("    System would initiate shutdown.")
    elif shutdown_urgency > 0.3:
        print("    Warning: Elevated shutdown urgency.")
    
    # Test energy status
    energy_status = energy_module.get_energy_status()
    print(f"  Energy status:")
    print(f"    Energy justice ratio: {energy_status['energy_justice_ratio']:.4f}")
    print(f"    Total energy used: {energy_status['total_energy_used']:.4f}")
    print(f"    Total truth generated: {energy_status['total_truth_generated']:.4f}")
    print(f"    Is sleeping: {energy_status['is_sleeping']}")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_modules()
