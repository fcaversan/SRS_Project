#!/usr/bin/env python3
"""
Test script for SRS Validation functionality
"""

from p1_requirements_agent import GeminiAutomation
import os
import sys

def test_srs_validation():
    """Test the SRS validation process"""
    try:
        print("=" * 60)
        print("TESTING SRS VALIDATION FUNCTIONALITY")
        print("=" * 60)
        
        # Initialize the automation class
        automator = GeminiAutomation()
        
        # Check if required files exist
        required_files = ["URD.txt", "SRS_v1.txt", "830-1998.pdf"]
        missing_files = []
        
        for file_name in required_files:
            if not os.path.exists(file_name):
                missing_files.append(file_name)
        
        if missing_files:
            print(f"Missing required files: {', '.join(missing_files)}")
            print("Please ensure these files exist before running validation.")
            return False
        
        print("All required files found!")
        print("Running SRS validation...")
        print()
        
        # Run the validation
        validation_report = automator.run_srs_validation(
            urd_file_path="URD.txt",
            srs_file_path="SRS_v1.txt",
            pdf_file_path="830-1998.pdf",
            output_file="SRSVR_v1.txt"
        )
        
        print()
        print("=" * 60)
        print("VALIDATION TEST COMPLETED!")
        print("=" * 60)
        
        # Check if validation report was created
        report_path = os.path.join("reports", "SRSVR_v1.txt")
        if os.path.exists(report_path):
            file_size = os.path.getsize(report_path)
            print(f"✓ {report_path} - {file_size} bytes")
            
            # Extract and display error count
            error_count = automator.extract_error_count(validation_report)
            if error_count >= 0:
                print(f"✓ Error count extracted: {error_count}")
                if error_count == 0:
                    print("🎉 SRS validation PASSED!")
                else:
                    print(f"⚠️  SRS validation FAILED with {error_count} errors")
            else:
                print("⚠️  Could not extract error count")
        else:
            print("✗ reports/SRSVR_v1.txt - Not created")
            return False
        
        print()
        print("SRS validation test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Validation test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_srs_validation()
    if not success:
        sys.exit(1)