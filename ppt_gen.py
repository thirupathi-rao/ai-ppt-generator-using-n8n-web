import streamlit as st
import requests
import subprocess
import sys
import os

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="GenSlide AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ANIMATED BACKGROUND & CUSTOM VISUALS
st.markdown("""
    <style>
    /* --- ANIMATED BACKGROUND --- */
    @keyframes gradient-animation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        /* The Gradient: soft pastel colors (Orange, Pink, Blue, Purple) */
        background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #fad0c4, #a18cd1, #fbc2eb);
        background-size: 400% 400%;
        animation: gradient-animation 15s ease infinite;
        background-attachment: fixed;
    }

    /* --- SIDEBAR STYLING (UNIFIED FLOW) --- */
    [data-testid="stSidebar"] {
        /* Increased transparency to let the main gradient show through */
        background: rgba(255, 255, 255, 0.35); 
        /* Stronger blur to ensure text is readable over the moving colors */
        backdrop-filter: blur(20px); 
        /* A subtle border to define the edge without breaking the flow */
        border-right: 1px solid rgba(255, 255, 255, 0.4);
        /* Soft shadow to give it depth */
        box-shadow: 10px 0 30px rgba(0, 0, 0, 0.05);
    }
    
    /* Remove the default sidebar user content separation line to make it cleaner */
    [data-testid="stSidebarNav"] {
        border-bottom: 1px solid rgba(255, 255, 255, 0.3);
    }

    /* --- TEXT VISIBILITY FIX --- */
    h1, h2, h3, p, li, .stMarkdown, label, .stSelectbox label {
        color: #4a4a4a !important;
    }

    /* --- TITLE STYLING --- */
    .title-text {
        font-weight: 800;
        font-size: 3.5em;
        color: #2c3e50; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 0px;
    }
    .subtitle-text {
        font-size: 1.2em;
        color: #555 !important;
        margin-bottom: 30px;
        font-weight: 500;
    }
    
    /* --- TEXT AREA STYLING --- */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.7); /* More transparent */
        backdrop-filter: blur(10px);
        color: #333 !important; 
        border-radius: 15px;
        border: 2px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        font-size: 16px;
    }
    
    .stTextArea textarea:focus {
        background: rgba(255, 255, 255, 0.9);
        border-color: #fbc2eb;
        box-shadow: 0 4px 20px rgba(251, 194, 235, 0.4);
    }

    /* --- BUTTON STYLING --- */
    .stButton>button {
        background-image: linear-gradient(to right, #a18cd1 0%, #fbc2eb 100%);
        color: white !important;
        border: none;
        border-radius: 30px;
        padding: 15px 40px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(161, 140, 209, 0.4);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(161, 140, 209, 0.6);
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Configuration)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=60)
    st.header("🎨 Design Studio")
    st.write("Craft your presentation style.")
    
    st.divider()

    st.subheader("🔤 Typography")
    SUPPORTED_FONTS = ["Arial", "Calibri", "Comic Sans MS", "Georgia", "Impact", "Verdana"]
    title_font = st.selectbox("Title Font", SUPPORTED_FONTS, index=0)
    body_font = st.selectbox("Body Font", SUPPORTED_FONTS, index=1)
    
    st.divider()

    st.subheader("🎨 Theme")
    THEME_PRESETS = ["Corporate Blue", "Forest Green", "Sunset Orange", "Modern Dark", "Purple Haze"]
    theme = st.selectbox("Color Theme", THEME_PRESETS, index=0)

    st.divider()
    
    st.subheader("⚙️ Config")
    author_name = st.text_input("Author Name", value="AI Assistant")
    slide_count = st.slider("Total Slides", min_value=3, max_value=10, value=5)

# 4. MAIN PAGE CONTENT
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<p class="title-text">GenSlide AI ✨</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text">Turn simple ideas into dynamic PowerPoint presentations.</p>', unsafe_allow_html=True)

with col2:
    # Adding a transparent card effect for the tip
    st.markdown("""
    <div style="background-color: rgba(255,255,255,0.5); backdrop-filter: blur(10px); padding: 20px; border-radius: 10px; border-left: 5px solid #a18cd1; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
        <strong>💡 Pro Tip:</strong><br>
        Try asking for specific slide structures, like <em>"Include a Pros & Cons slide"</em>.
    </div>
    """, unsafe_allow_html=True)

st.write("") # Spacer

# Input Area
st.markdown("### 📝 Topic & Instructions")
prompt_input = st.text_area("What should this presentation be about?", height=150, placeholder="e.g. A pitch deck for a new mobile app that helps people find parking spots...")

# Generate Button
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    generate_btn = st.button("🚀 Generate Presentation")

# 5. LOGIC & EXECUTION
if generate_btn:
    if not prompt_input:
        st.warning("⚠️ Please describe your presentation topic first.")
    else:
        status_container = st.container()
        with status_container:
            with st.spinner("✨ Weaving magic... (Connecting to AI)"):
                try:
                    # N8N Webhook URL
                    n8n_webhook_url = "https://dtr44.app.n8n.cloud/webhook-test/b90f46af-a9c3-4558-b161-088909f0b124"
                    
                    payload = {
                        "prompt": prompt_input,
                        "title_font": title_font,
                        "body_font": body_font,
                        "theme": theme,
                        "slide_count": slide_count,
                        "author": author_name
                    }
                    
                    response = requests.post(n8n_webhook_url, json=payload)
                    
                    if response.status_code == 200:
                        # Success Logic
                        generated_code = response.json().get("output", "")
                        
                        # Clean Code
                        if "```python" in generated_code:
                            generated_code = generated_code.split("```python")[1]
                        if "```" in generated_code:
                            generated_code = generated_code.split("```")[0]
                        
                        # Save Script
                        script_path = "generated_presentation.py"
                        with open(script_path, "w") as f:
                            f.write(generated_code)
                        
                        # Run Script
                        result = subprocess.run(
                            [sys.executable, script_path], 
                            capture_output=True, 
                            text=True
                        )
                        
                        if result.returncode == 0:
                            st.balloons()
                            st.success("🎉 Presentation Ready!")
                            
                            col_res1, col_res2 = st.columns(2)
                            with col_res1:
                                st.markdown("""
                                <div style="background-color: rgba(255,255,255,0.6); backdrop-filter: blur(10px); padding: 15px; border-radius: 10px;">
                                    <h3>📁 File Summary</h3>
                                    <p>Your slides have been generated successfully based on your selected theme.</p>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with col_res2:
                                with open("aippt.pptx", "rb") as file:
                                    st.download_button(
                                        label="📥 Download .pptx",
                                        data=file,
                                        file_name="GenSlide_Presentation.pptx",
                                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                                        use_container_width=True
                                    )
                        else:
                            st.error("❌ Python Generation Failed")
                            with st.expander("Debug Logs"):
                                st.code(result.stderr)
                    else:
                        st.error(f"❌ Network Error: {response.status_code}")
                
                except Exception as e:
                    st.error(f"❌ System Error: {e}")