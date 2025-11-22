#!/usr/bin/env python3
"""
Test script for the cleaned up SRS automation workflow
"""

from p1_requirements_agent import GeminiAutomation
import os
import sys

def test_cleaned_workflow():
    """Test the cleaned SRS automation workflow"""
    try:
        print("=" * 60)
        print("TESTING CLEANED SRS AUTOMATION WORKFLOW")
        print("=" * 60)
        
        # Check if URD file exists
        if not os.path.exists("URD.txt"):
            print("❌ URD.txt not found")
            print("Please run 'python urd_generator.py' first")
            return False
        
        print("✓ URD.txt found")
        
        # Initialize the automation class
        automator = GeminiAutomation()
        
        # Test that URD-related methods are removed
        try:
            automator.run_automation("test")
            print("❌ run_automation method still exists (should be removed)")
            return False
        except AttributeError:
            print("✓ run_automation method removed successfully")
        
        try:
            automator.save_to_file("test", "test")
            print("❌ save_to_file method still exists (should be removed)")
            return False
        except AttributeError:
            print("✓ save_to_file method removed successfully")
        
        # Test that SRS methods still exist
        required_methods = [
            'run_srs_generation',
            'run_srs_validation', 
            'run_srs_review',
            'get_next_srs_version'
        ]
        
        for method_name in required_methods:
            if hasattr(automator, method_name):
                print(f"✓ {method_name} method exists")
            else:
                print(f"❌ {method_name} method missing")
                return False
        
        # Test version detection
        next_version = automator.get_next_srs_version("SRS")
        print(f"✓ Version detection working: {next_version}")
        
        print()
        print("=" * 60)
        print("CLEANED WORKFLOW TEST PASSED!")
        print("=" * 60)
        print("The cleaned automation workflow is ready:")
        print("- URD generation moved to separate file")
        print("- Main automation focuses on SRS → Validation → Review")
        print("- All required methods are present")
        print("- Obsolete methods removed")
        
        return True
        
    except Exception as e:
        print(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_cleaned_workflow()
    if not success:
        sys.exit(1)