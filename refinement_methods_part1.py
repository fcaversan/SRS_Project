# Refinement Loop Methods for p2_design_agent.py
# Add these methods to the UMLDiagramAutomation class

import os

def generate_design_reviewer_prompt(self, requirements: str, current_puml: str, qa_metrics: Dict, diagram_type: str, iteration_num: int) -> str:
    """
    Generate a prompt for the Design Reviewer agent to improve diagrams based on QA feedback.
    
    Args:
        requirements (str): Original requirements
        current_puml (str): Current PlantUML code
        qa_metrics (Dict): QA validation metrics with scores and recommendations
        diagram_type (str): Type of diagram (class, sequence, activity)
        iteration_num (int): Current iteration number
        
    Returns:
        str: Design reviewer prompt
    """
    diagram_name = diagram_type.capitalize()
    
    prompt = f"""
You are a senior UML architect and design improvement specialist. Your task is to IMPROVE an existing {diagram_name} Diagram based on QA validation feedback.

ITERATION: {iteration_num}

ORIGINAL REQUIREMENTS:
{requirements}

CURRENT {diagram_name.upper()} DIAGRAM (PlantUML):
{current_puml}

QA VALIDATION RESULTS:
- Overall Score: {qa_metrics.get('overall_score', 'N/A')}/10
- Consistency Score: {qa_metrics.get('consistency_score', 'N/A')}/10
- Completeness Score: {qa_metrics.get('completeness_score', 'N/A')}/10
- Quality Score: {qa_metrics.get('quality_score', 'N/A')}/10

CONSISTENCY ANALYSIS:
{qa_metrics.get('consistency_analysis', 'No analysis provided')}

COMPLETENESS ANALYSIS:
{qa_metrics.get('completeness_analysis', 'No analysis provided')}

QUALITY ANALYSIS:
{qa_metrics.get('quality_analysis', 'No analysis provided')}

IDENTIFIED GAPS:
{qa_metrics.get('gap_analysis', 'No gaps identified')}

RECOMMENDATIONS FOR IMPROVEMENT:
"""
    recommendations = qa_metrics.get('recommendations', [])
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            prompt += f"{i}. {rec}\n"
    else:
        prompt += "No specific recommendations provided.\n"
    
    prompt += f"""

TASK: Generate an IMPROVED {diagram_name} Diagram that addresses the QA feedback above.

CRITICAL REQUIREMENTS:
1. Address ALL identified gaps and recommendations
2. Maintain consistency with the original requirements
3. Improve completeness by covering all requirement aspects
4. Enhance quality by following UML best practices
5. Keep the diagram readable and well-structured

IMPORTANT INSTRUCTIONS:
- Generate ONLY PlantUML code - no explanations, comments, or additional text
- Start with @startuml and end with @enduml
- Use proper PlantUML syntax for {diagram_type} diagrams
- Make meaningful improvements, don't just copy the current diagram

Generate the improved {diagram_name} Diagram now:
"""
    return prompt

def refine_diagram_with_feedback(self, diagram_type: str, requirements: str, current_diagram_info: Dict, qa_metrics: Dict, slice_name: str, iteration_num: int) -> Dict[str, str]:
    """
    Refine a single diagram based on QA feedback.
    
    Args:
        diagram_type (str): Type of diagram (class, sequence, activity)
        requirements (str): Original requirements
        current_diagram_info (Dict): Current diagram info with puml path
        qa_metrics (Dict): QA validation metrics
        slice_name (str): Name of the requirements slice
        iteration_num (int): Current iteration number (for versioning)
        
    Returns:
        Dict: New diagram info with paths to refined files
    """
    try:
        # Read current PlantUML
        current_puml_path = current_diagram_info.get('puml')
        if not current_puml_path or not os.path.exists(current_puml_path):
            raise Exception(f"Current PlantUML file not found: {current_puml_path}")
        
        with open(current_puml_path, 'r', encoding='utf-8') as f:
            current_puml = f.read()
        
        print(f"  🔄 Refining {diagram_type} diagram (iteration {iteration_num})...")
        
        # Generate Design Reviewer prompt
        reviewer_prompt = self.generate_design_reviewer_prompt(
            requirements, current_puml, qa_metrics, diagram_type, iteration_num
        )
        
        # Get improved PlantUML from Gemini
        improved_puml = self.send_prompt(reviewer_prompt)
        improved_puml = self.extract_plantuml_code(improved_puml)
        
        # Save with version number
        version_suffix = f"_v{iteration_num}"
        filename = f"{slice_name}{version_suffix}_{diagram_type}_diagram"
        puml_path = self.save_puml_file(diagram_type, improved_puml, filename)
        
        # Generate image
        image_path = self.generate_image_from_puml(puml_path)
        
        print(f"  ✅ Refined {diagram_type} diagram saved: {puml_path}")
        
        return {
            'puml': puml_path,
            'image': image_path,
            'type': f'{diagram_type.capitalize()} Diagram (v{iteration_num})',
            'version': f'v{iteration_num}'
        }
        
    except Exception as e:
        print(f"  ❌ Failed to refine {diagram_type} diagram: {e}")
        return {'error': str(e), 'version': f'v{iteration_num}'}

def save_iteration_qa_report(self, validation_result: Dict, slice_name: str, iteration_num: int) -> str:
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
        
        report_content = f"""# QA Validation Report - Iteration {iteration_num}
**Slice:** {slice_name}
**Version:** v{iteration_num}
**Timestamp:** {timestamp}

## Validation Scores
- **Overall Score:** {metrics.get('overall_score', 'N/A')}/10
- **Consistency Score:** {metrics.get('consistency_score', 'N/A')}/10
- **Completeness Score:** {metrics.get('completeness_score', 'N/A')}/10
- **Quality Score:** {metrics.get('quality_score', 'N/A')}/10

## Detailed Analysis

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

# Continue in next file...
