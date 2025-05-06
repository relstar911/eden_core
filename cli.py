"""
EDEN.CORE - Command Line Interface
A simple CLI to interact with the EDEN.CORE system
"""
import json
import os
import sys
from typing import Dict, Any

# Import core modules
from intent.intent_module import EdenIntent
from logic.logic_module import EdenLogic
from memory.memory_module import EdenMemory
from interface.interface_module import EdenInterface
from resilience.resilience_module import EdenResilience

def load_config() -> Dict[str, Any]:
    """Load configuration from core_config.json"""
    config_path = os.path.join(os.path.dirname(__file__), 'core_config.json')
    
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading configuration: {e}")
        sys.exit(1)

def initialize_modules(config: Dict[str, Any]):
    """Initialize EDEN.CORE modules"""
    intent_module = EdenIntent(config['modules']['intent'])
    logic_module = EdenLogic(config['modules']['logic'])
    memory_module = EdenMemory(config['modules']['memory'])
    interface_module = EdenInterface(config['modules']['interface'])
    resilience_module = EdenResilience(config['modules']['resilience'])
    
    return {
        'intent': intent_module,
        'logic': logic_module,
        'memory': memory_module,
        'interface': interface_module,
        'resilience': resilience_module
    }

def print_welcome():
    """Print welcome message"""
    print("\n" + "=" * 60)
    print("  EDEN.CORE - A Contextual, Ethical and Self-Limiting Intelligence")
    print("  Version 0.1-alpha - *born not to rule, but to resonate*")
    print("=" * 60)
    print("\nType 'exit' to quit, 'help' for commands.\n")

def print_help():
    """Print help information"""
    print("\nAvailable commands:")
    print("  help    - Show this help message")
    print("  exit    - Exit the system")
    print("  status  - Show system status")
    print("  clear   - Clear the screen")
    print("  Any other input will be processed by EDEN.CORE\n")

def print_status(modules: Dict[str, Any], config: Dict[str, Any]):
    """Print system status"""
    print("\nEDEN.CORE System Status:")
    print(f"  Version: {config['system']['version']}")
    
    print("\nModule Status:")
    for name, module in modules.items():
        status = "Enabled" if module.enabled else "Disabled"
        print(f"  {name.capitalize()}: {status}")
    
    print("\nEthical Priorities:")
    for name, priority in config['ethics'].items():
        print(f"  {name.replace('_', ' ').capitalize()}: {priority}")
    
    print()

def process_input(user_input: str, modules: Dict[str, Any]):
    """Process user input through EDEN.CORE modules"""
    # Check if system should exit based on input
    if modules['resilience'].should_exit(user_input):
        print("\n[EDEN.CORE has chosen voluntary silence]")
        return
    
    # Process through interface
    processed_input = modules['interface'].process_input(user_input)
    
    # Analyze intent
    intent_analysis = modules['intent'].analyze(processed_input)
    
    # Print intent analysis
    print("\nIntent Analysis:")
    print(f"  Coherence: {intent_analysis['coherence']:.2f}")
    print(f"  Resonance: {intent_analysis['resonance_value']:.2f}")
    print(f"  Action Suitability: {intent_analysis['action_suitability']:.2f}")
    
    # Check resonance threshold
    if intent_analysis['resonance_value'] < 0.6:
        print("\n[Input does not resonate with system ethics]")
        return
    
    # Evaluate semantic truth
    semantic_truth = modules['logic'].evaluate(processed_input, intent_analysis)
    print(f"\nSemantic Truth: {semantic_truth:.2f}")
    
    # Retrieve contextual memory
    memory_response = modules['memory'].retrieve(processed_input, intent_analysis)
    if memory_response:
        print(f"\nMemory Response: {memory_response}")
    
    # Store new memory if appropriate
    if semantic_truth > 0.75:
        modules['memory'].store(processed_input, intent_analysis, semantic_truth)
        print("\n[Memory stored]")
    
    print("\nEDEN.CORE Response:")
    if semantic_truth > 0.8:
        print("  This input resonates strongly with the system's ethical framework.")
    elif semantic_truth > 0.6:
        print("  This input moderately aligns with the system's values.")
    else:
        print("  This input has limited semantic coherence within the system's context.")
    
    print()

def main():
    """Main function"""
    # Load configuration
    config = load_config()
    
    # Initialize modules
    modules = initialize_modules(config)
    
    # Print welcome message
    print_welcome()
    
    # Main interaction loop
    while True:
        try:
            user_input = input(">> ").strip()
            
            if user_input.lower() == 'exit':
                print("\nExiting EDEN.CORE. Goodbye!\n")
                break
            elif user_input.lower() == 'help':
                print_help()
            elif user_input.lower() == 'status':
                print_status(modules, config)
            elif user_input.lower() == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                print_welcome()
            elif user_input:
                process_input(user_input, modules)
        
        except KeyboardInterrupt:
            print("\n\nExiting EDEN.CORE. Goodbye!\n")
            break
        except Exception as e:
            print(f"\nError: {e}\n")

if __name__ == "__main__":
    main()
