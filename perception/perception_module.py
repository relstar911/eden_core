"""
EDEN.CORE - Perception Module
Implementiert multimodale Wahrnehmung für EDEN.CORE, einschließlich visueller, 
auditiver und sensorischer Eingaben.
"""

import os
import time
import base64
import logging
from typing import Dict, Any, List, Optional, Union, Tuple
from PIL import Image
import numpy as np

class VisualProcessor:
    """
    Verarbeitet visuelle Eingaben wie Bilder und Videoframes.
    Implementiert Bildverarbeitung unter Berücksichtigung des Prinzips
    "Bedeutung über Vorhersage".
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialisiert den visuellen Prozessor.
        
        Args:
            config: Konfigurationseinstellungen für den visuellen Prozessor
        """
        self.enabled = config.get('enabled', True)
        self.max_resolution = config.get('max_resolution', (1280, 720))
        self.meaning_threshold = config.get('meaning_threshold', 0.3)
        self.last_processed_image = None
        self.visual_context = {}
        
    def process(self, image_data: Union[str, bytes, np.ndarray, Image.Image]) -> Dict[str, Any]:
        """
        Verarbeitet ein Bild und extrahiert bedeutungsvolle Informationen.
        
        Args:
            image_data: Bilddaten als Base64-String, Bytes, NumPy-Array oder PIL-Image
            
        Returns:
            Dict[str, Any]: Extrahierte Informationen aus dem Bild
        """
        if not self.enabled:
            return {'enabled': False, 'message': 'Visual processing is disabled'}
        
        # Bild in ein einheitliches Format konvertieren
        try:
            image = self._normalize_image(image_data)
        except Exception as e:
            return {'error': f'Failed to process image: {str(e)}'}
        
        # Bild für spätere Verarbeitung speichern
        self.last_processed_image = image
        
        # Einfache Bildanalyse durchführen
        image_info = self._analyze_image(image)
        
        # Kontextinformationen aktualisieren
        self._update_context(image_info)
        
        return image_info
    
    def _normalize_image(self, image_data: Union[str, bytes, np.ndarray, Image.Image]) -> Image.Image:
        """
        Konvertiert verschiedene Bildeingabeformate in ein PIL-Image.
        
        Args:
            image_data: Bilddaten in verschiedenen Formaten
            
        Returns:
            Image.Image: Normalisiertes PIL-Image
        """
        if isinstance(image_data, str):
            # Base64-String
            if image_data.startswith('data:image'):
                # Daten-URL
                image_data = image_data.split(',')[1]
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
        elif isinstance(image_data, bytes):
            # Binäre Bilddaten
            image = Image.open(io.BytesIO(image_data))
        elif isinstance(image_data, np.ndarray):
            # NumPy-Array
            image = Image.fromarray(image_data)
        elif isinstance(image_data, Image.Image):
            # Bereits ein PIL-Image
            image = image_data
        else:
            raise ValueError(f"Unsupported image data type: {type(image_data)}")
        
        # Auflösung begrenzen, falls erforderlich
        if (image.width > self.max_resolution[0] or image.height > self.max_resolution[1]):
            image.thumbnail(self.max_resolution, Image.LANCZOS)
            
        return image
    
    def _analyze_image(self, image: Image.Image) -> Dict[str, Any]:
        """
        Führt eine einfache Analyse des Bildes durch.
        
        Args:
            image: PIL-Image zur Analyse
            
        Returns:
            Dict[str, Any]: Analyseergebnisse
        """
        # Grundlegende Bildmerkmale extrahieren
        width, height = image.size
        aspect_ratio = width / height
        
        # Durchschnittliche Helligkeit berechnen
        try:
            gray_image = image.convert('L')
            brightness = np.array(gray_image).mean() / 255.0
        except Exception:
            brightness = 0.5
            
        # Durchschnittliche Farbwerte berechnen
        try:
            rgb_image = image.convert('RGB')
            rgb_array = np.array(rgb_image)
            avg_color = rgb_array.mean(axis=(0, 1)) / 255.0
        except Exception:
            avg_color = [0.5, 0.5, 0.5]
        
        # Einfache Kantenerkennung als Komplexitätsmaß
        try:
            from scipy import ndimage
            gray_array = np.array(gray_image)
            edges_x = ndimage.sobel(gray_array, axis=0)
            edges_y = ndimage.sobel(gray_array, axis=1)
            edge_magnitude = np.hypot(edges_x, edges_y)
            complexity = np.mean(edge_magnitude) / 255.0
        except Exception:
            complexity = 0.5
            
        return {
            'dimensions': (width, height),
            'aspect_ratio': aspect_ratio,
            'brightness': brightness,
            'avg_color': avg_color.tolist() if isinstance(avg_color, np.ndarray) else avg_color,
            'complexity': complexity,
            'timestamp': time.time()
        }
    
    def _update_context(self, image_info: Dict[str, Any]) -> None:
        """
        Aktualisiert den visuellen Kontext mit neuen Bildinformationen.
        
        Args:
            image_info: Analyseergebnisse des aktuellen Bildes
        """
        self.visual_context = {
            'last_image_info': image_info,
            'last_processed_time': time.time()
        }
    
    def get_context(self) -> Dict[str, Any]:
        """
        Gibt den aktuellen visuellen Kontext zurück.
        
        Returns:
            Dict[str, Any]: Aktueller visueller Kontext
        """
        return self.visual_context


