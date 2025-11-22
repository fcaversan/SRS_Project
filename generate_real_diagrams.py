#!/usr/bin/env python3
"""
Quick UML Generation from Real Specifications

Paste your real specification text in the designated areas below and run this script.
"""

from p2_design_agent import UMLDiagramAutomation

def generate_from_real_specs():
    """Generate UML diagrams from your real specifications."""
    
    # Initialize automation
    print("🚀 Initializing UML Automation...")
    uml_automation = UMLDiagramAutomation()
    uml_automation.setup_gemini()
    uml_automation.setup_directories()
    uml_automation.verify_plantuml_installation()
    print("✅ Setup complete!\n")
    
    # =======================================================================
    # PASTE YOUR SPECIFICATIONS HERE
    # =======================================================================
    
    # A. Data Requirements / Entities (for Class Diagram)
    # Replace this with your actual data requirements section:
    data_requirements_text = """
    PASTE YOUR DATA REQUIREMENTS OR ENTITIES SECTION HERE
    
    Example format:
    - Entity names and their attributes
    - Relationships between entities
    - Operations/methods for each entity
    """
    
    # B. Functional Requirements (for Sequence Diagram)  
    # Replace this with a specific functional requirement:
    feature_name = "REPLACE WITH YOUR FEATURE NAME"
    functional_requirements_text = """
    PASTE YOUR FUNCTIONAL REQUIREMENT HERE
    
    Example: Login process, Remote start, Payment flow, etc.
    Include normal flow and error scenarios
    """
    
    # C. Complex Workflow (for Activity Diagram)
    # Replace this with your workflow with decision points:
    workflow_name = "REPLACE WITH YOUR WORKFLOW NAME"
    workflow_text = """
    PASTE YOUR COMPLEX WORKFLOW HERE
    
    Example: Business process with if/then logic, decision points, loops
    """
    
    # =======================================================================
    # GENERATION (only modify if you want different filenames)
    # =======================================================================
    
    results = {}
    
    # Generate Structure (Class) Diagram
    if "PASTE YOUR DATA" not in data_requirements_text:
        try:
            print("📊 Generating Structure (Class) Diagram...")
            structure_result = uml_automation.generate_structure_diagram(
                data_requirements_text,
                "real_structure_diagram"
            )
            results['structure'] = structure_result
            print(f"✅ Class Diagram: {structure_result['image']}")
        except Exception as e:
            print(f"❌ Structure diagram failed: {e}")
    else:
        print("⏭️  Skipping Structure diagram - no real data provided")
    
    # Generate Interaction (Sequence) Diagram
    if "PASTE YOUR FUNCTIONAL" not in functional_requirements_text:
        try:
            print("\n🔄 Generating Interaction (Sequence) Diagram...")
            interaction_result = uml_automation.generate_interaction_diagram(
                feature_name,
                functional_requirements_text,
                "real_interaction_diagram"
            )
            results['interaction'] = interaction_result
            print(f"✅ Sequence Diagram: {interaction_result['image']}")
        except Exception as e:
            print(f"❌ Interaction diagram failed: {e}")
    else:
        print("⏭️  Skipping Interaction diagram - no real data provided")
    
    # Generate Logic (Activity) Diagram
    if "PASTE YOUR COMPLEX" not in workflow_text:
        try:
            print("\n⚡ Generating Logic (Activity) Diagram...")
            logic_result = uml_automation.generate_logic_diagram(
                workflow_text,
                workflow_name,
                "real_logic_diagram"
            )
            results['logic'] = logic_result
            print(f"✅ Activity Diagram: {logic_result['image']}")
        except Exception as e:
            print(f"❌ Logic diagram failed: {e}")
    else:
        print("⏭️  Skipping Logic diagram - no real data provided")
    
    # =======================================================================
    # ALTERNATIVE: Use existing SRS file
    # =======================================================================
    
    try:
        print(f"\n🔍 Alternative: Checking for existing SRS file...")
        srs_file = "SRS_v5.txt"  # Change this to your SRS filename
        if uml_automation.read_srs_file(srs_file):
            print(f"📄 Found SRS file: {srs_file}")
            
            user_input = input("Do you want to generate diagrams from the SRS file instead? (y/n): ")
            if user_input.lower() == 'y':
                print("\n🚀 Generating comprehensive diagrams from SRS file...")
                srs_content = uml_automation.read_srs_file(srs_file)
                comprehensive_results = uml_automation.generate_comprehensive_design_set(srs_content)
                
                print(f"\n📊 SRS-based Generation Results:")
                for name, result in comprehensive_results.items():
                    if 'error' in result:
                        print(f"❌ {name}: {result['error']}")
                    else:
                        print(f"✅ {name}: {result.get('type', 'Generated')}")
    
    except Exception as e:
        print(f"ℹ️  SRS file not found or accessible: {e}")
    
    # =======================================================================
    # SUMMARY
    # =======================================================================
    
    print(f"\n🎉 Generation Complete!")
    if results:
        print(f"Generated {len(results)} diagrams:")
        for name, result in results.items():
            print(f"  📁 {name}: {result['image']}")
        print(f"\nCheck the 'uml_diagrams/' directory for all files!")
    else:
        print(f"No diagrams generated. Please paste your specifications in the script and run again.")

if __name__ == "__main__":
    generate_from_real_specs()