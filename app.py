"""
EDEN.CORE - A Contextual, Ethical and Self-Limiting Intelligence Architecture
Main application entry point
"""
import json
import os
import time
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
from energy.energy_module import EdenEnergy

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
energy_module = EdenEnergy(config['modules']['energy'])

# Define request models
class UserInput(BaseModel):
    text: str

class SystemResponse(BaseModel):
    intent_analysis: dict
    semantic_truth: float
    memory_response: str
    system_message: str
    energy_metrics: dict = None

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

@app.post("/process", response_model=SystemResponse)
async def process_input(user_input: UserInput):
    # Record start time for energy tracking
    start_time = time.time()
    """Process user input through the EDEN.CORE system"""
    
    # Check if system should self-exit based on input
    if resilience_module.should_exit(user_input.text):
        raise HTTPException(status_code=403, detail="System has chosen voluntary silence")
    
    # Check if system should sleep or shutdown based on energy justice
    if energy_module.should_shutdown():
        raise HTTPException(status_code=403, detail="System has shut down due to energy justice principles")
    
    if energy_module.should_sleep():
        # If system is sleeping, only high-resonance inputs can wake it
        intent_analysis = intent_module.analyze(user_input.text)
        if intent_analysis['resonance_value'] > config['modules']['intent']['threshold']:
            energy_module.wake()
        else:
            raise HTTPException(status_code=503, detail="System is in energy-saving sleep mode")
    
    # Process through interface
    processed_input = interface_module.process_input(user_input.text)
    
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
    
    # Evaluate semantic truth
    semantic_truth = logic_module.evaluate(processed_input, intent_analysis)
    
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
    
    # Combine energy metrics with status
    energy_data = {
        'energy_used': energy_metrics['energy_used'],
        'energy_justice_ratio': energy_metrics['energy_justice_ratio'],
        'is_sleeping': energy_status['is_sleeping']
    }
    
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
        energy_metrics=energy_data
    )

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
