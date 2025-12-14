"""
NASA + Groq AI Space Simplifier
Project for Programming and Data Science - Fall 2025

OVERVIEW:
This program solves the problem of inaccessible space education by combining
NASA's professional space imagery with AI-powered text simplification.

WHY TWO APIs:
- NASA APOD API: Provides credible, scientifically accurate space content
- Groq AI API: Translates technical language into student-friendly explanations

The combination creates an educational tool that makes astronomy accessible
to high school students and casual space enthusiasts.

AUTHOR: Pierre
DATE: December 2024
"""

import requests
from groq import Groq
import os
from dotenv import load_dotenv
from datetime import datetime
import time

# Load environment variables from .env file
# WHY: Keeps API keys secure and out of the codebase
load_dotenv()

# Get API keys from environment variables
NASA_KEY = os.getenv('NASA_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')


def get_nasa_apod(date=None):
    """
    Fetch Astronomy Picture of the Day from NASA API
    
    We need to retrieve authentic space content and technical descriptions
    from NASA to later simplify for our target audience. This is the first
    step in our two-API workflow where we gather professional astronomical
    content that needs to be made accessible.
    """
    
    # NASA APOD API endpoint - this is NASA's service
    url = "https://api.nasa.gov/planetary/apod"
    
    # Set up parameters for the API request
    # WHY: We need to include our API key for authentication and optionally 
    # specify a date to get historical space photos
    params = {
        'api_key': NASA_KEY
    }
    
    # Add date parameter if provided
    if date:
        params['date'] = date
    
    try:
        # Make GET request to NASA API
        # WHY: This is the standard way to retrieve data from RESTful APIs
        # The timeout prevents hanging if NASA's servers are slow
        print(f"Fetching NASA APOD data for {date if date else 'today'}...")
        response = requests.get(url, params=params, timeout=10)
        
        # Check if request was successful (status code 200)
        # WHY: We need error handling in case the API is down, returns an error,
        # or we hit rate limits. raise_for_status() will throw an exception for 4xx/5xx errors
        response.raise_for_status()
        
        # Parse JSON response into Python dictionary
        data = response.json()
        
        # Verify that we have an explanation (some entries might not have one)
        # WHY: We need text to simplify - without it, the project doesn't work
        # Some NASA entries are just images without descriptions
        if 'explanation' not in data or not data['explanation']:
            print("Warning: No explanation available for this date")
            return None
            
        print("✓ Successfully retrieved NASA data")
        return data
        
    except requests.exceptions.Timeout:
        # Handle timeout specifically - helps with debugging
        print("Error: NASA API request timed out. Please try again.")
        return None
    except requests.exceptions.RequestException as e:
        # Catch all other requests errors (network issues, invalid responses, etc.)
        print(f"Error fetching NASA data: {e}")
        return None
    except ValueError as e:
        # Handle JSON parsing errors
        print(f"Error parsing NASA response: {e}")
        return None


def simplify_with_ai(text):
    """
    Use Groq AI to simplify complex astronomy text
    
    Args:
        text (str): Technical explanation from NASA
    
    Returns:
        str: Simplified version suitable for high school students
    
    WHY THIS FUNCTION:
    NASA explanations are written for scientific audiences and often contain
    technical jargon. We use Groq's AI (powered by Llama 3.1) to translate 
    this into language that's accessible to beginners while maintaining 
    scientific accuracy. This is the core value-add of our application.
    
    WHY GROQ:
    Groq provides fast, reliable free API access with generous rate limits.
    It's faster than other free alternatives and has excellent uptime.
    """
    
    try:
        # Initialize Groq client
        # WHY: Need to authenticate with our API key to use the service
        client = Groq(api_key=GROQ_API_KEY)
        
        print("Sending to Groq AI for simplification...")
        
        # Make API call to Groq
        # WHY: We use the chat completions endpoint with llama-3.1-8b-instant
        # which is fast and good at following instructions
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Fast, free model good for text simplification
            messages=[{
                "role": "user",
                "content": f"""Explain this astronomy concept in simple terms for a high school student. 
                Keep it under 100 words and make it engaging and easy to understand.
                Avoid jargon and use everyday analogies where helpful.
                
                Technical explanation:
                {text}
                
                Simple explanation:"""
            }],
            temperature=0.7,  # Balanced creativity vs consistency
            max_tokens=200,   # Limit response length
            top_p=1,
            stream=False
        )
        
        print("✓ Successfully simplified with Groq AI")
        
        # Extract the text from the response
        # WHY: The API returns a complex object, we just need the message content
        return response.choices[0].message.content
        
    except Exception as e:
        # Handle any Groq API errors
        # WHY: API calls can fail for many reasons (rate limits, network issues, 
        # invalid keys, etc.). We want to fail gracefully and show the user what went wrong
        print(f"✗ ERROR with Groq AI: {type(e).__name__}")
        print(f"   Details: {str(e)}")
        print("   Falling back to original explanation...")
        
        # Return a truncated version of original text as fallback
        return f"[AI Simplification unavailable - {type(e).__name__}]\n\nOriginal explanation (truncated):\n{text[:300]}..."


