#!/usr/bin/env python3
"""
SRS Automation Script with Google Gemini 2.5 Pro

This script automates the SRS (Software Requirements Specification) workflow:
- SRS Generation: Creates SRS from URD and IEEE 830-1998 standard
- SRS Validation: Validates SRS against URD and standards
- SRS Review: Improves SRS based on validation feedback
"""

import os
import sys
import datetime
import google.generativeai as genai
from typing import Optional
from dotenv import load_dotenv
import PyPDF2

# Load environment variables from .env file
load_dotenv()


class GeminiAutomation:
    """Class to handle SRS automation workflows with Google Gemini API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the GeminiAutomation class.
        
        Args:
            api_key (str, optional): Google AI API key. If not provided, 
                                   will look for GOOGLE_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        self.model = None
        
        if not self.api_key:
            raise ValueError("API key is required. Set GOOGLE_API_KEY environment variable or pass it directly.")
    
    def setup_gemini(self):
        """Configure and initialize the Gemini model."""
        try:
            # Configure the API key
            genai.configure(api_key=self.api_key)
            
            # Initialize the Gemini 2.5 Pro model
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            print("Gemini 2.5 Pro model initialized successfully!")
            
        except Exception as e:
            raise Exception(f"Failed to initialize Gemini model: {e}")
    
    def send_prompt(self, prompt: str) -> str:
        """
        Send a prompt to Gemini and return the response.
        
        Args:
            prompt (str): The prompt to send to Gemini
            
        Returns:
            str: Gemini's response
        """
        if not self.model:
            raise Exception("Gemini model not initialized. Call setup_gemini() first.")
        
        try:
            print(f"Sending prompt to Gemini...")
            response = self.model.generate_content(prompt)
            
            if response.text:
                print("Response received successfully!")
                return response.text
            else:
                raise Exception("No response text received from Gemini")
                
        except Exception as e:
            raise Exception(f"Failed to send prompt to Gemini: {e}")
    
    def read_pdf_file(self, pdf_path: str) -> str:
        """
        Read content from a PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: Extracted text content from PDF
        """
        try:
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
            print(f"Reading PDF file: {pdf_path}")
            text_content = ""
            
            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text_content += page.extract_text() + "\n"
            
            print(f"Successfully extracted text from PDF ({len(text_content)} characters)")
            return text_content
            
        except Exception as e:
            raise Exception(f"Failed to read PDF file: {e}")
    
    def read_text_file(self, file_path: str) -> str:
        """
        Read content from a text file.
        
        Args:
            file_path (str): Path to the text file
            
        Returns:
            str: Content of the text file
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Text file not found: {file_path}")
            
            print(f"Reading text file: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            print(f"Successfully read text file ({len(content)} characters)")
            return content
            
        except Exception as e:
            raise Exception(f"Failed to read text file: {e}")
    
    def generate_srs_prompt(self, urd_content: str, pdf_content: str) -> str:
        """
        Generate the SRS generation prompt with URD and PDF content.
        
        Args:
            urd_content (str): Content from the URD file
            pdf_content (str): Content from the PDF file
            
        Returns:
            str: Complete prompt for SRS generation
        """
        prompt = f"""
You are a senior software requirements engineer tasked with creating a comprehensive Software Requirements Specification (SRS) document. 

You have been provided with:
1. User Requirements Document (URD) - describing what the user wants
2. IEEE 830-1998 Standard - the template and guidelines for SRS documents

Your task is to transform the user requirements into a professional, complete SRS document following the IEEE 830-1998 standard.

**USER REQUIREMENTS DOCUMENT (URD):**
{urd_content}

**IEEE 830-1998 STANDARD CONTENT:**
{pdf_content}

**Instructions:**
1. Follow the IEEE 830-1998 standard structure and format
2. Transform the user requirements from the URD into technical software requirements
3. Ensure all sections required by the standard are included
4. Make the requirements specific, measurable, achievable, relevant, and time-bound (SMART)
5. Include functional requirements, non-functional requirements, and constraints
6. Provide clear requirement IDs and priorities
7. Ensure traceability between user needs and software requirements

**Please generate a complete SRS document that includes:**
- Introduction (Purpose, Scope, Definitions, References, Overview)
- Overall Description (Product perspective, functions, user characteristics, constraints, assumptions)
- Specific Requirements (Functional requirements, Performance requirements, Design constraints, Attributes, External interface requirements)

Generate the SRS document now:
"""
        return prompt
    
    def generate_srs_validation_prompt(self, urd_content: str, srs_content: str, pdf_content: str, previous_validation: str = None) -> str:
        """
        Generate the SRS validation prompt with URD, SRS, and PDF content.
        
        Args:
            urd_content (str): Content from the URD file
            srs_content (str): Content from the SRS file to be validated
            pdf_content (str): Content from the IEEE 830-1998 PDF file
            previous_validation (str, optional): Previous validation report if available
            
        Returns:
            str: Complete prompt for SRS validation
        """
        previous_section = ""
        if previous_validation:
            previous_section = f"""
**PREVIOUS VALIDATION REPORT:**
{previous_validation}

NOTE: This SRS might be a reviewed version attempting to address previous evaluation points. 
Take into consideration any notes and sections mentioning "this section didn't change" or similar remarks.
"""
        
        prompt = f"""
You work with software development requirements, particularly in the quality and auditing area.

You will receive:
1. User Requirements Document (URD) - the original user requirements
2. Software Requirements Specification (SRS) - generated based on the URD 
3. IEEE 830-1998 Standard - the template and guidelines for SRS documents
{4 if previous_validation else ""}. Previous validation report (if applicable)

Your objective is to validate that:
- ALL user requirements from the URD are present and properly addressed in the SRS
- The SRS follows the IEEE 830-1998 standard structure, format, and quality guidelines
- There are no inconsistencies, ambiguities, or missing critical information

**USER REQUIREMENTS DOCUMENT (URD):**
{urd_content}

**SOFTWARE REQUIREMENTS SPECIFICATION (SRS) TO VALIDATE:**
{srs_content}

**IEEE 830-1998 STANDARD CONTENT:**
{pdf_content}
{previous_section}
**VALIDATION INSTRUCTIONS:**

1. **Completeness Check:**
   - Verify every user requirement from the URD is addressed in the SRS
   - Identify any missing functional or non-functional requirements
   - Check for missing sections required by IEEE 830-1998

2. **IEEE 830-1998 Compliance:**
   - Verify the document structure follows the standard
   - Check that all mandatory sections are present and properly formatted
   - Ensure requirements are specific, measurable, achievable, relevant, and time-bound (SMART)
   - Validate requirement IDs, priorities, and traceability

3. **Quality Assessment:**
   - Identify ambiguous, unclear, or contradictory requirements
   - Check for consistency in terminology and definitions
   - Verify external interface requirements are properly defined
   - Assess performance and design constraints adequacy

4. **Traceability Analysis:**
   - Ensure clear mapping between user needs and software requirements
   - Verify requirements are testable and verifiable
   - Check for orphaned requirements (not traceable to user needs)

**OUTPUT FORMAT:**
Provide a comprehensive validation report that includes:
- Executive Summary of findings
- Detailed analysis by section
- List of missing requirements
- Compliance gaps with IEEE 830-1998
- Specific recommendations for improvement
- Clear identification of each problem found

**CRITICAL: At the end of your report, insert a tag specifying the total number of problems found using this exact format:**
<errors: #>

Where # is the actual number of problems/issues identified (e.g., <errors: 3>, <errors: 0>, <errors: 15>).
This tag is used by automated systems to determine if the SRS passed or failed the audit process.

Generate the SRS Validation Report now:
"""
        return prompt
    
    def save_validation_report_to_file(self, validation_report: str, filename: str = "SRSVR_v1.txt"):
        """
        Save the SRS validation report to a specific file.
        
        Args:
            validation_report (str): The validation report content from Gemini
            filename (str): Name of the validation report file to save to
        """
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"SRS Validation Report (SRSVR)\n")
                file.write(f"Generated on: {timestamp}\n")
                file.write(f"{'='*80}\n\n")
                file.write(validation_report)
            
            print(f"SRS Validation Report saved to {filename}")
            
        except Exception as e:
            raise Exception(f"Failed to save validation report to file: {e}")
    
    def run_srs_validation(self, urd_file_path: str = "URD.txt", srs_file_path: str = "SRS_v1.txt", 
                          pdf_file_path: str = "830-1998.pdf", output_file: str = "SRSVR_v1.txt",
                          previous_validation_file: str = None):
        """
        Main SRS validation workflow that reads URD, SRS, and PDF files, generates validation prompt,
        sends it to Gemini, and saves the validation report.
        
        Args:
            urd_file_path (str): Path to the URD file
            srs_file_path (str): Path to the SRS file to validate
            pdf_file_path (str): Path to the IEEE 830-1998 PDF file
            output_file (str): Name of the output validation report file
            previous_validation_file (str, optional): Path to previous validation report
            
        Returns:
            str: The generated validation report content
        """
        try:
            print("Starting SRS Validation Process...")
            print("=" * 50)
            
            # Setup Gemini if not already done
            if not self.model:
                self.setup_gemini()
            
            # Read the URD file
            print("Step 1: Reading URD file...")
            urd_content = self.read_text_file(urd_file_path)
            
            # Read the SRS file
            print("Step 2: Reading SRS file...")
            srs_content = self.read_text_file(srs_file_path)
            
            # Read the PDF file
            print("Step 3: Reading IEEE 830-1998 PDF file...")
            pdf_content = self.read_pdf_file(pdf_file_path)
            
            # Read previous validation report if provided
            previous_validation = None
            if previous_validation_file and os.path.exists(previous_validation_file):
                print("Step 4: Reading previous validation report...")
                previous_validation = self.read_text_file(previous_validation_file)
            
            # Generate the validation prompt
            print("Step 5: Generating SRS validation prompt...")
            validation_prompt = self.generate_srs_validation_prompt(
                urd_content, srs_content, pdf_content, previous_validation
            )
            
            # Send the prompt to Gemini
            print("Step 6: Sending validation prompt to Gemini...")
            print("This may take a while due to the comprehensive analysis required...")
            validation_response = self.send_prompt(validation_prompt)
            
            # Save the validation report
            print("Step 7: Saving SRS validation report...")
            self.save_validation_report_to_file(validation_response, output_file)
            
            # Extract error count from the response
            error_count = self.extract_error_count(validation_response)
            
            print("=" * 50)
            print("SRS Validation Process Completed Successfully!")
            print(f"Validation report saved as: {output_file}")
            print(f"Errors found: {error_count}")
            
            if error_count == 0:
                print("🎉 SRS PASSED validation!")
            else:
                print(f"⚠️  SRS FAILED validation with {error_count} error(s)")
            
            return validation_response
            
        except Exception as e:
            raise Exception(f"SRS validation failed: {e}")
    
    def extract_error_count(self, validation_report: str) -> int:
        """
        Extract the error count from the validation report.
        
        Args:
            validation_report (str): The validation report content
            
        Returns:
            int: Number of errors found, or -1 if tag not found
        """
        import re
        
        # Look for the <errors: #> tag
        match = re.search(r'<errors:\s*(\d+)>', validation_report)
        if match:
            return int(match.group(1))
        else:
            print("Warning: Error count tag not found in validation report")
            return -1
    
    def generate_srs_review_prompt(self, original_srs: str, validation_report: str) -> str:
        """
        Generate the SRS review prompt with original SRS and validation feedback.
        
        Args:
            original_srs (str): Content from the original SRS file
            validation_report (str): Content from the SRSVR validation report
            
        Returns:
            str: Complete prompt for SRS review and improvement
        """
        prompt = f"""
You are a software engineer who wrote an SRS (Software Requirements Specification) for a user requirement. Another department responsible for quality and auditing has reviewed your SRS and identified gaps, inconsistencies, and areas for improvement. They have created a detailed validation report with specific feedback and recommendations.

Your task is to review your original SRS and take into account all the feedback from the validation report to create a new, improved version that addresses all identified issues.

**YOUR ORIGINAL SRS DOCUMENT:**
{original_srs}

**VALIDATION REPORT WITH FEEDBACK:**
{validation_report}

**INSTRUCTIONS FOR SRS REVIEW AND IMPROVEMENT:**

1. **Address All Identified Issues:**
   - Carefully review each problem identified in the validation report
   - Fix missing requirements, ambiguous statements, and incomplete sections
   - Add specific details where the validation report indicates gaps

2. **Maintain Document Structure:**
   - Keep the IEEE 830-1998 standard structure and format
   - Ensure all sections are properly organized and numbered
   - Update the version number to reflect this is a revised document

3. **Improve Requirement Quality:**
   - Make requirements more specific, measurable, and testable
   - Add missing requirement IDs and priorities where needed
   - Ensure clear traceability between user needs and software requirements

4. **Enhance Completeness:**
   - Add missing sections or subsections identified in the validation report
   - Include detailed specifications for interfaces, performance, and constraints
   - Provide comprehensive error handling and security details

5. **Address Compliance Issues:**
   - Ensure full compliance with IEEE 830-1998 standard
   - Add any missing mandatory sections or content
   - Include proper references, definitions, and appendices

6. **Improve Clarity and Precision:**
   - Replace ambiguous language with specific, technical terms
   - Add quantitative metrics where qualitative descriptions were used
   - Ensure consistency in terminology throughout the document

**SPECIFIC AREAS TO FOCUS ON (based on validation feedback):**
- Add user confirmation requirements for critical operations
- Specify security protocols with exact versions and standards
- Include detailed error handling mechanisms
- Add comprehensive traceability matrix
- Specify data update frequencies and real-time definitions
- Include regulatory compliance requirements
- Add missing UI/UX specifications for accessibility and localization
- Enhance integration details for external systems

**OUTPUT REQUIREMENTS:**
- Generate a complete, revised SRS document
- Address every issue mentioned in the validation report
- Maintain professional technical writing standards
- Include version history noting this revision addresses validation feedback
- Ensure the document is ready for implementation by development teams

Create the improved SRS document now:
"""
        return prompt
    
    def get_next_srs_version(self, base_filename: str = "SRS") -> str:
        """
        Determine the next version number for SRS files.
        
        Args:
            base_filename (str): Base filename pattern (e.g., "SRS")
            
        Returns:
            str: Next version filename (e.g., "SRS_v2.txt")
        """
        import glob
        import re
        
        try:
            # Find all existing SRS files matching the pattern
            pattern = f"{base_filename}_v*.txt"
            existing_files = glob.glob(pattern)
            
            if not existing_files:
                # No existing versions found, start with v1
                return f"{base_filename}_v1.txt"
            
            # Extract version numbers
            version_numbers = []
            for filename in existing_files:
                match = re.search(r'_v(\d+)\.txt$', filename)
                if match:
                    version_numbers.append(int(match.group(1)))
            
            if not version_numbers:
                return f"{base_filename}_v1.txt"
            
            # Get the highest version number and increment
            highest_version = max(version_numbers)
            next_version = highest_version + 1
            
            return f"{base_filename}_v{next_version}.txt"
            
        except Exception as e:
            print(f"Warning: Could not determine version number: {e}")
            return f"{base_filename}_v2.txt"  # Default fallback
    
    def save_reviewed_srs_to_file(self, reviewed_srs: str, filename: str):
        """
        Save the reviewed SRS to a versioned file.
        
        Args:
            reviewed_srs (str): The reviewed SRS content from Gemini
            filename (str): Name of the SRS file to save to
        """
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"Software Requirements Specification (SRS) - Reviewed Version\n")
                file.write(f"Generated on: {timestamp}\n")
                file.write(f"Note: This version addresses validation feedback and recommendations\n")
                file.write(f"{'='*80}\n\n")
                file.write(reviewed_srs)
            
            print(f"Reviewed SRS document saved to {filename}")
            
        except Exception as e:
            raise Exception(f"Failed to save reviewed SRS to file: {e}")
    
    def run_srs_review(self, srs_file_path: str, validation_report_path: str, output_file: str = None):
        """
        Main SRS review workflow that reads the original SRS and validation report,
        generates an improved SRS based on feedback.
        
        Args:
            srs_file_path (str): Path to the original SRS file
            validation_report_path (str): Path to the SRSVR validation report
            output_file (str, optional): Output filename. If not provided, auto-generates next version
            
        Returns:
            str: The generated improved SRS content
        """
        try:
            print("Starting SRS Review Process...")
            print("=" * 50)
            
            # Setup Gemini if not already done
            if not self.model:
                self.setup_gemini()
            
            # Determine output filename if not provided
            if not output_file:
                output_file = self.get_next_srs_version("SRS")
                print(f"Auto-determined next version: {output_file}")
            
            # Read the original SRS file
            print("Step 1: Reading original SRS file...")
            original_srs = self.read_text_file(srs_file_path)
            
            # Read the validation report
            print("Step 2: Reading validation report...")
            validation_report = self.read_text_file(validation_report_path)
            
            # Generate the review prompt
            print("Step 3: Generating SRS review prompt...")
            review_prompt = self.generate_srs_review_prompt(original_srs, validation_report)
            
            # Send the prompt to Gemini
            print("Step 4: Sending review prompt to Gemini...")
            print("This may take a while as the SRS is being thoroughly reviewed and improved...")
            reviewed_srs = self.send_prompt(review_prompt)
            
            # Save the reviewed SRS
            print("Step 5: Saving reviewed SRS document...")
            self.save_reviewed_srs_to_file(reviewed_srs, output_file)
            
            print("=" * 50)
            print("SRS Review Process Completed Successfully!")
            print(f"Improved SRS document saved as: {output_file}")
            print("The new SRS addresses all validation feedback and recommendations.")
            
            return reviewed_srs
            
        except Exception as e:
            raise Exception(f"SRS review failed: {e}")
    
    def save_srs_to_file(self, response: str, filename: str = "SRS_v1.txt"):
        """
        Save the SRS response to a specific file.
        
        Args:
            response (str): The SRS content from Gemini
            filename (str): Name of the SRS file to save to
        """
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"Software Requirements Specification (SRS)\n")
                file.write(f"Generated on: {timestamp}\n")
                file.write(f"{'='*80}\n\n")
                file.write(response)
            
            print(f"SRS document saved to {filename}")
            
        except Exception as e:
            raise Exception(f"Failed to save SRS to file: {e}")
    
    def run_srs_generation(self, urd_file_path: str = "URD.txt", pdf_file_path: str = "830-1998.pdf", output_file: str = "SRS_v1.txt"):
        """
        Main SRS generation workflow that reads URD and PDF files, generates SRS prompt,
        sends it to Gemini, and saves the result.
        
        Args:
            urd_file_path (str): Path to the URD file
            pdf_file_path (str): Path to the IEEE 830-1998 PDF file
            output_file (str): Name of the output SRS file
            
        Returns:
            str: The generated SRS content
        """
        try:
            print("Starting SRS Generation Process...")
            print("=" * 50)
            
            # Setup Gemini if not already done
            if not self.model:
                self.setup_gemini()
            
            # Read the URD file
            print("Step 1: Reading URD file...")
            urd_content = self.read_text_file(urd_file_path)
            
            # Read the PDF file
            print("Step 2: Reading IEEE 830-1998 PDF file...")
            pdf_content = self.read_pdf_file(pdf_file_path)
            
            # Generate the SRS prompt
            print("Step 3: Generating SRS prompt...")
            srs_prompt = self.generate_srs_prompt(urd_content, pdf_content)
            
            # Send the prompt to Gemini
            print("Step 4: Sending prompt to Gemini for SRS generation...")
            print("This may take a while due to the large amount of content...")
            srs_response = self.send_prompt(srs_prompt)
            
            # Save the SRS response
            print("Step 5: Saving SRS document...")
            self.save_srs_to_file(srs_response, output_file)
            
            print("=" * 50)
            print("SRS Generation Process Completed Successfully!")
            print(f"SRS document saved as: {output_file}")
            
            return srs_response
            
        except Exception as e:
            raise Exception(f"SRS generation failed: {e}")
    
    def test_srs_generation_with_sample_urd(self):
        """
        Test method that creates a sample URD and runs the SRS generation process.
        Useful for testing when no URD file exists yet.
        """
        try:
            print("Creating sample URD for testing...")
            
            # Create a sample URD content
            sample_urd = """User Requirements Document (URD)
Electric Car Management Mobile Application

As a member of the car engineering team, I need a mobile application to manage and monitor our electric vehicles. Here are my requirements:

Vehicle Monitoring:
- I want to see the current battery level of the vehicle in real-time
- I need to monitor the charging status and time remaining for full charge
- I want to track the vehicle's location and route history
- I need to see energy consumption patterns and efficiency metrics

Charging Management:
- I want to find nearby charging stations with availability status
- I need to schedule charging sessions and set charging limits
- I want to receive notifications when charging is complete
- I need to track charging costs and history

Vehicle Control:
- I want to remotely start/stop charging
- I need to pre-condition the cabin temperature before driving
- I want to lock/unlock the vehicle remotely
- I need to activate the vehicle's horn and lights for location purposes

Trip Planning:
- I want to plan routes with charging stops included
- I need to calculate trip energy requirements
- I want to save favorite locations and routes
- I need weather-based range adjustments

Maintenance & Diagnostics:
- I want to receive maintenance reminders and alerts
- I need to access vehicle diagnostic information
- I want to schedule service appointments
- I need to track maintenance history and costs

User Experience:
- The app should work offline with limited functionality
- I need dark/light mode options
- The interface should be intuitive for non-technical users
- Response time should be under 3 seconds for most operations

Security & Privacy:
- All vehicle data should be encrypted
- I need secure authentication (biometric if available)
- Vehicle access should have multiple authorization levels
- Personal data should not be shared without consent"""

            # Save the sample URD
            with open("URD.txt", "w", encoding="utf-8") as file:
                file.write(sample_urd)
            
            print("Sample URD created successfully!")
            
            # Now run the SRS generation process
            return self.run_srs_generation()
            
        except Exception as e:
            raise Exception(f"Test SRS generation failed: {e}")
    
    def run_iterative_srs_improvement(self, max_iterations: int = 10, target_errors: int = 0):
        """
        Run iterative SRS improvement loop: Generation → Validation → Review until errors = 0 or max iterations.
        
        Args:
            max_iterations (int): Maximum number of iterations (default 10, max SRS_v10)
            target_errors (int): Target error count to stop iteration (default 0)
            
        Returns:
            dict: Results summary including final version, error count, and iteration count
        """
        try:
            print("=" * 60)
            print("STARTING ITERATIVE SRS IMPROVEMENT PROCESS")
            print(f"Target: {target_errors} errors | Max iterations: {max_iterations}")
            print("=" * 60)
            
            # Setup Gemini if not already done
            if not self.model:
                self.setup_gemini()
            
            current_version = 1
            current_errors = float('inf')  # Start with high error count
            
            # Generate initial SRS (v1)
            print(f"\n🚀 ITERATION {current_version}: Generating initial SRS")
            print("-" * 40)
            
            srs_file = f"SRS_v{current_version}.txt"
            print("Step 1: Generating initial SRS...")
            self.run_srs_generation(
                urd_file_path="URD.txt",
                pdf_file_path="830-1998.pdf",
                output_file=srs_file
            )
            
            # Main iteration loop
            while current_version <= max_iterations and current_errors > target_errors:
                print(f"\n🔍 ITERATION {current_version}: Validation and Review")
                print("-" * 40)
                
                # Step 1: Validate current SRS
                srsvr_file = f"SRSVR_v{current_version}.txt"
                print(f"Step 2: Validating {srs_file}...")
                
                validation_report = self.run_srs_validation(
                    urd_file_path="URD.txt",
                    srs_file_path=srs_file,
                    pdf_file_path="830-1998.pdf",
                    output_file=srsvr_file
                )
                
                # Extract error count
                current_errors = self.extract_error_count(validation_report)
                print(f"📊 Validation completed: {current_errors} errors found")
                
                # Check if we've reached target
                if current_errors <= target_errors:
                    print(f"🎉 SUCCESS! Target of {target_errors} errors reached!")
                    break
                
                # Check if we've reached max iterations
                if current_version >= max_iterations:
                    print(f"⚠️  Maximum iterations ({max_iterations}) reached")
                    break
                
                # Step 2: Review and improve SRS
                next_version = current_version + 1
                next_srs_file = f"SRS_v{next_version}.txt"
                
                print(f"Step 3: Reviewing and improving SRS → {next_srs_file}...")
                
                # Determine previous validation file for context
                previous_srsvr = None
                if current_version > 1:
                    previous_srsvr = f"SRSVR_v{current_version-1}.txt"
                
                reviewed_srs = self.run_srs_review(
                    srs_file_path=srs_file,
                    validation_report_path=srsvr_file,
                    output_file=next_srs_file
                )
                
                # Move to next iteration
                current_version = next_version
                srs_file = next_srs_file
                
                print(f"✅ Iteration completed. Moving to version {current_version}")
            
            # Final results
            print("\n" + "=" * 60)
            print("ITERATIVE IMPROVEMENT COMPLETED")
            print("=" * 60)
            
            final_results = {
                'final_version': current_version,
                'final_error_count': current_errors,
                'iterations_completed': current_version,
                'target_reached': current_errors <= target_errors,
                'final_srs_file': f"SRS_v{current_version}.txt",
                'final_srsvr_file': f"SRSVR_v{current_version}.txt"
            }
            
            print(f"📄 Final SRS Version: {final_results['final_srs_file']}")
            print(f"📊 Final Error Count: {final_results['final_error_count']}")
            print(f"🔄 Total Iterations: {final_results['iterations_completed']}")
            print(f"🎯 Target Reached: {'✅ YES' if final_results['target_reached'] else '❌ NO'}")
            
            if final_results['target_reached']:
                print(f"🎉 SRS successfully improved to {target_errors} errors!")
            else:
                print(f"⚠️  Process stopped at maximum iterations with {current_errors} errors remaining")
            
            return final_results
            
        except Exception as e:
            raise Exception(f"Iterative SRS improvement failed: {e}")


