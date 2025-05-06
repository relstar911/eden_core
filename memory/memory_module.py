"""
EDEN.Memory Module
Function: Stores contextual, meaningful experiences – not raw data
Structure: ε = (s, κ, t, ρ)
Output: Active memory only when contextually resonant
"""
import time
import json
import os
import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime

class MemoryEntry:
    """
    Represents a single memory entry in the EDEN.Memory system.
    """
    
    def __init__(self, semantic_content: str, context: Dict[str, Any], 
                 timestamp: float, resonance: float):
        """
        Initialize a memory entry.
        
        Args:
            semantic_content: The semantic content of the memory
            context: The context in which the memory was formed
            timestamp: The time when the memory was created
            resonance: The resonance value of the memory
        """
        self.semantic_content = semantic_content
        self.context = context
        self.timestamp = timestamp
        self.resonance = resonance
        self.access_count = 0
        self.last_accessed = timestamp
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert memory entry to dictionary for storage"""
        return {
            'semantic_content': self.semantic_content,
            'context': self.context,
            'timestamp': self.timestamp,
            'resonance': self.resonance,
            'access_count': self.access_count,
            'last_accessed': self.last_accessed
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryEntry':
        """Create memory entry from dictionary"""
        memory = cls(
            data['semantic_content'],
            data['context'],
            data['timestamp'],
            data['resonance']
        )
        memory.access_count = data.get('access_count', 0)
        memory.last_accessed = data.get('last_accessed', data['timestamp'])
        return memory
    
    def access(self) -> None:
        """Mark memory as accessed"""
        self.access_count += 1
        self.last_accessed = time.time()


class EdenMemory:
    """
    The Memory module stores contextual, meaningful experiences – not raw data.
    It provides active memory only when contextually resonant.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Memory module with configuration settings.
        
        Args:
            config: Configuration dictionary for the Memory module
        """
        self.retention_period = config.get('retention_period', 30)  # days
        self.context_weight = config.get('context_weight', 0.8)
        self.decay_rate = config.get('decay_rate', 0.05)
        self.enabled = config.get('enabled', True)
        
        # Create memory storage directory if it doesn't exist
        self.memory_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'memory_store')
        os.makedirs(self.memory_dir, exist_ok=True)
        
        # Initialize memory storage
        self.memory_file = os.path.join(self.memory_dir, 'memories.json')
        self.memories = self._load_memories()
    
    def _load_memories(self) -> List[MemoryEntry]:
        """Load memories from storage"""
        if not os.path.exists(self.memory_file):
            return []
        
        try:
            with open(self.memory_file, 'r') as f:
                memory_data = json.load(f)
                return [MemoryEntry.from_dict(entry) for entry in memory_data]
        except (json.JSONDecodeError, FileNotFoundError):
            # If file is corrupted or missing, start with empty memories
            return []
    
    def _save_memories(self) -> None:
        """Save memories to storage"""
        memory_data = [memory.to_dict() for memory in self.memories]
        
        with open(self.memory_file, 'w') as f:
            json.dump(memory_data, f, indent=2)
    
    def store(self, content: str, context: Dict[str, Any], resonance: float) -> None:
        """
        Store a new memory.
        
        Args:
            content: The content to store
            context: The context of the memory
            resonance: The resonance value of the memory
        """
        if not self.enabled:
            return
        
        # Create new memory entry
        memory = MemoryEntry(
            semantic_content=content,
            context=context,
            timestamp=time.time(),
            resonance=resonance
        )
        
        # Add to memories
        self.memories.append(memory)
        
        # Prune old memories
        self._prune_memories()
        
        # Save to disk
        self._save_memories()
    
    def retrieve(self, query: str, context: Dict[str, Any] = None) -> str:
        """
        Retrieve memories based on query and context.
        
        Args:
            query: The query to search for
            context: The context for retrieval
            
        Returns:
            Retrieved memory content or empty string if no relevant memory
        """
        if not self.enabled or not self.memories:
            return ""
        
        # Calculate relevance scores for all memories
        scored_memories = []
        current_time = time.time()
        
        for memory in self.memories:
            # Calculate semantic relevance
            semantic_relevance = self._calculate_semantic_relevance(query, memory.semantic_content)
            
            # Calculate context relevance
            context_relevance = self._calculate_context_relevance(context, memory.context)
            
            # Calculate temporal decay
            days_old = (current_time - memory.timestamp) / (60 * 60 * 24)
            temporal_factor = max(0.0, 1.0 - (days_old / self.retention_period))
            
            # Calculate access frequency boost
            access_boost = min(0.2, 0.02 * memory.access_count)
            
            # Calculate final relevance score
            relevance = (
                0.4 * semantic_relevance +
                0.3 * context_relevance +
                0.2 * temporal_factor +
                0.1 * memory.resonance +
                access_boost
            )
            
            scored_memories.append((memory, relevance))
        
        # Sort by relevance score
        scored_memories.sort(key=lambda x: x[1], reverse=True)
        
        # Return the most relevant memory if it exceeds threshold
        if scored_memories and scored_memories[0][1] > 0.6:
            most_relevant = scored_memories[0][0]
            most_relevant.access()
            self._save_memories()  # Update access stats
            
            # Format the memory for output
            timestamp_str = datetime.fromtimestamp(most_relevant.timestamp).strftime('%Y-%m-%d %H:%M:%S')
            return f"Memory ({timestamp_str}): {most_relevant.semantic_content}"
        
        return ""  # No relevant memory found
    
    def _calculate_semantic_relevance(self, query: str, content: str) -> float:
        """Calculate semantic relevance between query and memory content"""
        # Simplified implementation
        # In a real system, this would use embeddings or other semantic similarity measures
        
        query_words = set(query.lower().split())
        content_words = set(content.lower().split())
        
        if not query_words or not content_words:
            return 0.0
        
        # Calculate Jaccard similarity
        intersection = len(query_words.intersection(content_words))
        union = len(query_words.union(content_words))
        
        return intersection / union if union > 0 else 0.0
    
    def _calculate_context_relevance(self, query_context: Optional[Dict[str, Any]], 
                                    memory_context: Dict[str, Any]) -> float:
        """Calculate context relevance between query context and memory context"""
        # Simplified implementation
        
        if not query_context or not memory_context:
            return 0.5  # Neutral relevance if context is missing
        
        # Extract relevant features from contexts
        query_features = {}
        memory_features = {}
        
        # Extract resonance value if available
        if 'resonance_value' in query_context:
            query_features['resonance'] = query_context['resonance_value']
        
        if 'resonance' in memory_context:
            memory_features['resonance'] = memory_context['resonance']
        
        # Extract ethical alignment if available
        if 'ethical_alignment' in query_context:
            for key, value in query_context['ethical_alignment'].items():
                query_features[f'ethical_{key}'] = value
        
        if 'ethical_alignment' in memory_context:
            for key, value in memory_context['ethical_alignment'].items():
                memory_features[f'ethical_{key}'] = value
        
        # If we couldn't extract matching features, return neutral relevance
        common_keys = set(query_features.keys()).intersection(set(memory_features.keys()))
        if not common_keys:
            return 0.5
        
        # Calculate average difference for common features
        total_diff = 0.0
        for key in common_keys:
            total_diff += abs(query_features[key] - memory_features[key])
        
        avg_diff = total_diff / len(common_keys)
        
        # Convert difference to similarity (1.0 - diff)
        return max(0.0, 1.0 - avg_diff)
    
    def _prune_memories(self) -> None:
        """Prune old or low-resonance memories"""
        current_time = time.time()
        retention_seconds = self.retention_period * 24 * 60 * 60
        
        # Keep memories that are either recent or have high resonance
        self.memories = [
            memory for memory in self.memories
            if (current_time - memory.timestamp < retention_seconds) or
               (memory.resonance > 0.8)
        ]
        
        # If we still have too many memories, keep only the most resonant ones
        if len(self.memories) > 100:
            self.memories.sort(key=lambda m: m.resonance, reverse=True)
            self.memories = self.memories[:100]