def process_and_display(date):
    """
    Main function to process a single date: fetch NASA data and simplify it
    
    Args:
        date (str): Date in YYYY-MM-DD format
    
    WHY THIS FUNCTION:
    Combines both APIs in a meaningful way - showing the before/after
    transformation that solves our core problem. This orchestrates the
    entire workflow: data retrieval → AI processing → output display.
    """
    
    print("\n" + "="*80)
    print(f"PROCESSING DATE: {date}")
    print("="*80 + "\n")
    
    # Step 1: Get NASA data
    # WHY: First we need the source material to work with
    nasa_data = get_nasa_apod(date)
    
    # Check if we successfully got data
    # WHY: Error handling - if NASA API failed, we can't continue with this date
    # Better to skip gracefully than crash the entire program
    if not nasa_data:
        print(f"Skipping {date} due to NASA API error\n")
        return
    
    # Step 2: Simplify the explanation with AI
    # WHY: This is where the magic happens - technical → accessible
    # We take NASA's scientific description and make it understandable
    simplified_explanation = simplify_with_ai(nasa_data['explanation'])
    
    # Step 3: Display results in a clear, formatted way
    # WHY: Clear output format shows both versions for comparison, demonstrating
    # the value of our simplification process
    print("\n" + "-"*80)
    print(f"📅 DATE: {date}")
    print(f"🌟 TITLE: {nasa_data['title']}")
    print(f"🖼️  IMAGE URL: {nasa_data['url']}")
    print("-"*80)
    
    print("\n📖 ORIGINAL NASA EXPLANATION:")
    print("-"*80)
    print(nasa_data['explanation'])
    
    print("\n✨ SIMPLIFIED VERSION (for high school students):")
    print("-"*80)
    print(simplified_explanation)
    print("\n" + "="*80 + "\n")
    
    # Step 4: Save to file for documentation/screenshots
    # WHY: Makes it easy to capture outputs for project documentation
    # and provides a permanent record of results
    try:
        # Create screenshots directory if it doesn't exist
        os.makedirs('screenshots', exist_ok=True)
        
        # Create filename based on date for easy identification
        filename = f"screenshots/output_{date}.txt"
        
        # Write formatted output to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"NASA + Groq AI Space Simplifier\n")
            f.write(f"Date: {date}\n")
            f.write(f"Title: {nasa_data['title']}\n")
            f.write(f"Image URL: {nasa_data['url']}\n\n")
            f.write("ORIGINAL EXPLANATION:\n")
            f.write(nasa_data['explanation'])
            f.write("\n\nSIMPLIFIED VERSION:\n")
            f.write(simplified_explanation)
        
        print(f"✓ Output saved to {filename}")
        
    except Exception as e:
        # Non-critical error - just log it, don't crash
        print(f"Note: Could not save to file: {e}")
    
    # Add small delay between API calls to be respectful of rate limits
    # WHY: Prevents hitting rate limits on free tiers, especially for Groq
    time.sleep(1)


def main():
    """
    Main function to run the program with multiple test cases
    
    WHY THIS FUNCTION:
    The assignment requires testing with at least 3 different inputs to show
    the solution works across different complexity levels. This demonstrates
    that our approach is robust and handles various types of astronomical
    content (simple descriptions, technical papers, observational data, etc.).
    """
    
    print("\n" + "="*80)
    print("NASA + GROQ AI SPACE SIMPLIFIER")
    print("Making complex astronomy accessible to everyone")
    print("="*80)
    
    # Verify API keys are loaded
    # WHY: Fail fast if configuration is wrong rather than getting cryptic
    # errors later. This saves debugging time and provides clear instructions.
    if not NASA_KEY or not GROQ_API_KEY:
        print("\n❌ ERROR: API keys not found!")
        print("Please make sure you have a .env file with:")
        print("NASA_KEY=your_nasa_key_here")
        print("GROQ_API_KEY=your_groq_key_here")
        print("\nGet Groq API key at: https://console.groq.com/keys")
        return
    
    print("\n✓ API keys loaded successfully")
    print(f"✓ NASA Key: {NASA_KEY[:20]}...")
    print(f"✓ Groq Key: {GROQ_API_KEY[:20]}...")
    
    # Test Case 1: Recent date (normal complexity)
    # WHY: Shows the system works with current data and handles
    # standard astronomical descriptions
    process_and_display("2024-12-10")
    
    # Test Case 2: Date with complex topic (higher complexity)
    # WHY: Tests if simplification really helps with highly technical content
    # This pushes the AI to demonstrate its value on difficult material
    process_and_display("2024-03-15")
    
    # Test Case 3: Older date (different complexity level)
    # WHY: Demonstrates consistency across different dates and topics
    # Also shows we can access historical data, not just recent images
    process_and_display("2024-01-20")
    
    print("\n" + "="*80)
    print("PROCESSING COMPLETE!")
    print("Check the screenshots/ folder for saved outputs")
    print("="*80 + "\n")


# Standard Python pattern for running the main function
# WHY: Allows the file to be imported as a module without auto-running
# This is a Python best practice for reusable code
if __name__ == "__main__":
    main()