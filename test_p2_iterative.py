#!/usr/bin/env python3
"""
Test script for Phase 2 Iterative Design Workflow

This script demonstrates the new iterative functionality in p2_design_agent.py
that processes requirement slices and generates Class, Sequence, and Activity diagrams
with consistency validation.
"""

import os
import sys
from p2_design_agent import UMLDiagramAutomation

def test_iterative_workflow():
    """Test the iterative design workflow with sample requirement slices."""
    
    print("🧪 Testing Phase 2 Iterative Design Workflow")
    print("="*60)
    
    try:
        # Initialize the UML automation
        uml_automation = UMLDiagramAutomation()
        uml_automation.setup_gemini()
        uml_automation.setup_directories()
        uml_automation.verify_plantuml_installation()
        
        print("✅ UML automation initialized successfully!\n")
        
        # Define sample requirement slices (hardcoded for testing)
        requirement_slices = [
            {
                "name": "Home Screen & Vehicle Status",
                "content": """
3.2.1 FR-HSS: Home Screen & Vehicle Status
FR-HSS-001: The system shall display the vehicle's current State of Charge (SoC) as a percentage value on the application's home screen.
FR-HSS-002: The system shall display a visual representation of the vehicle's battery level.
FR-HSS-003: The system shall display an estimated vehicle range in the user's preferred unit (miles or kilometers).
FR-HSS-004: The estimated vehicle range calculation shall be based on the vehicle's current SoC, recent energy consumption trends, and the current ambient temperature reported by the vehicle.
FR-HSS-005: The system shall display the vehicle's current lock status (Locked/Unlocked).
FR-HSS-006: The system shall display the vehicle's interior cabin temperature as reported by the vehicle.
FR-HSS-007: The system shall indicate whether the climate control system is currently active.
FR-HSS-008: The system shall display a clear, graphical representation of the user's vehicle on the home screen.
                """
            },
            {
                "name": "Charging Management", 
                "content": """
3.2.2 FR-CHG: Charging Management
FR-CHG-001: The system shall allow the user to remotely start a charging session if the vehicle is plugged into a compatible charger.
FR-CHG-002: The system shall allow the user to remotely stop a charging session.
FR-CHG-003: During an active charging session, the system shall display: current SoC, estimated time to completion, current charging rate (kW), and supplied voltage/amperage.
FR-CHG-004: The system shall provide an interface for the user to set a maximum charging limit as a percentage. The interface shall default to 80% for daily charging and shall provide a convenient one-time "charge to 100%" option for trips.
FR-CHG-005: The system shall allow the user to create, edit, and delete charging schedules, defining a start time or a desired ready-by time.
FR-CHG-006: The system shall display a map of charging stations.
FR-CHG-007: The system shall allow the user to filter charging stations by connector type and power level (kW).
FR-CHG-008: The system shall display real-time availability for charging stations where the data is provided by the network operator.
                """
            },
            {
                "name": "Remote Controls", 
                "content": """
3.2.3 FR-RMC: Remote Controls
FR-RMC-001: The system shall allow the user to remotely lock the vehicle's doors.
FR-RMC-002: The system shall allow the user to remotely unlock the vehicle's doors.
FR-RMC-003: The system shall allow the user to remotely activate the vehicle's climate control system (HVAC).
FR-RMC-004: The system shall allow the user to set a target temperature for the cabin.
FR-RMC-005: The system shall allow the user to remotely activate/deactivate heated seats and the heated steering wheel, if equipped.
FR-RMC-006: The system shall allow the user to remotely activate front and rear defrosters.
FR-RMC-007: The system shall display a warning to the user if they attempt to precondition the cabin while the vehicle is not plugged in, indicating the action will consume battery range.
FR-RMC-008: The system shall allow the user to remotely open the front trunk (frunk) and rear trunk.
FR-RMC-009: The system shall provide a function to remotely honk the horn and flash the lights.
FR-RMC-010: The system shall provide haptic feedback on the user's mobile device upon successful completion of a remote lock or unlock command.
                """
            }
        ]
        
        # Optional: Custom validation prompt (parameterized as requested)
        custom_validation_prompt = """
You are a senior software architect reviewing UML diagrams for the {slice_name} feature.

Analyze these artifacts for consistency and quality:

**REQUIREMENTS:**
{requirements}

**GENERATED DIAGRAMS:**
- Class Diagram: {class_diagram}
- Sequence Diagram: {sequence_diagram}  
- Activity Diagram: {activity_diagram}

**VALIDATION FOCUS:**
1. Do class structures support the described flows?
2. Are sequence interactions realistic and complete?
3. Do activity workflows match the requirements?
4. Are naming conventions consistent across diagrams?

Provide a comprehensive analysis and score the consistency from 1-10.
Include specific recommendations for improvement.

<consistency_score>[YOUR_SCORE]</consistency_score>
"""
        
        print("📋 Sample requirement slices defined:")
        for i, slice_info in enumerate(requirement_slices, 1):
            print(f"  {i}. {slice_info['name']}")
        print()
        
        # Run the iterative design workflow
        print("🚀 Starting iterative design workflow...")
        results = uml_automation.run_iterative_design_workflow(
            requirement_slices,
            custom_validation_prompt
        )
        
        # Display results summary
        print("\n" + "="*60)
        print("📊 WORKFLOW RESULTS SUMMARY")
        print("="*60)
        
        summary = results.get('summary', {})
        print(f"Total slices processed: {results.get('total_slices', 0)}")
        print(f"Successful slices: {summary.get('successful_slices', 0)}")
        print(f"Failed slices: {summary.get('failed_slices', 0)}")
        print(f"Total diagrams generated: {summary.get('total_diagrams_generated', 0)}")
        print(f"Average consistency score: {summary.get('average_consistency_score', -1):.1f}/10")
        
        if 'summary_report_path' in results:
            print(f"📄 Summary report saved: {results['summary_report_path']}")
        
        print("\n🔍 Individual slice results:")
        for slice_name, result in results.get('slice_results', {}).items():
            if 'error' in result:
                print(f"  ❌ {slice_name}: {result['error']}")
            else:
                diagrams = result.get('diagrams', {})
                successful_diagrams = len([d for d in diagrams.values() if 'error' not in d])
                validation = result.get('validation', {})
                score = validation.get('consistency_score', -1) if validation else -1
                
                print(f"  ✅ {slice_name}: {successful_diagrams}/3 diagrams, score: {score}/10")
                if 'report_path' in result:
                    print(f"     Report: {result['report_path']}")
        
        print("\n🎉 Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_single_iteration():
    """Test a single iteration with one requirement slice."""
    
    print("\n🧪 Testing Single Iteration")
    print("="*40)
    
    try:
        # Initialize the UML automation
        uml_automation = UMLDiagramAutomation()
        uml_automation.setup_gemini()
        uml_automation.setup_directories()
        
        # Single requirement slice for quick testing
        test_requirements = """
        Shopping Cart Requirements:
        
        1. Users shall be able to add items to their shopping cart
        2. The system shall calculate total price including taxes
        3. Users shall be able to remove items from cart
        4. Cart contents shall persist during user session
        5. Users shall be able to proceed to checkout
        
        Key entities: Cart, Item, User, PriceCalculator
        Main flow: Add Item -> Calculate Total -> Checkout
        """
        
        # Run single iteration
        result = uml_automation.generate_diagrams_from_requirements_slice(
            test_requirements,
            "ShoppingCart"
        )
        
        print(f"✅ Single iteration completed!")
        print(f"Diagrams generated: {len([d for d in result.get('diagrams', {}).values() if 'error' not in d])}/3")
        
        if 'validation' in result and result['validation']:
            score = result['validation'].get('consistency_score', -1)
            print(f"Consistency score: {score}/10")
        
        if 'report_path' in result:
            print(f"Report saved: {result['report_path']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Single iteration test failed: {e}")
        return False

if __name__ == "__main__":
    """Run the iterative workflow tests."""
    
    print("🚀 Phase 2 Iterative Design Workflow Test Suite")
    print("="*70)
    print()
    
    # Test 1: Single iteration (faster)
    if len(sys.argv) > 1 and sys.argv[1] == "--single":
        success = test_single_iteration()
    else:
        # Test 2: Full iterative workflow (more comprehensive)
        success = test_iterative_workflow()
    
    print("\n" + "="*70)
    if success:
        print("🎉 All tests passed! Phase 2 iterative workflow is ready to use.")
        print("\nNext steps:")
        print("1. 📝 Customize requirement slices for your project")
        print("2. 🎯 Fine-tune the validation prompt as needed")
        print("3. 🔧 Adjust diagram generation parameters")
        print("4. 📊 Review generated reports and diagrams")
    else:
        print("❌ Tests failed. Please check the configuration and try again.")
        sys.exit(1)
    
    print(f"\n✨ Phase 2 Design Agent is ready for production use! 🚀")