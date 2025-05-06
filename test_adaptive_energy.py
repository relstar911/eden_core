"""
EDEN.CORE - Adaptive Energy Module Test
Tests the functionality of the adaptive energy module
"""
import json
import time
import os
from typing import Dict, Any

# Import adaptive energy module
from energy.adaptive_energy import EdenAdaptiveEnergy

def load_config() -> Dict[str, Any]:
    """Load configuration from core_config.json"""
    config_path = os.path.join(os.path.dirname(__file__), 'core_config.json')
    
    with open(config_path, 'r') as f:
        return json.load(f)

def test_adaptive_energy():
    """Test the adaptive energy module"""
    print("Testing EDEN.CORE Adaptive Energy Module...")
    
    # Load configuration
    config = load_config()
    
    # Initialize adaptive energy module
    energy_module = EdenAdaptiveEnergy(config['modules']['energy'])
    
    # Test energy source detection
    print("\n1. Testing Energy Source Detection...")
    energy_source = energy_module.detect_energy_source()
    print(f"  Battery powered: {energy_source['battery_powered']}")
    if energy_source['battery_powered']:
        print(f"  Battery level: {energy_source['battery_level']:.2f}")
        print(f"  Power plugged: {energy_source['power_plugged']}")
    
    # Test profile selection
    print("\n2. Testing Energy Profile Selection...")
    profile = energy_module.select_energy_profile()
    print(f"  Selected profile: {profile}")
    print(f"  Profile details:")
    profile_details = energy_module.energy_profiles[profile]
    for key, value in profile_details.items():
        print(f"    {key}: {value}")
    
    # Test processing depth calculation
    print("\n3. Testing Processing Depth Calculation...")
    input_complexities = [2, 5, 8, 12]
    for complexity in input_complexities:
        depth = energy_module.get_processing_depth(complexity)
        print(f"  Input complexity: {complexity}, Max processing depth: {depth}")
    
    # Test memory limit calculation
    print("\n4. Testing Memory Limit Calculation...")
    memory_limit = energy_module.get_memory_limit()
    print(f"  Memory limit: {memory_limit:.2f} (proportion of available memory)")
    
    # Test energy tracking with different truth values
    print("\n5. Testing Energy Tracking...")
    truth_values = [0.3, 0.6, 0.9]
    for truth in truth_values:
        # Simulate processing time
        start_time = time.time()
        time.sleep(0.2)  # Simulate work
        processing_time = time.time() - start_time
        
        # Track energy use
        energy_metrics = energy_module.track_energy_use(truth, processing_time)
        
        print(f"\n  Truth value: {truth:.2f}, Processing time: {processing_time:.4f}s")
        print(f"  Energy used: {energy_metrics['energy_used']:.4f}")
        print(f"  Truth generated: {energy_metrics['truth_generated']:.4f}")
        print(f"  Energy justice ratio: {energy_metrics['energy_justice_ratio']:.4f}")
        print(f"  Current profile: {energy_metrics['current_profile']}")
        print(f"  Max processing depth: {energy_metrics['max_processing_depth']}")
    
    # Test processing limitation
    print("\n6. Testing Processing Limitation...")
    limit_info = energy_module.should_limit_processing(10)
    print(f"  Should limit: {limit_info['should_limit']}")
    print(f"  Current profile: {limit_info['current_profile']}")
    print(f"  Input complexity: {limit_info['input_complexity']}")
    print(f"  Max depth: {limit_info['max_depth']}")
    if limit_info['should_limit']:
        print(f"  Reason: {limit_info['reason']}")
        print(f"  Recommended depth: {limit_info['recommended_depth']}")
    
    # Test energy status
    print("\n7. Testing Energy Status...")
    status = energy_module.get_energy_status()
    print(f"  Energy justice ratio: {status['energy_justice_ratio']:.4f}")
    print(f"  Total energy used: {status['total_energy_used']:.4f}")
    print(f"  Total truth generated: {status['total_truth_generated']:.4f}")
    print(f"  Is sleeping: {status['is_sleeping']}")
    print(f"  Adaptive enabled: {status['adaptive_enabled']}")
    print(f"  Current profile: {status['current_profile']}")
    print(f"  Profile description: {status['profile_description']}")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_adaptive_energy()
