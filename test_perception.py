"""
EDEN.CORE - Perception Module Test
Tests the functionality of the multimodal perception module
"""
import json
import time
import os
import numpy as np
from typing import Dict, Any
from PIL import Image

# Import perception module
from perception.perception_module import EdenPerception

def load_config() -> Dict[str, Any]:
    """Load configuration from core_config.json"""
    config_path = os.path.join(os.path.dirname(__file__), 'core_config.json')
    
    with open(config_path, 'r') as f:
        return json.load(f)

def create_test_image() -> Image.Image:
    """Create a simple test image"""
    # Create a simple gradient image
    width, height = 320, 240
    image = Image.new('RGB', (width, height))
    pixels = image.load()
    
    for x in range(width):
        for y in range(height):
            r = int(255 * x / width)
            g = int(255 * y / height)
            b = int(255 * (x + y) / (width + height))
            pixels[x, y] = (r, g, b)
            
    return image

def create_test_audio() -> np.ndarray:
    """Create a simple test audio signal"""
    # Create a simple sine wave
    sample_rate = 16000
    duration = 1.0  # seconds
    frequency = 440  # Hz (A4 note)
    
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    audio = np.sin(2 * np.pi * frequency * t) * 32767
    return audio.astype(np.int16)

def create_test_sensor_data() -> Dict[str, Any]:
    """Create test sensor data"""
    return {
        'temperature': 22.5,
        'humidity': 45.0,
        'light': 75.0,
        'motion': 0
    }

def test_perception():
    """Test the perception module"""
    print("Testing EDEN.CORE Perception Module...")
    
    # Load configuration
    config = load_config()
    
    # Initialize perception module
    perception_module = EdenPerception(config['modules']['perception'])
    
    # Test visual processing
    print("\n1. Testing Visual Processing...")
    test_image = create_test_image()
    visual_results = perception_module.process_visual(test_image)
    print(f"  Image dimensions: {visual_results.get('dimensions', 'N/A')}")
    print(f"  Aspect ratio: {visual_results.get('aspect_ratio', 'N/A'):.2f}")
    print(f"  Brightness: {visual_results.get('brightness', 'N/A'):.2f}")
    print(f"  Complexity: {visual_results.get('complexity', 'N/A'):.2f}")
    
    # Test audio processing
    print("\n2. Testing Audio Processing...")
    test_audio = create_test_audio()
    audio_results = perception_module.process_audio(test_audio)
    print(f"  Duration: {audio_results.get('duration', 'N/A'):.2f}s")
    print(f"  Amplitude: {audio_results.get('amplitude', 'N/A'):.2f}")
    print(f"  Dominant frequency: {audio_results.get('dominant_frequency', 'N/A'):.2f} Hz")
    
    # Test sensor processing
    print("\n3. Testing Sensor Processing...")
    test_sensor_data = create_test_sensor_data()
    sensor_results = perception_module.process_sensor(test_sensor_data)
    print(f"  Sensors: {sensor_results.get('sensors', 'N/A')}")
    print(f"  Changes detected: {len(sensor_results.get('changes', {}))}")
    print(f"  Patterns detected: {len(sensor_results.get('patterns', []))}")
    
    # Test multimodal processing
    print("\n4. Testing Multimodal Processing...")
    multimodal_results = perception_module.process_multimodal(
        visual_data=test_image,
        audio_data=test_audio,
        sensor_data=test_sensor_data
    )
    print(f"  Active modalities: {multimodal_results.get('modalities', [])}")
    
    if 'integrated' in multimodal_results:
        print("  Integrated results:")
        for corr_name, corr_data in multimodal_results['integrated'].get('correlation', {}).items():
            print(f"    {corr_name}: {corr_data.get('value', 'N/A'):.2f} - {corr_data.get('description', '')}")
    
    # Test multimodal context
    print("\n5. Testing Multimodal Context...")
    context = perception_module.get_multimodal_context()
    print(f"  Context timestamp: {context.get('timestamp', 'N/A')}")
    print(f"  Available contexts: {list(context.keys())}")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_perception()
