from transformers import pipeline

classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)

def analyze_text(text):
    results = classifier(text)
    results = results[0]  
    return results

def get_top_emotion(analysis):
    return analysis[0]['label']
