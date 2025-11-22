#!/usr/bin/env python3
"""
Test script for SRS Review functionality
"""

from p1_requirements_agent import GeminiAutomation
import os
import sys

def test_srs_review():
    """Test the SRS review process"""
    try:
        print("=" * 60)
        print("TESTING SRS REVIEW FUNCTIONALITY")
        print("=" * 60)
        
        # Initialize the automation class
        automator = GeminiAutomation()
        
        # Check if required files exist
        required_files = ["SRS_v1.txt", "SRSVR_v1.txt"]
        missing_files = []
        
        for file_name in required_files:
            if not os.path.exists(file_name):
                missing_files.append(file_name)
        
        if missing_files:
            print(f"Missing required files: {', '.join(missing_files)}")
            print("Please ensure these files exist before running SRS review.")
            print("Run SRS generation and validation first.")
            return False
        
        print("All required files found!")
        
        # Test version detection
        print("Testing version detection...")
        next_version = automator.get_next_srs_version("SRS")
        print(f"Next SRS version will be: {next_version}")
        
        print()
        print("Running SRS review...")
        print()
        
        # Run the SRS review
        reviewed_srs = automator.run_srs_review(
            srs_file_path="SRS_v1.txt",
            validation_report_path="SRSVR_v1.txt"
        )
        
        print()
        print("=" * 60)
        print("SRS REVIEW TEST COMPLETED!")
        print("=" * 60)
        
        # Check if the new SRS version was created
        if os.path.exists(next_version):
            file_size = os.path.getsize(next_version)
            print(f"✓ {next_version} - {file_size} bytes")
            
            # Compare file sizes to see if improvements were made
            original_size = os.path.getsize("SRS_v1.txt")
            print(f"Original SRS (v1): {original_size} bytes")
            print(f"Reviewed SRS ({next_version}): {file_size} bytes")
            
            if file_size > original_size:
                print(f"✓ Reviewed SRS is larger (+{file_size - original_size} bytes) - likely more detailed")
            elif file_size < original_size:
                print(f"✓ Reviewed SRS is smaller (-{original_size - file_size} bytes) - possibly more concise")
            else:
                print("✓ Reviewed SRS is similar in size")
                
        else:
            print(f"✗ {next_version} - Not created")
            return False
        
        print()
        print("SRS review test completed successfully!")
        print("The improved SRS should address all validation feedback.")
        return True
        
    except Exception as e:
        print(f"SRS review test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_srs_review()
    if not success:
        sys.exit(1)