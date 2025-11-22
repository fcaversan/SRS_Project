# 📁 Project Organization Structure

This document outlines the organized structure of the SRS automation project, divided by phases and functionality.

## 🎯 **Project Phases Overview**

### **Phase 1: Requirements Engineering** 
- **Main Agent**: `p1_requirements_agent.py`
- **Purpose**: Automate SRS generation, validation, and improvement
- **Input**: URD (User Requirements Document) + IEEE 830-1998 Standard
- **Output**: Validated and improved SRS documents

### **Phase 2: Software Design**
- **Main Agent**: `p2_design_agent.py` 
- **Purpose**: Generate UML diagrams from SRS specifications
- **Input**: SRS documents (any format)
- **Output**: Professional UML diagrams (Class, Sequence, Activity, etc.)

---

## 📂 **File Structure by Category**

### **🤖 Core Automation Agents**
```
├── p1_requirements_agent.py     # Phase 1: SRS automation workflow
└── p2_design_agent.py           # Phase 2: UML diagram generation
```

### **🚀 Workflow Automation Scripts**
```
├── software_design_automation.py    # Generic UML generation from any SRS
├── urd_generator.py                 # Initial URD creation
├── example_uml_usage.py             # UML automation examples
├── specialized_uml_examples.py      # Specialized diagram examples
└── generate_real_diagrams.py        # Quick UML generation tool
```

### **🧪 Test Scripts**
```
├── test_srs_generation.py          # Test SRS generation
├── test_srs_validation.py          # Test SRS validation
├── test_srs_review.py              # Test SRS review
├── test_cleaned_workflow.py        # Test clean workflow
└── test_iterative_workflow.py      # Test iterative improvement
```

### **📄 Documentation**
```
├── README.md                        # Main project documentation
├── UML_README.md                    # UML automation documentation
└── PROJECT_STRUCTURE.md            # This file - project organization
```

### **📊 Input/Output Files**
```
├── URD.txt                          # User Requirements Document
├── SRS_v*.txt                       # Generated SRS versions
├── SRSVR_v*.txt                     # SRS validation reports
├── SRS_sample1.txt                  # Sample SRS for testing
└── uml_diagrams/                    # Generated UML diagrams
    ├── class/                       # Class diagrams
    ├── sequence/                    # Sequence diagrams
    ├── activity/                    # Activity diagrams
    └── ... (other diagram types)
```

### **🔧 Configuration & Tools**
```
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
├── .vscode/settings.json           # VS Code PlantUML configuration
├── plantuml/                        # PlantUML installation
└── test.puml                        # PlantUML test file
```

---

## 🔄 **Workflow Overview**

### **Phase 1: Requirements Engineering Workflow**
```
URD.txt → p1_requirements_agent.py → SRS_v*.txt → SRSVR_v*.txt
   ↓                                      ↓              ↓
User Reqs          Generate SRS       Validate SRS   Review & Improve
                       ↓                    ↓              ↓
                   IEEE 830-1998       Quality Check   Iterative Loop
```

### **Phase 2: Software Design Workflow**  
```
SRS_v*.txt → p2_design_agent.py → uml_diagrams/
     ↓              ↓                    ↓
SRS Content   AI Analysis        Class Diagrams
              ↓                  Sequence Diagrams  
         Extract Sections       Activity Diagrams
              ↓                  Component Diagrams
         Generate PlantUML           ... etc
```

---

## 🎯 **Usage Patterns**

### **For Requirements Phase:**
```bash
# Generate URD (one-time setup)
python urd_generator.py

# Run complete requirements workflow
python p1_requirements_agent.py

# Test specific components
python test_srs_generation.py
python test_srs_validation.py
```

### **For Design Phase:**
```bash
# Generate UML diagrams from any SRS
python software_design_automation.py

# Use specific diagram generation
python p2_design_agent.py

# Run examples and tests
python example_uml_usage.py
python specialized_uml_examples.py
```

---

## 🚀 **Future Phases (Planned)**

### **Phase 3: Implementation** 
- `p3_implementation_agent.py` - Code generation from UML diagrams
- Scaffold generation, API creation, database schemas

### **Phase 4: Testing**
- `p4_testing_agent.py` - Test case generation from requirements
- Unit tests, integration tests, test automation

### **Phase 5: Documentation**
- `p5_documentation_agent.py` - Technical documentation generation
- API docs, user manuals, deployment guides

---

## 📋 **Maintenance Notes**

### **Import Dependencies:**
- All test files import from `p1_requirements_agent`
- All UML files import from `p2_design_agent`
- Update imports when renaming files

### **Configuration:**
- API keys stored in `.env` file (not committed)
- PlantUML configuration in `.vscode/settings.json`
- Java 17+ required for PlantUML functionality

### **Version Control:**
- Generated images (*.png) are ignored by git
- Large files (plantuml.jar) are ignored by git
- Source files (.puml, .txt) are tracked for review