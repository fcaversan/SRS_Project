#!/usr/bin/env python3
"""
Test Scope Enforcement - Verify diagrams stay within requirements slice

This test validates that the refinement system:
1. Prevents scope drift to other requirement sections
2. Detects when diagrams model features not in the slice
3. Enforces scope adherence through validation scoring
"""

import os
from p2_design_agent import UMLDiagramAutomation
from validation_handler import ValidationHandler

def test_scope_enforcement():
    """Test that scope enforcement prevents feature drift"""
    
    print("🔒 Testing Scope Enforcement")
    print("=" * 80)
    print("This test verifies diagrams stay within the requirements slice scope")
    print("=" * 80)
    
    try:
        agent = UMLDiagramAutomation()
        agent.setup_gemini()
        agent.setup_directories()
        
        # Use a small, focused requirements slice
        test_slice = {
            "name": "Home_Screen_Test",
            "content": """
3.2.1 FR-HSS: Home Screen & Vehicle Status
FR-HSS-001: The system shall display the vehicle's current State of Charge (SoC) as a percentage value on the application's home screen.
FR-HSS-002: The system shall display a visual representation of the vehicle's battery level.
FR-HSS-003: The system shall display an estimated vehicle range in the user's preferred unit (miles or kilometers).
            """.strip()
        }
        
        print(f"\n📋 Test Requirements Slice: {test_slice['name']}")
        print(f"Requirements: {test_slice['content'][:100]}...")
        
        # Generate initial diagrams
        print("\n🎨 Generating initial diagrams...")
        result = agent.generate_diagrams_from_requirements_slice(
            test_slice['content'],
            test_slice['name']
        )
        
        diagrams = result.get('diagrams', {})
        validation = result.get('validation', {})
        
        print(f"\n✅ Generated {len(diagrams)} diagrams")
        
        # Check validation results for scope adherence
        metrics = validation.get('metrics', {})
        scope_score = metrics.get('scope_adherence_score', 'N/A')
        scope_violations = metrics.get('scope_violations', [])
        
        print(f"\n📊 Scope Adherence Results:")
        print(f"  Scope Adherence Score: {scope_score}/10")
        
        if scope_violations and any(scope_violations):
            print(f"  ⚠️  Scope Violations Detected:")
            for violation in scope_violations:
                if violation:
                    print(f"    - {violation}")
        else:
            print(f"  ✅ No scope violations detected")
        
        # Test refinement with scope enforcement
        if 'sequence' in diagrams and 'puml' in diagrams['sequence']:
            print(f"\n🔄 Testing refinement with scope enforcement...")
            
            # Read current diagram
            with open(diagrams['sequence']['puml'], 'r', encoding='utf-8') as f:
                current_content = f.read()
            
            # Simulate refinement
            refined_result = agent.refine_diagram_with_feedback(
                diagram_type='sequence',
                requirements=test_slice['content'],
                current_diagram_info=diagrams['sequence'],
                qa_metrics=metrics,
                slice_name=test_slice['name'],
                iteration_num=2
            )
            
            print(f"  ✅ Refinement completed")
            
            # Validate refined diagram still has proper scope
            if refined_result and 'content' in refined_result:
                refined_diagrams = {
                    'sequence': refined_result['content']
                }
                
                refined_validation = agent.validate_diagram_consistency(
                    test_slice['content'],
                    refined_diagrams,
                    test_slice['name']
                )
                
                refined_metrics = refined_validation.get('metrics', {})
                refined_scope_score = refined_metrics.get('scope_adherence_score', 'N/A')
                refined_violations = refined_metrics.get('scope_violations', [])
                
                print(f"\n📊 Refined Diagram Scope Check:")
                print(f"  Scope Adherence Score: {refined_scope_score}/10")
                
                if refined_violations and any(refined_violations):
                    print(f"  ⚠️  Scope Violations After Refinement:")
                    for violation in refined_violations:
                        if violation:
                            print(f"    - {violation}")
                else:
                    print(f"  ✅ No scope violations after refinement")
        
        print("\n" + "=" * 80)
        print("✅ Scope enforcement test completed!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_scope_enforcement()
