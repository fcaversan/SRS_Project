#!/usr/bin/env python3
"""
UML Diagram Generation Automation Script with Google Gemini 2.5 Pro

This script automates UML diagram generation using PlantUML:
- Use Case Diagrams: System functionality from user perspective
- Class Diagrams: System structure and relationships
- Sequence Diagrams: Interaction flows between objects
- Activity Diagrams: Workflow and business processes
- Component Diagrams: System architecture components
- State Diagrams: Object state transitions
- Deployment Diagrams: Physical system deployment
"""

import os
import sys
import datetime
import subprocess
import google.generativeai as genai
from typing import Optional, Dict, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class UMLDiagramAutomation:
    """Class to handle UML diagram generation workflows with Google Gemini API and PlantUML."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the UMLDiagramAutomation class.
        
        Args:
            api_key (str, optional): Google AI API key. If not provided, 
                                   will look for GOOGLE_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        self.model = None
        self.plantuml_jar_path = "plantuml/plantuml.jar"
        self.diagrams_dir = "uml_diagrams"
        
        # Supported diagram types
        self.diagram_types = {
            'usecase': 'Use Case Diagram',
            'class': 'Class Diagram', 
            'sequence': 'Sequence Diagram',
            'activity': 'Activity Diagram',
            'component': 'Component Diagram',
            'state': 'State Diagram',
            'deployment': 'Deployment Diagram',
            'object': 'Object Diagram',
            'communication': 'Communication Diagram',
            'timing': 'Timing Diagram'
        }
        
        if not self.api_key:
            raise ValueError("API key is required. Set GOOGLE_API_KEY environment variable or pass it directly.")
    
    def setup_gemini(self):
        """Configure and initialize the Gemini model."""
        try:
            # Configure the API key
            genai.configure(api_key=self.api_key)
            
            # Initialize the Gemini 2.5 Pro model
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            print("Gemini 2.5 Pro model initialized successfully!")
            
        except Exception as e:
            raise Exception(f"Failed to initialize Gemini model: {e}")
    
    def setup_directories(self):
        """Create necessary directories for UML diagrams."""
        try:
            if not os.path.exists(self.diagrams_dir):
                os.makedirs(self.diagrams_dir)
                print(f"Created directory: {self.diagrams_dir}")
            
            # Create subdirectories for each diagram type
            for diagram_type in self.diagram_types.keys():
                type_dir = os.path.join(self.diagrams_dir, diagram_type)
                if not os.path.exists(type_dir):
                    os.makedirs(type_dir)
                    print(f"Created directory: {type_dir}")
                    
        except Exception as e:
            raise Exception(f"Failed to setup directories: {e}")
    
    def verify_plantuml_installation(self):
        """Verify that PlantUML is installed and accessible."""
        try:
            if not os.path.exists(self.plantuml_jar_path):
                raise FileNotFoundError(f"PlantUML JAR not found at: {self.plantuml_jar_path}")
            
            # Test PlantUML installation
            result = subprocess.run(
                ["java", "-jar", self.plantuml_jar_path, "-version"],
                capture_output=True,
                text=True,
                check=True
            )
            
            print("PlantUML installation verified successfully!")
            return True
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"PlantUML test failed: {e}")
        except Exception as e:
            raise Exception(f"Failed to verify PlantUML: {e}")
    
    def send_prompt(self, prompt: str) -> str:
        """
        Send a prompt to Gemini and return the response.
        
        Args:
            prompt (str): The prompt to send to Gemini
            
        Returns:
            str: Gemini's response
        """
        if not self.model:
            raise Exception("Gemini model not initialized. Call setup_gemini() first.")
        
        try:
            print(f"Sending prompt to Gemini...")
            response = self.model.generate_content(prompt)
            
            if response.text:
                print("Response received successfully!")
                return response.text
            else:
                raise Exception("No response text received from Gemini")
                
        except Exception as e:
            raise Exception(f"Failed to send prompt to Gemini: {e}")
    
    def read_srs_file(self, srs_path: str) -> str:
        """
        Read content from an SRS file.
        
        Args:
            srs_path (str): Path to the SRS file
            
        Returns:
            str: Content of the SRS file
        """
        try:
            if not os.path.exists(srs_path):
                raise FileNotFoundError(f"SRS file not found: {srs_path}")
            
            print(f"Reading SRS file: {srs_path}")
            
            with open(srs_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            print(f"Successfully read SRS file ({len(content)} characters)")
            return content
            
        except Exception as e:
            raise Exception(f"Failed to read SRS file: {e}")
    
    def generate_base_prompt(self, diagram_type: str, srs_content: str) -> str:
        """
        Generate the base prompt for UML diagram creation.
        
        Args:
            diagram_type (str): Type of UML diagram to generate
            srs_content (str): Content from the SRS document
            
        Returns:
            str: Base prompt for diagram generation
        """
        diagram_name = self.diagram_types.get(diagram_type, "UML Diagram")
        
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
    
    def generate_structure_class_prompt(self, data_requirements_text: str) -> str:
        """
        Generate specialized prompt for Structure (Class Diagram) based on Data Requirements/Entities.
        
        Args:
            data_requirements_text (str): Text containing data requirements or entities
            
        Returns:
            str: Specialized class diagram prompt
        """
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
    
    def generate_interaction_sequence_prompt(self, feature_name: str, functional_requirements_text: str) -> str:
        """
        Generate specialized prompt for Interactions (Sequence Diagram) based on Functional Requirements.
        
        Args:
            feature_name (str): Name of the feature to model
            functional_requirements_text (str): Text containing functional requirements
            
        Returns:
            str: Specialized sequence diagram prompt
        """
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
    
    def generate_logic_activity_prompt(self, workflow_text: str) -> str:
        """
        Generate specialized prompt for Logic (Activity Diagram) for complex workflows with decisions.
        
        Args:
            workflow_text (str): Text containing workflow logic and decision points
            
        Returns:
            str: Specialized activity diagram prompt
        """
        prompt = f"""
