"""
NASA + Groq AI Space Simplifier
"""

import requests
from groq import Groq
import os
from dotenv import load_dotenv
import time

load_dotenv()

NASA_KEY = os.getenv('NASA_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')


def get_nasa_apod(date=None):
    url = "https://api.nasa.gov/planetary/apod"
    params = {'api_key': NASA_KEY}
    if date:
        params['date'] = date
    
    try:
        print(f"Fetching NASA APOD data for {date if date else 'today'}...")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'explanation' not in data or not data['explanation']:
            print("Warning: No explanation available")
            return None
            
        print("✓ Successfully retrieved NASA data")
        return data
        
    except Exception as e:
        print(f"Error fetching NASA data: {e}")
        return None


def simplify_with_ai(text):
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        print("Sending to Groq AI for simplification...")
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{
                "role": "user",
                "content": f"""Explain this astronomy concept in simple terms for a high school student. 
                Keep it under 100 words and make it engaging.
                
                Technical explanation:
                {text}
                
                Simple explanation:"""
            }],
            temperature=0.7,
            max_tokens=200
        )
        
        print("✓ Successfully simplified with Groq AI")
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"✗ ERROR with Groq AI: {e}")
        return f"[AI Simplification unavailable]\n\n{text[:300]}..."


def process_and_display(date):
    print("\n" + "="*80)
    print(f"PROCESSING DATE: {date}")
    print("="*80 + "\n")
    
    nasa_data = get_nasa_apod(date)
    
    if not nasa_data:
        print(f"Skipping {date} due to NASA API error\n")
        return
    
    simplified_explanation = simplify_with_ai(nasa_data['explanation'])
    
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
    
    try:
        os.makedirs('screenshots', exist_ok=True)
        filename = f"screenshots/output_{date}.txt"
        
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
        print(f"Note: Could not save to file: {e}")
    
    time.sleep(1)


def main():
    print("\n" + "="*80)
    print("NASA + GROQ AI SPACE SIMPLIFIER")
    print("Making complex astronomy accessible to everyone")
    print("="*80)
    
    if not NASA_KEY or not GROQ_API_KEY:
        print("\n❌ ERROR: API keys not found!")
        print("Please make sure you have a .env file with:")
        print("NASA_KEY=your_nasa_key_here")
        print("GROQ_API_KEY=your_groq_key_here")
        return
    
    print("\n✓ API keys loaded successfully")
    print(f"✓ NASA Key: {NASA_KEY[:20]}...")
    print(f"✓ Groq Key: {GROQ_API_KEY[:20]}...")
    
    process_and_display("2024-12-10")
    process_and_display("2024-03-15")
    process_and_display("2024-01-20")
    
    print("\n" + "="*80)
    print("PROCESSING COMPLETE!")
    print("Check the screenshots/ folder for saved outputs")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()