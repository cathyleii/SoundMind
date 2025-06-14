from gradio_client import Client

classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)

def analyze_text(text):
    client = Client("Cleii/SentimentAnalysis")
    result = client.predict(
		text=text,
		api_name="/predict"
    )
    return result

def get_top_emotion(analysis):
    return analysis[0]['label']

def get_emotions(analysis):
    emotions = []
    for emotion in analysis:
        emotions.append(emotion["label"])
    
    return emotions
