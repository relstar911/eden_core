"""
EDEN.CORE - Adaptive Energy Module
Erweitert das Energy-Modul um adaptive Energieverbrauchssteuerung
"""

import os
import time
import psutil
import platform
from typing import Dict, Any, Optional
from .energy_module import EdenEnergy

class EdenAdaptiveEnergy(EdenEnergy):
    """
    Erweitertes Energy-Modul mit adaptiver Energieverbrauchssteuerung.
    Implementiert das Prinzip "Energy Justice Over Performance" mit dynamischer Anpassung
    an verfügbare Energiequellen und Systemzustände.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialisiert das adaptive Energy-Modul.
        
        Args:
            config: Konfigurationseinstellungen für das Modul
        """
        super().__init__(config)
        
        # Adaptive Konfiguration laden
        adaptive_config = config.get('adaptive', {})
        self.adaptive_enabled = adaptive_config.get('enabled', True)
        self.energy_profiles = adaptive_config.get('energy_profiles', {
            'eco': {'max_processing_depth': 2, 'max_memory_usage': 0.3},
            'balanced': {'max_processing_depth': 5, 'max_memory_usage': 0.6},
            'performance': {'max_processing_depth': 10, 'max_memory_usage': 0.9}
        })
        self.default_profile = adaptive_config.get('default_profile', 'balanced')
        self.current_profile = self.default_profile
        self.adaptive_mode = adaptive_config.get('adaptive_mode', True)
        
        # Systemspezifische Informationen
        self.platform = platform.system()
        self.battery_powered = self._is_battery_powered()
        
        # Profilwechsel-Historie
        self.profile_changes = []
        
    def _is_battery_powered(self) -> bool:
        """
        Erkennt, ob das System mit Batterie betrieben wird.
        
        Returns:
            bool: True, wenn das System mit Batterie betrieben wird, sonst False
        """
        if self.platform == 'Windows':
            try:
                battery = psutil.sensors_battery()
                return battery is not None and battery.power_plugged is False
            except (AttributeError, NotImplementedError):
                return False
        elif self.platform == 'Linux':
            # Überprüfung auf Linux-Systemen
            battery_path = '/sys/class/power_supply/BAT0'
            return os.path.exists(battery_path)
        elif self.platform == 'Darwin':  # macOS
            try:
                battery = psutil.sensors_battery()
                return battery is not None
            except (AttributeError, NotImplementedError):
                return False
        return False
    
    def detect_energy_source(self) -> Dict[str, Any]:
        """
        Erkennt die verfügbare Energiequelle und deren Zustand.
        
        Returns:
            Dict[str, Any]: Informationen über die Energiequelle
        """
        energy_info = {
            'battery_powered': False,
            'battery_level': 1.0,
            'power_plugged': True
        }
        
        try:
            battery = psutil.sensors_battery()
            if battery:
                energy_info['battery_powered'] = True
                energy_info['battery_level'] = battery.percent / 100.0
                energy_info['power_plugged'] = battery.power_plugged
        except (AttributeError, NotImplementedError):
            # Fallback, wenn keine Batterieinformationen verfügbar sind
            pass
            
        return energy_info
    
    def select_energy_profile(self) -> str:
        """
        Wählt das geeignete Energieprofil basierend auf dem Systemzustand aus.
        
        Returns:
            str: Name des ausgewählten Energieprofils
        """
        if not self.adaptive_mode or not self.adaptive_enabled:
            return self.current_profile
        
        energy_source = self.detect_energy_source()
        
        # Profilauswahl basierend auf Energiequelle
        if energy_source['battery_powered'] and not energy_source['power_plugged']:
            # Batteriebetrieb
            if energy_source['battery_level'] < 0.2:
                selected_profile = 'eco'
            elif energy_source['battery_level'] < 0.5:
                selected_profile = 'balanced'
            else:
                selected_profile = 'performance'
        else:
            # Netzbetrieb
            selected_profile = 'performance'
        
        # Profilwechsel protokollieren, wenn sich das Profil ändert
        if selected_profile != self.current_profile:
            self.profile_changes.append({
                'timestamp': time.time(),
                'old_profile': self.current_profile,
                'new_profile': selected_profile,
                'reason': f"Battery: {energy_source['battery_level']:.2f}, Plugged: {energy_source['power_plugged']}"
            })
            self.current_profile = selected_profile
            
        return selected_profile
    
    def get_processing_depth(self, input_complexity: float) -> int:
        """
        Ermittelt die maximale Verarbeitungstiefe basierend auf dem aktuellen Energieprofil.
        
        Args:
            input_complexity: Komplexität der Eingabe (0.0 bis 10.0)
            
        Returns:
            int: Maximale Verarbeitungstiefe
        """
        profile_name = self.select_energy_profile()
        profile = self.energy_profiles[profile_name]
        max_depth = profile.get('max_processing_depth', 5)
        
        # Verarbeitungstiefe basierend auf Eingabekomplexität und Profilgrenze
        return min(int(input_complexity), max_depth)
    
    def get_memory_limit(self) -> float:
        """
        Ermittelt das Speicherlimit basierend auf dem aktuellen Energieprofil.
        
        Returns:
            float: Maximaler Speicherverbrauch als Anteil (0.0 bis 1.0)
        """
        profile_name = self.select_energy_profile()
        profile = self.energy_profiles[profile_name]
        return profile.get('max_memory_usage', 0.6)
    
    def track_energy_use(self, truth_value: float, processing_time: float) -> Dict[str, float]:
        """
        Erweiterte Version der Energieverbrauchsverfolgung.
        
        Args:
            truth_value: Semantischer Wahrheitswert (0.0 bis 1.0)
            processing_time: Verarbeitungszeit in Sekunden
            
        Returns:
            Dict[str, Any]: Energiemetriken
        """
        # Basisimplementierung aufrufen
        energy_metrics = super().track_energy_use(truth_value, processing_time)
        
        # Zusätzliche adaptive Metriken
        profile_name = self.current_profile
        profile = self.energy_profiles[profile_name]
        
        energy_metrics['current_profile'] = profile_name
        energy_metrics['max_processing_depth'] = profile.get('max_processing_depth', 5)
        energy_metrics['max_memory_usage'] = profile.get('max_memory_usage', 0.6)
        
        # Energiequelleninformationen
        energy_source = self.detect_energy_source()
        if energy_source['battery_powered']:
            energy_metrics['battery_level'] = energy_source['battery_level']
            energy_metrics['power_plugged'] = energy_source['power_plugged']
        
        return energy_metrics
    
    def get_energy_status(self) -> Dict[str, Any]:
        """
        Erweiterte Version des Energiestatus.
        
        Returns:
            Dict[str, Any]: Erweiterter Energiestatus
        """
        # Basisimplementierung aufrufen
        status = super().get_energy_status()
        
        # Adaptive Informationen hinzufügen
        status['adaptive_enabled'] = self.adaptive_enabled
        status['current_profile'] = self.current_profile
        status['profile_description'] = self.energy_profiles[self.current_profile].get('description', '')
        
        # Energiequelleninformationen
        energy_source = self.detect_energy_source()
        if energy_source['battery_powered']:
            status['battery_level'] = energy_source['battery_level']
            status['power_plugged'] = energy_source['power_plugged']
        
        return status
    
    def limit_readiness(self, input_complexity: float) -> Dict[str, Any]:
        """
        Kontinuierliche Bereitschaft zur Verarbeitungsbegrenzung (0.0 = keine Begrenzung, 1.0 = maximale Begrenzung)
        Basierend auf dem Verhältnis von input_complexity zu max_processing_depth.
        """
        profile_name = self.select_energy_profile()
        profile = self.energy_profiles[profile_name]
        max_depth = profile.get('max_processing_depth', 5)
        # Skalenwert: je mehr input_complexity das Limit übersteigt, desto höher die readiness
        if input_complexity <= max_depth:
            readiness = 0.0
        else:
            # Linearer Anstieg, maximal 1.0
            readiness = min(1.0, (input_complexity - max_depth) / max(1.0, max_depth))
        limit_info = {
            'limit_readiness': readiness,
            'max_depth': max_depth,
            'input_complexity': input_complexity,
            'current_profile': profile_name
        }
        if readiness > 0.0:
            limit_info['reason'] = f"Input complexity ({input_complexity:.1f}) exceeds profile limit ({max_depth})"
            limit_info['recommended_depth'] = max_depth
        return limit_info

