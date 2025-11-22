#!/usr/bin/env python3
"""
Example usage script for UML Diagram Automation

This script demonstrates how to use the UMLDiagramAutomation class
to generate various UML diagrams from your SRS document.
"""

from p2_design_agent import UMLDiagramAutomation

def demonstrate_uml_automation():
    """Demonstrate the UML automation capabilities."""
    try:
        print("=== UML Diagram Automation Example ===\n")
        
        # Initialize the automation
        uml_automation = UMLDiagramAutomation()
        
        # Setup
        print("Setting up automation...")
        uml_automation.setup_gemini()
        uml_automation.setup_directories()
        uml_automation.verify_plantuml_installation()
        
        print("✅ Setup completed!\n")
        
        # Read the latest SRS file
        srs_file = "SRS_sample1.txt"  # Update this to your latest SRS file
        print(f"Reading SRS file: {srs_file}")
        srs_content = uml_automation.read_srs_file(srs_file)
        
        # Example 1: Generate a Use Case Diagram
        print("\n=== Example 1: Use Case Diagram ===")
        use_case_result = uml_automation.generate_diagram(
            diagram_type="usecase",
            srs_content=srs_content,
            filename="electric_car_app_usecases"
        )
        print(f"Use Case Diagram generated:")
        print(f"  PUML file: {use_case_result['puml']}")
        print(f"  Image file: {use_case_result['image']}")
        
        # Example 2: Generate a Class Diagram with custom prompt
        print("\n=== Example 2: Class Diagram with Custom Prompt ===")
        custom_class_prompt = """
You are a senior software architect. Create a comprehensive Class Diagram in PlantUML format for the Electric Car Management Mobile Application based on the provided SRS.

Focus on:
- Core domain classes (Vehicle, User, ChargingStation, Trip, etc.)
- Data transfer objects and entities
- Service/Controller classes
- Repository/Data access classes
- Relationships between classes (inheritance, composition, aggregation)
- Key attributes and methods for each class

SRS CONTENT:
{srs_content}

Generate ONLY PlantUML code - no explanations:
"""
        
        class_result = uml_automation.generate_diagram(
            diagram_type="class",
            srs_content=srs_content,
            custom_prompt=custom_class_prompt,
            filename="electric_car_app_classes"
        )
        print(f"Class Diagram generated:")
        print(f"  PUML file: {class_result['puml']}")
        print(f"  Image file: {class_result['image']}")
        
        # Example 3: Generate multiple diagrams at once
        print("\n=== Example 3: Generate Multiple Diagrams ===")
        selected_diagrams = ["sequence", "activity", "component"]
        
        results = uml_automation.generate_all_diagrams(
            srs_content=srs_content,
            selected_types=selected_diagrams
        )
        
        for diagram_type, result in results.items():
            if 'error' in result:
                print(f"❌ {diagram_type}: {result['error']}")
            else:
                print(f"✅ {diagram_type}: {result['puml']} -> {result['image']}")
        
        # List all generated diagrams
        print("\n=== Generated Diagrams Summary ===")
        all_diagrams = uml_automation.list_generated_diagrams()
        
        for diagram_type, files in all_diagrams.items():
            if files:
                print(f"{diagram_type.upper()}: {len(files)} files")
                for file in files[:3]:  # Show first 3 files
                    print(f"  - {file}")
                if len(files) > 3:
                    print(f"  ... and {len(files) - 3} more")
            else:
                print(f"{diagram_type.upper()}: No files generated")
        
        print(f"\n🎉 UML Automation demonstration completed!")
        print(f"Check the '{uml_automation.diagrams_dir}' directory for all generated diagrams.")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")

if __name__ == "__main__":
    demonstrate_uml_automation()