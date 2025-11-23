#!/usr/bin/env python3
"""
Test Script for ValidationHandler Integration

This script tests the penalty system integration with the main p2_design_agent workflow.
"""

from validation_handler import ValidationHandler

def test_penalty_system():
    """Test the penalty application logic."""
    print("🧪 Testing ValidationHandler Penalty System")
    print("=" * 50)
    
    # Test Case 1: No missing diagrams
    print("\n📋 Test Case 1: All diagrams successful")
    metrics1 = {'overall_score': 8}
    diagram_contents1 = {
        'class': '@startuml\nclass User\n@enduml',
        'sequence': '@startuml\nUser -> API\n@enduml',
        'activity': '@startuml\nstart\n:action;\nstop\n@enduml'
    }
    
    result1 = ValidationHandler.apply_diagram_penalties(metrics1, diagram_contents1)
    print(f"Original Score: {metrics1['overall_score']}")
    print(f"Final Score: {result1['overall_score']}")
    print(f"Penalties: {result1.get('penalties_applied', {}).get('total_penalty', 0)}")
    
    # Test Case 2: One missing diagram
    print("\n📋 Test Case 2: One missing diagram")
    metrics2 = {'overall_score': 8}
    diagram_contents2 = {
        'class': '@startuml\nclass User\n@enduml',
        'sequence': 'Not generated',
        'activity': '@startuml\nstart\n:action;\nstop\n@enduml'
    }
    
    result2 = ValidationHandler.apply_diagram_penalties(metrics2, diagram_contents2)
    print(f"Original Score: {metrics2['overall_score']}")
    print(f"Final Score: {result2['overall_score']}")
    print(f"Penalties: {result2.get('penalties_applied', {}).get('total_penalty', 0)}")
    print(f"Penalty Notes: {result2.get('penalties_applied', {}).get('penalty_notes', [])}")
    
    # Test Case 3: One error diagram
    print("\n📋 Test Case 3: One diagram with errors")
    metrics3 = {'overall_score': 7}
    diagram_contents3 = {
        'class': '@startuml\nclass User\n@enduml',
        'sequence': '@startuml\nUser -> API\n@enduml',
        'activity': 'Diagram generation failed: Syntax error'
    }
    
    result3 = ValidationHandler.apply_diagram_penalties(metrics3, diagram_contents3)
    print(f"Original Score: {metrics3['overall_score']}")
    print(f"Final Score: {result3['overall_score']}")
    print(f"Penalties: {result3.get('penalties_applied', {}).get('total_penalty', 0)}")
    print(f"Penalty Notes: {result3.get('penalties_applied', {}).get('penalty_notes', [])}")
    
    # Test Case 4: Multiple issues
    print("\n📋 Test Case 4: Multiple issues")
    metrics4 = {'overall_score': 6}
    diagram_contents4 = {
        'class': 'Not generated',
        'sequence': 'Error reading file: File not found',
        'activity': '@startuml\nstart\n:action;\nstop\n@enduml'
    }
    
    result4 = ValidationHandler.apply_diagram_penalties(metrics4, diagram_contents4)
    print(f"Original Score: {metrics4['overall_score']}")
    print(f"Final Score: {result4['overall_score']}")
    print(f"Penalties: {result4.get('penalties_applied', {}).get('total_penalty', 0)}")
    print(f"Penalty Notes: {result4.get('penalties_applied', {}).get('penalty_notes', [])}")
    
    print("\n" + "=" * 50)
    print("✅ Penalty system test completed!")
    print("\n🎯 Expected behavior:")
    print("- Missing diagrams: -5 points each")
    print("- Error diagrams: -3 points each")
    print("- Minimum score: 0 (no negative scores)")

if __name__ == "__main__":
    test_penalty_system()