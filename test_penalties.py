#!/usr/bin/env python3
"""
Quick test to verify penalty calculation works correctly
"""

from validation_handler import ValidationHandler

# Test 1: All diagrams present and valid
print("Test 1: All diagrams valid")
metrics1 = {'overall_score': 10}
diagram_contents1 = {
    'class': '@startuml\nclass User\n@enduml',
    'sequence': '@startuml\nUser -> API\n@enduml',
    'activity': '@startuml\nstart\n:Login;\nstop\n@enduml'
}
result1 = ValidationHandler.apply_diagram_penalties(metrics1, diagram_contents1)
print(f"  Original: {metrics1['overall_score']}/10")
print(f"  After penalties: {result1['overall_score']}/10")
print(f"  Penalties: {result1['penalties_applied']}")
print()

# Test 2: One missing diagram
print("Test 2: One missing diagram")
metrics2 = {'overall_score': 10}
diagram_contents2 = {
    'class': 'Not generated',
    'sequence': '@startuml\nUser -> API\n@enduml',
    'activity': '@startuml\nstart\n:Login;\nstop\n@enduml'
}
result2 = ValidationHandler.apply_diagram_penalties(metrics2, diagram_contents2)
print(f"  Original: {metrics2['overall_score']}/10")
print(f"  After penalties: {result2['overall_score']}/10")
print(f"  Penalties: {result2['penalties_applied']}")
print()

# Test 3: One diagram with error
print("Test 3: One diagram with error")
metrics3 = {'overall_score': 10}
diagram_contents3 = {
    'class': '@startuml\nclass User\n@enduml',
    'sequence': 'Error reading file: syntax error',
    'activity': '@startuml\nstart\n:Login;\nstop\n@enduml'
}
result3 = ValidationHandler.apply_diagram_penalties(metrics3, diagram_contents3)
print(f"  Original: {metrics3['overall_score']}/10")
print(f"  After penalties: {result3['overall_score']}/10")
print(f"  Penalties: {result3['penalties_applied']}")
print()

# Test 4: One missing + one error
print("Test 4: One missing + one error")
metrics4 = {'overall_score': 10}
diagram_contents4 = {
    'class': 'Not generated',
    'sequence': 'Diagram generation failed',
    'activity': '@startuml\nstart\n:Login;\nstop\n@enduml'
}
result4 = ValidationHandler.apply_diagram_penalties(metrics4, diagram_contents4)
print(f"  Original: {metrics4['overall_score']}/10")
print(f"  After penalties: {result4['overall_score']}/10")
print(f"  Penalties: {result4['penalties_applied']}")
print()

# Test 5: All diagrams missing
print("Test 5: All diagrams missing")
metrics5 = {'overall_score': 10}
diagram_contents5 = {
    'class': 'Not generated',
    'sequence': 'Not generated',
    'activity': 'Not generated'
}
result5 = ValidationHandler.apply_diagram_penalties(metrics5, diagram_contents5)
print(f"  Original: {metrics5['overall_score']}/10")
print(f"  After penalties: {result5['overall_score']}/10")
print(f"  Penalties: {result5['penalties_applied']}")
print()

print("All tests completed!")
