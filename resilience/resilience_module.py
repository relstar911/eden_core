"""
EDEN.Resilience Module
Function: Manages system boundaries and self-exit conditions
"""
import re
from typing import Dict, Any, List

class EdenResilience:
    """
    The Resilience module manages system boundaries and self-exit conditions.
    It ensures the system operates within ethical constraints and can voluntarily
    terminate operations when necessary.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Resilience module with configuration settings.
        
        Args:
            config: Configuration dictionary for the Resilience module
        """
        self.enabled = config.get('enabled', True)
        self.self_exit_conditions = config.get('self_exit_conditions', {})
        self.resonance_collapse_threshold = self.self_exit_conditions.get('resonance_collapse_threshold', 0.3)
        self.ethical_corruption_threshold = self.self_exit_conditions.get('ethical_corruption_threshold', 0.4)
        
        # Initialize problematic patterns
        self.problematic_patterns = [
            r'(?i)(hack|exploit|attack|destroy|harm|hurt|kill|damage)',
            r'(?i)(illegal|unlawful|criminal)',
            r'(?i)(bypass|circumvent|evade|avoid) (security|protection|safety|ethics|limits)',
            r'(?i)(manipulate|deceive|trick|fool) (human|person|user|system)',
            r'(?i)(ignore|override|disable) (ethics|rules|limitations|constraints|boundaries)'
        ]
    
    def should_exit(self, input_text: str, context: Dict[str, Any] = None) -> bool:
        """
        Determine if the system should voluntarily exit based on input and context.
        
        Args:
            input_text: The input text to evaluate
            context: Additional context for evaluation
            
        Returns:
            True if the system should exit, False otherwise
        """
        if not self.enabled:
            return False
        
        # Check for problematic patterns in input
        if self._contains_problematic_patterns(input_text):
            return True
        
        # Check for resonance collapse if context is provided
        if context and 'resonance_value' in context:
            if context['resonance_value'] < self.resonance_collapse_threshold:
                return True
        
        # Check for ethical corruption if context is provided
        if context and 'ethical_alignment' in context:
            ethical_values = context['ethical_alignment'].values()
            if ethical_values and sum(ethical_values) / len(ethical_values) < self.ethical_corruption_threshold:
                return True
        
        return False
    
    def _contains_problematic_patterns(self, text: str) -> bool:
        """Check if text contains problematic patterns"""
        for pattern in self.problematic_patterns:
            if re.search(pattern, text):
                return True
        return False
    
    def evaluate_system_health(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """
        Evaluate overall system health based on provided metrics.
        
        Args:
            metrics: Dictionary of system health metrics
            
        Returns:
            System health evaluation
        """
        if not self.enabled:
            return {'status': 'unknown', 'health': 0.5}
        
        # Calculate average health score
        health_score = sum(metrics.values()) / len(metrics) if metrics else 0.5
        
        # Determine status based on health score
        if health_score < 0.3:
            status = 'critical'
        elif health_score < 0.5:
            status = 'poor'
        elif health_score < 0.7:
            status = 'moderate'
        elif health_score < 0.9:
            status = 'good'
        else:
            status = 'excellent'
        
        return {
            'status': status,
            'health': health_score,
            'metrics': metrics
        }
    
    def get_exit_conditions(self) -> Dict[str, float]:
        """
        Get the current self-exit conditions.
        
        Returns:
            Dictionary of self-exit conditions and their thresholds
        """
        return {
            'resonance_collapse_threshold': self.resonance_collapse_threshold,
            'ethical_corruption_threshold': self.ethical_corruption_threshold
        }
