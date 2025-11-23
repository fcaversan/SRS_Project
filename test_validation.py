
import os
import sys
from p2_design_agent import UMLDiagramAutomation

def test_validation():
    try:
        agent = UMLDiagramAutomation()
        
        # Mock requirements
        requirements = "The system shall allow users to log in using their email and password. If the password is correct, the user is redirected to the dashboard. If incorrect, an error message is shown."
        slice_name = "Login_Test"
        
        print(f"Testing validation for slice: {slice_name}")
        
        # Run the generation and validation
        # We need to ensure directories exist
        agent.setup_directories()
        agent.setup_gemini()
        agent.verify_plantuml_installation()
        
        result = agent.generate_diagrams_from_requirements_slice(requirements, slice_name)
        
        print("\n=== Test Results ===")
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
        else:
            print("✅ Iteration completed successfully")
            
            validation = result.get('validation', {})
            metrics = validation.get('metrics', {})
            
            print(f"Consistency Score: {metrics.get('consistency_score')}")
            print(f"Overall Score: {metrics.get('overall_score')}")
            print(f"Consistency Analysis: {metrics.get('consistency_analysis')[:100]}...")
            
            if metrics.get('consistency_score') != -1:
                print("✅ JSON parsing successful!")
            else:
                print("❌ JSON parsing failed or scores missing.")
                print(f"Raw Report: {validation.get('report')[:500]}...")

    except Exception as e:
        print(f"❌ Test failed with exception: {e}")

if __name__ == "__main__":
    test_validation()
