# SRS Automation Project

Comprehensive automation system for Software Requirements Specification (SRS) workflows using Google Gemini 2.5 Pro, spanning from requirements engineering through software design.

## 🎯 **Project Overview**

This project provides end-to-end automation for software engineering workflows:

- **Phase 1: Requirements Engineering** (`p1_requirements_agent.py`) - SRS generation, validation, and iterative improvement
- **Phase 2: Software Design** (`p2_design_agent.py`) - UML diagram generation from SRS specifications

## 📁 **Project Structure**

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed organization and file descriptions.

### **Core Automation Agents:**
- **`p1_requirements_agent.py`** - Main SRS automation workflow (Generation → Validation → Review)
- **`p2_design_agent.py`** - UML diagram generation from any SRS format
- **`urd_generator.py`** - User Requirements Document generator

## Setup Instructions

1. **Get a Google AI API Key:**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a new API key
   - Copy the API key

2. **Set up your API Key:**
   - Copy `.env.example` to `.env`
   - Replace `your_api_key_here` with your actual API key
   - Or set the `GOOGLE_API_KEY` environment variable

3. **Install Dependencies:**
   ```bash
   pip install google-generativeai python-dotenv PyPDF2
   ```

## Usage Workflow

### Step 1: Generate URD (Run Once)
```bash
python urd_generator.py
```
This creates `URD.txt` with user requirements based on an initial prompt.

### Step 2: Run SRS Automation Workflow
```bash
python p1_requirements_agent.py
```
This automatically handles the complete SRS workflow:
- **SRS Generation**: URD + IEEE Standard → `SRS_v1.txt`
- **SRS Validation**: Validates SRS quality → `SRSVR_v1.txt`
- **SRS Review**: Improves SRS based on feedback → `SRS_v2.txt`

## Files Generated

| File | Description |
|------|-------------|
| `URD.txt` | User Requirements Document |
| `SRS_v1.txt` | Initial Software Requirements Specification |
| `SRSVR_v1.txt` | SRS Validation Report |
| `SRS_v2.txt` | Improved SRS addressing validation feedback |
| `SRS_v3.txt...` | Further iterations (if needed) |

## Automation Features

- ✅ **URD Generation** from initial user prompts
- ✅ **SRS Creation** following IEEE 830-1998 standard
- ✅ **Quality Validation** with detailed feedback
- ✅ **Automated Review** and improvement
- ✅ **Version Management** for iterative development
- ✅ **Error Detection** with pass/fail validation

## Advanced Usage

### Iterative Improvement
To create additional SRS versions:
1. Run validation on the latest SRS version
2. Use the validation report to review and improve
3. Repeat until validation passes

### Custom Workflows
```python
from p1_requirements_agent import GeminiAutomation

automator = GeminiAutomation()

# Generate SRS
srs = automator.run_srs_generation("URD.txt", "830-1998.pdf", "SRS_v1.txt")

# Validate SRS
validation = automator.run_srs_validation("URD.txt", "SRS_v1.txt", "830-1998.pdf")

# Review and improve
improved_srs = automator.run_srs_review("SRS_v1.txt", "SRSVR_v1.txt")
```

## Error Handling

The validation system provides:
- Detailed error reports with specific issues
- Error count tags (`<errors: #>`) for automated processing
- Pass/fail determination based on validation results
- Specific recommendations for improvement

## Next Steps

This workflow provides a foundation for:
- Automated requirements engineering
- Quality assurance in SRS development
- Iterative document improvement
- Standards compliance verification