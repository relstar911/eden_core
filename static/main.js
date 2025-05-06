// EDEN.CORE - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Get form and response elements
    const form = document.getElementById('interaction-form');
    const userInput = document.getElementById('user-input');
    const responseContainer = document.getElementById('response-container');
    const systemResponse = document.getElementById('system-response');
    
    // Metrics elements
    const coherenceValue = document.getElementById('coherence-value');
    const coherenceBar = document.getElementById('coherence-bar');
    const resonanceValue = document.getElementById('resonance-value');
    const resonanceBar = document.getElementById('resonance-bar');
    const truthValue = document.getElementById('truth-value');
    const truthBar = document.getElementById('truth-bar');
    const actionValue = document.getElementById('action-value');
    const actionBar = document.getElementById('action-bar');
    
    // Handle form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const inputText = userInput.value.trim();
        if (!inputText) return;
        
        // Clear input and show loading state
        userInput.value = '';
        systemResponse.textContent = 'Processing...';
        
        try {
            // Send request to backend
            const response = await fetch('/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: inputText })
            });
            
            if (!response.ok) {
                // Handle error responses
                const errorData = await response.json();
                
                if (response.status === 403) {
                    systemResponse.textContent = 'EDEN.CORE has chosen voluntary silence.';
                    responseContainer.classList.add('error');
                } else {
                    systemResponse.textContent = `Error: ${errorData.detail || 'Unknown error'}`;
                    responseContainer.classList.add('error');
                }
                
                // Reset metrics
                updateMetrics(0, 0, 0, 0);
                return;
            }
            
            // Process successful response
            response.json()
            .then(data => {
                responseContainer.classList.remove('error');
                
                // Update response text
                let responseText = data.system_message;
                if (data.memory_response) {
                    responseText = `${data.memory_response}\n\n${data.system_message}`;
                }
                systemResponse.textContent = responseText;
                
                // Update metrics
                updateMetrics(
                    data.intent_analysis.coherence || 0,
                    data.intent_analysis.resonance_value || 0,
                    data.semantic_truth || 0,
                    data.intent_analysis.action_suitability || 0,
                    data.energy_metrics
                );
            })
            .catch(error => {
                console.error('Error:', error);
                systemResponse.textContent = 'An error occurred while communicating with the system.';
                responseContainer.classList.add('error');
            });
            
        } catch (error) {
            console.error('Error:', error);
            systemResponse.textContent = 'An error occurred while communicating with the system.';
            responseContainer.classList.add('error');
        }
    });
    
    // Function to update metrics display
    function updateMetrics(coherence, resonance, truth, action, energyMetrics) {
        // Update coherence
        coherenceValue.textContent = coherence.toFixed(2);
        coherenceBar.style.width = `${coherence * 100}%`;
        
        // Update resonance
        resonanceValue.textContent = resonance.toFixed(2);
        resonanceBar.style.width = `${resonance * 100}%`;
        
        // Update truth
        truthValue.textContent = truth.toFixed(2);
        truthBar.style.width = `${truth * 100}%`;
        
        // Update action suitability
        actionValue.textContent = action.toFixed(2);
        actionBar.style.width = `${action * 100}%`;
        
        // Update energy metrics if available
        if (energyMetrics) {
            // Get energy metric elements
            const energyJusticeValue = document.getElementById('energy-justice-value');
            const energyJusticeBar = document.getElementById('energy-justice-bar');
            const energyUsedValue = document.getElementById('energy-used-value');
            const energyStateValue = document.getElementById('energy-state-value');
            
            if (energyJusticeValue && energyJusticeBar) {
                // Cap the display at 100% for very high values
                const justiceRatio = Math.min(energyMetrics.energy_justice_ratio, 10);
                energyJusticeValue.textContent = energyMetrics.energy_justice_ratio.toFixed(2);
                energyJusticeBar.style.width = `${(justiceRatio / 10) * 100}%`;
            }
            
            if (energyUsedValue) {
                energyUsedValue.textContent = energyMetrics.energy_used.toFixed(4);
            }
            
            if (energyStateValue) {
                energyStateValue.textContent = energyMetrics.is_sleeping ? 'Sleep Mode' : 'Active';
                energyStateValue.className = energyMetrics.is_sleeping ? 'metric-value sleeping' : 'metric-value';
            }
        }
    }
    
    // Initial metrics reset
    updateMetrics(0, 0, 0, 0);
});
