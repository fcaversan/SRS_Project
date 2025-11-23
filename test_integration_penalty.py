#!/usr/bin/env python3
"""
Integration Test for ValidationHandler with p2_design_agent

This script tests the enhanced validation system with penalty logic
integrated into the main workflow.
"""

import os
from p2_design_agent import UMLDiagramAutomation

def test_integrated_validation():
    """Test the integrated validation with penalty system."""
    print("🧪 Testing ValidationHandler Integration with p2_design_agent")
    print("=" * 60)
    
    try:
        # Initialize the automation system
        agent = UMLDiagramAutomation()
        agent.setup_gemini()
        agent.setup_directories()
        
        print("✅ System initialized successfully!")
        
        # Test with a simple requirement slice
        test_requirements = """
        User Authentication Requirements:
        
        1. The system shall provide login functionality
        2. Users must authenticate with email/password
        3. Failed login attempts shall be tracked
        4. Session management shall be implemented
        """
        
        print("\n🚀 Testing validation with penalty system...")
        print("Requirements slice: User Authentication")
        
        # Run the iteration (this will generate diagrams and apply penalties)
        result = agent.generate_diagrams_from_requirements_slice(
            test_requirements,
            "UserAuth_ValidationTest"
        )
        
        # Check the results
        print("\n📊 Integration Test Results:")
        print("=" * 40)
        
        diagrams = result.get('diagrams', {})
        validation = result.get('validation', {})
        metrics = validation.get('metrics', {}) if validation else {}
        
        print(f"Diagrams Generated: {len([d for d in diagrams.values() if 'error' not in d])}/3")
        print(f"Validation Score: {validation.get('consistency_score', 'N/A')}/10")
        
        # Show penalty information if applied
        penalties = metrics.get('penalties_applied')
        if penalties:
            print(f"\n📋 Penalty System Active:")
            print(f"Original Score: {metrics.get('original_overall_score', 'N/A')}/10")
            print(f"Penalties Applied: -{penalties.get('total_penalty', 0)} points")
            print(f"Final Score: {metrics.get('overall_score', 'N/A')}/10")
            
            penalty_notes = penalties.get('penalty_notes', [])
            if penalty_notes:
                print("Penalty Details:")
                for note in penalty_notes:
                    print(f"  - {note}")
        else:
            print("✅ No penalties applied - all diagrams generated successfully!")
        
        # Check if report was generated
        report_path = result.get('report_path')
        if report_path and os.path.exists(report_path):
            print(f"\n📄 Report generated: {report_path}")
            
            # Read a snippet of the report to verify penalty info is included
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'Penalties Applied' in content:
                print("✅ Penalty information included in report")
            else:
                print("ℹ️  No penalty information in report (no penalties applied)")
        
        print("\n🎉 Integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

if __name__ == "__main__":
    test_integrated_validation()