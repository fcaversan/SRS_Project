"""
Refinement Loop Module for UML Diagram Automation

This module handles the iterative refinement process to improve diagrams
based on QA feedback.
"""

import os
from typing import Dict, Any


class RefinementLoop:
    """Handles iterative diagram refinement based on QA feedback."""
    
    def __init__(self, diagram_generator):
        """
        Initialize the refinement loop with a reference to the diagram generator.
        
        Args:
            diagram_generator: Instance of UMLDiagramAutomation
        """
        self.generator = diagram_generator
    
    def refine_diagram_with_feedback(self, diagram_type: str, requirements: str, 
                                    current_diagram_info: Dict, qa_metrics: Dict, 
                                    slice_name: str, iteration_num: int) -> Dict[str, str]:
        """
        Refine a single diagram based on QA feedback.
        
        Args:
            diagram_type (str): Type of diagram (class, sequence, activity)
            requirements (str): Original requirements
            current_diagram_info (Dict): Current diagram info with puml path
            qa_metrics (Dict): QA validation metrics
            slice_name (str): Name of the requirements slice
            iteration_num (int): Current iteration number (for versioning)
            
        Returns:
            Dict: New diagram info with paths to refined files
        """
        try:
            # Read current PlantUML
            current_puml_path = current_diagram_info.get('puml')
            if not current_puml_path or not os.path.exists(current_puml_path):
                raise Exception(f"Current PlantUML file not found: {current_puml_path}")
            
            with open(current_puml_path, 'r', encoding='utf-8') as f:
                current_puml = f.read()
            
            print(f"  🔄 Refining {diagram_type} diagram (iteration {iteration_num})...")
            
            # Generate Design Reviewer prompt
            from prompt_generator import PromptGenerator
            reviewer_prompt = PromptGenerator.generate_design_reviewer_prompt(
                requirements, current_puml, qa_metrics, diagram_type, iteration_num
            )
            
            # Get improved PlantUML from Gemini
            improved_puml = self.generator.send_prompt(reviewer_prompt)
            improved_puml = self.generator.extract_plantuml_code(improved_puml)
            
            # Save with version number
            version_suffix = f"_v{iteration_num}"
            filename = f"{slice_name}{version_suffix}_{diagram_type}_diagram"
            puml_path = self.generator.save_puml_file(diagram_type, improved_puml, filename)
            
            # Generate image
            image_path = self.generator.generate_image_from_puml(puml_path)
            
            print(f"  ✅ Refined {diagram_type} diagram saved: {puml_path}")
            
            return {
                'puml': puml_path,
                'image': image_path,
                'type': f'{diagram_type.capitalize()} Diagram (v{iteration_num})',
                'version': f'v{iteration_num}'
            }
            
        except Exception as e:
            print(f"  ❌ Failed to refine {diagram_type} diagram: {e}")
            return {'error': str(e), 'version': f'v{iteration_num}'}
    
    def run_iterative_refinement(self, requirements_slice: str, slice_name: str = "RequirementSlice", 
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
        print(f"\n{'='*70}")
        print(f"🔄 ITERATIVE REFINEMENT LOOP: {slice_name}")
        print(f"{'='*70}")
        print(f"Max iterations: {max_iterations} | Target score: {target_score}/10\n")
        
        iteration_history = {
            'slice_name': slice_name,
            'requirements': requirements_slice,
            'iterations': [],
            'max_iterations': max_iterations,
            'target_score': target_score,
            'final_score': 0,
            'total_iterations': 0,
            'target_achieved': False
        }
        
        try:
            # ITERATION 1: Generate initial diagrams
            print(f"🚀 ITERATION 1: Generating initial diagrams...")
            
            iteration_1_result = {
                'iteration_num': 1,
                'version': 'v1',
                'diagrams': {},
                'validation': None
            }
            
            # Generate initial diagrams with v1 versioning
            print(f"\n📊 Generating Class Diagram (v1)...")
            try:
                class_result = self.generator.generate_structure_diagram(
                    requirements_slice,
                    f"{slice_name}_v1_class_diagram"
                )
                iteration_1_result['diagrams']['class'] = class_result
                print(f"✅ Class Diagram: {class_result['image']}")
            except Exception as e:
                print(f"❌ Class Diagram failed: {e}")
                iteration_1_result['diagrams']['class'] = {'error': str(e)}
                return iteration_history

            print(f"\n🔄 Generating Sequence Diagram (v1)...")
            try:
                sequence_result = self.generator.generate_interaction_diagram(
                    f"{slice_name} Interactions",
                    requirements_slice,
                    f"{slice_name}_v1_sequence_diagram"
                )
                iteration_1_result['diagrams']['sequence'] = sequence_result
                print(f"✅ Sequence Diagram: {sequence_result['image']}")
            except Exception as e:
                print(f"❌ Sequence Diagram failed: {e}")
                iteration_1_result['diagrams']['sequence'] = {'error': str(e)}

            print(f"\n🔀 Generating Activity Diagram (v1)...")
            try:
                activity_result = self.generator.generate_logic_diagram(
                    requirements_slice,
                    f"{slice_name} Workflow",
                    f"{slice_name}_v1_activity_diagram"
                )
                iteration_1_result['diagrams']['activity'] = activity_result
                print(f"✅ Activity Diagram: {activity_result['image']}")
            except Exception as e:
                print(f"❌ Activity Diagram failed: {e}")
                iteration_1_result['diagrams']['activity'] = {'error': str(e)}

            # Validate iteration 1
            print(f"\n🔍 Validating iteration 1...")
            validation_result = self.generator.validate_diagram_consistency(
                requirements_slice,
                iteration_1_result['diagrams'],
                slice_name,
                custom_validation_prompt
            )
            iteration_1_result['validation'] = validation_result
            
            # Save iteration 1 QA report
            from validation_handler import ValidationHandler
            qa_report_path = ValidationHandler.save_iteration_qa_report(validation_result, slice_name, 1)
            iteration_1_result['qa_report_path'] = qa_report_path
            
            current_score = validation_result.get('metrics', {}).get('overall_score', 0)
            print(f"\n✅ Iteration 1 Complete. Overall Score: {current_score}/10")
            
            iteration_history['iterations'].append(iteration_1_result)
            iteration_history['final_score'] = current_score
            iteration_history['total_iterations'] = 1
            
            # Check if target achieved
            if current_score >= target_score:
                print(f"\n🎉 Target score {target_score}/10 achieved! Stopping refinement.")
                iteration_history['target_achieved'] = True
                return iteration_history
            
            # ITERATIONS 2-N: Refinement loop
            for iteration_num in range(2, max_iterations + 1):
                print(f"\n{'='*70}")
                print(f"🔄 ITERATION {iteration_num}: Refining diagrams based on QA feedback...")
                print(f"{'='*70}")
                
                previous_iteration = iteration_history['iterations'][-1]
                previous_metrics = previous_iteration['validation'].get('metrics', {})
                
                current_iteration = {
                    'iteration_num': iteration_num,
                    'version': f'v{iteration_num}',
                    'diagrams': {},
                    'validation': None
                }
                
                # Refine each diagram type
                for diagram_type in ['class', 'sequence', 'activity']:
                    if diagram_type in previous_iteration['diagrams'] and 'error' not in previous_iteration['diagrams'][diagram_type]:
                        refined_diagram = self.refine_diagram_with_feedback(
                            diagram_type,
                            requirements_slice,
                            previous_iteration['diagrams'][diagram_type],
                            previous_metrics,
                            slice_name,
                            iteration_num
                        )
                        current_iteration['diagrams'][diagram_type] = refined_diagram
                    else:
                        print(f"  ⚠️  Skipping {diagram_type} (previous iteration failed)")
                        current_iteration['diagrams'][diagram_type] = {'error': 'Previous iteration failed'}
                
                # Validate refined diagrams
                print(f"\n🔍 Validating iteration {iteration_num}...")
                validation_result = self.generator.validate_diagram_consistency(
                    requirements_slice,
                    current_iteration['diagrams'],
                    slice_name,
                    custom_validation_prompt
                )
                current_iteration['validation'] = validation_result
                
                # Save iteration QA report
                qa_report_path = ValidationHandler.save_iteration_qa_report(validation_result, slice_name, iteration_num)
                current_iteration['qa_report_path'] = qa_report_path
                
                current_score = validation_result.get('metrics', {}).get('overall_score', 0)
                previous_score = previous_metrics.get('overall_score', 0)
                score_delta = current_score - previous_score
                
                print(f"\n✅ Iteration {iteration_num} Complete.")
                print(f"   Overall Score: {current_score}/10 (Δ {score_delta:+d})")
                
                iteration_history['iterations'].append(current_iteration)
                iteration_history['final_score'] = current_score
                iteration_history['total_iterations'] = iteration_num
                
                # Check if target achieved
                if current_score >= target_score:
                    print(f"\n🎉 Target score {target_score}/10 achieved! Stopping refinement.")
                    iteration_history['target_achieved'] = True
                    break
            
            # Final summary
            print(f"\n{'='*70}")
            print(f"📊 REFINEMENT LOOP COMPLETE")
            print(f"{'='*70}")
            print(f"Total iterations: {iteration_history['total_iterations']}")
            print(f"Final score: {iteration_history['final_score']}/10")
            print(f"Target achieved: {'Yes ✅' if iteration_history['target_achieved'] else 'No ❌'}")
            
            return iteration_history
            
        except Exception as e:
            print(f"\n❌ Refinement loop failed: {e}")
            iteration_history['error'] = str(e)
            return iteration_history
