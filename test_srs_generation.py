#!/usr/bin/env python3
"""
Test script for SRS Generation functionality
"""

from p1_requirements_agent import GeminiAutomation
import os
import sys

def test_srs_generation():
    """Test the SRS generation process"""
    try:
        print("=" * 60)
        print("TESTING SRS GENERATION FUNCTIONALITY")
        print("=" * 60)
        
        # Initialize the automation class
        automator = GeminiAutomation()
        
        # Test with sample URD
        print("Running SRS generation test with sample URD...")
        print()
        
        srs_content = automator.test_srs_generation_with_sample_urd()
        
        print()
        print("=" * 60)
        print("TEST COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("Generated files:")
        
        # Check generated files
        files_to_check = ["URD.txt", "SRS_v1.txt"]
        for file_name in files_to_check:
            if os.path.exists(file_name):
                file_size = os.path.getsize(file_name)
                print(f"✓ {file_name} - {file_size} bytes")
            else:
                print(f"✗ {file_name} - Not found")
        
        print()
        print("SRS generation test completed!")
        
        return True
        
    except Exception as e:
        print(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_srs_generation()
    if not success:
        sys.exit(1)