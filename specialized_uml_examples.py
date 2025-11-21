#!/usr/bin/env python3
"""
Specialized UML Generation Examples

This script demonstrates the three specialized UML diagram generation patterns:
A. Structure (Class Diagram) - from Data Requirements
B. Interaction (Sequence Diagram) - from Functional Requirements  
C. Logic (Activity Diagram) - from Complex Workflows
"""

from uml_automation import UMLDiagramAutomation

def demonstrate_specialized_diagrams():
    """Demonstrate the specialized diagram generation patterns."""
    try:
        print("=== Specialized UML Diagram Generation ===\n")
        
        # Initialize automation
        uml_automation = UMLDiagramAutomation()
        uml_automation.setup_gemini()
        uml_automation.setup_directories()
        uml_automation.verify_plantuml_installation()
        
        print("✅ Setup completed!\n")
        
        # Read SRS for content extraction
        srs_file = "SRS_v5.txt"  # Update this to your latest SRS file
        print(f"Reading SRS file: {srs_file}")
        srs_content = uml_automation.read_srs_file(srs_file)
        
        # =====================================================================
        # A. STRUCTURE (Class Diagram) - Data Requirements Example
        # =====================================================================
        print("\n" + "="*60)
        print("A. STRUCTURE (Class Diagram) - Data Requirements")
        print("="*60)
        
        # Example data requirements text
        data_requirements_example = """
        3.6 Data Requirements

        The Electric Car Management Mobile Application requires the following data entities:

        User Profile: Contains user ID, name, email, phone number, preferences, authentication credentials.
        Operations: authenticate(), updateProfile(), getPreferences(), setPreferences()

        Vehicle Information: Contains vehicle ID, make, model, year, VIN, battery capacity, current charge level, 
        location coordinates, odometer reading. Each user can have multiple vehicles.
        Operations: getBatteryLevel(), getLocation(), updateLocation(), getOdometer()

        Charging Station: Contains station ID, name, location coordinates, connector types, charging rates, 
        availability status, pricing information. Stations have multiple charging ports.
        Operations: checkAvailability(), reservePort(), startCharging(), stopCharging()

        Charging Session: Contains session ID, user ID, vehicle ID, station ID, start time, end time, 
        energy consumed, cost. Each session belongs to one user and one vehicle.
        Operations: startSession(), endSession(), calculateCost(), generateReceipt()

        Trip History: Contains trip ID, vehicle ID, start location, end location, distance, energy consumed,
        charging stops. Each trip belongs to one vehicle.
        Operations: recordTrip(), calculateEfficiency(), addChargingStop()

        Relationships:
        - User has multiple Vehicles (1 to many)
        - Vehicle has multiple Charging Sessions (1 to many) 
        - Charging Station has multiple Charging Sessions (1 to many)
        - Vehicle has multiple Trips (1 to many)
        - Trip can have multiple Charging Stops (aggregation)
        """
        
        structure_result = uml_automation.generate_structure_diagram(
            data_requirements_example,
            "electric_car_data_model"
        )
        
        print(f"📊 Structure (Class) Diagram generated:")
        print(f"   📄 PUML: {structure_result['puml']}")
        print(f"   🖼️  Image: {structure_result['image']}")
        
        # =====================================================================
        # B. INTERACTION (Sequence Diagram) - Functional Requirements Example
        # =====================================================================
        print("\n" + "="*60)
        print("B. INTERACTION (Sequence Diagram) - Functional Requirements")
        print("="*60)
        
        # Example functional requirements for Remote Start feature
        remote_start_requirements = """
        VC-1.0: Remotely start/stop charging

        The system shall allow users to remotely start and stop charging sessions for their vehicles.

        Normal Flow:
        1. User opens the mobile application
        2. User selects their vehicle from the vehicle list
        3. User navigates to the charging control interface
        4. User taps "Start Charging" button
        5. Application sends authentication token to API
        6. API validates user permissions and vehicle ownership
        7. API sends start charging command to vehicle manufacturer's API
        8. Vehicle manufacturer API processes the command
        9. Vehicle starts charging and updates status
        10. API retrieves updated charging status from vehicle
        11. Application displays confirmation and live charging status to user

        Error Flows:
        - If user authentication fails: Display "Authentication failed, please log in again"
        - If vehicle is not connected: Display "Vehicle not connected, check network"
        - If charging port not connected: Display "Please connect charging cable first"
        - If API is unavailable: Display "Service temporarily unavailable, try again later"
        - If vehicle manufacturer API fails: Display "Vehicle communication error, contact support"

        Success Criteria:
        - Charging starts within 30 seconds of command
        - User receives real-time status updates
        - All errors are logged for troubleshooting
        """
        
        interaction_result = uml_automation.generate_interaction_diagram(
            "Remote Start Charging",
            remote_start_requirements,
            "remote_start_charging_sequence"
        )
        
        print(f"🔄 Interaction (Sequence) Diagram generated:")
        print(f"   📄 PUML: {interaction_result['puml']}")
        print(f"   🖼️  Image: {interaction_result['image']}")
        
        # =====================================================================
        # C. LOGIC (Activity Diagram) - Complex Workflow Example  
        # =====================================================================
        print("\n" + "="*60)
        print("C. LOGIC (Activity Diagram) - Complex Workflow")
        print("="*60)
        
        # Example complex workflow with decision logic
        trip_planning_workflow = """
        Trip Planning Logic Workflow

        The system shall plan optimal routes with charging stops based on the following logic:

        Start: User enters destination
        
        Step 1: Calculate direct distance to destination
        Step 2: Get current battery level from vehicle
        Step 3: Calculate maximum range with current battery (considering weather, terrain, driving style)
        
        Decision Point 1: If current battery range >= trip distance + 20% buffer
        - YES: Plan direct route without charging stops
        - NO: Continue to charging planning logic
        
        Step 4: Find all charging stations along potential routes
        Step 5: Filter stations by compatibility (connector type, charging speed)
        Step 6: Calculate optimal charging stops to minimize total trip time
        
        Decision Point 2: If multiple viable routes found
        - YES: Rank routes by total time (driving + charging)
        - NO: Continue with single route
        
        Step 7: For each potential charging stop, check real-time availability
        
        Decision Point 3: If preferred stations are available
        - YES: Reserve charging slot if possible
        - NO: Find alternative stations or adjust route
        
        Step 8: Calculate arrival times at each charging stop
        Step 9: Determine required charging time at each stop
        
        Decision Point 4: If weather conditions are severe
        - YES: Add 15% buffer to energy calculations and extend charging times
        - NO: Use standard calculations
        
        Step 10: Generate final route with turn-by-turn directions
        Step 11: Send route to vehicle navigation system
        Step 12: Monitor trip progress and adjust dynamically if needed
        
        End: Trip planning complete, navigation active
        
        Error Handling:
        - If no charging stations found: Suggest alternative destinations within range
        - If all stations are occupied: Provide estimated wait times and alternatives
        - If vehicle communication fails: Use cached vehicle data with warnings
        """
        
        logic_result = uml_automation.generate_logic_diagram(
            trip_planning_workflow,
            "Trip Planning Logic",
            "trip_planning_logic_activity"
        )
        
        print(f"⚡ Logic (Activity) Diagram generated:")
        print(f"   📄 PUML: {logic_result['puml']}")
        print(f"   🖼️  Image: {logic_result['image']}")
        
        # =====================================================================
        # COMPREHENSIVE GENERATION
        # =====================================================================
        print("\n" + "="*60)
        print("BONUS: Comprehensive Design Set Generation")
        print("="*60)
        
        print("🚀 Generating comprehensive design set from full SRS...")
        comprehensive_results = uml_automation.generate_comprehensive_design_set(srs_content)
        
        print(f"\n📊 Comprehensive Generation Summary:")
        for diagram_name, result in comprehensive_results.items():
            if 'error' in result:
                print(f"   ❌ {diagram_name}: {result['error']}")
            else:
                print(f"   ✅ {diagram_name}: {result['type']}")
        
        # =====================================================================
        # SUMMARY
        # =====================================================================
        print("\n" + "="*60)
        print("🎉 SPECIALIZED UML GENERATION COMPLETE!")
        print("="*60)
        
        print(f"""
Generated Diagrams:
├── Structure (Class): {structure_result['image']}
├── Interaction (Sequence): {interaction_result['image']}  
├── Logic (Activity): {logic_result['image']}
└── Additional diagrams in uml_diagrams/ directory

These diagrams follow the specific constraints you requested:
✅ A. Class Diagram: Attributes, operations, relationships (--|>, *--, o--), multiplicity
✅ B. Sequence Diagram: Autonumber, participants, alt/else blocks for error paths
✅ C. Activity Diagram: New syntax (start/stop), if/then structures, merge nodes

Ready for your custom prompts and specific requirements!
        """)
        
    except Exception as e:
        print(f"❌ Error during specialized demonstration: {e}")

if __name__ == "__main__":
    demonstrate_specialized_diagrams()