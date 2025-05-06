"""
EDEN.Logic Module
Function: Evaluates statements by semantic coherence, not binary logic
Key Mechanism: T(s, κ, t) ∈ [0,1]
Output: Contextual truth value, semantic integrity score
"""
import numpy as np
from typing import Dict, Any

class EdenLogic:
    """
    The Logic module evaluates statements by semantic coherence, not binary logic.
    It provides contextual truth values and semantic integrity scores.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Logic module with configuration settings.
        
        Args:
            config: Configuration dictionary for the Logic module
        """
        self.semantic_integrity_threshold = config.get('semantic_integrity_threshold', 0.75)
        self.enabled = config.get('enabled', True)
        
        # Initialize semantic coherence parameters
        self.context_weight = 0.7
        self.time_decay_factor = 0.05
    
    def evaluate(self, statement: str, context: Dict[str, Any] = None) -> float:
        """
        Evaluate a statement based on semantic coherence.
        
        Args:
            statement: The statement to evaluate
            context: Additional context for evaluation (e.g., intent analysis)
            
        Returns:
            Semantic truth value in the range [0,1]
        """
        if not self.enabled:
            return 0.5  # Neutral value when disabled
        
        # Extract parameters from the statement and context
        s = self._extract_semantic_content(statement)
        k = self._extract_context_parameter(context)
        t = self._extract_temporal_relevance()
        
        # Calculate T(s, κ, t) - the contextual truth value
        truth_value = self._calculate_truth_value(s, k, t)
        
        return truth_value
    
    def _extract_semantic_content(self, statement: str) -> Dict[str, float]:
        """Extract semantic content from the statement"""
        # Simplified implementation
        # In a real system, this would use more sophisticated NLP techniques
        
        words = statement.lower().split()
        semantic_content = {}
        
        # Create a simple semantic representation
        for word in words:
            # Assign a pseudo-random semantic value to each word
            semantic_content[word] = 0.5 + np.sin(hash(word) % 100) * 0.5
        
        return semantic_content
    
    def _extract_context_parameter(self, context: Dict[str, Any] = None) -> Dict[str, float]:
        """Extract context parameter from the provided context"""
        # Simplified implementation
        
        if not context:
            return {'default_context': 0.5}
        
        # Extract relevant information from the context
        context_param = {}
        
        # If we have intent analysis, use it
        if 'coherence' in context:
            context_param['coherence'] = context['coherence']
        
        if 'resonance_value' in context:
            context_param['resonance'] = context['resonance_value']
        
        if 'ethical_alignment' in context:
            for key, value in context['ethical_alignment'].items():
                context_param[f'ethical_{key}'] = value
        
        # If we couldn't extract anything useful, use a default
        if not context_param:
            context_param['default_context'] = 0.5
        
        return context_param
    
    def _extract_temporal_relevance(self) -> float:
        """Extract temporal relevance parameter"""
        # Simplified implementation
        # In a real system, this would consider time-based factors
        
        # For now, return a reasonable default
        return 0.9  # Assume high temporal relevance by default
    
    def _calculate_truth_value(self, s: Dict[str, float], k: Dict[str, float], t: float) -> float:
        """Calculate the contextual truth value T(s, κ, t)"""
        # Simplified implementation
        
        # Calculate semantic integrity
        semantic_integrity = self._calculate_semantic_integrity(s)
        
        # Calculate contextual coherence
        contextual_coherence = self._calculate_contextual_coherence(s, k)
        
        # Apply temporal adjustment
        temporal_adjustment = t * self.time_decay_factor
        
        # Combine factors to get truth value
        truth_value = (
            0.4 * semantic_integrity +
            0.5 * contextual_coherence +
            0.1 * (1.0 - temporal_adjustment)
        )
        
        return max(0.0, min(1.0, truth_value))
    
    def _calculate_semantic_integrity(self, s: Dict[str, float]) -> float:
        """Calculate semantic integrity of the content"""
        # Simplified implementation
        
        if not s:
            return 0.5
        
        # Calculate average semantic value
        avg_value = sum(s.values()) / len(s)
        
        # Calculate variance as a measure of consistency
        if len(s) > 1:
            variance = sum((v - avg_value) ** 2 for v in s.values()) / len(s)
            # Higher variance means lower integrity
            integrity = 1.0 - min(1.0, variance * 2)
        else:
            integrity = 0.7  # Default for single-word statements
        
        return integrity
    
    def _calculate_contextual_coherence(self, s: Dict[str, float], k: Dict[str, float]) -> float:
        """Calculate contextual coherence between semantic content and context"""
        # Simplified implementation
        
        if not s or not k:
            return 0.5
        
        # Calculate average context value
        avg_context = sum(k.values()) / len(k)
        
        # Calculate average semantic value
        avg_semantic = sum(s.values()) / len(s)
        
        # Simple coherence measure based on difference
        coherence = 1.0 - min(1.0, abs(avg_semantic - avg_context))
        
        return coherence
