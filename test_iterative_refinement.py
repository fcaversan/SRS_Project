#!/usr/bin/env python3
"""
CORRECTED Iterative Refinement Test - FULL SCALE

This test properly implements iterative refinement by:
1. Generating initial diagrams for all slices
2. Using QA feedback to REFINE existing diagrams (not regenerate)
3. Using the actual refinement_methods workflow
4. Tracking score improvements across iterations for all slices
"""

import os
import sys
from p2_design_agent import UMLDiagramAutomation
from validation_handler import ValidationHandler

def run_full_scale_iterative_refinement_test():
    """Run the CORRECTED iterative refinement test with all slices"""
    
    print("🔧 CORRECTED Iterative Refinement Test - FULL SCALE")
    print("=" * 80)
    print("🎯 This test will actually REFINE diagrams based on QA feedback")
    print("🔄 Instead of generating fresh diagrams each iteration")
    print("📊 ValidationHandler penalty system: -5 missing, -3 errors")
    print("📁 All reports will be saved to 'reports' folder")
    print("🚀 Testing ALL 3 slices with up to 6 iterations")
    print("=" * 80)
    
    try:
        # Initialize the UML automation
        agent = UMLDiagramAutomation()
        agent.setup_gemini()
        agent.setup_directories()
        agent.verify_plantuml_installation()
        
        print("✅ System initialized successfully!\n")
        
        # Use all 3 requirement slices for comprehensive testing
        requirement_slices = [
            {
                "name": "Home_Screen_Vehicle_Status",
                "content": """
3.2.1 FR-HSS: Home Screen & Vehicle Status
FR-HSS-001: The system shall display the vehicle's current State of Charge (SoC) as a percentage value on the application's home screen.
FR-HSS-002: The system shall display a visual representation of the vehicle's battery level.
FR-HSS-003: The system shall display an estimated vehicle range in the user's preferred unit (miles or kilometers).
FR-HSS-004: The estimated vehicle range calculation shall be based on the vehicle's current SoC, recent energy consumption trends, and the current ambient temperature reported by the vehicle.
FR-HSS-005: The system shall display the vehicle's lock status (Locked/Unlocked).
FR-HSS-006: The system shall display the vehicle's interior cabin temperature as reported by the vehicle.
FR-HSS-007: The system shall indicate whether the climate control system is currently active.
FR-HSS-008: The system shall display a clear, graphical representation of the user's vehicle on the home screen.
                """.strip()
            },
            {
                "name": "Charging_Management", 
                "content": """
3.2.2 FR-CHG: Charging Management
FR-CHG-001: The system shall allow the user to remotely start a charging session if the vehicle is plugged into a compatible charger.
FR-CHG-002: The system shall allow the user to remotely stop a charging session.
FR-CHG-003: During an active charging session, the system shall display: current SoC, estimated time to completion, current charging rate (kW), and supplied voltage/amperage.
FR-CHG-004: The system shall provide an interface for the user to set a maximum charging limit as a percentage. The interface shall default to 80% for daily charging and shall provide a convenient one-time "charge to 100%" option for trips.
FR-CHG-005: The system shall allow the user to create, edit, and delete charging schedules, defining a start time or a desired ready-by time.
FR-CHG-006: The system shall display a map of charging stations.
FR-CHG-007: The system shall allow the user to filter charging stations by connector type and power level (kW).
FR-CHG-008: The system shall display real-time availability for charging stations where the data is provided by the network operator.
                """.strip()
            },
            {
                "name": "Remote_Controls", 
                "content": """
3.2.3 FR-RMC: Remote Controls
FR-RMC-001: The system shall allow the user to remotely lock the vehicle's doors.
FR-RMC-002: The system shall allow the user to remotely unlock the vehicle's doors.
FR-RMC-003: The system shall allow the user to remotely activate the vehicle's climate control system (HVAC).
FR-RMC-004: The system shall allow the user to set a target temperature for the cabin.
FR-RMC-005: The system shall allow the user to remotely activate/deactivate heated seats and the heated steering wheel, if equipped.
FR-RMC-006: The system shall allow the user to remotely activate front and rear defrosters.
FR-RMC-007: The system shall display a warning to the user if they attempt to precondition the cabin while the vehicle is not plugged in, indicating the action will consume battery range.
FR-RMC-008: The system shall allow the user to remotely open the front trunk (frunk) and rear trunk.
FR-RMC-009: The system shall provide a function to remotely honk the horn and flash the lights.
FR-RMC-010: The system shall provide haptic feedback on the user's mobile device upon successful completion of a remote lock or unlock command.
                """.strip()
            }
        ]
        
        target_score = 10
        max_iterations = 6
        
        print(f"📋 Processing {len(requirement_slices)} requirement slices:")
        for i, slice_info in enumerate(requirement_slices, 1):
            print(f"  {i}. {slice_info['name']}")
        print(f"🎯 Target score: {target_score}/10")
        print(f"🔄 Max iterations: {max_iterations}\n")
        
        # Process all slices together in iterations
        all_results = []
        iteration = 1
        all_slices_achieved_target = False
        slice_data = {}  # Track data for each slice
        
        # Initialize slice data
        for req_slice in requirement_slices:
            slice_data[req_slice['name']] = {
                'requirements': req_slice['content'],
                'current_diagrams': None,
                'current_validation': None,
                'current_score': 0,
                'scores_history': []
            }
        
        while not all_slices_achieved_target and iteration <= max_iterations:
            print(f"\n🔄 ITERATION {iteration}/{max_iterations} - Processing All Slices")
            print("=" * 70)
            
            iteration_results = []
            all_scores_meet_target = True
            
            for req_slice in requirement_slices:
                slice_name = req_slice['name']
                requirements = req_slice['content']
                
                print(f"\n📊 Processing {slice_name} (Iteration {iteration})")
                print("-" * 50)
                
                if iteration == 1:
                    # STEP 1: Generate initial diagrams
                    print(f"🚀 Generating initial diagrams for {slice_name}...")
                    result = agent.generate_diagrams_from_requirements_slice(
                        requirements,
                        f"{slice_name}_v{iteration}"
                    )
                    
                    if 'error' in result:
                        print(f"❌ Generation failed: {result['error']}")
                        all_scores_meet_target = False
                        continue
                    
                    # Apply ValidationHandler penalties
                    if 'validation' in result and result['validation']:
                        metrics = result['validation'].get('metrics', {})
                        diagrams = result.get('diagrams', {})
                        
                        # Prepare diagram contents for penalty calculation
                        diagram_contents = {}
                        successful_diagrams = 0
                        for diagram_type, diagram_data in diagrams.items():
                            if isinstance(diagram_data, dict):
                                if 'error' in diagram_data:
                                    diagram_contents[diagram_type] = f"Diagram generation failed: {diagram_data['error']}"
                                else:
                                    diagram_contents[diagram_type] = diagram_data.get('content', 'Generated')
                                    successful_diagrams += 1
                            else:
                                diagram_contents[diagram_type] = "Generated"
                                successful_diagrams += 1
                        
                        print(f"📊 Initial Diagrams Generated: {successful_diagrams}/3")
                        
                        # Apply penalties
                        print("⚖️  Applying ValidationHandler penalties...")
                        updated_metrics = ValidationHandler.apply_diagram_penalties(metrics, diagram_contents)
                        result['validation']['metrics'] = updated_metrics
                        
                        current_score = updated_metrics.get('overall_score', 0)
                        original_score = updated_metrics.get('original_overall_score', current_score)
                        penalty_info = updated_metrics.get('penalties_applied', {})
                        
                        print(f"📈 Original AI Score: {original_score}/10")
                        if penalty_info.get('total_penalty', 0) > 0:
                            print(f"🔻 Penalties Applied: -{penalty_info['total_penalty']} points")
                        print(f"🎯 Initial Score: {current_score}/10")
                        
                        # Save QA report
                        qa_report_path = ValidationHandler.save_iteration_qa_report(
                            result['validation'], slice_name, iteration
                        )
                        print(f"📄 QA report saved: {qa_report_path}")
                        
                        # Store slice data
                        slice_data[slice_name]['current_diagrams'] = result.get('diagrams', {})
                        slice_data[slice_name]['current_validation'] = result['validation']
                        slice_data[slice_name]['current_score'] = current_score
                        slice_data[slice_name]['scores_history'].append(current_score)
                        
                        if current_score < target_score:
                            all_scores_meet_target = False
                        
                        print(f"Status: {current_score}/10 ({'TARGET MET' if current_score >= target_score else 'CONTINUE'})")
                
                else:
                    # STEP 2+: Iterative refinement
                    print(f"🔧 Refining diagrams for {slice_name} (iteration {iteration})...")
                    
                    current_diagrams = slice_data[slice_name]['current_diagrams']
                    current_validation = slice_data[slice_name]['current_validation']
                    
                    if not current_diagrams or not current_validation:
                        print(f"❌ No baseline data for {slice_name} refinement")
                        all_scores_meet_target = False
                        continue
                    
                    # Refine each diagram based on QA feedback
                    refined_diagrams = {}
                    refined_successfully = 0
                    
                    for diagram_type in ['class', 'sequence', 'activity']:
                        if diagram_type in current_diagrams and 'error' not in current_diagrams[diagram_type]:
                            print(f"  🔧 Refining {diagram_type} diagram...")
                            
                            refined_result = agent.refine_diagram_with_feedback(
                                diagram_type,
                                requirements,
                                current_diagrams[diagram_type],
                                current_validation['metrics'],
                                slice_name,
                                iteration
                            )
                            
                            if 'error' not in refined_result:
                                refined_diagrams[diagram_type] = refined_result
                                refined_successfully += 1
                                print(f"    ✅ {diagram_type} refined successfully")
                            else:
                                print(f"    ❌ {diagram_type} refinement failed: {refined_result['error']}")
                                refined_diagrams[diagram_type] = current_diagrams[diagram_type]
                        else:
                            print(f"    ⏭️  Skipping {diagram_type} (not available)")
                            refined_diagrams[diagram_type] = current_diagrams.get(diagram_type, {'error': 'Not available'})
                    
                    print(f"  📊 Refined successfully: {refined_successfully}/3")
                    
                    # Re-validate refined diagrams
                    print(f"  📋 Re-validating refined diagrams...")
                    
                    # Prepare only successful diagrams for validation
                    refined_diagram_contents = {}
                    successful_diagrams = []
                    for diagram_type, diagram_info in refined_diagrams.items():
                        if 'error' not in diagram_info and 'puml' in diagram_info:
                            try:
                                with open(diagram_info['puml'], 'r', encoding='utf-8') as f:
                                    puml_content = f.read()
                                    if puml_content.strip() and '@startuml' in puml_content and '@enduml' in puml_content:
                                        refined_diagram_contents[diagram_type] = puml_content
                                        successful_diagrams.append(diagram_type)
                            except Exception as e:
                                print(f"    ⚠️  Skipping {diagram_type} - error reading: {e}")
                    
                    print(f"    📊 Validating {len(successful_diagrams)} successful diagrams")
                    
                    if refined_diagram_contents:
                        validation_result = agent.validate_diagram_consistency(
                            requirements, refined_diagram_contents, slice_name
                        )
                        
                        if validation_result and 'metrics' in validation_result:
                            # Apply penalties
                            updated_metrics = ValidationHandler.apply_diagram_penalties(
                                validation_result['metrics'], refined_diagram_contents
                            )
                            validation_result['metrics'] = updated_metrics
                            
                            new_score = updated_metrics.get('overall_score', 0)
                            old_score = slice_data[slice_name]['current_score']
                            score_change = new_score - old_score
                            
                            print(f"  📈 Score: {old_score}/10 → {new_score}/10 ({'+' if score_change >= 0 else ''}{score_change})")
                            
                            # Save QA report
                            qa_report_path = ValidationHandler.save_iteration_qa_report(
                                validation_result, slice_name, iteration
                            )
                            print(f"  📄 QA report saved: {qa_report_path}")
                            
                            # Update slice data
                            slice_data[slice_name]['current_diagrams'] = refined_diagrams
                            slice_data[slice_name]['current_validation'] = validation_result
                            slice_data[slice_name]['current_score'] = new_score
                            slice_data[slice_name]['scores_history'].append(new_score)
                            
                            if new_score < target_score:
                                all_scores_meet_target = False
                        else:
                            print(f"  ❌ Validation failed")
                            all_scores_meet_target = False
                    else:
                        print(f"  ❌ No successful diagrams to validate")
                        all_scores_meet_target = False
            
            # Check iteration completion
            print(f"\n📊 ITERATION {iteration} SUMMARY:")
            print("=" * 50)
            for slice_name, data in slice_data.items():
                current_score = data['current_score']
                history = data['scores_history']
                status = "✅ TARGET MET" if current_score >= target_score else "🔄 CONTINUE"
                print(f"  {slice_name}: {current_score}/10 {status}")
                print(f"    Score History: {history}")
            
            if all_scores_meet_target:
                print(f"\n🎉 ALL SLICES ACHIEVED TARGET {target_score}/10 IN ITERATION {iteration}!")
                all_slices_achieved_target = True
            elif iteration >= max_iterations:
                print(f"\n⚠️  Maximum iterations reached ({max_iterations})")
                all_slices_achieved_target = True
            else:
                print(f"\n🔄 Moving to iteration {iteration + 1}...")
            
            iteration += 1
        
        # Final results
        print(f"\n🏁 FINAL RESULTS")
        print("=" * 60)
        print(f"🎯 Target Score: {target_score}/10")
        print(f"🔄 Total Iterations: {iteration - 1}")
        
        final_results = {}
        total_improvement = 0
        for slice_name, data in slice_data.items():
            final_score = data['current_score']
            history = data['scores_history']
            improvement = history[-1] - history[0] if len(history) > 1 else 0
            total_improvement += improvement
            
            final_results[slice_name] = {
                'final_score': final_score,
                'target_achieved': final_score >= target_score,
                'score_history': history,
                'improvement': improvement
            }
            
            status = "🎉 SUCCESS" if final_score >= target_score else "⚠️  INCOMPLETE"
            print(f"  {slice_name}: {final_score}/10 {status}")
            print(f"    History: {history}")
            print(f"    Improvement: {'+' if improvement >= 0 else ''}{improvement} points")
        
        avg_improvement = total_improvement / len(requirement_slices)
        print(f"\n📊 OVERALL METRICS:")
        print(f"  Average Improvement: {'+' if avg_improvement >= 0 else ''}{avg_improvement:.1f} points")
        print(f"  Slices Meeting Target: {sum(1 for r in final_results.values() if r['target_achieved'])}/{len(requirement_slices)}")
        
        return final_results
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = run_full_scale_iterative_refinement_test()
    if result:
        print(f"\n✅ Full scale iterative refinement test completed!")
        print(f"Results: {result}")
    else:
        print(f"\n❌ Full scale iterative refinement test failed!")