class AudioProcessor:
    """
    Verarbeitet Audioeingaben wie Sprache und Umgebungsgeräusche.
    Implementiert Audioverarbeitung unter Berücksichtigung des Prinzips
    "Bedeutung über Vorhersage".
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialisiert den Audio-Prozessor.
        
        Args:
            config: Konfigurationseinstellungen für den Audio-Prozessor
        """
        self.enabled = config.get('enabled', True)
        self.sample_rate = config.get('sample_rate', 16000)
        self.meaning_threshold = config.get('meaning_threshold', 0.3)
        self.last_processed_audio = None
        self.audio_context = {}
        
    def process(self, audio_data: Union[str, bytes, np.ndarray]) -> Dict[str, Any]:
        """
        Verarbeitet Audiodaten und extrahiert bedeutungsvolle Informationen.
        
        Args:
            audio_data: Audiodaten als Base64-String, Bytes oder NumPy-Array
            
        Returns:
            Dict[str, Any]: Extrahierte Informationen aus dem Audio
        """
        if not self.enabled:
            return {'enabled': False, 'message': 'Audio processing is disabled'}
        
        # Audio in ein einheitliches Format konvertieren
        try:
            audio = self._normalize_audio(audio_data)
        except Exception as e:
            return {'error': f'Failed to process audio: {str(e)}'}
        
        # Audio für spätere Verarbeitung speichern
        self.last_processed_audio = audio
        
        # Einfache Audioanalyse durchführen
        audio_info = self._analyze_audio(audio)
        
        # Kontextinformationen aktualisieren
        self._update_context(audio_info)
        
        return audio_info
    
    def _normalize_audio(self, audio_data: Union[str, bytes, np.ndarray]) -> np.ndarray:
        """
        Konvertiert verschiedene Audioeingabeformate in ein NumPy-Array.
        
        Args:
            audio_data: Audiodaten in verschiedenen Formaten
            
        Returns:
            np.ndarray: Normalisiertes Audio als NumPy-Array
        """
        if isinstance(audio_data, str):
            # Base64-String
            if audio_data.startswith('data:audio'):
                # Daten-URL
                audio_data = audio_data.split(',')[1]
            audio_bytes = base64.b64decode(audio_data)
            # Einfache Konvertierung zu NumPy-Array (in realer Implementierung würde hier
            # eine Audiobibliothek wie librosa verwendet werden)
            audio = np.frombuffer(audio_bytes, dtype=np.int16)
        elif isinstance(audio_data, bytes):
            # Binäre Audiodaten
            audio = np.frombuffer(audio_data, dtype=np.int16)
        elif isinstance(audio_data, np.ndarray):
            # Bereits ein NumPy-Array
            audio = audio_data
        else:
            raise ValueError(f"Unsupported audio data type: {type(audio_data)}")
            
        return audio
    
    def _analyze_audio(self, audio: np.ndarray) -> Dict[str, Any]:
        """
        Führt eine einfache Analyse der Audiodaten durch.
        
        Args:
            audio: NumPy-Array mit Audiodaten
            
        Returns:
            Dict[str, Any]: Analyseergebnisse
        """
        # Grundlegende Audiomerkmale extrahieren
        duration = len(audio) / self.sample_rate
        
        # Durchschnittliche Amplitude berechnen
        try:
            amplitude = np.abs(audio).mean() / 32768.0  # Normalisieren auf [0, 1]
        except Exception:
            amplitude = 0.5
            
        # Einfache Frequenzanalyse
        try:
            from scipy.fftpack import fft
            # Nur einen Teil des Audios für die FFT verwenden
            n = min(len(audio), 1024)
            audio_segment = audio[:n]
            spectrum = np.abs(fft(audio_segment))
            frequency = np.argmax(spectrum[:n//2]) * self.sample_rate / n
        except Exception:
            frequency = 0
            
        return {
            'duration': duration,
            'amplitude': amplitude,
            'dominant_frequency': frequency,
            'timestamp': time.time()
        }
    
    def _update_context(self, audio_info: Dict[str, Any]) -> None:
        """
        Aktualisiert den Audio-Kontext mit neuen Audioinformationen.
        
        Args:
            audio_info: Analyseergebnisse der aktuellen Audiodaten
        """
        self.audio_context = {
            'last_audio_info': audio_info,
            'last_processed_time': time.time()
        }
    
    def get_context(self) -> Dict[str, Any]:
        """
        Gibt den aktuellen Audio-Kontext zurück.
        
        Returns:
            Dict[str, Any]: Aktueller Audio-Kontext
        """
        return self.audio_context


class SensorProcessor:
    """
    Verarbeitet Sensordaten wie Temperatur, Licht, Bewegung, etc.
    Implementiert Sensorverarbeitung unter Berücksichtigung des Prinzips
    "Bedeutung über Vorhersage".
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialisiert den Sensor-Prozessor.
        
        Args:
            config: Konfigurationseinstellungen für den Sensor-Prozessor
        """
        self.enabled = config.get('enabled', True)
        self.sensors = config.get('sensors', {})
        self.meaning_threshold = config.get('meaning_threshold', 0.3)
        self.sensor_context = {}
        self.sensor_history = {}
        
    def process(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verarbeitet Sensordaten und extrahiert bedeutungsvolle Informationen.
        
        Args:
            sensor_data: Sensordaten als Dictionary mit Sensorname als Schlüssel
            
        Returns:
            Dict[str, Any]: Verarbeitete Sensorinformationen
        """
        if not self.enabled:
            return {'enabled': False, 'message': 'Sensor processing is disabled'}
        
        # Sensordaten validieren
        validated_data = self._validate_sensor_data(sensor_data)
        
        # Sensordaten analysieren
        sensor_info = self._analyze_sensor_data(validated_data)
        
        # Kontextinformationen aktualisieren
        self._update_context(sensor_info)
        
        # Sensorhistorie aktualisieren
        self._update_history(validated_data)
        
        return sensor_info
    
    def _validate_sensor_data(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validiert die eingehenden Sensordaten.
        
        Args:
            sensor_data: Rohe Sensordaten
            
        Returns:
            Dict[str, Any]: Validierte Sensordaten
        """
        validated_data = {}
        
        for sensor_name, value in sensor_data.items():
            if sensor_name in self.sensors:
                sensor_config = self.sensors[sensor_name]
                
                # Bereichsprüfung
                min_value = sensor_config.get('min_value', float('-inf'))
                max_value = sensor_config.get('max_value', float('inf'))
                
                if isinstance(value, (int, float)) and min_value <= value <= max_value:
                    validated_data[sensor_name] = value
                else:
                    logging.warning(f"Sensor value out of range: {sensor_name}={value}")
            else:
                # Unbekannter Sensor, aber trotzdem akzeptieren
                validated_data[sensor_name] = value
                
        return validated_data
    
    def _analyze_sensor_data(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analysiert die Sensordaten und erkennt Muster oder signifikante Änderungen.
        
        Args:
            sensor_data: Validierte Sensordaten
            
        Returns:
            Dict[str, Any]: Analyseergebnisse
        """
        analysis_results = {
            'timestamp': time.time(),
            'sensors': {},
            'changes': {},
            'patterns': []
        }
        
        # Sensordaten in die Ergebnisse kopieren
        analysis_results['sensors'] = sensor_data.copy()
        
        # Änderungen gegenüber vorherigen Werten erkennen
        for sensor_name, value in sensor_data.items():
            if sensor_name in self.sensor_history:
                history = self.sensor_history[sensor_name]
                if history and isinstance(value, (int, float)):
                    last_value = history[-1]['value']
                    change = value - last_value
                    percent_change = change / last_value if last_value != 0 else float('inf')
                    
                    # Signifikante Änderungen markieren
                    if abs(percent_change) > 0.1:  # 10% Änderung
                        analysis_results['changes'][sensor_name] = {
                            'absolute': change,
                            'percent': percent_change * 100
                        }
        
        # Einfache Mustererkennung
        # Beispiel: Temperatur steigt und Luftfeuchtigkeit sinkt
        if ('temperature' in sensor_data and 'humidity' in sensor_data and
            'temperature' in self.sensor_history and 'humidity' in self.sensor_history):
            
            temp_history = self.sensor_history['temperature']
            humidity_history = self.sensor_history['humidity']
            
            if (len(temp_history) > 1 and len(humidity_history) > 1):
                temp_change = sensor_data['temperature'] - temp_history[-2]['value']
                humidity_change = sensor_data['humidity'] - humidity_history[-2]['value']
                
                if temp_change > 0 and humidity_change < 0:
                    analysis_results['patterns'].append({
                        'name': 'warming_drying',
                        'description': 'Temperature rising while humidity falling'
                    })
        
        return analysis_results
    
    def _update_context(self, sensor_info: Dict[str, Any]) -> None:
        """
        Aktualisiert den Sensor-Kontext mit neuen Sensorinformationen.
        
        Args:
            sensor_info: Analyseergebnisse der aktuellen Sensordaten
        """
        self.sensor_context = {
            'last_sensor_info': sensor_info,
            'last_processed_time': time.time()
        }
    
    def _update_history(self, sensor_data: Dict[str, Any]) -> None:
        """
        Aktualisiert die Sensorhistorie mit neuen Sensordaten.
        
        Args:
            sensor_data: Aktuelle Sensordaten
        """
        current_time = time.time()
        
        for sensor_name, value in sensor_data.items():
            if sensor_name not in self.sensor_history:
                self.sensor_history[sensor_name] = []
                
            # Neuen Datenpunkt hinzufügen
            self.sensor_history[sensor_name].append({
                'timestamp': current_time,
                'value': value
            })
            
            # Historie auf maximal 100 Einträge begrenzen
            if len(self.sensor_history[sensor_name]) > 100:
                self.sensor_history[sensor_name] = self.sensor_history[sensor_name][-100:]
    
    def get_context(self) -> Dict[str, Any]:
        """
        Gibt den aktuellen Sensor-Kontext zurück.
        
        Returns:
            Dict[str, Any]: Aktueller Sensor-Kontext
        """
        return self.sensor_context
    
    def get_history(self, sensor_name: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Gibt die Sensorhistorie zurück.
        
        Args:
            sensor_name: Optional, Name des Sensors für den die Historie zurückgegeben werden soll
            
        Returns:
            Dict[str, List[Dict[str, Any]]]: Sensorhistorie
        """
        if sensor_name:
            return {sensor_name: self.sensor_history.get(sensor_name, [])}
        return self.sensor_history


class EdenPerception:
    """
    Hauptklasse für multimodale Wahrnehmung in EDEN.CORE.
    Integriert visuelle, auditive und sensorische Verarbeitung.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialisiert das Perception-Modul.
        
        Args:
            config: Konfigurationseinstellungen für das Modul
        """
        self.enabled = config.get('enabled', True)
        
        # Submodule initialisieren
        self.visual_enabled = config.get('visual_enabled', False)
        self.audio_enabled = config.get('audio_enabled', False)
        self.sensor_enabled = config.get('sensor_enabled', False)
        
        if self.visual_enabled:
            self.visual_processor = VisualProcessor(config.get('visual_config', {}))
        else:
            self.visual_processor = None
            
        if self.audio_enabled:
            self.audio_processor = AudioProcessor(config.get('audio_config', {}))
        else:
            self.audio_processor = None
            
        if self.sensor_enabled:
            self.sensor_processor = SensorProcessor(config.get('sensor_config', {}))
        else:
            self.sensor_processor = None
            
        # Integrierter Kontext
        self.integrated_context = {}
        self.last_update_time = time.time()
    
    def process_visual(self, image_data: Union[str, bytes, np.ndarray, Image.Image]) -> Dict[str, Any]:
        """
        Verarbeitet visuelle Eingaben.
        
        Args:
            image_data: Bilddaten in verschiedenen Formaten
            
        Returns:
            Dict[str, Any]: Verarbeitungsergebnisse
        """
        if not self.enabled or not self.visual_enabled or not self.visual_processor:
            return {'enabled': False, 'message': 'Visual processing is disabled'}
            
        return self.visual_processor.process(image_data)
    
    def process_audio(self, audio_data: Union[str, bytes, np.ndarray]) -> Dict[str, Any]:
        """
        Verarbeitet Audioeingaben.
        
        Args:
            audio_data: Audiodaten in verschiedenen Formaten
            
        Returns:
            Dict[str, Any]: Verarbeitungsergebnisse
        """
        if not self.enabled or not self.audio_enabled or not self.audio_processor:
            return {'enabled': False, 'message': 'Audio processing is disabled'}
            
        return self.audio_processor.process(audio_data)
    
    def process_sensor(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verarbeitet Sensoreingaben.
        
        Args:
            sensor_data: Sensordaten als Dictionary
            
        Returns:
            Dict[str, Any]: Verarbeitungsergebnisse
        """
        if not self.enabled or not self.sensor_enabled or not self.sensor_processor:
            return {'enabled': False, 'message': 'Sensor processing is disabled'}
            
        return self.sensor_processor.process(sensor_data)
    
    def process_multimodal(self, 
                          visual_data: Optional[Union[str, bytes, np.ndarray, Image.Image]] = None,
                          audio_data: Optional[Union[str, bytes, np.ndarray]] = None,
                          sensor_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Verarbeitet multimodale Eingaben und integriert die Ergebnisse.
        
        Args:
            visual_data: Optional, Bilddaten
            audio_data: Optional, Audiodaten
            sensor_data: Optional, Sensordaten
            
        Returns:
            Dict[str, Any]: Integrierte Verarbeitungsergebnisse
        """
        results = {
            'timestamp': time.time(),
            'modalities': []
        }
        
        # Visuelle Verarbeitung
        if visual_data is not None and self.visual_enabled and self.visual_processor:
            visual_results = self.visual_processor.process(visual_data)
            results['visual'] = visual_results
            results['modalities'].append('visual')
            
        # Audio-Verarbeitung
        if audio_data is not None and self.audio_enabled and self.audio_processor:
            audio_results = self.audio_processor.process(audio_data)
            results['audio'] = audio_results
            results['modalities'].append('audio')
            
        # Sensor-Verarbeitung
        if sensor_data is not None and self.sensor_enabled and self.sensor_processor:
            sensor_results = self.sensor_processor.process(sensor_data)
            results['sensor'] = sensor_results
            results['modalities'].append('sensor')
            
        # Multimodale Integration
        if len(results['modalities']) > 1:
            results['integrated'] = self._integrate_modalities(results)
            
        # Kontext aktualisieren
        self._update_integrated_context(results)
            
        return results
    
    def _integrate_modalities(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Integriert die Ergebnisse verschiedener Modalitäten.
        
        Args:
            results: Verarbeitungsergebnisse der einzelnen Modalitäten
            
        Returns:
            Dict[str, Any]: Integrierte Ergebnisse
        """
        integrated = {
            'timestamp': time.time(),
            'correlation': {}
        }
        
        # Beispiel für Korrelationsanalyse zwischen visuellen und Audiodaten
        if 'visual' in results and 'audio' in results:
            visual_info = results['visual']
            audio_info = results['audio']
            
            # Einfache Korrelation: Helligkeit und Lautstärke
            if ('brightness' in visual_info and 
                'amplitude' in audio_info):
                
                brightness = visual_info['brightness']
                amplitude = audio_info['amplitude']
                
                # Korrelation berechnen (einfache Differenz)
                correlation = 1.0 - abs(brightness - amplitude)
                
                integrated['correlation']['brightness_amplitude'] = {
                    'value': correlation,
                    'description': 'Correlation between visual brightness and audio amplitude'
                }
        
        # Beispiel für Korrelationsanalyse zwischen visuellen und Sensordaten
        if 'visual' in results and 'sensor' in results:
            visual_info = results['visual']
            sensor_info = results['sensor'].get('sensors', {})
            
            # Korrelation zwischen Helligkeit und Lichtsensor
            if ('brightness' in visual_info and 
                'light' in sensor_info):
                
                brightness = visual_info['brightness']
                light_level = sensor_info['light']
                
                # Normalisieren des Lichtsensors auf [0, 1]
                if isinstance(light_level, (int, float)):
                    normalized_light = min(1.0, max(0.0, light_level / 100.0))
                    
                    # Korrelation berechnen
                    correlation = 1.0 - abs(brightness - normalized_light)
                    
                    integrated['correlation']['brightness_light'] = {
                        'value': correlation,
                        'description': 'Correlation between visual brightness and light sensor'
                    }
        
        return integrated
    
    def _update_integrated_context(self, results: Dict[str, Any]) -> None:
        """
        Aktualisiert den integrierten Kontext mit neuen Verarbeitungsergebnissen.
        
        Args:
            results: Aktuelle Verarbeitungsergebnisse
        """
        self.integrated_context = {
            'last_results': results,
            'last_update_time': time.time(),
            'active_modalities': results.get('modalities', [])
        }
    
    def get_multimodal_context(self) -> Dict[str, Any]:
        """
        Gibt den aktuellen multimodalen Kontext zurück.
        
        Returns:
            Dict[str, Any]: Aktueller multimodaler Kontext
        """
        context = {
            'timestamp': time.time(),
            'integrated': self.integrated_context
        }
        
        # Kontexte der einzelnen Modalitäten hinzufügen
        if self.visual_enabled and self.visual_processor:
            context['visual'] = self.visual_processor.get_context()
            
        if self.audio_enabled and self.audio_processor:
            context['audio'] = self.audio_processor.get_context()
            
        if self.sensor_enabled and self.sensor_processor:
            context['sensor'] = self.sensor_processor.get_context()
            
        return context
