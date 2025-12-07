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
        
        requirement_slices = [
            {
                "name": "Home_Screen_Vehicle_Status",
                "content": """
1. Introduction
This section provides an overview of the Software Requirements Specification (SRS) for the Vehicle Connect Mobile Application.
1.1 Purpose
The purpose of this document is to provide a detailed description of the requirements for the Vehicle Connect mobile application. It will serve as the guiding document for the design, development, and testing of the software. This SRS defines the functional and non-functional requirements of the system and establishes the agreement between the stakeholders (Vehicle Engineering) and the development team.
1.2 Document Conventions
This SRS document adheres to the IEEE 830-1998 standard. Functional requirements are uniquely identified with the prefix FR- followed by a category code and a number (e.g., FR-CHG-001). Non-functional requirements are identified with the prefix NFR-. The keyword "shall" is used to denote a mandatory requirement.
1.3 Intended Audience and Reading Suggestions
This document is intended for:
Project Managers: To understand the scope and plan the project.
Software Developers: To understand the specific features to be built.
QA & Testing Teams: To create test cases that verify the functionality.
Stakeholders (Vehicle Engineering): To review and confirm that the requirements accurately capture their needs.
It is recommended to read Sections 1 and 2 for a high-level overview before delving into the detailed requirements in Section 3.
1.4 Product Scope
The Vehicle Connect application is a mobile client for iOS and Android platforms that will provide vehicle owners with the ability to remotely monitor, control, and manage their electric vehicle. The scope of this SRS is limited to the mobile application itself. It does not cover the vehicle's onboard telematics unit or the backend cloud infrastructure, which are considered external systems with which this application will interact.
1.5 Overview
This SRS is organized into three main sections. Section 1 provides an introduction, scope, and overview of the document. Section 2 gives an overall description of the product, its constraints, and its dependencies. Section 3 details the specific functional and non-functional requirements that the software must satisfy. The document concludes with a glossary and an index for ease of reference.
1.6 References
User Requirements Document: Vehicle Connect Mobile App, Version 1.0, October 6, 2025.
IEEE Std 830-1998, Recommended Practice for Software Requirements Specifications.
2. Overall Description
2.1 Product Perspective
The Vehicle Connect app is a component of a larger vehicle ecosystem. It is a client application that communicates via a secure API with a central backend server. This server, in turn, communicates with the vehicle's Telematics Control Unit (TCU). The application will not communicate directly with the vehicle, with the exception of proximity-based functions like Phone as a Key (PaaK) which will use Bluetooth Low Energy (BLE) or Ultra-Wideband (UWB).
2.2 Product Functions
The major functions of the Vehicle Connect application are summarized as follows:
Real-time vehicle status monitoring (SoC, range, location).
Comprehensive charging management (remote control, scheduling, station finding).
Remote vehicle controls (climate, locks, trunk).
Vehicle health and diagnostic information display.
Intelligent trip planning with integrated charging stops.
Secure key and access management.
2.3 User Characteristics
The primary user is the vehicle owner. This user is assumed to be familiar with using modern mobile applications but is not expected to have technical knowledge of the vehicle's internal systems. The application's interface must be intuitive and straightforward. Secondary users may include family members or other temporary drivers granted access by the primary owner.
2.4 Constraints
The application shall be developed for modern iOS and Android operating systems.
All communication between the mobile app and the backend server shall be encrypted using industry-standard protocols (e.g., TLS 1.2 or higher).
The app must authenticate the user securely before allowing access to vehicle data or controls.
The application must comply with all relevant data privacy regulations (e.g., GDPR, CCPA).
2.5 Assumptions and Dependencies
The user's mobile device has a stable internet connection (Wi-Fi or cellular) for most remote functions.
The vehicle is equipped with a functioning Telematics Control Unit (TCU) and has an active data connection.
A secure backend API for communication between the app and the vehicle systems exists and is documented.
Third-party services for maps and charging station data will be available and reliable.
2.6 Apportioning of Requirements
All functional and non-functional requirements detailed in this document are considered part of the initial release (Version 1.0) unless explicitly noted otherwise. There are currently no requirements designated to be delayed until future versions.
3. Specific Requirements
3.1 External Interface Requirements
User Interfaces: The application shall feature a clean, modern user interface that is consistent with the brand's design language. The UI must be optimized for both light and dark modes and be responsive to various screen sizes on supported devices.
Software Interfaces: The application shall interface with:
The Vehicle Backend API for all vehicle data and remote commands.
A third-party mapping service (e.g., Google Maps, Apple Maps) for navigation and location features.
A third-party payment gateway for in-app charging payments.
The mobile device's operating system for push notifications, GPS, and Bluetooth/UWB services.
3.2 Functional Requirements
3.2.1 FR-HSS: Home Screen & Vehicle Status
FR-HSS-001: The system shall display the vehicle's current State of Charge (SoC) as a percentage value on the application's home screen.
FR-HSS-002: The system shall display a visual representation of the vehicle's battery level.
FR-HSS-003: The system shall display an estimated vehicle range in the user's preferred unit (miles or kilometers).
FR-HSS-004: The estimated vehicle range calculation shall be based on the vehicle's current SoC, recent energy consumption trends, and the current ambient temperature reported by the vehicle.
FR-HSS-005: The system shall display the vehicle's current lock status (Locked/Unlocked).
FR-HSS-006: The system shall display the vehicle's interior cabin temperature as reported by the vehicle.
FR-HSS-007: The system shall indicate whether the climate control system is currently active.
FR-HSS-008: The system shall display a clear, graphical representation of the user's vehicle on the home screen.
3.2.2 FR-CHG: Charging Management
FR-CHG-001: The system shall allow the user to remotely start a charging session if the vehicle is plugged into a compatible charger.
FR-CHG-002: The system shall allow the user to remotely stop a charging session.
FR-CHG-003: During an active charging session, the system shall display: current SoC, estimated time to completion, current charging rate (kW), and supplied voltage/amperage.
FR-CHG-004: The system shall provide an interface for the user to set a maximum charging limit as a percentage. The interface shall default to 80% for daily charging and shall provide a convenient one-time "charge to 100%" option for trips.
FR-CHG-005: The system shall allow the user to create, edit, and delete charging schedules, defining a start time or a desired ready-by time.
FR-CHG-006: The system shall display a map of charging stations.
FR-CHG-007: The system shall allow the user to filter charging stations by connector type and power level (kW).
FR-CHG-008: The system shall display real-time availability for charging stations where the data is provided by the network operator.
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
3.2.4 FR-VHD: Vehicle Health & Details
FR-VHD-001: The system shall display the individual pressure of each tire as reported by the TPMS.
FR-VHD-002: The system shall visually flag any tire whose pressure is outside the recommended range.
FR-VHD-003: The system shall display the vehicle's total odometer reading.
FR-VHD-004: The system shall display a qualitative indicator of the high-voltage battery's internal temperature (e.g., Cold, Optimal, Hot).
FR-VHD-005: The system shall display any active service alerts or diagnostic trouble codes from the vehicle in a human-readable format.
3.2.5 FR-TRP: Trip & Driving Analytics
FR-TRP-001: The system shall allow the user to search for a destination within the app and send it to the vehicle's in-car navigation system.
FR-TRP-002: The system shall provide a trip planner that calculates a route to a destination, automatically adding required charging stops.
FR-TRP-003: The trip planner's calculation shall consider the vehicle's current SoC, route topography (elevation changes), and charger power levels to estimate charging times.
FR-TRP-004: The system shall display historical trip data, including energy consumption (e.g., kWh/100km or Wh/mile) and energy recaptured via regenerative braking.
3.2.6 FR-SEC: Security & Access Management
FR-SEC-001: The system shall support a Phone as a Key (PaaK) feature, allowing the authenticated app to unlock and start the vehicle via proximity (BLE/UWB).
FR-SEC-002: The system shall allow the primary user to invite other users to have digital key access to the vehicle.
FR-SEC-003: The primary user shall be able to revoke digital key access at any time.
FR-SEC-004: The system shall allow the primary user to apply restrictions to secondary keys, such as a maximum speed limit or a defined geographical boundary (geo-fence).
FR-SEC-005: The system shall allow the user to remotely activate and deactivate the vehicle's Sentry/Surveillance Mode.
FR-SEC-006: The system shall send a push notification to the user if a Sentry Mode event is triggered.
FR-SEC-007: The system shall allow the user to view recorded camera footage from triggered Sentry Mode events.
FR-SEC-008: The system shall display the vehicle's current GPS location on a map.
3.2.7 FR-USR: User Profile & Notifications
FR-USR-001: The system shall allow the user to configure their preferred units (e.g., miles/km, °F/°C).
FR-USR-002: The system shall allow the user to manage notification settings, enabling/disabling alerts for events such as:
Charging started/completed/interrupted.
Vehicle unlocked.
Sentry mode event.
FR-USR-003: The user shall be able to manage their account profile and payment methods for charging services.
3.3 Non-Functional Requirements
3.3.1 NFR-PERF: Performance Requirements
NFR-PERF-001: A remote command (e.g., lock, start climate) sent from the app shall receive a success/fail confirmation from the server and display it in the UI within 3 seconds under normal network conditions.
NFR-PERF-002: Vehicle status data displayed on the home screen shall be updated from the vehicle and reflect a state no older than 60 seconds from the time of the last successful data poll.
NFR-PERF-003: The application shall launch from a cold start to a usable home screen within 4 seconds.
3.3.2 NFR-SEC: Security Requirements
NFR-SEC-001: User authentication shall be required upon app launch, using biometrics (Face ID/fingerprint) or a PIN.
NFR-SEC-002: All sensitive data stored locally on the device (e.g., authentication tokens, user credentials) shall be encrypted.
NFR-SEC-003: The application shall implement certificate pinning to prevent man-in-the-middle attacks when communicating with the backend API.
3.3.3 NFR-REL: Reliability Requirements
NFR-REL-001: The core application functions shall have an uptime of 99.9%.
NFR-REL-002: The system shall handle loss of network connectivity gracefully, informing the user that the device is offline and that remote commands are unavailable. Cached data may be shown with a "last updated" timestamp.
NFR-REL-003: Critical remote commands (lock, unlock) shall have a success rate of 99.9% under standard operating conditions (vehicle and phone have stable connectivity).
3.3.4 NFR-USA: Usability Requirements
NFR-USA-001: The application shall adhere to the platform-specific human interface guidelines for iOS and Android.
NFR-USA-002: The primary functions (lock/unlock, climate, charge status) shall be accessible from the main screen with no more than one tap.

Appendix A: Glossary
API: Application Programming Interface
BLE: Bluetooth Low Energy
CAN bus: Controller Area Network bus; a vehicle bus standard.
HVAC: Heating, Ventilation, and Air Conditioning
PaaK: Phone as a Key
SoC: State of Charge; the level of charge of an electric battery relative to its capacity.
SRS: Software Requirements Specification
TCU: Telematics Control Unit
TPMS: Tire Pressure Monitoring System
UWB: Ultra-Wideband
                """.strip()
            }
        ]
        
        target_score = 10
        max_iterations = 3
        
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