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
    def _format_scope_violations(violations: List[str]) -> str:
        """Format scope violations for QA report."""
        if not violations or (len(violations) == 1 and not violations[0]):
            return "**Scope Violations:** None detected ✅"
        
        result = "**⚠️ SCOPE VIOLATIONS DETECTED:**\n"
        for violation in violations:
            if violation:  # Skip empty strings
                result += f"- {violation}\n"
        return result
    
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

    @staticmethod
    def save_iteration_qa_report(validation_result: Dict, slice_name: str, iteration_num: int) -> str:
        """
        Save individual QA report for a specific iteration.
        
        Args:
            validation_result (Dict): Validation results with metrics
            slice_name (str): Name of the requirements slice
            iteration_num (int): Iteration number
            
        Returns:
            str: Path to saved report file
        """
        try:
            metrics = validation_result.get('metrics', {})
            timestamp = validation_result.get('timestamp', 'Unknown')
            
            # Include penalty information if available
            penalty_info = ""
            if 'penalties_applied' in metrics:
                penalties = metrics['penalties_applied']
                if penalties.get('total_penalty', 0) > 0:
                    penalty_info = f"""

## Penalty System Applied
- **Original Score:** {metrics.get('original_overall_score', 'N/A')}/10
- **Penalties Applied:** -{penalties.get('total_penalty', 0)} points
- **Final Score:** {metrics.get('overall_score', 'N/A')}/10

### Penalty Breakdown:
"""
                    for note in penalties.get('penalty_notes', []):
                        penalty_info += f"- {note}\n"
            
            report_content = f"""# QA Validation Report - Iteration {iteration_num}
**Slice:** {slice_name}
**Version:** v{iteration_num}
**Timestamp:** {timestamp}

## Validation Scores
- **Overall Score:** {metrics.get('overall_score', 'N/A')}/10
- **Scope Adherence Score:** {metrics.get('scope_adherence_score', 'N/A')}/10
- **Consistency Score:** {metrics.get('consistency_score', 'N/A')}/10
- **Completeness Score:** {metrics.get('completeness_score', 'N/A')}/10
- **Quality Score:** {metrics.get('quality_score', 'N/A')}/10{penalty_info}

## Detailed Analysis

### Scope Adherence Analysis
{metrics.get('scope_adherence_analysis', 'No scope analysis provided')}

{ValidationHandler._format_scope_violations(metrics.get('scope_violations', []))}

### Consistency Analysis
{metrics.get('consistency_analysis', 'No analysis provided')}

### Completeness Analysis
{metrics.get('completeness_analysis', 'No analysis provided')}

### Quality Analysis
{metrics.get('quality_analysis', 'No analysis provided')}

### Gap Analysis
{metrics.get('gap_analysis', 'No gaps identified')}

## Recommendations
"""
            recommendations = metrics.get('recommendations', [])
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    report_content += f"{i}. {rec}\n"
            else:
                report_content += "No specific recommendations provided.\n"
            
            # Save report
            reports_dir = "reports"
            os.makedirs(reports_dir, exist_ok=True)
            
            report_filename = f"qa_report_{slice_name}_v{iteration_num}.md"
            report_path = os.path.join(reports_dir, report_filename)
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            print(f"  📄 QA report saved: {report_path}")
            return report_path
            
        except Exception as e:
            print(f"  ❌ Failed to save QA report: {e}")
            return None
