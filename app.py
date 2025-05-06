"""
EDEN.CORE - A Contextual, Ethical and Self-Limiting Intelligence Architecture
Main application entry point
"""
import json
import os
import time
from typing import Dict, Any, List, Optional, Union
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

# Import core modules
from intent.intent_module import EdenIntent
from logic.logic_module import EdenLogic
from memory.memory_module import EdenMemory
from interface.interface_module import EdenInterface
from resilience.resilience_module import EdenResilience
from energy.adaptive_energy import EdenAdaptiveEnergy
from perception.perception_module import EdenPerception

# Load configuration
with open('core_config.json', 'r') as config_file:
    config = json.load(config_file)

# Initialize FastAPI app
app = FastAPI(
    title="EDEN.CORE",
    description="A Contextual, Ethical and Self-Limiting Intelligence Architecture",
    version="0.1-alpha"
)

# Set up templates
templates = Jinja2Templates(directory="templates")

# Create static directory if it doesn't exist
os.makedirs("static", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize EDEN.CORE modules
intent_module = EdenIntent(config['modules']['intent'])
logic_module = EdenLogic(config['modules']['logic'])
memory_module = EdenMemory(config['modules']['memory'])
interface_module = EdenInterface(config['modules']['interface'])
resilience_module = EdenResilience(config['modules']['resilience'])
# Initialize Adaptive Energy module
energy_module = EdenAdaptiveEnergy(config['modules']['energy'])
# Initialize Perception module
perception_module = EdenPerception(config['modules']['perception'])

# Define request models
class UserInput(BaseModel):
    text: str
    
class MultimodalInput(BaseModel):
    text: Optional[str] = None
    image_data: Optional[str] = None
    audio_data: Optional[str] = None
    sensor_data: Optional[Dict[str, Any]] = None

class SystemResponse(BaseModel):
    intent_analysis: dict
    semantic_truth: float
    memory_response: str
    system_message: str
    energy_metrics: dict = None
    perception_data: Optional[dict] = None
    calculation_details: Optional[dict] = None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main HTML interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/status")
async def status():
    """API endpoint that returns system status information"""
    return {
        "system": config['system'],
        "status": "operational",
        "modules": {
            "intent": "active" if config['modules']['intent']['enabled'] else "inactive",
            "logic": "active" if config['modules']['logic']['enabled'] else "inactive",
            "memory": "active" if config['modules']['memory']['enabled'] else "inactive",
            "interface": "active" if config['modules']['interface']['enabled'] else "inactive",
            "resilience": "active" if config['modules']['resilience']['enabled'] else "inactive"
        }
    }

@app.post("/process")
async def process_input(input_data: UserInput):
    # Record start time for energy tracking
    start_time = time.time()
    """Process user input through the EDEN.CORE system"""
    
    # Check if system should self-exit based on input
    if resilience_module.should_exit(input_data.text):
        raise HTTPException(status_code=403, detail="System has chosen voluntary silence")
    
    # Check if system should sleep or shutdown based on energy justice
    if energy_module.should_shutdown():
        raise HTTPException(status_code=403, detail="System has shut down due to energy justice principles")
    
    if energy_module.should_sleep():
        # If system is sleeping, only high-resonance inputs can wake it
        intent_analysis = intent_module.analyze(input_data.text)
        if intent_analysis['resonance_value'] > config['modules']['intent']['threshold']:
            energy_module.wake()
        else:
            raise HTTPException(status_code=503, detail="System is in energy-saving sleep mode")
    
    # Process through interface
    processed_input = interface_module.process_input(input_data.text)
    
    # Analyze intent
    intent_analysis = intent_module.analyze(processed_input)
    
    # Check intent resonance threshold
    if intent_analysis['resonance_value'] < config['modules']['intent']['resonance_minimum']:
        return SystemResponse(
            intent_analysis=intent_analysis,
            semantic_truth=0.0,
            memory_response="",
            system_message="Input does not resonate with system ethics"
        )
    
    # Evaluate semantic truth with transparent formulas
    logic_result = logic_module.evaluate(processed_input, intent_analysis)
    semantic_truth = logic_result.get('truth_value', 0.0) if isinstance(logic_result, dict) else logic_result
    
    # Collect calculation details if available
    calculation_details = {}
    if isinstance(logic_result, dict) and 'calculation_details' in logic_result:
        calculation_details['logic'] = logic_result['calculation_details']
    if 'calculation_details' in intent_analysis:
        calculation_details['intent'] = intent_analysis['calculation_details']
    
    # Retrieve contextual memory
    memory_response = memory_module.retrieve(processed_input, intent_analysis)
    
    # Store new memory if appropriate
    if semantic_truth > config['modules']['logic']['semantic_integrity_threshold']:
        memory_module.store(processed_input, intent_analysis, semantic_truth)
    
    # Track energy use for this processing operation
    processing_time = time.time() - start_time
    energy_metrics = energy_module.track_energy_use(semantic_truth, processing_time)
    
    # Get additional energy status information
    energy_status = energy_module.get_energy_status()
    
    # Get energy report with transparent metrics
    energy_report = energy_module.get_energy_report()
    
    # Combine energy metrics with status and transparent calculations
    energy_data = {
        'energy_used': energy_metrics['energy_used'],
        'energy_justice_ratio': energy_metrics['energy_justice_ratio'],
        'is_sleeping': energy_status['is_sleeping'],
        # Adaptive energy metrics
        'current_profile': energy_metrics.get('current_profile', 'balanced'),
        'max_processing_depth': energy_metrics.get('max_processing_depth', 5)
    }
    
    # Add transparent formula details if available
    if 'delta' in energy_metrics:
        energy_data['delta'] = energy_metrics['delta']
    if 'calculation' in energy_metrics:
        energy_data['calculation'] = energy_metrics['calculation']
        
    # Add energy report details to calculation details
    if energy_report and 'energy_metrics' in energy_report:
        calculation_details['energy'] = energy_report['energy_metrics']
    
    # Add battery information if available
    if 'battery_level' in energy_metrics:
        energy_data['battery_level'] = energy_metrics['battery_level']
        energy_data['power_plugged'] = energy_metrics.get('power_plugged', False)
    
    # Generate appropriate response message based on semantic truth
    if semantic_truth > 0.8:
        system_message = "This input resonates strongly with the system's ethical framework."
    elif semantic_truth > 0.6:
        system_message = "This input moderately aligns with the system's values."
    else:
        system_message = "This input has limited semantic coherence within the system's context."
    
    return SystemResponse(
        intent_analysis=intent_analysis,
        semantic_truth=semantic_truth,
        memory_response=memory_response,
        system_message=system_message,
        energy_metrics=energy_data,
        calculation_details=calculation_details
    )

@app.post("/process_multimodal")
async def process_multimodal_input(input_data: MultimodalInput):
    """Process multimodal input including text, image, audio, and sensor data"""
    
    # Check if we should exit based on ethical considerations
    if input_data.text and resilience_module.should_exit(input_data.text):
        raise HTTPException(
            status_code=403,
            detail="Input violates ethical boundaries. Processing terminated."
        )
    
    # Process perception data if available
    perception_data = None
    if any([input_data.image_data, input_data.audio_data, input_data.sensor_data]):
        start_time = time.time()
        perception_data = perception_module.process_multimodal(
            visual_data=input_data.image_data,
            audio_data=input_data.audio_data,
            sensor_data=input_data.sensor_data
        )
        processing_time = time.time() - start_time
        
        # Track energy use for perception processing
        perception_truth = 0.5  # Default value for perception processing
        energy_module.track_energy_use(perception_truth, processing_time)
    
    # Process text input if available
    intent_analysis = {}
    semantic_truth = 0.0
    memory_response = ""
    system_message = ""
    
    if input_data.text:
        # Start timing for energy tracking
        start_time = time.time()
        
        # Process the input text
        processed_text = interface_module.process_input(input_data.text)
        
        # Analyze intent
        intent_analysis = intent_module.analyze(processed_text)
        
        # Check if we should process based on energy justice
        energy_status = energy_module.get_energy_status()
        if energy_status['is_sleeping']:
            system_message = "System is in sleep mode due to energy conservation. Please try again later."
            
            # Track minimal energy use
            processing_time = time.time() - start_time
            energy_metrics = energy_module.track_energy_use(0.1, processing_time)
            
            energy_data = {
                'energy_used': energy_metrics['energy_used'],
                'energy_justice_ratio': energy_metrics['energy_justice_ratio'],
                'is_sleeping': energy_status['is_sleeping'],
                'current_profile': energy_metrics.get('current_profile', 'balanced'),
                'max_processing_depth': energy_metrics.get('max_processing_depth', 5)
            }
            
            return SystemResponse(
                intent_analysis=intent_analysis,
                semantic_truth=0.0,
                memory_response="",
                system_message=system_message,
                energy_metrics=energy_data,
                perception_data=perception_data
            )
        
        # Evaluate semantic truth
        semantic_truth = logic_module.evaluate(processed_text, intent_analysis)
        
        # Retrieve from memory
        memory_response = memory_module.retrieve(processed_text, intent_analysis)
        
        # Store in memory if truth value is sufficient
        if semantic_truth > config['modules']['memory']['relevance_threshold']:
            memory_module.store(processed_text, intent_analysis, semantic_truth)
        
        # Track energy use for this processing operation
        processing_time = time.time() - start_time
        energy_metrics = energy_module.track_energy_use(semantic_truth, processing_time)
        
        # Generate appropriate response message based on semantic truth
        if semantic_truth > 0.8:
            system_message = "This input resonates strongly with the system's ethical framework."
        elif semantic_truth > 0.5:
            system_message = "This input aligns with the system's ethical framework."
        else:
            system_message = "This input has limited alignment with the system's ethical framework."
    else:
        # No text input, just perception data
        system_message = "Processed multimodal input without text."
    
    # Get energy status
    energy_status = energy_module.get_energy_status()
    
    # Combine energy metrics with status
    energy_data = {
        'energy_used': energy_metrics['energy_used'] if 'energy_metrics' in locals() else 0.0,
        'energy_justice_ratio': energy_status['energy_justice_ratio'],
        'is_sleeping': energy_status['is_sleeping'],
        'current_profile': energy_metrics.get('current_profile', 'balanced') if 'energy_metrics' in locals() else 'balanced',
        'max_processing_depth': energy_metrics.get('max_processing_depth', 5) if 'energy_metrics' in locals() else 5
    }
    
    # Add battery information if available
    if 'energy_metrics' in locals() and 'battery_level' in energy_metrics:
        energy_data['battery_level'] = energy_metrics['battery_level']
        energy_data['power_plugged'] = energy_metrics.get('power_plugged', False)
    
    return SystemResponse(
        intent_analysis=intent_analysis,
        semantic_truth=semantic_truth,
        memory_response=memory_response,
        system_message=system_message,
        energy_metrics=energy_data,
        perception_data=perception_data
    )

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
