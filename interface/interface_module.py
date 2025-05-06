"""
EDEN.Interface Module
Function: Provides a multimodal interface layer for interaction with the system
"""
from typing import Dict, Any, List

class EdenInterface:
    """
    The Interface module provides a layer for interaction between users and the system.
    It processes input and formats output according to the system's principles.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Interface module with configuration settings.
        
        Args:
            config: Configuration dictionary for the Interface module
        """
        self.input_modes = config.get('input_modes', ['text'])
        self.output_modes = config.get('output_modes', ['text'])
        self.enabled = config.get('enabled', True)
        
        # Initialize input processors
        self.input_processors = {
            'text': self._process_text_input
        }
        
        # Initialize output formatters
        self.output_formatters = {
            'text': self._format_text_output
        }
    
    def process_input(self, input_data: str, input_mode: str = 'text') -> str:
        """
        Process input data according to the specified mode.
        
        Args:
            input_data: The input data to process
            input_mode: The mode of the input (default: 'text')
            
        Returns:
            Processed input data
        """
        if not self.enabled:
            return input_data
        
        if input_mode not in self.input_modes:
            raise ValueError(f"Unsupported input mode: {input_mode}")
        
        processor = self.input_processors.get(input_mode)
        if not processor:
            return input_data
        
        return processor(input_data)
    
    def format_output(self, output_data: Any, output_mode: str = 'text') -> str:
        """
        Format output data according to the specified mode.
        
        Args:
            output_data: The output data to format
            output_mode: The mode of the output (default: 'text')
            
        Returns:
            Formatted output data
        """
        if not self.enabled:
            return str(output_data)
        
        if output_mode not in self.output_modes:
            raise ValueError(f"Unsupported output mode: {output_mode}")
        
        formatter = self.output_formatters.get(output_mode)
        if not formatter:
            return str(output_data)
        
        return formatter(output_data)
    
    def _process_text_input(self, text: str) -> str:
        """Process text input"""
        # Simplified implementation
        # In a real system, this would do more sophisticated processing
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Basic sanitization
        text = text.strip()
        
        return text
    
    def _format_text_output(self, data: Any) -> str:
        """Format data as text output"""
        # Simplified implementation
        
        if isinstance(data, str):
            return data
        
        if isinstance(data, dict):
            # Format dictionary as readable text
            lines = []
            for key, value in data.items():
                lines.append(f"{key}: {value}")
            return '\n'.join(lines)
        
        if isinstance(data, list):
            # Format list as readable text
            return '\n'.join(str(item) for item in data)
        
        # Default to string representation
        return str(data)
    
    def create_response(self, intent_analysis: Dict[str, Any], 
                       semantic_truth: float, 
                       memory_response: str,
                       system_message: str) -> Dict[str, Any]:
        """
        Create a structured response based on system outputs.
        
        Args:
            intent_analysis: Analysis of user intent
            semantic_truth: Semantic truth value
            memory_response: Response from memory module
            system_message: System message
            
        Returns:
            Structured response
        """
        # Format intent analysis for readability
        intent_summary = {
            'coherence': f"{intent_analysis.get('coherence', 0):.2f}",
            'resonance': f"{intent_analysis.get('resonance_value', 0):.2f}",
            'action_suitability': f"{intent_analysis.get('action_suitability', 0):.2f}"
        }
        
        # Format semantic truth for readability
        truth_rating = f"{semantic_truth:.2f}"
        
        # Combine memory response and system message
        response_text = ""
        if memory_response:
            response_text += f"{memory_response}\n\n"
        
        response_text += system_message
        
        return {
            'intent_summary': intent_summary,
            'truth_rating': truth_rating,
            'response': response_text
        }
