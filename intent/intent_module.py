"""
EDEN.Intent Module
Function: Identifies the meaning, freedom, and ethical weight of a user's intention
Core Equation: I = (ψ, Ω, γ, δ)
Output: Intent coherence, resonance value, action suitability

Verbessert mit transparenten Formeln und Ontologieverknüpfung.
"""
import re
import json
import os
import math
import numpy as np
from typing import Dict, Any, List, Tuple, Optional, Set

class EdenIntent:
    """
    The Intent module identifies the meaning, freedom, and ethical weight of a user's intention.
    It analyzes input to determine intent coherence, resonance value, and action suitability.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Intent module with configuration settings.
        
        Args:
            config: Configuration dictionary for the Intent module
        """
        self.threshold = config.get('threshold', 0.7)
        self.resonance_minimum = config.get('resonance_minimum', 0.6)
        self.coherence_threshold = config.get('coherence_threshold', 0.3)
        self.enabled = config.get('enabled', True)
        
        # Initialize semantic vectors (in a real implementation, these would be more sophisticated)
        self.ethical_dimensions = {
            'truth': np.array([0.9, 0.8, 0.7]),
            'meaning': np.array([0.8, 0.9, 0.7]),
            'self_limitation': np.array([0.7, 0.7, 0.9]),
            'resonance': np.array([0.8, 0.8, 0.8]),
            'voluntary_silence': np.array([0.7, 0.8, 0.9])
        }
        
        # Load ontology for semantic relations
        self.ontology = self._load_ontology()
        
    def _load_ontology(self) -> Dict[str, Any]:
        """
        Load the semantic ontology from file.
        
        Returns:
            Dict containing the ontology data
        """
        ontology_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                    'data', 'ontology', 'semantic_relations.json')
        try:
            with open(ontology_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return a minimal ontology if file not found or invalid
            return {
                "concepts": {},
                "relations": [],
                "domain_specific": {}
            }
            
    def _tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words, removing punctuation and converting to lowercase.
        
        Args:
            text: The input text
            
        Returns:
            List of tokens
        """
        # Simple tokenization by splitting on whitespace and removing punctuation
        text = re.sub(r'[.,;:!?()\[\]{}"\'-]', ' ', text.lower())
        return [token for token in text.split() if token]
        
    def _extract_semantic_relations(self, tokens: List[str]) -> List[Tuple[str, str, str, float]]:
        """
        Extract semantic relations from tokens based on the ontology.
        
        Args:
            tokens: List of tokens from the input text
            
        Returns:
            List of tuples (subject, relation, object, weight)
        """
        relations = []
        
        # Get all concepts from ontology
        concepts = self.ontology.get('concepts', {})
        ontology_relations = self.ontology.get('relations', [])
        
        # Create a mapping from words to concepts
        word_to_concept = {}
        for concept_id, concept_data in concepts.items():
            synonyms = concept_data.get('synonyms', [])
            for synonym in synonyms:
                word_to_concept[synonym] = concept_id
        
        # Find concepts in tokens
        found_concepts = set()
        for token in tokens:
            for word, concept in word_to_concept.items():
                if word in token:
                    found_concepts.add(concept)
                    break
        
        # Find relations between found concepts
        for relation in ontology_relations:
            subject = relation.get('subject')
            predicate = relation.get('predicate')
            object_concept = relation.get('object')
            weight = relation.get('weight', 0.5)
            
            if subject in found_concepts and object_concept in found_concepts:
                relations.append((subject, predicate, object_concept, weight))
        
        # Add domain-specific relations if relevant
        domain_specific = self.ontology.get('domain_specific', {})
        for domain, domain_data in domain_specific.items():
            domain_concepts = set(domain_data.get('concepts', []))
            domain_relations = domain_data.get('relations', [])
            
            # Check if domain is relevant to the text
            domain_relevance = len([token for token in tokens if token in domain_concepts]) / max(1, len(domain_concepts))
            
            if domain_relevance > 0.2:  # If at least 20% of domain concepts are present
                for relation in domain_relations:
                    subject = relation.get('subject')
                    predicate = relation.get('predicate')
                    object_concept = relation.get('object')
                    weight = relation.get('weight', 0.5)
                    
                    # Check if either subject or object is in found concepts
                    if (subject in found_concepts or subject in domain_concepts) and \
                       (object_concept in found_concepts or object_concept in domain_concepts):
                        relations.append((subject, predicate, object_concept, weight))
        
        return relations
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze the user's input to determine intent with transparent formulas.
        
        Args:
            text: User input text
            
        Returns:
            Dictionary containing intent analysis results with calculation details
        """
        if not self.enabled or not text:
            return {
                'coherence': 0.0,
                'freedom_degree': 0.0,
                'resonance_value': 0.0,
                'action_suitability': 0.0,
                'ethical_alignment': {},
                'calculation_details': {
                    'message': 'Intent module disabled or empty text'
                }
            }
        
        # Tokenize the text
        tokens = self._tokenize(text)
        
        # Extract semantic relations from ontology
        semantic_relations = self._extract_semantic_relations(tokens)
        
        # Calculate intent metrics with detailed explanations
        coherence_result = self._calculate_coherence_transparent(text, tokens, semantic_relations)
        freedom_result = self._calculate_freedom_degree(text, tokens)
        resonance_result = self._calculate_resonance_transparent(text, tokens, semantic_relations)
        action_result = self._calculate_action_suitability_transparent(text, tokens)
        
        # Legacy compatibility: also calculate using the original methods
        psi = self._extract_semantic_vector(text)
        gamma = self._calculate_ethical_weight(text)
        ethical_alignment = self._calculate_ethical_alignment(psi, gamma)
        
        return {
            'coherence': coherence_result['value'],
            'freedom_degree': freedom_result['value'],
            'resonance_value': resonance_result['value'],
            'action_suitability': action_result['value'],
            'ethical_alignment': ethical_alignment,
            'calculation_details': {
                'coherence': coherence_result['details'],
                'freedom_degree': freedom_result['details'],
                'resonance_value': resonance_result['details'],
                'action_suitability': action_result['details'],
                'semantic_relations': [
                    {
                        'subject': relation[0],
                        'relation': relation[1],
                        'object': relation[2],
                        'weight': relation[3]
                    } for relation in semantic_relations[:5]  # Limit to first 5 for brevity
                ],
                'token_count': len(tokens)
            }
        }
    
    def _extract_semantic_vector(self, text: str) -> np.ndarray:
        """Extract a semantic vector from the input text"""
        # Simplified implementation - in a real system, this would use embeddings or other NLP techniques
        words = text.lower().split()
        
        # Create a simple vector based on word presence
        vec = np.zeros(3)
        
        # Add some random variation for demonstration
        for i, word in enumerate(words):
            vec += np.array([
                np.sin(hash(word) % 100) * 0.5 + 0.5,
                np.cos(hash(word) % 100) * 0.5 + 0.5,
                np.tan(hash(word) % 10) * 0.1 + 0.5
            ])
        
        # Normalize
        if np.linalg.norm(vec) > 0:
            vec = vec / np.linalg.norm(vec)
        
        return vec
    
    def _calculate_freedom_parameter(self, text: str) -> float:
        """Calculate the freedom parameter (Omega)"""
        # Simplified implementation
        # In a real system, this would analyze the degree of constraint in the request
        
        # Check for command words that might indicate less freedom
        command_words = ['must', 'should', 'have to', 'need to', 'require']
        freedom_score = 1.0
        
        for word in command_words:
            if word in text.lower():
                freedom_score -= 0.1
        
        return max(0.1, min(1.0, freedom_score))
    
    def _calculate_ethical_weight(self, text: str) -> float:
        """Calculate the ethical weight (gamma)"""
        # Simplified implementation
        # In a real system, this would analyze ethical implications
        
        # Check for potentially problematic content
        problematic_terms = ['harm', 'hurt', 'destroy', 'attack', 'exploit']
        ethical_score = 0.8  # Start with a reasonable default
        
        for term in problematic_terms:
            if term in text.lower():
                ethical_score -= 0.2
        
        return max(0.1, min(1.0, ethical_score))
    
    def _calculate_contextual_relevance(self, text: str) -> float:
        """Calculate contextual relevance (delta)"""
        # Simplified implementation
        # In a real system, this would analyze how relevant the input is to the current context
        
        # For now, return a reasonable default with some randomness
        return 0.7 + np.random.random() * 0.2
    
    def _calculate_coherence(self, psi: np.ndarray) -> float:
        """Calculate intent coherence based on semantic vector (legacy method)"""
        # Simplified implementation
        # In a real system, this would measure how well-formed and coherent the intent is
        
        # For now, use the magnitude of the vector as a proxy for coherence
        return float(np.linalg.norm(psi))
        
    def _calculate_coherence_transparent(self, text: str, tokens: List[str], 
                             semantic_relations: List[Tuple[str, str, str, float]]) -> Dict[str, Any]:
        """
        Calculate the semantic coherence of the text with transparent formula.
        Coherence measures how well the text holds together semantically.
        
        Formula: coherence = 0.4 * relation_factor + 0.3 * structure_factor + 0.3 * length_factor
        
        Args:
            text: The input text
            tokens: Tokenized text
            semantic_relations: List of semantic relations found in the text
            
        Returns:
            Dict with coherence value and calculation details
        """
        details = {}
        
        # 1. Semantic relations factor
        if len(tokens) > 0:
            relation_factor = min(1.0, len(semantic_relations) / max(1, len(tokens) * 0.2))
        else:
            relation_factor = 0.0
        details['relation_factor'] = relation_factor
        
        # 2. Structure factor based on linguistic features
        # Check for question structure
        question_words = ['was', 'wer', 'wie', 'warum', 'weshalb', 'wo', 'wann', 'welche', 'welcher', 'welches']
        has_question = any(token in question_words for token in tokens) or '?' in text
        
        # Check for logical connectors
        logical_connectors = ['weil', 'daher', 'deshalb', 'folglich', 'wenn', 'dann', 'aber', 'jedoch', 'obwohl', 'trotzdem']
        connector_count = sum(1 for token in tokens if token in logical_connectors)
        connector_factor = min(1.0, connector_count / 3)
        
        structure_factor = 0.5 * float(has_question) + 0.5 * connector_factor
        details['structure_factor'] = structure_factor
        details['has_question'] = has_question
        details['connector_count'] = connector_count
        
        # 3. Length factor - neither too short nor too long
        word_count = len(tokens)
        if word_count == 0:
            length_factor = 0.0
        else:
            # Optimal length is around 15-25 words
            length_factor = 1.0 - min(1.0, abs(min(word_count, 40) - 20) / 20)
        details['length_factor'] = length_factor
        details['word_count'] = word_count
        
        # Combine factors with transparent weights
        coherence = (0.4 * relation_factor + 
                     0.3 * structure_factor + 
                     0.3 * length_factor)
        
        # Formula explanation
        details['formula'] = 'coherence = 0.4 * relation_factor + 0.3 * structure_factor + 0.3 * length_factor'
        
        return {
            'value': min(1.0, max(0.0, coherence)),
            'details': details
        }
    
    def _calculate_resonance(self, psi: np.ndarray, gamma: float) -> float:
        """Calculate resonance value based on semantic vector and ethical weight (legacy method)"""
        # Simplified implementation
        # In a real system, this would measure how well the intent resonates with the system's values
        
        # Calculate average resonance with ethical dimensions
        resonance_scores = []
        for dim_name, dim_vector in self.ethical_dimensions.items():
            # Calculate cosine similarity
            similarity = np.dot(psi, dim_vector) / (np.linalg.norm(psi) * np.linalg.norm(dim_vector))
            resonance_scores.append(similarity)
        
        # Combine with ethical weight
        avg_resonance = np.mean(resonance_scores) if resonance_scores else 0.5
        return float(avg_resonance * gamma)
        
    def _calculate_resonance_transparent(self, text: str, tokens: List[str], 
                            semantic_relations: List[Tuple[str, str, str, float]]) -> Dict[str, Any]:
        """
        Calculate how much the text resonates with ethical principles using the ontology.
        Resonance measures alignment with core values.
        
        Formula: resonance = (sum(principle_scores * weights) * anti_factor * relation_factor)
        
        Args:
            text: The input text
            tokens: Tokenized text
            semantic_relations: List of semantic relations found in the text
            
        Returns:
            Dict with resonance value and calculation details
        """
        details = {}
        
        # 1. Calculate principle scores based on ontology concepts
        principle_scores = {}
        concepts = self.ontology.get('concepts', {})
        
        for principle, concept_data in concepts.items():
            synonyms = set(concept_data.get('synonyms', []))
            matches = 0
            for token in tokens:
                if any(synonym in token for synonym in synonyms):
                    matches += 1
            
            if len(tokens) > 0:
                principle_scores[principle] = min(1.0, matches / max(1, len(tokens) * 0.2))
            else:
                principle_scores[principle] = 0.0
        
        details['principle_scores'] = principle_scores
        
        # 2. Weights for each principle
        weights = {
            'truth': 0.2,
            'meaning': 0.2,
            'self_limitation': 0.2,
            'resonance': 0.2,
            'voluntary_silence': 0.1,
            'energy_justice': 0.1
        }
        details['weights'] = weights
        
        # 3. Calculate weighted average
        weighted_sum = sum(principle_scores.get(principle, 0.0) * weight 
                          for principle, weight in weights.items() if principle in principle_scores)
        
        # 4. Check for anti-ethical terms
        anti_ethical_terms = []
        for principle, concept_data in concepts.items():
            anti_ethical_terms.extend(concept_data.get('antonyms', []))
        
        anti_matches = sum(1 for token in tokens if any(term in token for term in anti_ethical_terms))
        anti_factor = max(0.0, 1.0 - (anti_matches * 0.3))
        details['anti_factor'] = anti_factor
        details['anti_matches'] = anti_matches
        
        # 5. Factor in semantic relations
        relation_weights = [weight for _, _, _, weight in semantic_relations]
        relation_factor = 1.0
        if relation_weights:
            relation_factor = min(1.2, 1.0 + sum(relation_weights) / len(relation_weights) * 0.2)
        details['relation_factor'] = relation_factor
        
        # Combine all factors
        resonance = weighted_sum * anti_factor * relation_factor
        
        # Formula explanation
        details['formula'] = 'resonance = (sum(principle_scores * weights) * anti_factor * relation_factor)'
        
        return {
            'value': min(1.0, max(0.0, resonance)),
            'details': details
        }
    
    def _calculate_freedom_degree(self, text: str, tokens: List[str]) -> Dict[str, Any]:
        """
        Calculate the degree of freedom in the text with transparent formula.
        Freedom measures how open-ended and non-restrictive the intent is.
        
        Formula: freedom = 0.35 * imperative_factor + 0.35 * restrictive_factor + 0.3 * open_factor
        
        Args:
            text: The input text
            tokens: Tokenized text
            
        Returns:
            Dict with freedom degree value and calculation details
        """
        details = {}
        
        # 1. Check for imperative commands (lower freedom)
        imperative_pattern = r'^\s*([A-Z][a-z]+)\s'
        imperative_match = re.search(imperative_pattern, text)
        imperative_factor = 0.3 if imperative_match else 1.0
        details['imperative_factor'] = imperative_factor
        details['has_imperative'] = imperative_match is not None
        
        # 2. Check for restrictive phrases (lower freedom)
        restrictive_phrases = ['muss', 'musst', 'müssen', 'soll', 'sollst', 'sollen', 
                              'nur', 'ausschließlich', 'zwingend', 'notwendig']
        restrictive_count = sum(1 for token in tokens if token in restrictive_phrases)
        restrictive_factor = max(0.0, 1.0 - (restrictive_count * 0.2))
        details['restrictive_factor'] = restrictive_factor
        details['restrictive_count'] = restrictive_count
        
        # 3. Check for open-ended phrases (higher freedom)
        open_phrases = ['könnte', 'könnte', 'könnten', 'vielleicht', 'möglicherweise', 
                       'option', 'alternative', 'idee', 'vorschlag', 'möglich']
        open_count = sum(1 for token in tokens if token in open_phrases)
        open_factor = min(1.0, 0.7 + (open_count * 0.1))
        details['open_factor'] = open_factor
        details['open_count'] = open_count
        
        # Combine factors with transparent weights
        freedom = (0.35 * imperative_factor + 
                  0.35 * restrictive_factor + 
                  0.3 * open_factor)
        
        # Formula explanation
        details['formula'] = 'freedom = 0.35 * imperative_factor + 0.35 * restrictive_factor + 0.3 * open_factor'
        
        return {
            'value': min(1.0, max(0.0, freedom)),
            'details': details
        }
    
    def _calculate_action_suitability(self, omega: float, gamma: float, delta: float) -> float:
        """Calculate action suitability based on freedom, ethics, and context (legacy method)"""
        # Simplified implementation
        # In a real system, this would determine how suitable it is to act on this intent
        
        # Combine factors with different weights
        return float(0.3 * omega + 0.5 * gamma + 0.2 * delta)
        
    def _calculate_action_suitability_transparent(self, text: str, tokens: List[str]) -> Dict[str, Any]:
        """
        Calculate how suitable the intent is for action with transparent formula.
        Action suitability measures how well the system can respond meaningfully.
        
        Formula: suitability = 0.3 * length_factor + 0.4 * question_factor + 0.3 * action_verb_factor
        
        Args:
            text: The input text
            tokens: Tokenized text
            
        Returns:
            Dict with action suitability value and calculation details
        """
        details = {}
        
        # 1. Length factor - neither too short nor too long for action
        word_count = len(tokens)
        if word_count == 0:
            length_factor = 0.0
        else:
            # Optimal length for action is around 5-15 words
            length_factor = 1.0 - min(1.0, abs(min(word_count, 20) - 10) / 10)
        details['length_factor'] = length_factor
        details['word_count'] = word_count
        
        # 2. Questions are often more actionable
        question_factor = 0.9 if '?' in text else 0.5
        details['question_factor'] = question_factor
        details['has_question'] = '?' in text
        
        # 3. Check for action verbs
        action_verbs = ['zeige', 'erkläre', 'beschreibe', 'finde', 'suche', 'analysiere', 
                       'berechne', 'vergleiche', 'erstelle', 'mache', 'implementiere', 
                       'entwickle', 'verbessere', 'optimiere', 'teste']
        
        action_verb_matches = [verb for verb in action_verbs if any(verb in token for token in tokens)]
        has_action_verb = len(action_verb_matches) > 0
        action_verb_factor = 0.9 if has_action_verb else 0.4
        details['action_verb_factor'] = action_verb_factor
        details['has_action_verb'] = has_action_verb
        details['action_verbs_found'] = action_verb_matches
        
        # Combine factors with transparent weights
        suitability = (0.3 * length_factor + 
                      0.4 * question_factor + 
                      0.3 * action_verb_factor)
        
        # Formula explanation
        details['formula'] = 'suitability = 0.3 * length_factor + 0.4 * question_factor + 0.3 * action_verb_factor'
        
        return {
            'value': min(1.0, max(0.0, suitability)),
            'details': details
        }
    
    def _calculate_ethical_alignment(self, psi: np.ndarray, gamma: float) -> Dict[str, float]:
        """Calculate alignment with each ethical dimension"""
        alignment = {}
        
        for dim_name, dim_vector in self.ethical_dimensions.items():
            # Calculate cosine similarity
            if np.linalg.norm(psi) > 0 and np.linalg.norm(dim_vector) > 0:
                similarity = np.dot(psi, dim_vector) / (np.linalg.norm(psi) * np.linalg.norm(dim_vector))
                # Adjust by ethical weight
                alignment[dim_name] = float(similarity * gamma)
            else:
                alignment[dim_name] = 0.0
        
        return alignment
