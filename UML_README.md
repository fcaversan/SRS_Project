# UML Diagram Generation Automation

This module provides automated generation of UML diagrams using Google Gemini 2.5 Pro and PlantUML for software design documentation.

## Features

### Supported UML Diagram Types
- **Use Case Diagrams**: System functionality from user perspective
- **Class Diagrams**: System structure and class relationships  
- **Sequence Diagrams**: Interaction flows between objects
- **Activity Diagrams**: Workflow and business processes
- **Component Diagrams**: System architecture components
- **State Diagrams**: Object state transitions
- **Deployment Diagrams**: Physical system deployment
- **Object Diagrams**: Instance relationships
- **Communication Diagrams**: Message passing between objects
- **Timing Diagrams**: Time-based interactions

### Key Capabilities
- ✅ Generate PlantUML code from SRS documents using AI
- ✅ Automatic image generation (PNG format)
- ✅ Organized file structure by diagram type
- ✅ Custom prompt support for specialized diagrams
- ✅ Batch generation of multiple diagram types
- ✅ Error handling and validation

## Prerequisites

1. **Java 17+** (for PlantUML)
2. **PlantUML JAR** (installed in `plantuml/plantuml.jar`)
3. **Google AI API Key** (for Gemini access)
4. **Python packages**: `google-generativeai`, `python-dotenv`

## Quick Start

### 1. Setup Environment
```bash
# Ensure .env file contains your API key
echo "GOOGLE_API_KEY=your_api_key_here" >> .env
```

### 2. Basic Usage
```python
from uml_automation import UMLDiagramAutomation

# Initialize
uml_gen = UMLDiagramAutomation()
uml_gen.setup_gemini()
uml_gen.setup_directories()
uml_gen.verify_plantuml_installation()

# Read SRS content
srs_content = uml_gen.read_srs_file("SRS_v5.txt")

# Generate a use case diagram
result = uml_gen.generate_diagram("usecase", srs_content)
print(f"Generated: {result['puml']} -> {result['image']}")
```

### 3. Custom Prompts
```python
custom_prompt = """
Create a detailed Class Diagram focusing on:
- Domain entities and their relationships
- Service layer architecture
- Data access patterns

SRS CONTENT:
{srs_content}

Generate PlantUML code only:
"""

result = uml_gen.generate_diagram(
    diagram_type="class",
    srs_content=srs_content,
    custom_prompt=custom_prompt,
    filename="domain_model"
)
```

### 4. Batch Generation
```python
# Generate multiple diagrams at once
results = uml_gen.generate_all_diagrams(
    srs_content=srs_content,
    selected_types=["usecase", "class", "sequence", "component"]
)
```

## File Structure

```
uml_diagrams/
├── usecase/
│   ├── usecase_20241120_143022.puml
│   └── usecase_20241120_143022.png
├── class/
│   ├── class_20241120_143045.puml
│   └── class_20241120_143045.png
├── sequence/
│   ├── sequence_20241120_143102.puml
│   └── sequence_20241120_143102.png
└── ... (other diagram types)
```

## Prompt Templates

### Use Case Diagram Prompt
- Focus on actors and system boundaries
- Include primary and secondary use cases
- Show relationships and dependencies

### Class Diagram Prompt  
- Model domain entities and relationships
- Include attributes and key methods
- Show inheritance, composition, aggregation

### Sequence Diagram Prompt
- Model key interaction scenarios
- Show object lifelines and messages
- Include alternative flows

### Activity Diagram Prompt
- Model business processes and workflows
- Show decision points and parallel activities
- Include swim lanes for different actors

### Component Diagram Prompt
- Show system architecture components
- Model interfaces and dependencies
- Include deployment considerations

## Advanced Usage

### Custom Diagram Generation
```python
# Create specialized diagrams with detailed prompts
security_class_prompt = """
Create a Class Diagram focusing specifically on security aspects:
- Authentication and authorization classes
- Security service interfaces
- Encryption and data protection models
- User permission and role management

Based on the SRS requirements for security (section 3.5), generate PlantUML code:

{srs_content}
"""

result = uml_gen.generate_diagram(
    "class", 
    srs_content, 
    security_class_prompt, 
    "security_model"
)
```

### Error Handling
```python
try:
    result = uml_gen.generate_diagram("usecase", srs_content)
except Exception as e:
    print(f"Generation failed: {e}")
    # Handle error appropriately
```

### Listing Generated Diagrams
```python
diagrams = uml_gen.list_generated_diagrams()
for diagram_type, files in diagrams.items():
    print(f"{diagram_type}: {len(files)} files")
```

## Tips for Better Results

### 1. SRS Quality
- Ensure your SRS is comprehensive and well-structured
- Include functional and non-functional requirements
- Specify system interfaces and constraints

### 2. Custom Prompts
- Be specific about what aspects to focus on
- Mention specific SRS sections to reference
- Request specific PlantUML features (stereotypes, colors, etc.)

### 3. Iterative Refinement
- Generate initial diagrams with default prompts
- Review and identify areas for improvement
- Create custom prompts for specialized views

### 4. PlantUML Syntax
- The AI generates PlantUML code following best practices
- You can manually edit .puml files if needed
- Regenerate images after manual edits using PlantUML

## Troubleshooting

### Common Issues
1. **Java not found**: Ensure Java 17+ is installed and in PATH
2. **PlantUML JAR missing**: Verify `plantuml/plantuml.jar` exists
3. **API key issues**: Check `.env` file and API key validity
4. **Large SRS files**: Consider splitting into sections for better results

### Verification Commands
```bash
# Test Java installation
java -version

# Test PlantUML
java -jar plantuml/plantuml.jar -version

# Test diagram generation
java -jar plantuml/plantuml.jar test.puml
```

## Example Output

The automation generates professional UML diagrams like:

- **Use Case**: Actors, use cases, system boundaries, relationships
- **Class**: Classes with attributes/methods, inheritance hierarchies, associations
- **Sequence**: Object interactions with lifelines and messages
- **Activity**: Workflow with decision points and parallel processes
- **Component**: System architecture with interfaces and dependencies

Each diagram is saved as both PlantUML source (.puml) and rendered image (.png) for documentation and review purposes.