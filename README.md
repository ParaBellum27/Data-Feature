how to set it up

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py

after that you will see all the results appear in screenshot. 

REFLECTION:

What was the hardest part?
Making sure the API and keyboard. I started with the Gemini API key but kept failing, even though the API key was full and I was on a working. I then switched to Krog API T, which finally worked, and I no longer could see the unavailable summary response in the screenshot. 

The second thing was making sure the prompt was correct, because at the start, it was pretty much just as complex as the original NASA explanation. It took a few tries to make it good. 

Other problems when building it:
1. Time spent trying to find the right two APIs to compare. 
2. I went through the public free API list, and couldn't find the right ones the project I want. 
3. I looked at three public APIs. I found the free NASA one that delivered quality space images 
and for it would fit well with a Google groq API to analyze said images. 

What did I learn about working with APIs?
APIs can work sequentially, not just in parallel. The output of one API becomes
the input of another. Also learned that API design matters - NASA's consistent
JSON structure made it easy to work with, while groq required more careful
prompt engineering.

How did AI tools help or hinder understanding?
AI tools (like using Claude to generate initial code) helped with boilerplate
and structure, but I had to understand the logic to debug and refine. For example,
the AI didn't initially handle the case where NASA returns no explanation, so
I had to add that error handling myself. It accelerated development but couldn't
replace understanding how APIs actually work.
The AI tools help me understand the flowchart and the way I should structure the architecture of the code. 

PROBLEM STATEMENT:
"I want to help students and space enthusiasts understand complex 
astronomy by combining NASA's professional imagery with AI-powered explanations"

HOW EACH API HELPS:
- NASA APOD API: Provides authentic, high-quality space imagery and scientifically
  accurate descriptions written by professional astronomers. This gives us real,
  credible content to work with.

- Google groq AI: Acts as a translation layer, taking technical scientific
  language and converting it into accessible explanations suitable for beginners.
  This makes space education inclusive and removes the intimidation factor.

HOW THEY COMBINE MEANINGFULLY:
The APIs work in sequence - NASA provides the authoritative source material,
and groq transforms it for a different audience. Without NASA, we'd have no
reliable content. Without groq, that content would remain inaccessible to
many learners. Together, they democratize space education.

CHALLENGE FACED:
Initially, groq's responses were too verbose (200+ words), which defeated
the purpose of "simplification." The technical explanation was shorter than
the "simple" version! 

SOLUTION: Refined the prompt to explicitly request "under 100 words" and added
"engaging" to encourage concise, punchy language. Also added instruction to
"use everyday analogies" which made the output more relatable.