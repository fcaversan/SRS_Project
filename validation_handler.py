"""
Validation Module for UML Diagram Automation
Handles diagram validation, QA metrics extraction, and report generation.
"""

import json
import re
import datetime
import os
from typing import Dict, List, Any


class ValidationHandler:
    """Handles diagram validation and QA reporting."""
    
    @staticmethod
    def apply_diagram_penalties(metrics: Dict[str, Any], diagram_contents: Dict[str, str]) -> Dict[str, Any]:
        """
        Apply penalties to the overall score based on missing or failed diagrams.
        
        Penalty Rules:
        - Missing diagram (not generated): -5 points per diagram
        - Diagram with errors: -3 points per diagram
        
        Args:
            metrics (Dict): Original metrics from Gemini
            diagram_contents (Dict): Dictionary of diagram contents
            
        Returns:
            Dict: Updated metrics with penalties applied
        """
        missing_diagrams = []
        error_diagrams = []
        penalty_notes = []
        
        # Check each diagram type
        for diagram_type, content in diagram_contents.items():
            if not content or content == "Not generated":
                missing_diagrams.append(diagram_type)
            elif "Diagram generation failed" in content or "Error reading file" in content:
                error_diagrams.append(diagram_type)
        
        # Calculate penalties
        missing_penalty = len(missing_diagrams) * 5
        error_penalty = len(error_diagrams) * 3
        total_penalty = missing_penalty + error_penalty
        
        # Get original overall score (default to 10 if not provided)
        original_score = metrics.get('overall_score', 10)
        
        # Apply penalties
        adjusted_score = max(0, original_score - total_penalty)
        
        # Create penalty notes
        if missing_diagrams:
            penalty_notes.append(f"-{missing_penalty} points: {len(missing_diagrams)} missing diagram(s) - {', '.join(missing_diagrams)}")
        if error_diagrams:
            penalty_notes.append(f"-{error_penalty} points: {len(error_diagrams)} diagram(s) with errors - {', '.join(error_diagrams)}")
        
        # Update metrics
        metrics['original_overall_score'] = original_score
        metrics['overall_score'] = adjusted_score
        metrics['penalties_applied'] = {
            'missing_diagrams': len(missing_diagrams),
            'missing_diagram_list': missing_diagrams,
            'error_diagrams': len(error_diagrams),
            'error_diagram_list': error_diagrams,
            'total_penalty': total_penalty,
            'penalty_notes': penalty_notes
        }
        
        # Add penalty explanation to gap analysis
        if penalty_notes:
            penalty_summary = " | ".join(penalty_notes)
            if 'gap_analysis' in metrics:
                metrics['gap_analysis'] = f"[PENALTIES APPLIED: {penalty_summary}] " + metrics['gap_analysis']
            else:
                metrics['gap_analysis'] = f"[PENALTIES APPLIED: {penalty_summary}]"
        
        return metrics
