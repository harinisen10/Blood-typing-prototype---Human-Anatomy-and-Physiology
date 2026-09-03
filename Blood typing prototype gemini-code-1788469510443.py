import streamlit as st
from PIL import Image
from google import genai
from google.genai import types

# Page setup
st.set_page_config(page_title="Blood Typing Lab Assistant", layout="centered")
st.title("🩸 Blood Typing Lab Assistant")
st.write("Upload an image of your blood typing tray (Anti-A, Anti-B, Anti-Rh wells) for instant evaluation.")

# API Key handling via sidebar
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.info("Please enter your Gemini API Key in the sidebar to proceed.", icon="🔑")
    st.stop()

# Initialize Gemini Client
client = genai.Client(api_key=api_key)

# System Instructions / Prompt Definition
SYSTEM_PROMPT = """
You are an educational laboratory assistant for a college biology blood typing experiment.
Analyze the provided image of the blood typing test wells (Anti-A, Anti-B, Anti-Rh/D).

Provide your response strictly in the following format:
1. **Agglutination Analysis:** For each well (Anti-A, Anti-B, Anti-Rh), state whether clumping (agglutination) is Present (+) or Absent (-).
2. **Blood Phenotype:** State the determined blood group (e.g., A+, B-, AB+, O-).
3. **Possible Genotype(s):** List the potential genotypes (e.g., IAIA, IAi, etc.).
4. **Immunological Explanation:** Explain step-by-step why agglutination occurred or did not occur based on antigen-antibody interactions.
5. **Transfusion Compatibility:** List acceptable donor blood types for this patient.
"""

# Image Upload Widget
uploaded_file = st.file_uploader("Upload Blood Typing Slide Photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Test Sample", use_column_width=True)
    
    if st.button("Analyze Sample", type="primary"):
        with st.spinner("Analyzing agglutination patterns..."):
            try:
                # Send request to Gemini Flash model
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[image, SYSTEM_PROMPT]
                )
                
                st.success("Analysis Complete!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error processing image: {str(e)}")