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
    
    def validate_plantuml_syntax(self, puml_path: str) -> tuple[bool, str]:
        """
        Validate PlantUML syntax without generating image.
        
        Args:
            puml_path (str): Path to the .puml file
            
        Returns:
            tuple[bool, str]: (is_valid, error_message)
        """
        try:
            # Read the file and do basic syntax validation
            with open(puml_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic syntax checks
            if not content.strip():
                return False, "Empty PlantUML file"
            
            if not content.strip().startswith('@startuml'):
                return False, "Missing @startuml directive"
            
            if not content.strip().endswith('@enduml'):
                return False, "Missing @enduml directive"
            
            # Try to generate image with timeout to catch syntax errors
            result = subprocess.run(
                ['java', '-jar', self.plantuml_jar_path, '-timeout', '10', puml_path],
                capture_output=True,
                text=True,
                timeout=15,  # 15 second timeout
                cwd=os.getcwd()
            )
            
            if result.returncode != 0:
                # Extract meaningful error from output
                error_output = result.stderr or result.stdout or "Unknown syntax error"
                return False, error_output
            
            return True, "Syntax valid"
            
        except subprocess.TimeoutExpired:
            return False, "PlantUML syntax validation timed out"
        except Exception as e:
            return False, f"Syntax validation failed: {e}"
    
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
            
            # Run PlantUML to generate image with timeout
            result = subprocess.run(
                ["java", "-jar", self.plantuml_jar_path, puml_file_path],
                capture_output=True,
                text=True,
                timeout=30,  # 30 second timeout
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
    
    def generate_diagrams_from_requirements_slice(self, requirements_slice: str, slice_name: str = "RequirementSlice", custom_validation_prompt: str = None) -> Dict[str, any]:
        """
        Generate the core 3 diagrams (Class, Sequence, Activity) from a requirements slice and validate consistency.
        
        Args:
            requirements_slice (str): Slice of requirements to process
            slice_name (str): Name identifier for this slice
            custom_validation_prompt (str, optional): Custom prompt for validation phase
            
        Returns:
            Dict containing diagram results and validation report
        """
        print(f"🚀 Starting iterative design generation for: {slice_name}")
        
        iteration_results = {
            'slice_name': slice_name,
            'diagrams': {},
            'validation': None,
            'timestamp': datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        }
        
        try:
            # =================================================================
            # PHASE 1: Generate the 3 Core Diagrams
            # =================================================================
            
            print(f"\n📊 Generating Class Diagram for {slice_name}...")
            try:
                class_result = self.generate_structure_diagram(
                    requirements_slice,
                    f"{slice_name}_class_diagram"
                )
                iteration_results['diagrams']['class'] = class_result
                print(f"✅ Class Diagram: {class_result['image']}")
            except Exception as e:
                print(f"❌ Class Diagram failed: {e}")
                iteration_results['diagrams']['class'] = {'error': str(e)}
                print(f"🛑 Stopping iteration due to Class Diagram failure")
                return iteration_results
            
            print(f"\n🔄 Generating Sequence Diagram for {slice_name}...")
            try:
                sequence_result = self.generate_interaction_diagram(
                    f"{slice_name} Main Flow",
                    requirements_slice,
                    f"{slice_name}_sequence_diagram"
                )
                iteration_results['diagrams']['sequence'] = sequence_result
                print(f"✅ Sequence Diagram: {sequence_result['image']}")
            except Exception as e:
                print(f"❌ Sequence Diagram failed: {e}")
                iteration_results['diagrams']['sequence'] = {'error': str(e)}
                print(f"🛑 Stopping iteration due to Sequence Diagram failure")
                return iteration_results
            
            print(f"\n⚡ Generating Activity Diagram for {slice_name}...")
            try:
                activity_result = self.generate_logic_diagram(
                    requirements_slice,
                    f"{slice_name} Business Logic",
                    f"{slice_name}_activity_diagram"
                )
                iteration_results['diagrams']['activity'] = activity_result
                print(f"✅ Activity Diagram: {activity_result['image']}")
            except Exception as e:
                print(f"❌ Activity Diagram failed: {e}")
                iteration_results['diagrams']['activity'] = {'error': str(e)}
                print(f"🛑 Stopping iteration due to Activity Diagram failure")
                return iteration_results
            
            # =================================================================
            # PHASE 2: Validation - Check Consistency Between Diagrams
            # =================================================================
            
            # Only validate if all diagrams generated successfully
            successful_diagrams = [d for d in iteration_results['diagrams'].values() if 'error' not in d]
            if len(successful_diagrams) == 3:
                print(f"\n🔍 Validating diagram consistency for {slice_name}...")
                try:
                    validation_result = self.validate_diagram_consistency(
                        requirements_slice,
                        iteration_results['diagrams'],
                        slice_name,
                        custom_validation_prompt
                    )
                    iteration_results['validation'] = validation_result
                    print(f"✅ Validation completed: {validation_result['summary']}")
                except Exception as e:
                    print(f"❌ Validation failed: {e}")
                    iteration_results['validation'] = {'error': str(e)}
            else:
                print(f"\n⚠️  Skipping validation - only {len(successful_diagrams)}/3 diagrams succeeded")
                iteration_results['validation'] = {
                    'skipped': True,
                    'reason': f"Only {len(successful_diagrams)}/3 diagrams generated successfully"
                }
            
            # =================================================================
            # PHASE 3: Save Iteration Report
            # =================================================================
            
            report_path = self.save_iteration_report(iteration_results)
            iteration_results['report_path'] = report_path
            
            print(f"\n🎉 Iteration completed for {slice_name}!")
            print(f"📄 Report saved: {report_path}")
            
        except Exception as e:
            print(f"❌ Iteration failed for {slice_name}: {e}")
            iteration_results['error'] = str(e)
        
        return iteration_results
    
    def validate_diagram_consistency(self, requirements_slice: str, diagrams: Dict[str, Dict], slice_name: str, custom_validation_prompt: str = None) -> Dict[str, any]:
        """
        Validate the consistency between the three generated diagrams and the requirements.
        
        Args:
            requirements_slice (str): Original requirements
            diagrams (Dict): Generated diagram information
            slice_name (str): Name of the requirements slice
            custom_validation_prompt (str, optional): Custom validation prompt
            
        Returns:
            Dict containing validation results and consistency report
        """
        try:
            # Read the generated PlantUML files
            diagram_contents = {}
            
            for diagram_type, diagram_info in diagrams.items():
                if 'puml' in diagram_info and 'error' not in diagram_info:
                    try:
                        with open(diagram_info['puml'], 'r', encoding='utf-8') as f:
                            diagram_contents[diagram_type] = f.read()
                    except Exception as e:
                        diagram_contents[diagram_type] = f"Error reading file: {e}"
                else:
                    diagram_contents[diagram_type] = "Diagram generation failed"
            
            # Generate validation prompt
            if custom_validation_prompt:
                validation_prompt = custom_validation_prompt.format(
                    requirements=requirements_slice,
                    class_diagram=diagram_contents.get('class', 'Not generated'),
                    sequence_diagram=diagram_contents.get('sequence', 'Not generated'),
                    activity_diagram=diagram_contents.get('activity', 'Not generated'),
                    slice_name=slice_name
                )
            else:
                validation_prompt = self.generate_default_validation_prompt(
                    requirements_slice, diagram_contents, slice_name
                )
            
            # Get validation report from Gemini
            validation_report = self.send_prompt(validation_prompt)
            
            # Extract consistency score if present
            consistency_score = self.extract_consistency_score(validation_report)
            
            validation_result = {
                'report': validation_report,
                'consistency_score': consistency_score,
                'diagrams_validated': list(diagram_contents.keys()),
                'summary': f"Consistency analysis completed for {len(diagram_contents)} diagrams",
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            return validation_result
            
        except Exception as e:
            raise Exception(f"Validation failed: {e}")
    
    def generate_default_validation_prompt(self, requirements: str, diagram_contents: Dict[str, str], slice_name: str) -> str:
        """
        Generate the default validation prompt for diagram consistency checking.
        
        Args:
            requirements (str): Original requirements slice
            diagram_contents (Dict): PlantUML content for each diagram type
            slice_name (str): Name of the requirements slice
            
        Returns:
            str: Validation prompt for Gemini
        """
        prompt = f"""
You are a senior software architect and quality assurance expert. Your task is to validate the consistency and quality of UML diagrams generated from requirements.

Analyze the following requirements and corresponding UML diagrams for consistency, completeness, and quality:

**REQUIREMENTS SLICE: {slice_name}**
{requirements}

**GENERATED DIAGRAMS:**

**Class Diagram (PlantUML):**
{diagram_contents.get('class', 'Not generated')}

**Sequence Diagram (PlantUML):**
{diagram_contents.get('sequence', 'Not generated')}

**Activity Diagram (PlantUML):**
{diagram_contents.get('activity', 'Not generated')}

**VALIDATION CRITERIA:**

1. **Consistency Analysis:**
   - Do the class names in the Class Diagram match those used in the Sequence Diagram?
   - Are the operations/methods defined in classes actually used in the sequence flows?
   - Do the activities in the Activity Diagram correspond to the interactions in the Sequence Diagram?
   - Are the data flows consistent across all three diagrams?

2. **Completeness Analysis:**
   - Are all entities mentioned in the requirements represented in the Class Diagram?
   - Are all user interactions from requirements covered in the Sequence Diagram?
   - Are all business logic flows from requirements represented in the Activity Diagram?
   - Are there missing relationships or dependencies?

3. **Quality Analysis:**
   - Are the diagrams following UML best practices?
   - Are the naming conventions consistent and meaningful?
   - Is the level of detail appropriate for the requirements?
   - Are there any logical inconsistencies or errors?

4. **Gap Analysis:**
   - What requirements are not adequately represented in the diagrams?
   - What diagram elements don't have corresponding requirements?
   - Are there any contradictions between diagrams?

**OUTPUT FORMAT:**
Please provide your analysis in the following format:

## Consistency Report for {slice_name}

### Executive Summary
[Brief overview of overall consistency and quality]

### Consistency Analysis
- **Class-Sequence Alignment:** [Analysis]
- **Sequence-Activity Alignment:** [Analysis] 
- **Class-Activity Alignment:** [Analysis]
- **Data Flow Consistency:** [Analysis]

### Completeness Analysis
- **Requirements Coverage:** [Percentage and details]
- **Missing Elements:** [List any missing elements]
- **Excess Elements:** [List any unnecessary elements]

### Quality Assessment
- **UML Best Practices:** [Compliance level]
- **Naming Conventions:** [Assessment]
- **Diagram Clarity:** [Assessment]

### Issues Identified
1. [Issue 1 with severity level]
2. [Issue 2 with severity level]
...

### Recommendations
1. [Recommendation 1]
2. [Recommendation 2]
...

### Consistency Score
**Overall Score:** [X/10] - [Brief justification]

<consistency_score>[X]</consistency_score>

Generate the validation report now:
"""
        return prompt
    
    def extract_consistency_score(self, validation_report: str) -> int:
        """
        Extract the consistency score from the validation report.
        
        Args:
            validation_report (str): The validation report text
            
        Returns:
            int: Consistency score (0-10), or -1 if not found
        """
        try:
            import re
            
            # Look for <consistency_score>X</consistency_score> pattern
            score_match = re.search(r'<consistency_score>(\d+)</consistency_score>', validation_report)
            if score_match:
                return int(score_match.group(1))
            
            # Fallback: look for "Score: X/10" pattern
            score_match = re.search(r'Score:\s*(\d+)/10', validation_report)
            if score_match:
                return int(score_match.group(1))
            
            # Fallback: look for "X/10" pattern
            score_match = re.search(r'(\d+)/10', validation_report)
            if score_match:
                return int(score_match.group(1))
            
            return -1  # Score not found
            
        except Exception:
            return -1
    
    def save_iteration_report(self, iteration_results: Dict) -> str:
        """
        Save the iteration results to a report file.
        
        Args:
            iteration_results (Dict): Complete iteration results
            
        Returns:
            str: Path to the saved report file
        """
        try:
            # Create reports directory if it doesn't exist
            reports_dir = os.path.join(self.diagrams_dir, "reports")
            if not os.path.exists(reports_dir):
                os.makedirs(reports_dir)
            
            # Generate report filename
            timestamp = iteration_results.get('timestamp', datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
            slice_name = iteration_results.get('slice_name', 'UnknownSlice')
            report_filename = f"iteration_report_{slice_name}_{timestamp}.md"
            report_path = os.path.join(reports_dir, report_filename)
            
            # Generate report content
            report_content = self.generate_iteration_report_content(iteration_results)
            
            # Save report
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            return report_path
            
        except Exception as e:
            raise Exception(f"Failed to save iteration report: {e}")
    
    def generate_iteration_report_content(self, iteration_results: Dict) -> str:
        """
        Generate the content for the iteration report.
        
        Args:
            iteration_results (Dict): Complete iteration results
            
        Returns:
            str: Formatted report content in Markdown
        """
        slice_name = iteration_results.get('slice_name', 'Unknown')
        timestamp = iteration_results.get('timestamp', 'Unknown')
        diagrams = iteration_results.get('diagrams', {})
        validation = iteration_results.get('validation', {})
        
        report = f"""# Design Iteration Report: {slice_name}

**Generated:** {timestamp}
**Phase:** 2 - Software Design
**Slice:** {slice_name}

## 📊 Diagram Generation Results

### Class Diagram
"""
        
        if 'class' in diagrams and 'error' not in diagrams['class']:
            report += f"""
- ✅ **Status:** Generated successfully
- 📄 **PlantUML:** `{diagrams['class']['puml']}`
- 🖼️ **Image:** `{diagrams['class']['image']}`
"""
        else:
            error = diagrams.get('class', {}).get('error', 'Unknown error')
            report += f"""
- ❌ **Status:** Generation failed
- **Error:** {error}
"""
        
        report += "\n### Sequence Diagram\n"
        
        if 'sequence' in diagrams and 'error' not in diagrams['sequence']:
            report += f"""
- ✅ **Status:** Generated successfully
- 📄 **PlantUML:** `{diagrams['sequence']['puml']}`
- 🖼️ **Image:** `{diagrams['sequence']['image']}`
"""
        else:
            error = diagrams.get('sequence', {}).get('error', 'Unknown error')
            report += f"""
- ❌ **Status:** Generation failed
- **Error:** {error}
"""
        
        report += "\n### Activity Diagram\n"
        
        if 'activity' in diagrams and 'error' not in diagrams['activity']:
            report += f"""
- ✅ **Status:** Generated successfully
- 📄 **PlantUML:** `{diagrams['activity']['puml']}`
- 🖼️ **Image:** `{diagrams['activity']['image']}`
"""
        else:
            error = diagrams.get('activity', {}).get('error', 'Unknown error')
            report += f"""
- ❌ **Status:** Generation failed
- **Error:** {error}
"""
        
        report += "\n## 🔍 Validation Results\n"
        
        if validation and 'error' not in validation:
            consistency_score = validation.get('consistency_score', -1)
            if consistency_score >= 0:
                report += f"\n**Consistency Score:** {consistency_score}/10\n"
            
            report += f"""
**Diagrams Validated:** {', '.join(validation.get('diagrams_validated', []))}

### Detailed Validation Report

{validation.get('report', 'No validation report available')}
"""
        else:
            error = validation.get('error', 'Validation not performed') if validation else 'Validation not performed'
            report += f"""
- ❌ **Status:** Validation failed
- **Error:** {error}
"""
        
        report += f"""

## 📈 Summary

- **Diagrams Generated:** {len([d for d in diagrams.values() if 'error' not in d])}/3
- **Validation Status:** {'✅ Completed' if validation and 'error' not in validation else '❌ Failed/Skipped'}
- **Overall Quality:** {'✅ Good' if validation and validation.get('consistency_score', 0) >= 7 else '⚠️ Needs Review' if validation and validation.get('consistency_score', 0) >= 4 else '❌ Poor'}

Generated by Phase 2 Design Agent on {timestamp}
"""
        
        return report
    
    def run_iterative_design_workflow(self, requirement_slices: List[Dict[str, str]], custom_validation_prompt: str = None) -> Dict[str, any]:
        """
        Run the complete iterative design workflow for multiple requirement slices.
        
        Args:
            requirement_slices (List[Dict]): List of requirement slices with 'name' and 'content' keys
            custom_validation_prompt (str, optional): Custom validation prompt template
            
        Returns:
            Dict: Complete workflow results for all slices
        """
        print("🚀 Starting Iterative Design Workflow (Phase 2)")
        print(f"📋 Processing {len(requirement_slices)} requirement slices\n")
        
        workflow_results = {
            'workflow_start': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'total_slices': len(requirement_slices),
            'slice_results': {},
            'summary': {}
        }
        
        successful_iterations = 0
        total_diagrams_generated = 0
        validation_scores = []
        
        for i, slice_info in enumerate(requirement_slices, 1):
            slice_name = slice_info.get('name', f'Slice_{i}')
            slice_content = slice_info.get('content', '')
            
            print(f"🔄 Processing Slice {i}/{len(requirement_slices)}: {slice_name}")
            print("="*60)
            
            try:
                # Run iteration for this slice
                iteration_result = self.generate_diagrams_from_requirements_slice(
                    slice_content,
                    slice_name,
                    custom_validation_prompt
                )
                
                workflow_results['slice_results'][slice_name] = iteration_result
                
                # Update summary statistics
                successful_iterations += 1
                diagrams = iteration_result.get('diagrams', {})
                total_diagrams_generated += len([d for d in diagrams.values() if 'error' not in d])
                
                validation = iteration_result.get('validation', {})
                if validation and 'consistency_score' in validation and validation['consistency_score'] >= 0:
                    validation_scores.append(validation['consistency_score'])
                
                print(f"✅ Slice {slice_name} completed successfully!\n")
                
            except Exception as e:
                print(f"❌ Slice {slice_name} failed: {e}\n")
                workflow_results['slice_results'][slice_name] = {'error': str(e)}
        
        # Generate workflow summary
        workflow_results['summary'] = {
            'successful_slices': successful_iterations,
            'failed_slices': len(requirement_slices) - successful_iterations,
            'total_diagrams_generated': total_diagrams_generated,
            'average_consistency_score': sum(validation_scores) / len(validation_scores) if validation_scores else -1,
            'validation_scores': validation_scores,
            'workflow_end': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Save workflow summary report
        summary_report_path = self.save_workflow_summary_report(workflow_results)
        workflow_results['summary_report_path'] = summary_report_path
        
        print("🎉 Iterative Design Workflow Completed!")
        print(f"📊 Results: {successful_iterations}/{len(requirement_slices)} slices successful")
        print(f"📄 Summary report: {summary_report_path}")
        
        return workflow_results
    
    def save_workflow_summary_report(self, workflow_results: Dict) -> str:
        """
        Save a summary report for the complete workflow.
        
        Args:
            workflow_results (Dict): Complete workflow results
            
        Returns:
            str: Path to the summary report
        """
        try:
            reports_dir = os.path.join(self.diagrams_dir, "reports")
            if not os.path.exists(reports_dir):
                os.makedirs(reports_dir)
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            summary_filename = f"workflow_summary_{timestamp}.md"
            summary_path = os.path.join(reports_dir, summary_filename)
            
            summary = workflow_results.get('summary', {})
            
            content = f"""# Phase 2 Design Workflow Summary

**Workflow Started:** {workflow_results.get('workflow_start', 'Unknown')}
**Workflow Completed:** {summary.get('workflow_end', 'Unknown')}
**Total Slices Processed:** {workflow_results.get('total_slices', 0)}

## 📊 Overall Results

- **Successful Slices:** {summary.get('successful_slices', 0)}/{workflow_results.get('total_slices', 0)}
- **Failed Slices:** {summary.get('failed_slices', 0)}
- **Total Diagrams Generated:** {summary.get('total_diagrams_generated', 0)}
- **Average Consistency Score:** {summary.get('average_consistency_score', -1):.1f}/10

## 📈 Consistency Scores by Slice

"""
            
            validation_scores = summary.get('validation_scores', [])
            if validation_scores:
                content += "| Slice | Consistency Score |\n"
                content += "|-------|------------------|\n"
                
                slice_names = list(workflow_results.get('slice_results', {}).keys())
                for i, score in enumerate(validation_scores):
                    slice_name = slice_names[i] if i < len(slice_names) else f"Slice_{i+1}"
                    content += f"| {slice_name} | {score}/10 |\n"
            else:
                content += "No validation scores available.\n"
            
            content += "\n## 📋 Detailed Results by Slice\n\n"
            
            for slice_name, result in workflow_results.get('slice_results', {}).items():
                content += f"### {slice_name}\n\n"
                
                if 'error' in result:
                    content += f"- ❌ **Status:** Failed\n- **Error:** {result['error']}\n\n"
                else:
                    diagrams = result.get('diagrams', {})
                    successful_diagrams = len([d for d in diagrams.values() if 'error' not in d])
                    validation = result.get('validation', {})
                    
                    content += f"- **Diagrams Generated:** {successful_diagrams}/3\n"
                    content += f"- **Report:** [{result.get('report_path', 'N/A')}]\n"
                    
                    if validation and 'consistency_score' in validation:
                        content += f"- **Consistency Score:** {validation['consistency_score']}/10\n"
                    
                    content += "\n"
            
            content += f"\n---\n*Generated by Phase 2 Design Agent on {summary.get('workflow_end', 'Unknown')}*\n"
            
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return summary_path
            
        except Exception as e:
            raise Exception(f"Failed to save workflow summary report: {e}")


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
        
        # =====================================================================
        # Example: Iterative Design Workflow with Hardcoded Requirement Slices
        # =====================================================================
        print("\n" + "="*60)
        print("📋 ITERATIVE DESIGN WORKFLOW EXAMPLE")
        print("="*60)
        print("To run the iterative workflow, uncomment the example below:")
        print()
        print("# Sample requirement slices for testing")
        print("# requirement_slices = [")
        print('#     {"name": "UserAuth", "content": "User authentication requirements..."},')
        print('#     {"name": "VehicleMonitoring", "content": "Vehicle monitoring requirements..."},')
        print('#     {"name": "ChargingManagement", "content": "Charging management requirements..."}')
        print("# ]")
        print()
        print("# Custom validation prompt (optional)")
        print("# custom_prompt = '''")
        print("# Validate the consistency of these diagrams for {slice_name}:")
        print("# Requirements: {requirements}")
        print("# Class Diagram: {class_diagram}")
        print("# Sequence Diagram: {sequence_diagram}")
        print("# Activity Diagram: {activity_diagram}")
        print("# Provide detailed analysis and score 1-10.")
        print("# '''")
        print()
        print("# Run the iterative workflow")
        print("# results = uml_automation.run_iterative_design_workflow(")
        print("#     requirement_slices, custom_prompt")
        print("# )")
        print("# print(f'Workflow Results: {results}')")
        print()
        print("This workflow will:")
        print("  1. 🎯 Process each requirement slice")
        print("  2. 📊 Generate Class, Sequence, and Activity diagrams")
        print("  3. 🔍 Validate diagram consistency with Gemini")
        print("  4. 📄 Generate detailed reports for each iteration")
        print("  5. 📈 Create a comprehensive summary report")
        
        print(f"\n✨ Phase 2 Design Agent initialized successfully!")
        print("Ready for iterative UML diagram generation and validation! 🚀")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()