Task: Create an Activity Diagram representing the logic flow of the text below.

You are a senior software architect. Create a comprehensive Activity Diagram in PlantUML format.

Specific Constraints:
1. Use the new PlantUML syntax:
   - Start with start
   - Stop with stop  
   - Use :Action; for activities
2. Use if (condition) then (yes) structures for all logic branches
3. Ensure there is a "Merge Node" where the branches come back together
4. Generate ONLY PlantUML code - no explanations

Input Text:
{workflow_text}

Generate PlantUML Activity Diagram code:
"""
        return prompt
    
    def save_puml_file(self, diagram_type: str, puml_content: str, filename: str = None) -> str:
        """
        Save PlantUML content to a .puml file.
        
        Args:
            diagram_type (str): Type of diagram
            puml_content (str): PlantUML code content
            filename (str, optional): Custom filename. If not provided, uses timestamp.
            
        Returns:
            str: Path to the saved file
        """
        try:
            if not filename:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{diagram_type}_{timestamp}.puml"
            elif not filename.endswith('.puml'):
                filename += '.puml'
            
            file_path = os.path.join(self.diagrams_dir, diagram_type, filename)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(puml_content)
            
            print(f"PlantUML file saved: {file_path}")
            return file_path
            
        except Exception as e:
            raise Exception(f"Failed to save PlantUML file: {e}")
    
    def generate_image_from_puml(self, puml_file_path: str) -> str:
        """
        Generate an image from a PlantUML file.
        
        Args:
            puml_file_path (str): Path to the .puml file
            
        Returns:
            str: Path to the generated image file
        """
        try:
            if not os.path.exists(puml_file_path):
                raise FileNotFoundError(f"PlantUML file not found: {puml_file_path}")
            
            print(f"Generating image from: {puml_file_path}")
            
            # Run PlantUML to generate image
            result = subprocess.run(
                ["java", "-jar", self.plantuml_jar_path, puml_file_path],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Determine output image path
            base_path = puml_file_path.replace('.puml', '.png')
            
            if os.path.exists(base_path):
                print(f"Image generated successfully: {base_path}")
                return base_path
            else:
                raise Exception("Image file was not generated")
                
        except subprocess.CalledProcessError as e:
            raise Exception(f"PlantUML image generation failed: {e}")
        except Exception as e:
            raise Exception(f"Failed to generate image: {e}")
    
    def generate_diagram(self, diagram_type: str, srs_content: str, custom_prompt: str = None, filename: str = None) -> Dict[str, str]:
        """
        Generate a complete UML diagram (PUML file + image).
        
        Args:
            diagram_type (str): Type of diagram to generate
            srs_content (str): SRS content
            custom_prompt (str, optional): Custom prompt additions
            filename (str, optional): Custom filename
            
        Returns:
            Dict[str, str]: Paths to generated files {'puml': path, 'image': path}
        """
        try:
            if diagram_type not in self.diagram_types:
                raise ValueError(f"Unsupported diagram type: {diagram_type}")
            
            # Generate prompt
            if custom_prompt:
                prompt = custom_prompt.replace("{srs_content}", srs_content)
            else:
                prompt = self.generate_base_prompt(diagram_type, srs_content)
            
            # Get PlantUML code from Gemini
            puml_content = self.send_prompt(prompt)
            
            # Clean up the response to extract only PlantUML code
            puml_content = self.extract_plantuml_code(puml_content)
            
            # Save PUML file
            puml_path = self.save_puml_file(diagram_type, puml_content, filename)
            
            # Generate image
            image_path = self.generate_image_from_puml(puml_path)
            
            return {
                'puml': puml_path,
                'image': image_path,
                'type': self.diagram_types[diagram_type]
            }
            
        except Exception as e:
            raise Exception(f"Failed to generate {diagram_type} diagram: {e}")
    
    def extract_plantuml_code(self, response: str) -> str:
        """
        Extract PlantUML code from Gemini response.
        
        Args:
            response (str): Raw response from Gemini
            
        Returns:
            str: Cleaned PlantUML code
        """
        try:
            # Look for @startuml and @enduml markers
            start_marker = "@startuml"
            end_marker = "@enduml"
            
            start_index = response.find(start_marker)
            end_index = response.find(end_marker)
            
            if start_index != -1 and end_index != -1:
                # Extract content between markers (inclusive)
                puml_content = response[start_index:end_index + len(end_marker)]
                return puml_content.strip()
            else:
                # If markers not found, try to clean the response
                lines = response.strip().split('\n')
                cleaned_lines = []
                
                for line in lines:
                    # Skip markdown code block markers
                    if line.strip().startswith('```'):
                        continue
                    cleaned_lines.append(line)
                
                cleaned_content = '\n'.join(cleaned_lines).strip()
                
                # Add markers if missing
                if not cleaned_content.startswith('@startuml'):
                    cleaned_content = '@startuml\n' + cleaned_content
                if not cleaned_content.endswith('@enduml'):
                    cleaned_content = cleaned_content + '\n@enduml'
                
                return cleaned_content
                
        except Exception as e:
            raise Exception(f"Failed to extract PlantUML code: {e}")
    
    def list_generated_diagrams(self) -> Dict[str, List[str]]:
        """
        List all generated diagrams by type.
        
        Returns:
            Dict[str, List[str]]: Dictionary mapping diagram types to file lists
        """
        diagrams = {}
        
        try:
            for diagram_type in self.diagram_types.keys():
                type_dir = os.path.join(self.diagrams_dir, diagram_type)
                if os.path.exists(type_dir):
                    files = [f for f in os.listdir(type_dir) if f.endswith(('.puml', '.png'))]
                    diagrams[diagram_type] = sorted(files)
                else:
                    diagrams[diagram_type] = []
            
            return diagrams
            
        except Exception as e:
            raise Exception(f"Failed to list diagrams: {e}")
    
    def generate_all_diagrams(self, srs_content: str, selected_types: List[str] = None) -> Dict[str, Dict[str, str]]:
        """
        Generate all UML diagrams for the SRS.
        
        Args:
            srs_content (str): SRS content
            selected_types (List[str], optional): Specific diagram types to generate
            
        Returns:
            Dict[str, Dict[str, str]]: Results for each diagram type
        """
        if not selected_types:
            selected_types = list(self.diagram_types.keys())
        
        results = {}
        
        for diagram_type in selected_types:
            try:
                print(f"\n=== Generating {self.diagram_types[diagram_type]} ===")
                result = self.generate_diagram(diagram_type, srs_content)
                results[diagram_type] = result
                print(f"✅ {self.diagram_types[diagram_type]} completed successfully!")
                
            except Exception as e:
                print(f"❌ Failed to generate {self.diagram_types[diagram_type]}: {e}")
                results[diagram_type] = {'error': str(e)}
        
        return results
    
    def generate_structure_diagram(self, data_requirements_text: str, filename: str = None) -> Dict[str, str]:
        """
        Generate a Structure (Class) Diagram based on Data Requirements/Entities.
        
        Args:
            data_requirements_text (str): Text containing data requirements or entities
            filename (str, optional): Custom filename
            
        Returns:
            Dict[str, str]: Paths to generated files
        """
        try:
            prompt = self.generate_structure_class_prompt(data_requirements_text)
            
            # Get PlantUML code from Gemini
            puml_content = self.send_prompt(prompt)
            
            # Clean up the response
            puml_content = self.extract_plantuml_code(puml_content)
            
            # Save PUML file
            if not filename:
                filename = "structure_class_diagram"
            puml_path = self.save_puml_file("class", puml_content, filename)
            
            # Generate image
            image_path = self.generate_image_from_puml(puml_path)
            
            return {
                'puml': puml_path,
                'image': image_path,
                'type': 'Structure (Class Diagram)'
            }
            
        except Exception as e:
            raise Exception(f"Failed to generate structure diagram: {e}")
    
    def generate_interaction_diagram(self, feature_name: str, functional_requirements_text: str, filename: str = None) -> Dict[str, str]:
        """
        Generate an Interaction (Sequence) Diagram based on Functional Requirements.
        
        Args:
            feature_name (str): Name of the feature to model
            functional_requirements_text (str): Text containing functional requirements
            filename (str, optional): Custom filename
            
        Returns:
            Dict[str, str]: Paths to generated files
        """
        try:
            prompt = self.generate_interaction_sequence_prompt(feature_name, functional_requirements_text)
            
            # Get PlantUML code from Gemini
            puml_content = self.send_prompt(prompt)
            
            # Clean up the response
            puml_content = self.extract_plantuml_code(puml_content)
            
            # Save PUML file
            if not filename:
                filename = f"interaction_{feature_name.lower().replace(' ', '_')}_sequence"
            puml_path = self.save_puml_file("sequence", puml_content, filename)
            
            # Generate image
            image_path = self.generate_image_from_puml(puml_path)
            
            return {
                'puml': puml_path,
                'image': image_path,
                'type': f'Interaction ({feature_name} Sequence Diagram)'
            }
            
        except Exception as e:
            raise Exception(f"Failed to generate interaction diagram for {feature_name}: {e}")
    
    def generate_logic_diagram(self, workflow_text: str, workflow_name: str = "Logic Flow", filename: str = None) -> Dict[str, str]:
        """
        Generate a Logic (Activity) Diagram for complex workflows with decisions.
        
        Args:
            workflow_text (str): Text containing workflow logic and decision points
            workflow_name (str): Name of the workflow for documentation
            filename (str, optional): Custom filename
            
        Returns:
            Dict[str, str]: Paths to generated files
        """
        try:
            prompt = self.generate_logic_activity_prompt(workflow_text)
            
            # Get PlantUML code from Gemini
            puml_content = self.send_prompt(prompt)
            
            # Clean up the response
            puml_content = self.extract_plantuml_code(puml_content)
            
            # Save PUML file
            if not filename:
                filename = f"logic_{workflow_name.lower().replace(' ', '_')}_activity"
            puml_path = self.save_puml_file("activity", puml_content, filename)
            
            # Generate image
            image_path = self.generate_image_from_puml(puml_path)
            
            return {
                'puml': puml_path,
                'image': image_path,
                'type': f'Logic ({workflow_name} Activity Diagram)'
            }
            
        except Exception as e:
            raise Exception(f"Failed to generate logic diagram for {workflow_name}: {e}")
    
    def generate_comprehensive_design_set(self, srs_content: str) -> Dict[str, Dict[str, str]]:
        """
        Generate a comprehensive set of design diagrams from SRS sections.
        
        Args:
            srs_content (str): Complete SRS content
            
        Returns:
            Dict[str, Dict[str, str]]: Results for each diagram generated
        """
        results = {}
        
        try:
            # Extract sections for specialized diagrams
            # Note: These would need to be customized based on actual SRS structure
            print("🔍 Analyzing SRS content for diagram generation...")
            
            # Structure Diagram - Data Requirements section
            if "3.6 Data Requirements" in srs_content:
                data_section_start = srs_content.find("3.6 Data Requirements")
                data_section_end = srs_content.find("**4.", data_section_start)
                if data_section_end == -1:
                    data_section_end = len(srs_content)
                data_requirements = srs_content[data_section_start:data_section_end]
                
                print("\n=== Generating Structure (Class) Diagram ===")
                structure_result = self.generate_structure_diagram(
                    data_requirements, 
                    "electric_car_app_structure"
                )
                results['structure'] = structure_result
                print(f"✅ Structure diagram completed!")
            
            # Interaction Diagrams - Key functional requirements
            functional_features = [
                ("Vehicle Monitoring", "VM-1"),
                ("Charging Management", "CM-1"),
                ("Vehicle Control", "VC-1"),
                ("Trip Planning", "TP-1")
            ]
            
            for feature_name, feature_code in functional_features:
                if feature_code in srs_content:
                    print(f"\n=== Generating Interaction Diagram: {feature_name} ===")
                    
                    # Extract feature section
                    feature_start = srs_content.find(feature_code)
                    feature_end = srs_content.find("\n    *", feature_start + 100)  # Next major section
                    if feature_end == -1:
                        feature_end = feature_start + 2000  # Reasonable default
                    
                    feature_text = srs_content[feature_start:feature_end]
                    
                    interaction_result = self.generate_interaction_diagram(
                        feature_name, 
                        feature_text,
                        f"interaction_{feature_name.lower().replace(' ', '_')}"
                    )
                    results[f'interaction_{feature_name.lower().replace(" ", "_")}'] = interaction_result
                    print(f"✅ {feature_name} interaction diagram completed!")
            
            # Logic Diagram - Error handling and complex workflows
            if "Error Handling" in srs_content:
                error_start = srs_content.find("Error Handling")
                error_end = srs_content.find("**", error_start + 100)
                if error_end == -1:
                    error_end = error_start + 1000
                
                error_text = srs_content[error_start:error_end]
                
                print("\n=== Generating Logic (Activity) Diagram: Error Handling ===")
                logic_result = self.generate_logic_diagram(
                    error_text, 
                    "Error Handling Workflow",
                    "logic_error_handling"
                )
                results['logic_error_handling'] = logic_result
                print(f"✅ Error handling logic diagram completed!")
            
            print(f"\n🎉 Comprehensive design set generation completed!")
            print(f"Generated {len(results)} specialized diagrams")
            
        except Exception as e:
            print(f"❌ Error during comprehensive generation: {e}")
            results['error'] = {'error': str(e)}
        
        return results


def main():
    """Main function to demonstrate UML diagram automation."""
    try:
        print("=== UML Diagram Generation Automation ===")
        
        # Initialize automation
        uml_automation = UMLDiagramAutomation()
        
        # Setup
        uml_automation.setup_gemini()
        uml_automation.setup_directories()
        uml_automation.verify_plantuml_installation()
        
        print("\nUML Diagram Automation is ready!")
        print(f"Supported diagram types: {list(uml_automation.diagram_types.keys())}")
        print(f"Diagrams will be saved to: {uml_automation.diagrams_dir}")
        
        # Example usage (uncomment to test)
        # srs_content = uml_automation.read_srs_file("SRS_v5.txt")
        # result = uml_automation.generate_diagram("usecase", srs_content)
        # print(f"Generated: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()