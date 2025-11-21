from uml_automation import UMLDiagramAutomation
import os

def generate_diagrams_from_any_srs(srs_filename):
    """
    Generate UML diagrams from any SRS file format.
    This function uses AI to intelligently extract relevant sections.
    """
    print(f"🚀 Starting UML Generation from {srs_filename}...")

    # Initialize
    uml_automation = UMLDiagramAutomation()
    uml_automation.setup_gemini()
    uml_automation.setup_directories()
    uml_automation.verify_plantuml_installation()

    # Check if file exists
    if not os.path.exists(srs_filename):
        print(f"❌ File not found: {srs_filename}")
        return

    # Read SRS file
    print("📄 Reading SRS file...")
    srs_content = uml_automation.read_srs_file(srs_filename)
    print(f"✅ SRS loaded successfully ({len(srs_content)} characters)")

    results = {}

    # =================================================================
    # A. STRUCTURE (Class Diagram) - Extract data-related content
    # =================================================================
    print("\n📊 Generating Structure (Class) Diagram...")
    try:
        # Use AI to create a prompt that extracts data structures from any SRS
        data_extraction_prompt = f"""
        You are a software architect. Analyze the following SRS document and extract all data entities, their attributes, and relationships.

        Look for:
        - Data models, entities, objects
        - Database requirements
        - Data storage specifications
        - Entity relationships
        - User profiles, system objects, etc.

        From this SRS content, identify the data structures:

        {srs_content}

        Extract and format the data requirements for class diagram generation:
        """
        
        extracted_data = uml_automation.send_prompt(data_extraction_prompt)
        
        structure_result = uml_automation.generate_structure_diagram(
            extracted_data,
            f"{os.path.splitext(srs_filename)[0]}_structure"
        )
        results['structure'] = structure_result
        print(f"✅ Class Diagram generated: {structure_result['image']}")
        
    except Exception as e:
        print(f"❌ Structure diagram failed: {e}")

    # =================================================================
    # B. INTERACTION (Sequence Diagram) - Extract functional flows
    # =================================================================
    print("\n🔄 Generating Interaction (Sequence) Diagram...")
    try:
        # Use AI to identify and extract the most important functional requirement
        interaction_extraction_prompt = f"""
        You are a software architect. Analyze this SRS and identify the most important user interaction or functional requirement that would make a good sequence diagram.

        Look for:
        - User login/authentication flows
        - Core business processes
        - API interactions
        - User workflows with multiple steps

        From this SRS, extract ONE key functional requirement with its flow:

        {srs_content}

        Provide:
        1. The feature name
        2. The detailed functional requirement text
        Format as: "FEATURE: [name] | REQUIREMENT: [detailed text]"
        """
        
        extracted_interaction = uml_automation.send_prompt(interaction_extraction_prompt)
        
        # Parse the response to get feature name and requirement
        if "FEATURE:" in extracted_interaction and "REQUIREMENT:" in extracted_interaction:
            parts = extracted_interaction.split("REQUIREMENT:")
            feature_name = parts[0].replace("FEATURE:", "").strip()
            requirement_text = parts[1].strip()
        else:
            feature_name = "Key System Interaction"
            requirement_text = extracted_interaction
        
        interaction_result = uml_automation.generate_interaction_diagram(
            feature_name,
            requirement_text,
            f"{os.path.splitext(srs_filename)[0]}_interaction"
        )
        results['interaction'] = interaction_result
        print(f"✅ Sequence Diagram generated: {interaction_result['image']}")
        
    except Exception as e:
        print(f"❌ Interaction diagram failed: {e}")

    # =================================================================
    # C. LOGIC (Activity Diagram) - Extract workflow logic
    # =================================================================
    print("\n⚡ Generating Logic (Activity) Diagram...")
    try:
        # Use AI to identify complex workflows or business logic
        logic_extraction_prompt = f"""
        You are a software architect. Analyze this SRS and identify a complex business process or workflow that involves decision points, conditions, and multiple steps.

        Look for:
        - Business processes with if/then logic
        - Workflows with decision points
        - Multi-step processes
        - Error handling flows
        - Validation processes

        From this SRS, create a workflow description with decision points:

        {srs_content}

        Format the workflow with clear steps, decision points, and logic branches.
        """
        
        extracted_workflow = uml_automation.send_prompt(logic_extraction_prompt)
        
        logic_result = uml_automation.generate_logic_diagram(
            extracted_workflow,
            "Business Logic Flow",
            f"{os.path.splitext(srs_filename)[0]}_logic"
        )
        results['logic'] = logic_result
        print(f"✅ Activity Diagram generated: {logic_result['image']}")
        
    except Exception as e:
        print(f"❌ Logic diagram failed: {e}")

    # =================================================================
    # SUMMARY
    # =================================================================
    print("\n" + "="*60)
    print("🎉 GENERIC UML GENERATION COMPLETE!")
    print("="*60)

    if results:
        print(f"Generated {len(results)} diagrams from {srs_filename}:")
        for name, result in results.items():
            print(f"  📁 {name.upper()}: {result['image']}")
        print(f"\n📂 Check the 'uml_diagrams/' directory for all files!")
    else:
        print("❌ No diagrams were generated successfully")

    return results

# =================================================================
# MAIN EXECUTION
# =================================================================
if __name__ == "__main__":
    # Try multiple SRS files automatically
    possible_srs_files = [
        "SRS_sample1.txt"
    ]
    
    srs_file_found = None
    for srs_file in possible_srs_files:
        if os.path.exists(srs_file):
            srs_file_found = srs_file
            break
    
    if srs_file_found:
        print(f"📄 Found SRS file: {srs_file_found}")
        results = generate_diagrams_from_any_srs(srs_file_found)
    else:
        print("❌ No SRS file found. Available files:")
        for file in os.listdir("."):
            if file.endswith(".txt"):
                print(f"  - {file}")
        
        # Ask user for file
        user_file = input("\nEnter SRS filename: ").strip()
        if user_file and os.path.exists(user_file):
            results = generate_diagrams_from_any_srs(user_file)
        else:
            print("❌ File not found or invalid input")