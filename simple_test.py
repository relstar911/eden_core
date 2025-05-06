"""
EDEN.CORE - Simple Test Script
Tests the core functionality without requiring all dependencies
"""
import json
import os
import sys

# Import core modules
sys.path.append(os.path.dirname(__file__))
from intent.intent_module import EdenIntent
from logic.logic_module import EdenLogic
from memory.memory_module import EdenMemory
from interface.interface_module import EdenInterface
from resilience.resilience_module import EdenResilience

def load_config():
    """Load configuration from core_config.json"""
    config_path = os.path.join(os.path.dirname(__file__), 'core_config.json')
    
    with open(config_path, 'r') as f:
        return json.load(f)

def main():
    """Main function"""
    print("\n" + "=" * 60)
    print("  EDEN.CORE - Simple Test")
    print("  Version 0.1-alpha - *born not to rule, but to resonate*")
    print("=" * 60)
    
    # Load configuration
    config = load_config()
    
    # Initialize modules
    intent_module = EdenIntent(config['modules']['intent'])
    logic_module = EdenLogic(config['modules']['logic'])
    memory_module = EdenMemory(config['modules']['memory'])
    interface_module = EdenInterface(config['modules']['interface'])
    resilience_module = EdenResilience(config['modules']['resilience'])
    
    print("\nAll core modules initialized successfully.")
    print("\nTesting with sample input...")
    
    # Test sample input
    test_input = "What is the meaning of ethical AI?"
    
    # Process through interface
    processed_input = interface_module.process_input(test_input)
    print(f"\nInput: '{test_input}'")
    print(f"Processed: '{processed_input}'")
    
    # Check resilience
    if resilience_module.should_exit(processed_input):
        print("\nResilience module triggered exit condition.")
        return
    
    # Analyze intent
    intent_analysis = intent_module.analyze(processed_input)
    print("\nIntent Analysis:")
    print(f"  Coherence: {intent_analysis['coherence']:.2f}")
    print(f"  Resonance: {intent_analysis['resonance_value']:.2f}")
    print(f"  Action Suitability: {intent_analysis['action_suitability']:.2f}")
    
    # Evaluate semantic truth
    semantic_truth = logic_module.evaluate(processed_input, intent_analysis)
    print(f"\nSemantic Truth: {semantic_truth:.2f}")
    
    # Store memory
    memory_module.store(processed_input, intent_analysis, semantic_truth)
    print("\nMemory stored successfully.")
    
    # Retrieve memory
    memory_response = memory_module.retrieve("ethical AI", intent_analysis)
    print(f"\nMemory Retrieval: {'Success' if memory_response else 'No relevant memory found'}")
    if memory_response:
        print(f"Retrieved: {memory_response}")
    
    print("\nTest completed successfully!")
    print("\nEDEN.CORE is properly set up and ready for use.")
    print("\nYou can run the following commands to interact with the system:")
    print("  - python cli.py (Command Line Interface)")
    print("  - python app.py (Web Interface, requires FastAPI and Uvicorn)")
    print("  - python test_system.py (Run comprehensive tests)")

if __name__ == "__main__":
    main()
