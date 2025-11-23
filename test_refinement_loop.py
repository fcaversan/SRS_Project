#!/usr/bin/env python3
"""
Test script for Iterative Refinement Loop with Modular Architecture

This script demonstrates the new modular structure and iterative refinement functionality.
"""

import os
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from p2_design_agent import UMLDiagramAutomation
from refinement_loop import RefinementLoop
from validation_handler import ValidationHandler

def test_refinement_loop():
    """Test the iterative refinement loop with a sample requirement."""
    
    print("🧪 Testing Iterative Refinement Loop")
    print("="*70)
    
    try:
        # Initialize the UML automation
        agent = UMLDiagramAutomation()
        agent.setup_gemini()
        agent.setup_directories()
        agent.verify_plantuml_installation()
        
        print("✅ UML automation initialized successfully!\n")
        
        # Sample requirements
        requirements = """
Login Authentication Requirements:

1. The system shall allow users to log in using their email and password.
2. If the password is correct, the user is redirected to the dashboard.
3. If incorrect, an error message is shown.
4. The system shall track login attempts and lock the account after 3 failed attempts.
5. Users shall be able to reset their password via email.
6. The system shall maintain user sessions using secure tokens.
7. All passwords must be hashed and salted before storage.
"""
        
        slice_name = "Login_Authentication"
        
        # Initialize refinement loop
        refinement = RefinementLoop(agent)
        
        # Run iterative refinement with max 3 iterations for testing
        print(f"🚀 Starting iterative refinement for: {slice_name}")
        print(f"Max iterations: 3 | Target score: 10/10\n")
        
        iteration_history = refinement.run_iterative_refinement(
            requirements_slice=requirements,
            slice_name=slice_name,
            max_iterations=3,  # Reduced for testing
            target_score=10
        )
        
        # Save comprehensive refinement history report
        print("\n📄 Generating refinement history report...")
        report_path = ValidationHandler.save_refinement_history_report(iteration_history)
        
        # Display summary
        print("\n" + "="*70)
        print("📊 REFINEMENT LOOP SUMMARY")
        print("="*70)
        print(f"Slice: {iteration_history.get('slice_name')}")
        print(f"Total Iterations: {iteration_history.get('total_iterations')}")
        print(f"Final Score: {iteration_history.get('final_score')}/10")
        print(f"Target Achieved: {'✅ Yes' if iteration_history.get('target_achieved') else '❌ No'}")
        
        if report_path:
            print(f"\n📄 Full refinement history: {report_path}")
        
        # Show score progression
        print("\n📈 Score Progression:")
        for iteration in iteration_history.get('iterations', []):
            iter_num = iteration.get('iteration_num')
            version = iteration.get('version')
            metrics = iteration.get('validation', {}).get('metrics', {})
            overall = metrics.get('overall_score', 'N/A')
            print(f"  Iteration {iter_num} ({version}): {overall}/10")
        
        print("\n🎉 Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Iterative Refinement Loop Test Suite")
    print("="*70)
    print()
    
    success = test_refinement_loop()
    
    print("\n" + "="*70)
    if success:
        print("✅ All tests passed! Refinement loop is working correctly.")
    else:
        print("❌ Tests failed. Please check the configuration.")
        sys.exit(1)