def main():
    """Main function for SRS automation workflow."""
    try:
        # Initialize the automation class
        automator = GeminiAutomation()
        
        print("=== ITERATIVE SRS AUTOMATION WORKFLOW ===")
        print("Automatic improvement cycle: Generation → Validation → Review")
        print("Continues until 0 errors or 10 iterations maximum")
        print()
        
        # Check if URD file exists
        urd_file = "URD.txt"
        if not os.path.exists(urd_file):
            print(f"❌ URD file ({urd_file}) not found!")
            print("Please run 'python urd_generator.py' first to create the URD file.")
            print("Or ensure you have a URD.txt file in the current directory.")
            sys.exit(1)
        
        print(f"✓ URD file found: {urd_file}")
        
        # Run iterative improvement process
        results = automator.run_iterative_srs_improvement(
            max_iterations=5,
            target_errors=0
        )
        
        print()
        print("🏁 WORKFLOW SUMMARY:")
        print(f"   - Process completed in {results['iterations_completed']} iteration(s)")
        print(f"   - Final SRS: {results['final_srs_file']}")
        print(f"   - Final validation: {results['final_srsvr_file']}")
        print(f"   - Final error count: {results['final_error_count']}")
        print(f"   - Quality target reached: {'Yes' if results['target_reached'] else 'No'}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()