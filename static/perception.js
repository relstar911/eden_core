// EDEN.CORE - Perception JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Get perception elements
    const enableCameraBtn = document.getElementById('enable-camera');
    const enableAudioBtn = document.getElementById('enable-audio');
    const enableSensorsBtn = document.getElementById('enable-sensors');
    
    const cameraPreviewContainer = document.getElementById('camera-preview-container');
    const cameraPreview = document.getElementById('camera-preview');
    const cameraCanvas = document.getElementById('camera-canvas');
    
    const activeModalitiesValue = document.getElementById('active-modalities-value');
    const visualBrightnessValue = document.getElementById('visual-brightness-value');
    const visualBrightnessBar = document.getElementById('visual-brightness-bar');
    const audioAmplitudeValue = document.getElementById('audio-amplitude-value');
    const audioAmplitudeBar = document.getElementById('audio-amplitude-bar');
    
    // Perception state
    const perceptionState = {
        cameraEnabled: false,
        audioEnabled: false,
        sensorsEnabled: false,
        videoStream: null,
        audioStream: null,
        captureInterval: null,
        audioContext: null,
        audioAnalyser: null,
        activeModalities: []
    };
    
    // Camera handling
    enableCameraBtn.addEventListener('click', async function() {
        if (perceptionState.cameraEnabled) {
            // Disable camera
            if (perceptionState.videoStream) {
                perceptionState.videoStream.getTracks().forEach(track => track.stop());
                perceptionState.videoStream = null;
            }
            
            if (perceptionState.captureInterval) {
                clearInterval(perceptionState.captureInterval);
                perceptionState.captureInterval = null;
            }
            
            cameraPreviewContainer.style.display = 'none';
            enableCameraBtn.textContent = 'Enable Camera';
            perceptionState.cameraEnabled = false;
            
            // Update active modalities
            const index = perceptionState.activeModalities.indexOf('visual');
            if (index !== -1) {
                perceptionState.activeModalities.splice(index, 1);
            }
            updateActiveModalities();
        } else {
            // Enable camera
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { 
                        width: { ideal: 320 },
                        height: { ideal: 240 }
                    } 
                });
                
                cameraPreview.srcObject = stream;
                perceptionState.videoStream = stream;
                cameraPreviewContainer.style.display = 'block';
                enableCameraBtn.textContent = 'Disable Camera';
                perceptionState.cameraEnabled = true;
                
                // Add to active modalities
                if (!perceptionState.activeModalities.includes('visual')) {
                    perceptionState.activeModalities.push('visual');
                }
                updateActiveModalities();
                
                // Start periodic frame capture
                perceptionState.captureInterval = setInterval(captureVideoFrame, 1000);
            } catch (error) {
                console.error('Error accessing camera:', error);
                alert('Could not access camera: ' + error.message);
            }
        }
    });
    
    // Audio handling
    enableAudioBtn.addEventListener('click', async function() {
        if (perceptionState.audioEnabled) {
            // Disable audio
            if (perceptionState.audioStream) {
                perceptionState.audioStream.getTracks().forEach(track => track.stop());
                perceptionState.audioStream = null;
            }
            
            if (perceptionState.audioContext) {
                perceptionState.audioContext.close();
                perceptionState.audioContext = null;
                perceptionState.audioAnalyser = null;
            }
            
            enableAudioBtn.textContent = 'Enable Audio';
            perceptionState.audioEnabled = false;
            
            // Update active modalities
            const index = perceptionState.activeModalities.indexOf('audio');
            if (index !== -1) {
                perceptionState.activeModalities.splice(index, 1);
            }
            updateActiveModalities();
        } else {
            // Enable audio
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                perceptionState.audioStream = stream;
                
                // Set up audio analysis
                const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const analyser = audioContext.createAnalyser();
                const microphone = audioContext.createMediaStreamSource(stream);
                microphone.connect(analyser);
                
                analyser.fftSize = 256;
                perceptionState.audioContext = audioContext;
                perceptionState.audioAnalyser = analyser;
                
                enableAudioBtn.textContent = 'Disable Audio';
                perceptionState.audioEnabled = true;
                
                // Add to active modalities
                if (!perceptionState.activeModalities.includes('audio')) {
                    perceptionState.activeModalities.push('audio');
                }
                updateActiveModalities();
                
                // Start audio analysis
                analyzeAudio();
            } catch (error) {
                console.error('Error accessing microphone:', error);
                alert('Could not access microphone: ' + error.message);
            }
        }
    });
    
    // Sensor handling
    enableSensorsBtn.addEventListener('click', function() {
        if (perceptionState.sensorsEnabled) {
            // Disable sensors
            enableSensorsBtn.textContent = 'Enable Sensors';
            perceptionState.sensorsEnabled = false;
            
            // Update active modalities
            const index = perceptionState.activeModalities.indexOf('sensor');
            if (index !== -1) {
                perceptionState.activeModalities.splice(index, 1);
            }
            updateActiveModalities();
        } else {
            // Enable sensors if available
            if ('DeviceOrientationEvent' in window || 'DeviceMotionEvent' in window) {
                enableSensorsBtn.textContent = 'Disable Sensors';
                perceptionState.sensorsEnabled = true;
                
                // Add to active modalities
                if (!perceptionState.activeModalities.includes('sensor')) {
                    perceptionState.activeModalities.push('sensor');
                }
                updateActiveModalities();
                
                // Request permission for device sensors on iOS 13+
                if (typeof DeviceOrientationEvent.requestPermission === 'function') {
                    DeviceOrientationEvent.requestPermission()
                        .then(response => {
                            if (response === 'granted') {
                                window.addEventListener('deviceorientation', handleOrientation);
                            }
                        })
                        .catch(console.error);
                } else {
                    // For non-iOS devices
                    window.addEventListener('deviceorientation', handleOrientation);
                }
                
                if (typeof DeviceMotionEvent.requestPermission === 'function') {
                    DeviceMotionEvent.requestPermission()
                        .then(response => {
                            if (response === 'granted') {
                                window.addEventListener('devicemotion', handleMotion);
                            }
                        })
                        .catch(console.error);
                } else {
                    // For non-iOS devices
                    window.addEventListener('devicemotion', handleMotion);
                }
            } else {
                alert('Device sensors are not available on this device or browser.');
            }
        }
    });
    
    // Function to capture video frame
    function captureVideoFrame() {
        if (!perceptionState.cameraEnabled || !perceptionState.videoStream) return;
        
        const context = cameraCanvas.getContext('2d');
        cameraCanvas.width = cameraPreview.videoWidth;
        cameraCanvas.height = cameraPreview.videoHeight;
        
        context.drawImage(cameraPreview, 0, 0, cameraCanvas.width, cameraCanvas.height);
        
        // Simple brightness analysis
        const imageData = context.getImageData(0, 0, cameraCanvas.width, cameraCanvas.height);
        const data = imageData.data;
        let brightness = 0;
        
        // Calculate average brightness
        for (let i = 0; i < data.length; i += 4) {
            brightness += (0.2126 * data[i] + 0.7152 * data[i + 1] + 0.0722 * data[i + 2]) / 255;
        }
        
        brightness = brightness / (data.length / 4);
        
        // Update UI
        visualBrightnessValue.textContent = brightness.toFixed(2);
        visualBrightnessBar.style.width = `${brightness * 100}%`;
        
        // Convert canvas to base64 for sending to server
        const imageBase64 = cameraCanvas.toDataURL('image/jpeg', 0.7);
        
        // Send to server if other modalities are also active
        if (perceptionState.activeModalities.length > 1) {
            sendMultimodalData({
                image_data: imageBase64
            });
        }
    }
    
    // Function to analyze audio
    function analyzeAudio() {
        if (!perceptionState.audioEnabled || !perceptionState.audioAnalyser) return;
        
        const bufferLength = perceptionState.audioAnalyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);
        
        function updateAudio() {
            if (!perceptionState.audioEnabled) return;
            
            perceptionState.audioAnalyser.getByteFrequencyData(dataArray);
            
            // Calculate average amplitude
            let sum = 0;
            for (let i = 0; i < bufferLength; i++) {
                sum += dataArray[i];
            }
            
            const amplitude = sum / bufferLength / 255;
            
            // Update UI
            audioAmplitudeValue.textContent = amplitude.toFixed(2);
            audioAmplitudeBar.style.width = `${amplitude * 100}%`;
            
            // Send to server if other modalities are also active
            if (perceptionState.activeModalities.length > 1) {
                // In a real implementation, we would convert audio data to a format
                // suitable for sending to the server
                sendMultimodalData({
                    audio_data: 'audio_placeholder'
                });
            }
            
            requestAnimationFrame(updateAudio);
        }
        
        updateAudio();
    }
    
    // Handle device orientation data
    function handleOrientation(event) {
        if (!perceptionState.sensorsEnabled) return;
        
        const sensorData = {
            alpha: event.alpha, // Z-axis rotation [0, 360)
            beta: event.beta,   // X-axis rotation [-180, 180]
            gamma: event.gamma  // Y-axis rotation [-90, 90]
        };
        
        // Send to server if other modalities are also active
        if (perceptionState.activeModalities.length > 1) {
            sendMultimodalData({
                sensor_data: {
                    orientation: sensorData
                }
            });
        }
    }
    
    // Handle device motion data
    function handleMotion(event) {
        if (!perceptionState.sensorsEnabled) return;
        
        const acceleration = event.accelerationIncludingGravity;
        if (!acceleration) return;
        
        const sensorData = {
            x: acceleration.x,
            y: acceleration.y,
            z: acceleration.z
        };
        
        // Send to server if other modalities are also active
        if (perceptionState.activeModalities.length > 1) {
            sendMultimodalData({
                sensor_data: {
                    motion: sensorData
                }
            });
        }
    }
    
    // Update active modalities display
    function updateActiveModalities() {
        if (perceptionState.activeModalities.length === 0) {
            activeModalitiesValue.textContent = 'None';
        } else {
            activeModalitiesValue.textContent = perceptionState.activeModalities.join(', ');
        }
    }
    
    // Send multimodal data to server
    function sendMultimodalData(data) {
        // Only send if we have at least text or one perception modality
        if (Object.keys(data).length === 0) return;
        
        // Get text from input field if available
        const userInput = document.getElementById('user-input');
        if (userInput && userInput.value.trim()) {
            data.text = userInput.value.trim();
        }
        
        // Don't send empty requests
        if (Object.keys(data).length === 0) return;
        
        // Send to server
        fetch('/process_multimodal', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Server responded with ${response.status}`);
            }
            return response.json();
        })
        .then(responseData => {
            console.log('Multimodal processing result:', responseData);
            
            // Update perception data display if available
            if (responseData.perception_data) {
                updatePerceptionDisplay(responseData.perception_data);
            }
        })
        .catch(error => {
            console.error('Error sending multimodal data:', error);
        });
    }
    
    // Update perception display with server response
    function updatePerceptionDisplay(perceptionData) {
        // Update based on available data
        if (perceptionData.visual && perceptionData.visual.brightness) {
            visualBrightnessValue.textContent = perceptionData.visual.brightness.toFixed(2);
            visualBrightnessBar.style.width = `${perceptionData.visual.brightness * 100}%`;
        }
        
        if (perceptionData.audio && perceptionData.audio.amplitude) {
            audioAmplitudeValue.textContent = perceptionData.audio.amplitude.toFixed(2);
            audioAmplitudeBar.style.width = `${perceptionData.audio.amplitude * 100}%`;
        }
    }
});
