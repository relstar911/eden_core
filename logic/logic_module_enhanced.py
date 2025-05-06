"""
EDEN.CORE - Logic Module (Enhanced)
Evaluates statements based on semantic coherence with emotional depth analysis and discrepancy detection
"""

import re
import json
import os
import math
from typing import Dict, Any, List, Tuple, Optional, Set

class EdenLogic:
    """
    Logic evaluation module for EDEN.CORE.
    Evaluates statements by semantic coherence, not binary logic.
    Implements the principle of "Truth Over Optimization" with transparent formulas.
    Includes emotional depth analysis and discrepancy detection.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the logic module.
        
        Args:
            config: Configuration settings for the module
        """
        self.enabled = config.get('enabled', True)
        self.truth_threshold = config.get('truth_threshold', 0.6)
        
        # Load emotion patterns for emotional depth analysis
        self.emotion_patterns = self._load_emotion_patterns()
        
    def _load_emotion_patterns(self) -> Dict[str, Any]:
        """
        Load the emotion patterns from file.
        
        Returns:
            Dict containing the emotion patterns data
        """
        patterns_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                    'data', 'emotion_patterns.json')
        try:
            with open(patterns_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return minimal emotion patterns if file not found or invalid
            return {
                "emotions": {},
                "emotional_patterns": {},
                "discrepancy_patterns": {}
            }
            
    def evaluate(self, text: str, intent_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate the semantic truth of the input text with emotional depth analysis.
        
        Args:
            text: The input text to evaluate
            intent_analysis: Intent analysis results
            
        Returns:
            Dict containing truth value and detailed calculation information
        """
        if not self.enabled or not text:
            return {
                'truth_value': 0.0,
                'calculation_details': {
                    'message': 'Logic module disabled or empty text'
                }
            }
            
        # Extract semantic context
        semantic_context = self._extract_semantic_context(text)
        
        # Get coherence from intent analysis
        coherence = intent_analysis.get('coherence', 0.0)
        
        # Extract temporal context
        temporal_context = self._extract_temporal_context(text)
        
        # Analyze emotional depth
        emotional_depth = self._analyze_emotional_depth(text)
        
        # Detect discrepancy between content and emotional expression
        discrepancy = self._detect_discrepancy(text, semantic_context, emotional_depth)
        
        # Calculate truth value with all factors
        truth_result = self._calculate_truth_value(
            semantic_context, 
            coherence, 
            temporal_context,
            emotional_depth,
            discrepancy
        )
        
        return {
            'truth_value': truth_result['value'],
            'calculation_details': {
                'semantic_context': semantic_context,
                'temporal_context': temporal_context,
                'emotional_depth': emotional_depth,
                'discrepancy': discrepancy,
                'calculation': truth_result['details']
            }
        }
    
    def _extract_semantic_context(self, text: str) -> Dict[str, Any]:
        """
        Extract semantic context from the text.
        
        Args:
            text: The input text
            
        Returns:
            Dict with semantic context information
        """
        # Identify key concepts and their relationships
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Count word frequencies
        word_counts = {}
        for word in words:
            if len(word) > 3:  # Skip very short words
                word_counts[word] = word_counts.get(word, 0) + 1
                
        # Identify most frequent words as key concepts
        key_concepts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Check for negations
        negation_words = ['nicht', 'kein', 'keine', 'keiner', 'niemals', 'nie']
        has_negation = any(neg in words for neg in negation_words)
        
        # Check for uncertainty markers
        uncertainty_words = ['vielleicht', 'möglicherweise', 'eventuell', 'könnte', 'vermutlich']
        uncertainty_level = sum(1 for word in words if word in uncertainty_words) / max(1, len(words))
        
        return {
            'key_concepts': key_concepts,
            'has_negation': has_negation,
            'uncertainty_level': uncertainty_level,
            'word_count': len(words)
        }
        
    def _extract_temporal_context(self, text: str) -> Dict[str, Any]:
        """
        Extract temporal context from the text.
        
        Args:
            text: The input text
            
        Returns:
            Dict with temporal context information
        """
        # Identify temporal markers
        past_markers = ['war', 'hatte', 'ging', 'gestern', 'früher', 'damals', 'vorher']
        present_markers = ['ist', 'hat', 'geht', 'heute', 'jetzt', 'gerade', 'aktuell']
        future_markers = ['wird', 'soll', 'morgen', 'bald', 'später', 'zukünftig', 'demnächst']
        
        words = re.findall(r'\b\w+\b', text.lower())
        
        past_count = sum(1 for word in words if word in past_markers)
        present_count = sum(1 for word in words if word in present_markers)
        future_count = sum(1 for word in words if word in future_markers)
        
        total_markers = past_count + present_count + future_count
        
        if total_markers == 0:
            # Default to present if no temporal markers
            temporal_orientation = 'present'
            confidence = 0.5
        else:
            # Determine primary temporal orientation
            if past_count >= present_count and past_count >= future_count:
                temporal_orientation = 'past'
            elif future_count >= present_count and future_count >= past_count:
                temporal_orientation = 'future'
            else:
                temporal_orientation = 'present'
                
            # Calculate confidence in temporal orientation
            confidence = max(past_count, present_count, future_count) / total_markers
            
        return {
            'temporal_orientation': temporal_orientation,
            'confidence': confidence,
            'past_markers': past_count,
            'present_markers': present_count,
            'future_markers': future_count
        }
        
    def _analyze_emotional_depth(self, text: str) -> Dict[str, Any]:
        """
        Analyze the emotional depth of the text using pattern matching.
        
        Args:
            text: The input text
            
        Returns:
            Dict with emotional depth analysis
        """
        # Get emotion patterns
        emotions = self.emotion_patterns.get('emotions', {})
        emotional_patterns = self.emotion_patterns.get('emotional_patterns', {})
        
        # Detect emotions
        detected_emotions = {}
        for emotion_name, emotion_data in emotions.items():
            patterns = emotion_data.get('patterns', [])
            intensity_modifiers = emotion_data.get('intensity_modifiers', {})
            
            # Check each pattern
            strength = 0.0
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    # Base strength for matching the pattern
                    pattern_strength = 0.2
                    
                    # Check for intensity modifiers
                    high_modifiers = intensity_modifiers.get('high', [])
                    low_modifiers = intensity_modifiers.get('low', [])
                    
                    # Apply modifiers if found
                    for match in matches:
                        context = self._get_context(text, match, 5)
                        if any(mod in context for mod in high_modifiers):
                            pattern_strength = 0.3
                        elif any(mod in context for mod in low_modifiers):
                            pattern_strength = 0.1
                    
                    strength += pattern_strength
            
            if strength > 0:
                detected_emotions[emotion_name] = min(1.0, strength)
        
        # Detect emotional complexity patterns
        emotional_complexity = {}
        for pattern_name, pattern_data in emotional_patterns.items():
            pattern = pattern_data.get('pattern', '')
            if re.search(pattern, text, re.IGNORECASE):
                emotional_complexity[pattern_name] = True
        
        # Calculate emotional depth metrics
        variety = len(detected_emotions) / max(1, len(emotions))
        intensity = sum(detected_emotions.values()) / max(1, len(detected_emotions))
        complexity = len(emotional_complexity) / max(1, len(emotional_patterns))
        
        # Overall emotional depth score
        depth_score = (0.4 * variety + 0.3 * intensity + 0.3 * complexity)
        
        return {
            'detected_emotions': detected_emotions,
            'emotional_complexity': list(emotional_complexity.keys()),
            'variety': variety,
            'intensity': intensity,
            'complexity': complexity,
            'depth_score': depth_score
        }
        
    def _get_context(self, text: str, match: str, window: int) -> str:
        """
        Get the context around a matched string.
        
        Args:
            text: The full text
            match: The matched string
            window: Number of words to include before and after
            
        Returns:
            Context string
        """
        words = text.split()
        try:
            match_words = match.split()
            for i in range(len(words) - len(match_words) + 1):
                if ' '.join(words[i:i+len(match_words)]).lower() == match.lower():
                    start = max(0, i - window)
                    end = min(len(words), i + len(match_words) + window)
                    return ' '.join(words[start:end])
        except:
            pass
        return match
        
    def _detect_discrepancy(self, text: str, semantic_context: Dict[str, Any], 
                           emotional_depth: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect discrepancies between semantic content and emotional expression.
        
        Args:
            text: The input text
            semantic_context: Extracted semantic context
            emotional_depth: Emotional depth analysis
            
        Returns:
            Dict with discrepancy information
        """
        # Get discrepancy patterns
        discrepancy_patterns = self.emotion_patterns.get('discrepancy_patterns', {})
        
        # Check for pattern matches
        detected_discrepancies = {}
        for pattern_name, pattern_data in discrepancy_patterns.items():
            pattern = pattern_data.get('pattern', '')
            if re.search(pattern, text, re.IGNORECASE):
                detected_discrepancies[pattern_name] = True
        
        # Check for semantic-emotional mismatch
        # E.g., positive semantic content with negative emotions or vice versa
        positive_emotions = ['joy', 'trust', 'anticipation']
        negative_emotions = ['sadness', 'anger', 'fear', 'disgust']
        
        positive_emotion_score = sum(emotional_depth.get('detected_emotions', {}).get(e, 0) 
                                    for e in positive_emotions)
        negative_emotion_score = sum(emotional_depth.get('detected_emotions', {}).get(e, 0) 
                                    for e in negative_emotions)
        
        # Determine if there's a significant difference
        emotion_mismatch = abs(positive_emotion_score - negative_emotion_score) > 0.3
        
        # Check for negation with positive emotion
        negation_with_positive = semantic_context.get('has_negation', False) and positive_emotion_score > 0.3
        
        # Calculate overall discrepancy score
        discrepancy_score = (
            0.4 * len(detected_discrepancies) / max(1, len(discrepancy_patterns)) +
            0.3 * float(emotion_mismatch) +
            0.3 * float(negation_with_positive)
        )
        
        return {
            'detected_discrepancies': list(detected_discrepancies.keys()),
            'emotion_mismatch': emotion_mismatch,
            'negation_with_positive': negation_with_positive,
            'discrepancy_score': discrepancy_score
        }
        
    def _calculate_truth_value(self, semantic_context: Dict[str, Any], coherence: float,
                              temporal_context: Dict[str, Any], emotional_depth: Dict[str, Any],
                              discrepancy: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate the semantic truth value with transparent formula.
        
        Formula: truth_value = (0.3 * coherence + 0.2 * (1 - uncertainty) + 0.2 * temporal_confidence + 
                               0.2 * emotional_depth - 0.1 * discrepancy)
        
        Args:
            semantic_context: Extracted semantic context
            coherence: Coherence value from intent analysis
            temporal_context: Extracted temporal context
            emotional_depth: Emotional depth analysis
            discrepancy: Discrepancy detection results
            
        Returns:
            Dict with truth value and calculation details
        """
        details = {}
        
        # 1. Coherence factor
        coherence_factor = coherence
        details['coherence_factor'] = coherence_factor
        
        # 2. Certainty factor (inverse of uncertainty)
        uncertainty = semantic_context.get('uncertainty_level', 0.0)
        certainty_factor = 1.0 - uncertainty
        details['certainty_factor'] = certainty_factor
        details['uncertainty_level'] = uncertainty
        
        # 3. Temporal confidence factor
        temporal_confidence = temporal_context.get('confidence', 0.5)
        details['temporal_confidence'] = temporal_confidence
        
        # 4. Emotional depth factor
        emotional_depth_factor = emotional_depth.get('depth_score', 0.0)
        details['emotional_depth_factor'] = emotional_depth_factor
        
        # 5. Discrepancy factor (reduces truth value)
        discrepancy_factor = discrepancy.get('discrepancy_score', 0.0)
        details['discrepancy_factor'] = discrepancy_factor
        
        # Calculate truth value with transparent weights
        truth_value = (
            0.3 * coherence_factor +
            0.2 * certainty_factor +
            0.2 * temporal_confidence +
            0.2 * emotional_depth_factor -
            0.1 * discrepancy_factor
        )
        
        # Formula explanation
        details['formula'] = ('truth_value = (0.3 * coherence + 0.2 * (1 - uncertainty) + ' +
                             '0.2 * temporal_confidence + 0.2 * emotional_depth - ' +
                             '0.1 * discrepancy)')
        
        return {
            'value': min(1.0, max(0.0, truth_value)),
            'details': details
        }
