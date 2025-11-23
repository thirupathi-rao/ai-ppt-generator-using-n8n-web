# ai-ppt-generator-using-n8n-web
GenSlide AI 🚀

Automated PowerPoint Generator using Streamlit, n8n, and Python

This project allows users to generate professional PowerPoint presentations (.pptx) by entering a topic. It uses a Streamlit frontend to capture user requirements, sends them to an n8n AI Agent, which generates Python code. This code is then executed locally to build the slide deck.

🛠️ Tech Stack

Frontend: Streamlit (Python)

Orchestration: n8n (Webhook & AI Agent)

PPT Generation: python-pptx library

LLM: OpenAI GPT-4o or GPT-3.5-Turbo (via n8n)

1. Python Setup (Local Machine)

Prerequisites

Python 3.10+ installed.

An n8n instance (Cloud or Self-hosted).

Installation Steps

Clone/Create Project Folder:
Open your terminal in your project directory (e.g., D:\ds3\bot\streamlit_n8n\powerpoint\).

Create a Virtual Environment:
It is crucial to use a virtual environment to manage dependencies.

# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate


Install Dependencies:
Create a file named requirements.txt with the content below, or install manually.

File: requirements.txt

streamlit
requests
python-pptx


Install Command:

pip install -r requirements.txt


2. n8n Workflow Structure 🧠

You need to create a simple 3-node workflow in n8n.

Node 1: Webhook (Trigger)

HTTP Method: POST

Path: webhook-test/b90f46af-a9c3-4558-b161-088909f0b124 (or your specific ID).

Authentication: None (for testing) or Header Auth.

Input Data: The Streamlit app sends this JSON payload:

{
  "prompt": "Topic string",
  "title_font": "Arial",
  "body_font": "Calibri",
  "slide_count": 5,
  "author": "User Name"
}


Node 2: AI Agent (The Brain)

Model: OpenAI (Chat Model) using gpt-4o or gpt-3.5-turbo.

System Message: Copy from Section 3 below.

User Message: Copy from Section 3 below.

Output: The model must generate raw Python code.

Node 3: Respond to Webhook (Output)

Respond With: JSON

Response Body:

{
  "output": "{{ $json.output }}" 
}


(Note: Ensure you map the text output from the AI Agent to the "output" key).

3. The Prompts (Critical for Stability) 📝

These prompts contain specific "Anti-Crash" rules (preventing IndexError and AttributeError). Copy them exactly.

🅰️ System Message (Paste in n8n Agent System Prompt)

Role: You are an expert Python Developer specialized in the `python-pptx` library.

Objective: Output a complete, runnable Python script that generates a PowerPoint file named 'aippt.pptx'.

Critical Rules:
1. Library: You must use `import pptx`, `from pptx.util import Pt, Inches`, `from pptx.dml.color import RGBColor`.
2. Safe Text Handling: NEVER access `.runs[0]` directly on a new slide. ALWAYS clear text and use `.add_run()`.
3. Formatting: Return ONLY the raw Python code. Do NOT wrap it in Markdown.


🅱️ User Message (Paste in n8n Agent User Prompt)

Note: The {{ ... }} syntax below is for n8n variable injection.

Write a Python script to generate a PowerPoint presentation.

Topic: "{{ $json.body.prompt }}"
Presented By: "{{ $json.body.author }}"
Number of Slides: {{ $json.body.slide_count }}

Design Config:
- Title Font: "{{ $json.body.title_font }}"
- Body Font: "{{ $json.body.body_font }}"
- Filename: "aippt.pptx"

**CRITICAL CODING RULES (STRICTLY ENFORCED):**
1. **NO `remove_paragraph`:** The method `tf.remove_paragraph()` DOES NOT EXIST. Never use it.
2. **NO `runs[0]` ACCESS:** Never access `paragraph.runs[0]` directly. It causes IndexErrors.
3. **HOW TO CLEAR TEXT:** To clear a TextFrame, you must ONLY use `text_frame.clear()`. This removes all text but leaves one empty paragraph.
4. **MANDATORY HELPER FUNCTION:** You MUST define and use this exact function for setting text:
   ```python
   def set_text(paragraph, text, font_name, font_size, color_rgb, is_bold=False):
       paragraph.clear()  # Removes all existing runs
       run = paragraph.add_run() 
       run.text = text
       run.font.name = font_name
       run.font.size = Pt(font_size)
       run.font.color.rgb = color_rgb
       run.font.bold = is_bold


Background Logic:

Select a theme based on the topic (e.g., Blue for Finance, Green for Nature).

Define THEME_PRESETS with a background key (light pastel RGB).

Apply background: slide.background.fill.solid() then slide.background.fill.fore_color.rgb = theme['background'].

Slide Generation Logic:

Slide 1 (Title): Layout 0.

Slides 2-N (Content): Layout 1.

Access body: tf = slide.shapes.placeholders[1].text_frame

CLEAR IT: tf.clear()

ADD BULLETS: - Item 1: p = tf.paragraphs[0] -> set_text(p, ...)

Item 2+: p = tf.add_paragraph() -> set_text(p, ...)

Output ONLY raw Python code.


---

## 4. How to Run 🏃‍♂️

1.  Activate your virtual environment.
    ```powershell
    .\venv\Scripts\activate
    ```
2.  Update the `n8n_webhook_url` variable in `app.py` to match your n8n Production URL.
3.  Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```
4.  Open your browser to the URL shown (usually `http://localhost:8501`).
5.  Enter a topic and click **Generate Presentation**.

## 5. Troubleshooting 🔧

* **`ModuleNotFoundError: No module named 'pptx'`**:
    * Make sure you installed requirements inside the virtual environment (`venv`).
    * Ensure the `subprocess.run` command in `app.py` is using `sys.executable`.

* **Script generates but no file downloads**:
    * Check your terminal for Python errors. The app is configured to show `stderr` (error logs) in a red box on the UI.
    * If you see `IndexError: tuple index out of range`, your n8n prompt is likely old. Update it with the prompts in **Section 3**.
