
# 🧠 AI Exam Answer Evaluator (Offline)

A simple **Streamlit-based offline tool** that evaluates students' written answers by comparing them to a model answer using **semantic similarity**. It also supports **image-based OCR** with spell correction to handle handwritten or scanned answers.

---

## 🚀 Features

- ✍️ **Answer Comparison**: Compares student answers (typed or image-based) with model answers.
- 📷 **OCR Support**: Extracts text from scanned or handwritten answers using Tesseract.
- 🧠 **Semantic Scoring**: Uses `sentence-transformers` (`all-MiniLM-L6-v2`) for meaning-based similarity.
- 🔧 **Spell Correction**: Uses `TextBlob` to improve OCR accuracy.
- ✅ **Auto-Grading**: Grades answers using cosine similarity and question weights (1, 3, or 5 marks).
- 📦 **Offline Capable**: Works fully offline after initial setup.

---

## 📦 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt

