"""
EDEN.CORE - Enhanced Adaptive Energy Module
Implements energy justice with transparent, training-independent logic rules
"""

import os
import time
import psutil
import datetime
import json
import math
from typing import Dict, Any, List, Tuple, Optional

class EdenAdaptiveEnergy:
    """
    Enhanced adaptive energy module for EDEN.CORE.
    Dynamically adjusts energy usage based on available resources with transparent formulas.
    Implements the principle of "Energy Justice Over Performance" with training-independent parameters.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the adaptive energy module.
        
        Args:
            config: Configuration settings for the module
        """
        self.enabled = config.get('enabled', True)
        self.config = config
        
        # Energy profiles with transparent parameters
        self.energy_profiles = {
            'eco': {
                'processing_depth': 0.3,  # Reduced processing depth
                'max_tokens': 100,        # Limited token generation
                'sleep_threshold': 0.7,   # Sleep more readily
                'description': 'Minimaler Energieverbrauch, reduzierte Verarbeitungstiefe'
            },
            'balanced': {
                'processing_depth': 0.6,  # Moderate processing depth
                'max_tokens': 250,        # Moderate token generation
                'sleep_threshold': 0.5,   # Balanced sleep behavior
                'description': 'Ausgewogenes Verhältnis zwischen Leistung und Energieverbrauch'
            },
            'performance': {
                'processing_depth': 0.9,  # High processing depth
                'max_tokens': 500,        # Extended token generation
                'sleep_threshold': 0.3,   # Sleep less readily
                'description': 'Maximale Leistung mit höherem Energieverbrauch'
            }
        }
        
        # Initialize with balanced profile by default
        self.current_profile = 'balanced'
        self.total_energy_used = 0.0
        self.energy_justice_ratio = 1.0
        self.last_energy_check = time.time()
        self.energy_log = []
        
        # Energy source detection
        self.on_battery = self._is_on_battery()
        self.last_source_check = time.time()
        self.source_check_interval = config.get('source_check_interval', 60)  # seconds
        
        # Load energy justice parameters with transparent values
        self.base_delta = config.get('energy_justice_delta', 5.0)
        self.time_factors = {
            'night': config.get('night_time_factor', 1.2),  # Higher justice requirement at night
            'peak': config.get('peak_time_factor', 0.8),    # Lower justice requirement during peak hours
            'normal': config.get('normal_time_factor', 1.0) # Normal justice requirement
        }
        self.load_factor = config.get('load_factor', 0.5)   # How much system load affects delta
        
        # Initialize energy justice delta
        self.last_delta_update = time.time()
        self.delta_update_interval = config.get('delta_update_interval', 300)  # 5 minutes
        self.energy_justice_delta = self._calculate_energy_justice_delta()
        
    def select_energy_profile(self) -> Dict[str, Any]:
        """
        Select the appropriate energy profile based on current system state.
        Uses transparent, rule-based logic instead of ML-based decisions.
        
        Returns:
            Dict containing the selected energy profile
        """
        # Check if we need to update energy source detection
        current_time = time.time()
        if current_time - self.last_source_check > self.source_check_interval:
            self.on_battery = self._is_on_battery()
            self.last_source_check = current_time
            
        # Get current system metrics
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        
        # Rule-based profile selection with transparent thresholds
        if self.on_battery:
            # On battery, prioritize energy conservation
            if cpu_percent > 70 or memory_percent > 80:
                # System under high load while on battery - use eco mode
                self.current_profile = 'eco'
            else:
                # Normal load on battery - use balanced mode
                self.current_profile = 'balanced'
        else:
            # On AC power
            if cpu_percent < 30 and memory_percent < 50:
                # System has plenty of resources - can use performance mode
                self.current_profile = 'performance'
            elif cpu_percent > 80 or memory_percent > 90:
                # System under very high load - use eco mode to avoid overload
                self.current_profile = 'eco'
            else:
                # Normal load on AC power - use balanced mode
                self.current_profile = 'balanced'
                
        # Get the selected profile
        profile = self.energy_profiles[self.current_profile]
        
        # Add current system metrics to the profile for transparency
        profile_with_metrics = profile.copy()
        profile_with_metrics.update({
            'name': self.current_profile,
            'system_metrics': {
                'on_battery': self.on_battery,
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'selection_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        })
        
        return profile_with_metrics
        
    def _is_on_battery(self) -> bool:
        """
        Detect if the system is running on battery power.
        Uses platform-specific methods with fallbacks.
        
        Returns:
            True if on battery, False if on AC power or unknown
        """
        try:
            # Try to use psutil for battery detection
            battery = psutil.sensors_battery()
            if battery:
                return not battery.power_plugged
        except (AttributeError, NotImplementedError):
            pass
            
        # Fallback method for Windows
        try:
            import ctypes
            status = ctypes.c_int()
            ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(status))
            # AC power status is the lowest bit in status.value
            return status.value & 1 == 0
        except:
            pass
            
        # Fallback to checking if battery exists
        try:
            return os.path.exists('/sys/class/power_supply/BAT0') or \
                   os.path.exists('/sys/class/power_supply/BAT1')
        except:
            pass
            
        # Default to False (assume AC power) if detection fails
        return False
        
    def _calculate_energy_justice_delta(self) -> float:
        """
        Calculate the energy justice factor δ with transparent, rule-based logic.
        Completely independent of ML training or LLM bias.
        
        Returns:
            The calculated delta value
        """
        # Check if we need to update delta
        current_time = time.time()
        if hasattr(self, 'energy_justice_delta') and current_time - self.last_delta_update < self.delta_update_interval:
            # Return cached value if recently updated
            return self.energy_justice_delta
            
        # Get base delta from configuration
        delta = self.base_delta
        
        # Factor 1: Time of day adjustment
        current_hour = datetime.datetime.now().hour
        time_factor = self.time_factors['normal']
        
        if 22 <= current_hour or current_hour < 6:
            # Night hours (10 PM - 6 AM): higher delta (more energy justice required)
            time_factor = self.time_factors['night']
        elif 10 <= current_hour <= 14:
            # Peak hours (10 AM - 2 PM): lower delta (less strict)
            time_factor = self.time_factors['peak']
            
        delta *= time_factor
        
        # Factor 2: System load adjustment
        system_load = psutil.cpu_percent() / 100.0
        load_adjustment = 1.0 - (system_load * self.load_factor)
        delta *= load_adjustment
        
        # Factor 3: Battery status adjustment
        if self.on_battery:
            # Increase delta when on battery (more energy justice required)
            battery_factor = 1.2
            
            # Check battery percentage if available
            try:
                battery = psutil.sensors_battery()
                if battery and battery.percent < 30:
                    # Even higher delta for low battery
                    battery_factor = 1.5
            except:
                pass
                
            delta *= battery_factor
            
        # Factor 4: Day of week adjustment (weekends vs weekdays)
        day_of_week = datetime.datetime.now().weekday()
        if day_of_week >= 5:  # 5 and 6 are Saturday and Sunday
            # Slightly lower delta on weekends
            delta *= 0.9
            
        # Ensure delta is within reasonable bounds
        delta = max(1.0, min(10.0, delta))
        
        # Cache the calculated value
        self.energy_justice_delta = delta
        self.last_delta_update = current_time
        
        return delta
        
    def track_energy_use(self, truth_value: float, processing_time: float) -> Dict[str, float]:
        """
        Track energy consumption with transparent formula.
        
        Formula: E_justice = (T_total * δ) / P_consumed
        
        Args:
            truth_value: Semantic truth value generated
            processing_time: Time spent processing in seconds
            
        Returns:
            Dict with energy tracking metrics
        """
        if not self.enabled:
            return {
                'energy_used': 0.0,
                'energy_justice_ratio': 1.0,
                'total_energy_used': 0.0
            }
            
        # Get current delta with transparent calculation
        delta = self._calculate_energy_justice_delta()
        
        # Estimate energy consumption
        energy_used = self._estimate_energy_consumption(processing_time)
        self.total_energy_used += energy_used
        
        # Calculate energy justice with transparent formula
        if energy_used > 0:
            energy_justice = (truth_value * delta) / energy_used
        else:
            energy_justice = 1.0
            
        # Update the energy justice ratio (weighted average)
        self.energy_justice_ratio = (0.7 * self.energy_justice_ratio) + (0.3 * energy_justice)
        
        # Log energy usage for transparency
        self.energy_log.append({
            'timestamp': time.time(),
            'truth_value': truth_value,
            'processing_time': processing_time,
            'energy_used': energy_used,
            'delta': delta,
            'energy_justice': energy_justice,
            'energy_justice_ratio': self.energy_justice_ratio
        })
        
        # Keep log size manageable
        if len(self.energy_log) > 100:
            self.energy_log = self.energy_log[-100:]
            
        return {
            'energy_used': energy_used,
            'energy_justice_ratio': self.energy_justice_ratio,
            'total_energy_used': self.total_energy_used,
            'delta': delta,
            'calculation': f"E_justice = ({truth_value} * {delta}) / {energy_used}"
        }
        
    def _estimate_energy_consumption(self, processing_time: float) -> float:
        """
        Estimate energy consumption based on processing time and system metrics.
        Uses a transparent formula instead of black-box estimation.
        
        Formula: E = processing_time * (cpu_power_factor + memory_factor) * profile_factor
        
        Args:
            processing_time: Time spent processing in seconds
            
        Returns:
            Estimated energy consumption in arbitrary units
        """
        # Get current CPU and memory usage
        cpu_percent = psutil.cpu_percent() / 100.0
        memory_percent = psutil.virtual_memory().percent / 100.0
        
        # Base energy factors
        cpu_power_factor = 1.0 + (cpu_percent * 2.0)  # CPU usage has significant impact
        memory_factor = 0.5 * memory_percent          # Memory usage has moderate impact
        
        # Profile-specific factor
        profile_factors = {
            'eco': 0.7,
            'balanced': 1.0,
            'performance': 1.5
        }
        profile_factor = profile_factors.get(self.current_profile, 1.0)
        
        # Calculate energy consumption with transparent formula
        energy = processing_time * (cpu_power_factor + memory_factor) * profile_factor
        
        return max(0.1, energy)  # Ensure minimum energy value
        
    def should_sleep(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Determine if the system should sleep based on energy justice ratio.
        Uses transparent thresholds from the current profile.
        
        Returns:
            Tuple of (should_sleep, details)
        """
        if not self.enabled:
            return False, {'reason': 'Energy module disabled'}
            
        # Get current profile
        profile = self.energy_profiles[self.current_profile]
        sleep_threshold = profile.get('sleep_threshold', 0.5)
        
        # Check energy justice ratio against threshold
        should_sleep = self.energy_justice_ratio < sleep_threshold
        
        details = {
            'energy_justice_ratio': self.energy_justice_ratio,
            'sleep_threshold': sleep_threshold,
            'current_profile': self.current_profile,
            'reason': f"Energy justice ratio ({self.energy_justice_ratio:.2f}) "
                     f"{'below' if should_sleep else 'above'} "
                     f"threshold ({sleep_threshold:.2f})"
        }
        
        return should_sleep, details
        
    def should_shutdown(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Determine if the system should shut down based on energy justice ratio.
        Uses a transparent, fixed threshold for critical energy justice violation.
        
        Returns:
            Tuple of (should_shutdown, details)
        """
        if not self.enabled:
            return False, {'reason': 'Energy module disabled'}
            
        # Fixed critical threshold
        critical_threshold = 0.2  # Transparent, fixed value
        
        # Check energy justice ratio against critical threshold
        should_shutdown = self.energy_justice_ratio < critical_threshold
        
        details = {
            'energy_justice_ratio': self.energy_justice_ratio,
            'critical_threshold': critical_threshold,
            'reason': f"Energy justice ratio ({self.energy_justice_ratio:.2f}) "
                     f"{'below' if should_shutdown else 'above'} "
                     f"critical threshold ({critical_threshold:.2f})"
        }
        
        return should_shutdown, details
        
    def get_energy_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive energy report with transparent metrics.
        
        Returns:
            Dict containing detailed energy usage information
        """
        # Get current profile
        current_profile = self.select_energy_profile()
        
        # Calculate energy efficiency
        if self.total_energy_used > 0:
            efficiency = self.energy_justice_ratio / self.total_energy_used
        else:
            efficiency = 1.0
            
        # Get system metrics
        system_metrics = {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'on_battery': self.on_battery
        }
        
        # Add battery information if available
        try:
            battery = psutil.sensors_battery()
            if battery:
                system_metrics['battery_percent'] = battery.percent
                system_metrics['battery_time_left'] = battery.secsleft
                system_metrics['power_plugged'] = battery.power_plugged
        except:
            pass
            
        # Generate report
        report = {
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'current_profile': current_profile,
            'energy_metrics': {
                'total_energy_used': self.total_energy_used,
                'energy_justice_ratio': self.energy_justice_ratio,
                'energy_efficiency': efficiency,
                'energy_justice_delta': self.energy_justice_delta
            },
            'system_metrics': system_metrics,
            'recent_energy_log': self.energy_log[-5:] if self.energy_log else [],
            'sleep_status': self.should_sleep()[0],
            'shutdown_status': self.should_shutdown()[0]
        }
        
        return report
