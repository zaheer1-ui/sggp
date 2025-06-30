import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
from sentence_transformers import SentenceTransformer, util
import pytesseract
from textblob import TextBlob
import torch

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load semantic model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Page setup
st.set_page_config(page_title="🧠 AI Exam Answer Evaluator", layout="centered")
st.title("📘 AI Exam Answer Evaluator (Offline)")

# Sidebar
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
st.sidebar.header("Instructions")
st.sidebar.markdown("""
1. Enter the **question** and **model answer**  
2. Type or upload the **student answer**  
3. Select marks type  
4. Click **Evaluate Answer**
""")

# Inputs
q_type = st.selectbox("🧾 Select Question Type", [1, 3, 5])
question = st.text_area("❓ Question (Optional)", height=100)
model_ans = st.text_area("📖 Expected Answer (Teacher's Key)", height=120)
typed_answer = st.text_area("🧑‍🎓 Student Answer (Typed or from Image)", height=120)

# OCR + Spell Correction
uploaded_file = st.file_uploader("📷 Upload Image of Student Answer", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.info("Extracting text using OCR...")
    gray = image.convert("L")
    sharpened = gray.filter(ImageFilter.SHARPEN)
    enhanced = ImageEnhance.Contrast(sharpened).enhance(2.0)

    raw_text = pytesseract.image_to_string(enhanced, config="--psm 6").strip()

    if raw_text:
        corrected_text = str(TextBlob(raw_text).correct())

        st.subheader("📄 Raw OCR Output")
        st.text_area("OCR Text", value=raw_text, height=120, key="raw_ocr")

        st.subheader("✏️ Corrected Answer (Editable)")
        st.text_area("Corrected OCR Output", value=corrected_text, height=150, key="corrected_ocr_input")

        # Store corrected OCR into session so we can use it during evaluation
        st.session_state.corrected_ocr_text = corrected_text
    else:
        st.warning("❌ No text could be extracted.")

# Evaluation button
if st.button("✅ Evaluate Answer"):
    final_student_answer = typed_answer.strip()

    # If nothing typed, fallback to corrected OCR
    if not final_student_answer:
        final_student_answer = st.session_state.get("corrected_ocr_text", "").strip()

    if not model_ans.strip() or not final_student_answer:
        st.warning("⚠️ Please enter both model and student answers.")
    else:
        with st.spinner("Calculating similarity..."):
            student_embedding = model.encode(final_student_answer, convert_to_tensor=True)
            model_embedding = model.encode(model_ans.strip(), convert_to_tensor=True)

            similarity = util.cos_sim(student_embedding, model_embedding).item()
            similarity = max(0.0, min(similarity, 1.0))  # Clamp between 0 and 1

            marks = round(similarity * q_type, 2)

            st.success(f"✅ Marks Awarded: **{marks} / {q_type}**")
            st.caption(f"🧠 Cosine Similarity Score: `{round(similarity, 3)}`")

# Footer
st.markdown("---")
st.markdown("*Made with ❤️ by Zeace*")
