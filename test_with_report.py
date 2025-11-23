#!/usr/bin/env python3
"""
Test script that generates diagrams and saves a detailed QA report
"""

import os
from p2_design_agent import UMLDiagramAutomation

def test_with_qa_report():
    """Generate diagrams and save QA validation report."""
    
    print("🧪 Running test with QA report generation")
    print("="*60)
    
    try:
        agent = UMLDiagramAutomation()
        agent.setup_directories()
        agent.setup_gemini()
        agent.verify_plantuml_installation()
        
        # Test requirements
        requirements = """
The system shall allow users to log in using their email and password. 
If the password is correct, the user is redirected to the dashboard. 
If incorrect, an error message is shown.
The system shall track login attempts and lock the account after 3 failed attempts.
"""
        
        print("\n📊 Generating diagrams and validation report...")
        result = agent.generate_diagrams_from_requirements_slice(
            requirements, 
            "Login_Authentication"
        )
        
        # Save the detailed report
        all_results = [result]
        agent.save_workflow_summary_report(all_results, "qa_validation_report.md")
        
        # Also print the metrics to console
        validation = result.get('validation', {})
        metrics = validation.get('metrics', {})
        
        print("\n" + "="*60)
        print("📊 QA VALIDATION METRICS")
        print("="*60)
        print(f"Overall Score:      {metrics.get('overall_score', 'N/A')}/10")
        print(f"Consistency Score:  {metrics.get('consistency_score', 'N/A')}/10")
        print(f"Completeness Score: {metrics.get('completeness_score', 'N/A')}/10")
        print(f"Quality Score:      {metrics.get('quality_score', 'N/A')}/10")
        print("\n📄 Full report saved to: reports/qa_validation_report.md")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_with_qa_report()
