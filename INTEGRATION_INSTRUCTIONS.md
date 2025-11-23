# Integration Instructions for p2_design_agent.py

## Step 1: Add Imports
Add these lines after line 21 (after `from dotenv import load_dotenv`):

```python
# Import modular components
from prompt_generator import PromptGenerator
from validation_handler import ValidationHandler
from refinement_loop import RefinementLoop
```

## Step 2: Add Refinement Loop Method to UMLDiagramAutomation Class
Add this method before the `if __name__ == "__main__":` block (around line 1122):

```python
def iterative_refinement_loop(self, requirements_slice: str, slice_name: str = "RequirementSlice", 
                              max_iterations: int = 5, target_score: int = 10, 
                              custom_validation_prompt: str = None) -> Dict[str, any]:
    """
    Run iterative refinement loop to improve diagrams based on QA feedback.
    
    Args:
        requirements_slice (str): Requirements to process
        slice_name (str): Name identifier for this slice
        max_iterations (int): Maximum number of refinement iterations (default: 5)
        target_score (int): Target overall score to achieve (default: 10)
        custom_validation_prompt (str, optional): Custom validation prompt
        
    Returns:
        Dict: Complete iteration history with all versions and scores
    """
    refinement = RefinementLoop(self)
    return refinement.run_iterative_refinement(
        requirements_slice, slice_name, max_iterations, target_score, custom_validation_prompt
    )
```

## Step 3: Update extract_validation_metrics Method
Replace the existing `extract_validation_metrics` method (around line 899) with:

```python
def extract_validation_metrics(self, validation_report: str) -> Dict[str, any]:
    """Extract validation metrics from the JSON validation report."""
    return ValidationHandler.extract_validation_metrics(validation_report)
```

## Step 4: Update generate_iteration_report_content Method
Replace the existing `generate_iteration_report_content` method (around line 998) with:

```python
def generate_iteration_report_content(self, results: Dict[str, any]) -> str:
    """Generate a markdown report for a single iteration."""
    return ValidationHandler.generate_iteration_report_content(results)
```

## Step 5: Update save_workflow_summary_report Method
Replace the existing `save_workflow_summary_report` method (around line 1051) with:

```python
def save_workflow_summary_report(self, all_iterations: List[Dict[str, any]], filename: str = "design_workflow_summary.md"):
    """Save a summary report of the entire workflow."""
    ValidationHandler.save_workflow_summary_report(all_iterations, filename)
```

## Benefits of This Refactoring:
1. **Modularity**: Code is organized into logical modules
2. **Maintainability**: Easier to find and update specific functionality
3. **Testability**: Each module can be tested independently
4. **Reusability**: Modules can be used in other projects
5. **Smaller Files**: Main file is more manageable

## New Files Created:
- `prompt_generator.py` - All prompt generation logic
- `validation_handler.py` - Validation and reporting logic
- `refinement_loop.py` - Iterative refinement logic
- `test_refinement_loop.py` - Test script for refinement loop

## Testing:
Run the test script to verify everything works:
```bash
python test_refinement_loop.py
```
