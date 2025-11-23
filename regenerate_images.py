#!/usr/bin/env python3
import os
import sys
from p2_design_agent import UMLDiagramAutomation

def regenerate_all_images():
    print("Starting image regeneration for all PUML files...")
    
    try:
        # Initialize automation
        uml = UMLDiagramAutomation()
        uml.setup_directories()
        uml.verify_plantuml_installation()
        
        # Walk through the diagrams directory
        count = 0
        errors = 0
        
        for root, dirs, files in os.walk(uml.diagrams_dir):
            for file in files:
                if file.endswith(".puml"):
                    puml_path = os.path.join(root, file)
                    print(f"Processing: {file}")
                    
                    try:
                        image_path = uml.generate_image_from_puml(puml_path)
                        print(f"   Generated: {image_path}")
                        count += 1
                    except Exception as e:
                        print(f"   Failed: {e}")
                        errors += 1
                        
        print("\n" + "="*50)
        print(f"Regeneration Complete!")
        print(f"Successfully generated: {count}")
        print(f"Failed: {errors}")
        print("="*50)
        
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    regenerate_all_images()
