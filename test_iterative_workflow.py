#!/usr/bin/env python3
"""
Test script for Iterative SRS Improvement workflow
"""

from gemini_automation import GeminiAutomation
import os
import sys

def test_iterative_workflow():
    """Test the iterative SRS improvement process"""
    try:
        print("=" * 60)
        print("TESTING ITERATIVE SRS IMPROVEMENT WORKFLOW")
        print("=" * 60)
        
        # Check if URD file exists
        if not os.path.exists("URD.txt"):
            print("❌ URD.txt not found")
            print("Please run 'python urd_generator.py' first")
            return False
        
        print("✓ URD.txt found")
        
        # Initialize the automation class
        automator = GeminiAutomation()
        
        # Test the iterative improvement method exists
        if hasattr(automator, 'run_iterative_srs_improvement'):
            print("✓ run_iterative_srs_improvement method exists")
        else:
            print("❌ run_iterative_srs_improvement method missing")
            return False
        
        # Clean up any existing SRS/SRSVR files for fresh test
        print("🧹 Cleaning up existing SRS/SRSVR files for fresh test...")
        for i in range(1, 11):
            for file_pattern in [f"SRS_v{i}.txt", f"SRSVR_v{i}.txt"]:
                if os.path.exists(file_pattern):
                    os.remove(file_pattern)
                    print(f"   Removed {file_pattern}")
        
        print()
        print("🚀 Starting iterative improvement test (limited to 3 iterations for testing)...")
        
        # Run iterative improvement with limited iterations for testing
        results = automator.run_iterative_srs_improvement(
            max_iterations=3,  # Limited for testing
            target_errors=0
        )
        
        print()
        print("=" * 60)
        print("ITERATIVE WORKFLOW TEST RESULTS")
        print("=" * 60)
        
        # Verify results
        if results:
            print(f"✓ Process completed")
            print(f"✓ Final version: {results['final_version']}")
            print(f"✓ Error count: {results['final_error_count']}")
            print(f"✓ Iterations: {results['iterations_completed']}")
            print(f"✓ Target reached: {results['target_reached']}")
            
            # Check if files were created
            final_srs = results['final_srs_file']
            final_srsvr = results['final_srsvr_file']
            
            if os.path.exists(final_srs):
                size = os.path.getsize(final_srs)
                print(f"✓ Final SRS created: {final_srs} ({size} bytes)")
            else:
                print(f"❌ Final SRS not found: {final_srs}")
                return False
            
            if os.path.exists(final_srsvr):
                size = os.path.getsize(final_srsvr)
                print(f"✓ Final SRSVR created: {final_srsvr} ({size} bytes)")
            else:
                print(f"❌ Final SRSVR not found: {final_srsvr}")
                return False
            
            # Show all generated files
            print()
            print("📁 Generated files:")
            for i in range(1, results['final_version'] + 1):
                srs_file = f"SRS_v{i}.txt"
                srsvr_file = f"SRSVR_v{i}.txt"
                
                if os.path.exists(srs_file):
                    print(f"   ✓ {srs_file}")
                if os.path.exists(srsvr_file):
                    print(f"   ✓ {srsvr_file}")
            
            return True
        else:
            print("❌ No results returned")
            return False
        
    except Exception as e:
        print(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_iterative_workflow()
    if not success:
        sys.exit(1)
    else:
        print()
        print("🎉 Iterative workflow test completed successfully!")
        print("The system can now automatically improve SRS documents until quality targets are met.")