#!/usr/bin/env python3
"""
URD Generation Script

This script handles the initial state prompt to generate User Requirements Documents (URD).
This is typically run once at the beginning of a project to create the initial URD file.
"""

import os
import sys
import datetime
import google.generativeai as genai
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class URDGenerator:
    """Class to handle URD generation from initial state prompts."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the URDGenerator class.
        
        Args:
            api_key (str, optional): Google AI API key. If not provided, 
                                   will look for GOOGLE_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        self.model = None
        self.output_file = os.getenv('URD', "URD.txt")
        
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
    
    def save_urd_to_file(self, prompt: str, response: str):
        """
        Save the URD response to a text file.
        
        Args:
            prompt (str): The original prompt
            response (str): Gemini's response
        """
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(self.output_file, "w", encoding="utf-8") as file:
                file.write(f"User Requirements Document (URD)\n")
                file.write(f"Generated on: {timestamp}\n")
                file.write(f"{'='*80}\n\n")
                file.write(response)
            
            print(f"URD saved to {self.output_file}")
            
        except Exception as e:
            raise Exception(f"Failed to save URD to file: {e}")
    
    def generate_urd(self, initial_prompt: str):
        """
        Main URD generation function that sends initial state prompt and saves URD.
        
        Args:
            initial_prompt (str): The initial state prompt to generate URD
        """
        try:
            print("Starting URD Generation Process...")
            print("=" * 50)
            
            # Setup Gemini if not already done
            if not self.model:
                self.setup_gemini()
            
            # Send prompt and get response
            response = self.send_prompt(initial_prompt)
            
            # Save to file
            self.save_urd_to_file(initial_prompt, response)
            
            print("=" * 50)
            print("URD Generation Process Completed Successfully!")
            print(f"URD saved as: {self.output_file}")
            
            return response
            
        except Exception as e:
            raise Exception(f"URD generation failed: {e}")


def main():
    """Main function for URD generation."""
    try:
        print("=== URD GENERATION ===")
        print()
        
        # Initialize the URD generator
        urd_generator = URDGenerator()
        
        # Default initial state prompt for electric car management app
        default_prompt = """Let's generate a document with user requirements for a mobile application that will be an electric car management app. 

Pretend you are the user describing what you want for the app. You're not a technical user, you are part of the car engineering team so you do have a deep understanding of the car itself.

Please provide detailed requirements covering:
- Vehicle monitoring and status
- Charging management and scheduling
- Remote vehicle control capabilities
- Trip planning and route optimization
- Maintenance and diagnostics
- User experience and interface needs
- Security and privacy requirements

Write from the perspective of an engineering team member who understands electric vehicles but needs a user-friendly mobile interface."""
        
        print("Using default electric car management app prompt...")
        print("(You can modify the prompt in the script if needed)")
        print()
        
        # Generate URD
        urd_content = urd_generator.generate_urd(default_prompt)
        
        print()
        print("URD generation completed!")
        print("You can now use the generated URD.txt file with the main SRS automation workflow.")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()