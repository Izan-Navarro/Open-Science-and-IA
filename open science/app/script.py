import requests
import os
import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import time

nltk.download('stopwords')
from nltk.corpus import stopwords

GROBID_URL = os.getenv("GROBID_URL", "http://localhost:8070")

def wait_for_grobid():
    """Espera a que Grobid esté disponible"""
    print("⌛ Esperando a que Grobid esté disponible...")
    while True:
        try:
            response = requests.get(GROBID_URL + "/api/isalive")
            if response.status_code == 200:
                print("✅ Grobid está listo.")
                break
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(5)

def extract_abstract(pdf_path):
    """Envía un PDF a Grobid y extrae el abstract"""
    with open(pdf_path, 'rb') as pdf_file:
        files = {'input': pdf_file}
        response = requests.post(GROBID_URL + "/api/processHeaderDocument", files=files)

    if response.status_code == 200:
        text = response.text
        start = text.find("<abstract>") + 10
        end = text.find("</abstract>")
        if start > 10 and end > start:
            return text[start:end]
    return None

def clean_text(text):
    """Limpia el texto eliminando stopwords y caracteres especiales"""
    stops = set(stopwords.words('english'))
    words = [word.lower() for word in text.split() if word.lower() not in stops]
    return ' '.join(words)

def generate_wordcloud(text, output_path):
    """Genera una nube de palabras y la guarda"""
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(output_path)
    plt.close()
    print(f"✅ Nube de palabras guardada en {output_path}")

if __name__ == "__main__":
    wait_for_grobid()

    os.makedirs("/data/wordclouds/", exist_ok=True)

    pdf_files = [f for f in os.listdir("/data/papers/") if f.endswith(".pdf")]
    if not pdf_files:
        print("⚠️ No se encontraron PDFs en /data/papers/")
        exit(1)

    for pdf in pdf_files:
        print(f"📄 Procesando {pdf}...")
        abstract_text = extract_abstract(f"/data/papers/{pdf}")
        if abstract_text:
            cleaned_text = clean_text(abstract_text)
            output_path = f"/data/wordclouds/{pdf.replace('.pdf', '_wordcloud.png')}"
            generate_wordcloud(cleaned_text, output_path)
        else:
            print(f"❌ No se pudo extraer el abstract de {pdf}")
