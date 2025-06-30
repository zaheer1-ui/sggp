from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def evaluate_answer(model_answer, student_answer, full_marks):
    embeddings = model.encode([model_answer, student_answer])
    similarity = util.cos_sim(embeddings[0], embeddings[1]).item()

    if similarity > 0.85:
        return full_marks
    elif similarity > 0.6:
        return round(full_marks * 0.5)
    else:
        return 0