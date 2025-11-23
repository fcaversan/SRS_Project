"""
Prompt Generation Module for UML Diagram Automation

This module contains all prompt generation methods for different diagram types
and validation scenarios.
"""

class PromptGenerator:
    """Handles all prompt generation for Gemini API."""
    
    @staticmethod
    def generate_base_prompt(diagram_type: str, srs_content: str, diagram_types: dict) -> str:
        """Generate the base prompt for UML diagram creation."""
        diagram_name = diagram_types.get(diagram_type, "UML Diagram")
        
        base_prompt = f"""
You are a senior software architect and UML modeling expert. You need to create a {diagram_name} in PlantUML format based on the provided Software Requirements Specification (SRS).

IMPORTANT INSTRUCTIONS:
1. Generate ONLY PlantUML code - no explanations, comments, or additional text
2. Start with @startuml and end with @enduml
3. Use proper PlantUML syntax for {diagram_type} diagrams
4. Follow UML best practices and conventions
5. Make the diagram comprehensive but readable
6. Use appropriate relationships and stereotypes
7. Include relevant details from the SRS

SRS CONTENT:
{srs_content}

Generate a complete {diagram_name} in PlantUML format:
"""
        return base_prompt
    
    @staticmethod
    def generate_structure_class_prompt(data_requirements_text: str) -> str:
        """Generate specialized prompt for Structure (Class Diagram)."""
        prompt = f"""
Task: Create a Class Diagram based on the following requirements text.

You are a senior software architect. Create a comprehensive Class Diagram in PlantUML format.

Specific Constraints:
1. Identify the Attributes (fields) and Operations (methods) for each class
2. Define the Relationships: 
   - Use --|> for inheritance
   - Use *-- for composition  
   - Use o-- for aggregation
3. Add Multiplicity (e.g., 1..*) to every relationship
4. Generate ONLY PlantUML code - no explanations

Input Text:
{data_requirements_text}

Generate PlantUML Class Diagram code:
"""
        return prompt
    
    @staticmethod
    def generate_interaction_sequence_prompt(feature_name: str, functional_requirements_text: str) -> str:
        """Generate specialized prompt for Interactions (Sequence Diagram)."""
        prompt = f"""
Task: Create a Sequence Diagram for the "{feature_name}" feature based on the text below.

You are a senior software architect. Create a detailed Sequence Diagram in PlantUML format.

Specific Constraints:
1. Use autonumber to index the steps
2. Clearly define participants: 
   - actor User
   - participant App  
   - participant API
   - database DB
3. Use alt/else blocks to handle the "Sad Paths" (errors/failures) mentioned in the text
4. Generate ONLY PlantUML code - no explanations

Input Text:
{functional_requirements_text}

Generate PlantUML Sequence Diagram code:
"""
        return prompt
    
    @staticmethod
    def generate_logic_activity_prompt(workflow_text: str) -> str:
        """Generate specialized prompt for Logic (Activity Diagram)."""
        prompt = f"""
Task: Create an Activity Diagram representing the logic flow of the text below.

You are a senior software architect. Create a comprehensive Activity Diagram in PlantUML format using MODERN PlantUML syntax.

CRITICAL SYNTAX REQUIREMENTS:
1. Start with: start
2. End with: stop
3. Use :Action description; for activities
4. Use if (condition?) then (yes/no) for decisions with proper endif
5. Use -> for flow connections
6. NO old syntax like (*) start or (*) stop
7. Example structure:
   start
   :First Action;
   if (condition?) then (yes)
     :Action if true;
   else (no)
     :Action if false;
   endif
   :Final Action;
   stop

Input Text (focus on business logic and decision flows):
{workflow_text}

Generate ONLY valid modern PlantUML Activity Diagram code:
"""
        return prompt
    
    @staticmethod
    def generate_default_validation_prompt(requirements: str, diagram_contents: dict, slice_name: str) -> str:
        """Generate the default validation prompt for diagram consistency checking with strict penalties."""
        prompt = f"""
You are a senior software architect and quality assurance expert. Your task is to validate the consistency and quality of UML diagrams generated from requirements.

Analyze the following requirements and corresponding UML diagrams for consistency, completeness, and quality:

REQUIREMENTS SLICE ({slice_name}):
{requirements}

GENERATED DIAGRAMS:

1. CLASS DIAGRAM (Structure):
{diagram_contents.get('class', 'Not generated')}

2. SEQUENCE DIAGRAM (Interactions):
{diagram_contents.get('sequence', 'Not generated')}

3. ACTIVITY DIAGRAM (Logic/Workflow):
{diagram_contents.get('activity', 'Not generated')}

VALIDATION CRITERIA:
1. Consistency: Do the diagrams contradict each other? (e.g., Sequence diagram uses classes not in Class diagram)
2. Completeness: Do the diagrams cover all requirements in the slice?
3. Quality: Are the diagrams syntactically correct and follow UML best practices?
4. Gap Analysis: What is missing or ambiguous?

**CRITICAL SCORING RULES - APPLY STRICTLY:**
- **Missing Diagram Penalty**: If ANY diagram shows "Not generated" or "Diagram generation failed", SUBTRACT 5 POINTS from the overall score for EACH missing diagram
- **Error Diagram Penalty**: If ANY diagram contains "Error reading file" or syntax errors, SUBTRACT 3 POINTS from the overall score for EACH failed diagram
- **Base Score**: Start with a base score of 10/10 and apply penalties
- **Minimum Score**: The overall score cannot go below 0

Example Scoring:
- All 3 diagrams perfect: 10/10
- 1 diagram missing: 10 - 5 = 5/10
- 2 diagrams missing: 10 - 10 = 0/10
- 1 diagram with errors: 10 - 3 = 7/10
- 1 missing + 1 with errors: 10 - 5 - 3 = 2/10

**OUTPUT FORMAT:**
Please provide your analysis in strict JSON format with the following structure:
{{
    "consistency_analysis": "Detailed analysis of consistency between diagrams...",
    "completeness_analysis": "Analysis of how well requirements are covered...",
    "quality_analysis": "Assessment of diagram quality and syntax...",
    "gap_analysis": "List of missing elements or ambiguities...",
    "consistency_score": 8,  // Integer 0-10
    "completeness_score": 9, // Integer 0-10
    "quality_score": 8,      // Integer 0-10
    "overall_score": 5,      // Integer 0-10 (APPLY PENALTIES: -5 per missing diagram, -3 per error diagram)
    "recommendations": ["List of specific recommendations for improvement..."],
    "penalties_applied": {{
        "missing_diagrams": 1,  // Count of missing diagrams
        "error_diagrams": 0,    // Count of diagrams with errors
        "total_penalty": 5      // Total points deducted
    }}
}}

**IMPORTANT**: You MUST apply the penalty rules strictly. Check each diagram content for "Not generated", "Diagram generation failed", or "Error reading file" and calculate penalties accordingly.

Ensure the output is valid JSON. Do not include markdown formatting (like ```json) around the output.
"""
        return prompt
    
    @staticmethod
    def generate_design_reviewer_prompt(requirements: str, current_puml: str, qa_metrics: dict, diagram_type: str, iteration_num: int) -> str:
        """Generate a prompt for the Design Reviewer agent to improve diagrams based on QA feedback."""
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
