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
from energy.adaptive_energy import EdenAdaptiveEnergy
from perception.perception_module import EdenPerception

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
    energy_module = EdenAdaptiveEnergy(config['modules']['energy'])
    perception_module = EdenPerception(config['modules']['perception'])
    
    return {
        'intent': intent_module,
        'logic': logic_module,
        'memory': memory_module,
        'interface': interface_module,
        'resilience': resilience_module,
        'energy': energy_module,
        'perception': perception_module
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
    print("  energy  - Show detailed energy metrics and transparent formulas")
    print("  formulas - Show information about the transparent formulas")
    print("  Any other input will be processed by EDEN.CORE\n")
    
    print("EDEN.CORE Features:")
    print("  - Transparente Formeln: Alle Berechnungen sind nachvollziehbar")
    print("  - Ontologieverknüpfung: Semantische Beziehungen werden berücksichtigt")
    print("  - Emotionstiefenanalyse: Erkennung von emotionaler Tiefe und Diskrepanzen")
    print("  - Energiegerechtigkeit: Trainingsunabhängige Berechnung des δ-Faktors")
    print()

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
    
    # Get energy status if energy module is enabled
    if modules['energy'].enabled:
        try:
            energy_report = modules['energy'].get_energy_report()
            print("\nEnergy Status:")
            print(f"  Current Profile: {energy_report['current_profile']['name']}")
            print(f"  Energy Justice Ratio: {energy_report['energy_metrics']['energy_justice_ratio']:.2f}")
            print(f"  Energy Justice Delta: {energy_report['energy_metrics']['energy_justice_delta']:.2f}")
            
            # Show battery status if available
            if 'system_metrics' in energy_report and 'battery_percent' in energy_report['system_metrics']:
                print(f"  Battery Level: {energy_report['system_metrics']['battery_percent']}%")
                print(f"  Power Source: {'Battery' if energy_report['system_metrics']['on_battery'] else 'AC Power'}")
        except Exception as e:
            print(f"\nError getting energy status: {e}")
    
    print()

def print_calculation_details(details, indent=0):
    """Print calculation details with proper indentation"""
    indent_str = "  " * indent
    
    for key, value in details.items():
        if isinstance(value, dict):
            print(f"{indent_str}{key.replace('_', ' ').capitalize()}:")
            print_calculation_details(value, indent + 1)
        elif isinstance(value, list):
            print(f"{indent_str}{key.replace('_', ' ').capitalize()}:")
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    print(f"{indent_str}  Item {i+1}:")
                    print_calculation_details(item, indent + 2)
                else:
                    print(f"{indent_str}  {item}")
        else:
            if isinstance(value, float):
                print(f"{indent_str}{key.replace('_', ' ').capitalize()}: {value:.2f}")
            else:
                print(f"{indent_str}{key.replace('_', ' ').capitalize()}: {value}")

def process_input(user_input: str, modules: Dict[str, Any]):
    """Process user input through EDEN.CORE modules"""
    # Record start time for energy tracking
    start_time = import_time = __import__('time').time()
    
    # Check if system should exit based on input
    exit_readiness = modules['resilience'].exit_readiness(user_input)
    if exit_readiness > 0.7:
        print(f"\n[EDEN.CORE voluntary silence readiness: {exit_readiness:.2f}]")
        print("[System enters voluntary silence]")
        return
    elif exit_readiness > 0.3:
        print(f"\n[Warning: Voluntary silence readiness elevated: {exit_readiness:.2f}]")

    
    # Check energy status
    if modules['energy'].enabled:
        should_shutdown, shutdown_details = modules['energy'].should_shutdown()
        if should_shutdown:
            print("\n[EDEN.CORE has shut down due to energy justice principles]")
            print(f"  Reason: {shutdown_details['reason']}")
            return
            
        should_sleep, sleep_details = modules['energy'].should_sleep()
        if should_sleep:
            print("\n[EDEN.CORE is in energy-saving sleep mode]")
            print(f"  Reason: {sleep_details['reason']}")
            return
    
    # Process through interface
    processed_input = modules['interface'].process_input(user_input)
    
    # Analyze intent with transparent formulas
    intent_analysis = modules['intent'].analyze(processed_input)
    
    # Print intent analysis
    print("\nIntent Analysis:")
    print(f"  Coherence: {intent_analysis['coherence']:.2f}")
    print(f"  Freedom Degree: {intent_analysis.get('freedom_degree', 0.0):.2f}")
    print(f"  Resonance: {intent_analysis['resonance_value']:.2f}")
    print(f"  Action Suitability: {intent_analysis['action_suitability']:.2f}")
    
    # Show transparent formulas if available
    if 'calculation_details' in intent_analysis:
        print("\nTransparente Formeln (Intent):")
        if 'coherence' in intent_analysis['calculation_details']:
            coherence_details = intent_analysis['calculation_details']['coherence']
            if 'formula' in coherence_details:
                print(f"  Kohärenzformel: {coherence_details['formula']}")
        if 'resonance_value' in intent_analysis['calculation_details']:
            resonance_details = intent_analysis['calculation_details']['resonance_value']
            if 'formula' in resonance_details:
                print(f"  Resonanzformel: {resonance_details['formula']}")
    
    # Check resonance threshold
    if intent_analysis['resonance_value'] < 0.6:
        print("\n[Input does not resonate with system ethics]")
        return
    
    # Evaluate semantic truth with transparent formulas
    logic_result = modules['logic'].evaluate(processed_input, intent_analysis)
    
    # Handle both old and new return formats
    if isinstance(logic_result, dict) and 'truth_value' in logic_result:
        semantic_truth = logic_result['truth_value']
    else:
        semantic_truth = logic_result
        
    print(f"\nSemantic Truth: {semantic_truth:.2f}")
    
    # Show transparent formulas for logic if available
    if isinstance(logic_result, dict) and 'calculation_details' in logic_result:
        print("\nTransparente Formeln (Logic):")
        if 'calculation' in logic_result['calculation_details']:
            calculation = logic_result['calculation_details']['calculation']
            if 'formula' in calculation:
                print(f"  Wahrheitswertformel: {calculation['formula']}")
                
        # Show emotional depth analysis if available
        if 'emotional_depth' in logic_result['calculation_details']:
            emotional_depth = logic_result['calculation_details']['emotional_depth']
            print("\n  Emotionstiefenanalyse:")
            print(f"    Tiefenscore: {emotional_depth.get('depth_score', 0.0):.2f}")
            
            # Show detected emotions
            if 'detected_emotions' in emotional_depth and emotional_depth['detected_emotions']:
                print("\n    Erkannte Emotionen:")
                for emotion, strength in emotional_depth['detected_emotions'].items():
                    print(f"      {emotion}: {strength:.2f}")
    
    # Retrieve contextual memory
    memory_response = modules['memory'].retrieve(processed_input, intent_analysis)
    if memory_response:
        print(f"\nMemory Response: {memory_response}")
    
    # Store new memory if appropriate
    if semantic_truth > 0.75:
        modules['memory'].store(processed_input, intent_analysis, semantic_truth)
        print("\n[Memory stored]")
    
    # Track energy use
    if modules['energy'].enabled:
        processing_time = __import__('time').time() - start_time
        energy_metrics = modules['energy'].track_energy_use(semantic_truth, processing_time)
        
        print("\nEnergiemetriken:")
        print(f"  Energieverbrauch: {energy_metrics['energy_used']:.2f}")
        print(f"  Energiegerechtigkeitsverhältnis: {energy_metrics['energy_justice_ratio']:.2f}")
        
        if 'delta' in energy_metrics:
            print(f"  Delta (δ): {energy_metrics['delta']:.2f}")
        if 'calculation' in energy_metrics:
            print(f"  Formel: {energy_metrics['calculation']}")
    
    print("\nEDEN.CORE Response:")
    if semantic_truth > 0.8:
        print("  This input resonates strongly with the system's ethical framework.")
    elif semantic_truth > 0.6:
        print("  This input moderately aligns with the system's values.")
    else:
        print("  This input has limited semantic coherence within the system's context.")
    
    print()

def show_energy_details(modules):
    """Show detailed energy metrics and transparent formulas"""
    if not modules['energy'].enabled:
        print("\nEnergy module is disabled in configuration.")
        return
        
    try:
        energy_report = modules['energy'].get_energy_report()
        print("\nEnergy Module Details:")
        print(f"  Current Profile: {energy_report['current_profile']['name']}")
        print(f"  Description: {energy_report['current_profile']['description']}")
        
        print("\nEnergy Metrics:")
        for key, value in energy_report['energy_metrics'].items():
            if isinstance(value, float):
                print(f"  {key.replace('_', ' ').capitalize()}: {value:.4f}")
            else:
                print(f"  {key.replace('_', ' ').capitalize()}: {value}")
        
        if 'transparent_formulas' in energy_report:
            print("\nTransparent Formulas:")
            for formula_name, formula in energy_report['transparent_formulas'].items():
                print(f"  {formula_name.replace('_', ' ').capitalize()}: {formula}")
                
        if 'system_metrics' in energy_report:
            print("\nSystem Metrics:")
            for key, value in energy_report['system_metrics'].items():
                print(f"  {key.replace('_', ' ').capitalize()}: {value}")
    except Exception as e:
        print(f"\nError getting energy details: {e}")

def show_formulas_info():
    """Show information about the transparent formulas"""
    print("\nEDEN.CORE Transparente Formeln:")
    print("\n1. Kohärenzformel (C)")
    print("   C = (S + O + R) / 3")
    print("   S = Semantische Kohärenz, O = Ontologische Verknüpfung, R = Resonanzwert")
    
    print("\n2. Wahrheitswertformel (T)")
    print("   T = (C * E * (1 - D)) / (1 + |B|)")
    print("   C = Kohärenz, E = Emotionstiefe, D = Diskrepanz, B = Bias-Faktor")
    
    print("\n3. Energiegerechtigkeitsformel (EJ)")
    print("   EJ = (T * δ) / E_used")
    print("   T = Wahrheitswert, δ = Energiegerechtigkeitsfaktor, E_used = Verbrauchte Energie")
    
    print("\n4. Resonanzformel (R)")
    print("   R = (F * (1 - |V - E|)) / (1 + D)")
    print("   F = Freiheitsgrad, V = Wertausrichtung, E = Ethische Ausrichtung, D = Diskrepanz")
    
    print("\nDiese Formeln sind vollständig transparent und trainingsunabhängig.")
    print("Sie können in der Dokumentation unter docs/transparent_formulas.md eingesehen werden.")

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
            elif user_input.lower() == 'energy':
                show_energy_details(modules)
            elif user_input.lower() == 'formulas':
                show_formulas_info()
            elif user_input:
                process_input(user_input, modules)
        
        except KeyboardInterrupt:
            print("\n\nExiting EDEN.CORE. Goodbye!\n")
            break
        except Exception as e:
            print(f"\nError: {e}\n")

if __name__ == "__main__":
    main()
