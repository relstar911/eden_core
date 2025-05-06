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
                
                // Display calculation details if available
                if (data.calculation_details) {
                    displayCalculationDetails(data.calculation_details);
                }
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
            
            // Update adaptive energy metrics if available
            const energyProfileValue = document.getElementById('energy-profile-value');
            const processingDepthValue = document.getElementById('processing-depth-value');
            const batteryMetric = document.getElementById('battery-metric');
            const batteryLevelValue = document.getElementById('battery-level-value');
            const batteryLevelBar = document.getElementById('battery-level-bar');
            
            if (energyProfileValue && energyMetrics.current_profile) {
                // Capitalize first letter of profile name
                const profileName = energyMetrics.current_profile.charAt(0).toUpperCase() + 
                                   energyMetrics.current_profile.slice(1);
                energyProfileValue.textContent = profileName;
                
                // Add profile-specific class
                energyProfileValue.className = `metric-value profile-${energyMetrics.current_profile}`;
            }
            
            if (processingDepthValue && energyMetrics.max_processing_depth) {
                processingDepthValue.textContent = energyMetrics.max_processing_depth;
            }
            
            // Show battery information if available
            if (batteryMetric && batteryLevelValue && batteryLevelBar && 
                typeof energyMetrics.battery_level !== 'undefined') {
                
                batteryMetric.style.display = 'block';
                const batteryPercent = Math.round(energyMetrics.battery_level * 100);
                batteryLevelValue.textContent = `${batteryPercent}%${energyMetrics.power_plugged ? ' (Charging)' : ''}`;
                batteryLevelBar.style.width = `${batteryPercent}%`;
                
                // Color the battery bar based on level
                if (batteryPercent < 20) {
                    batteryLevelBar.style.backgroundColor = '#e74c3c'; // Red for low battery
                } else if (batteryPercent < 50) {
                    batteryLevelBar.style.backgroundColor = '#f39c12'; // Orange for medium
                } else {
                    batteryLevelBar.style.backgroundColor = '#2ecc71'; // Green for good
                }
            } else if (batteryMetric) {
                batteryMetric.style.display = 'none';
            }
        }
    }
    
    // Function to display calculation details with transparent formulas
    function displayCalculationDetails(details) {
        // Check if calculation details container exists, if not create it
        let detailsContainer = document.getElementById('calculation-details');
        if (!detailsContainer) {
            // Create container for calculation details
            detailsContainer = document.createElement('div');
            detailsContainer.id = 'calculation-details';
            detailsContainer.className = 'calculation-details';
            
            // Create toggle button
            const toggleButton = document.createElement('button');
            toggleButton.textContent = 'Transparente Formeln anzeigen';
            toggleButton.className = 'toggle-details-btn';
            toggleButton.onclick = function() {
                const content = document.getElementById('calculation-details-content');
                if (content.style.display === 'none') {
                    content.style.display = 'block';
                    this.textContent = 'Transparente Formeln verbergen';
                } else {
                    content.style.display = 'none';
                    this.textContent = 'Transparente Formeln anzeigen';
                }
            };
            
            // Create content container
            const contentContainer = document.createElement('div');
            contentContainer.id = 'calculation-details-content';
            contentContainer.style.display = 'none';
            
            // Add elements to DOM
            detailsContainer.appendChild(toggleButton);
            detailsContainer.appendChild(contentContainer);
            
            // Add to status panel
            document.querySelector('.status-panel').appendChild(detailsContainer);
        }
        
        // Get content container
        const contentContainer = document.getElementById('calculation-details-content');
        contentContainer.innerHTML = '';
        
        // Create sections for each module
        if (details.intent) {
            const intentSection = createDetailsSection('Intent-Modul', details.intent);
            contentContainer.appendChild(intentSection);
        }
        
        if (details.logic) {
            const logicSection = createDetailsSection('Logic-Modul', details.logic);
            contentContainer.appendChild(logicSection);
        }
        
        if (details.energy) {
            const energySection = createDetailsSection('Energy-Modul', details.energy);
            contentContainer.appendChild(energySection);
        }
    }
    
    // Helper function to create a details section
    function createDetailsSection(title, details) {
        const section = document.createElement('div');
        section.className = 'details-section';
        
        // Add title
        const sectionTitle = document.createElement('h3');
        sectionTitle.textContent = title;
        section.appendChild(sectionTitle);
        
        // Add details
        const detailsList = document.createElement('ul');
        
        // Process details recursively
        function addDetailsToList(obj, list, indent = 0) {
            for (const [key, value] of Object.entries(obj)) {
                const item = document.createElement('li');
                item.style.marginLeft = `${indent * 20}px`;
                
                if (typeof value === 'object' && value !== null) {
                    // It's an object or array, create a nested structure
                    item.innerHTML = `<strong>${formatKey(key)}:</strong>`;
                    list.appendChild(item);
                    
                    const nestedList = document.createElement('ul');
                    addDetailsToList(value, nestedList, indent + 1);
                    list.appendChild(nestedList);
                } else {
                    // It's a primitive value
                    let displayValue = value;
                    
                    // Format numbers
                    if (typeof value === 'number') {
                        displayValue = value.toFixed(2);
                    }
                    
                    // Highlight formulas
                    if (key === 'formula') {
                        item.innerHTML = `<strong>${formatKey(key)}:</strong> <code>${displayValue}</code>`;
                    } else {
                        item.innerHTML = `<strong>${formatKey(key)}:</strong> ${displayValue}`;
                    }
                    
                    list.appendChild(item);
                }
            }
        }
        
        // Format keys for better readability
        function formatKey(key) {
            return key.replace(/_/g, ' ')
                     .split(' ')
                     .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                     .join(' ');
        }
        
        addDetailsToList(details, detailsList);
        section.appendChild(detailsList);
        
        return section;
    }
    
    // Initial metrics reset
    updateMetrics(0, 0, 0, 0);
});
