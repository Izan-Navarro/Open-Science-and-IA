import requests
import os
import re
import time

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

def extract_text(pdf_path):
    """Envía un PDF a Grobid y extrae el texto completo"""
    with open(pdf_path, 'rb') as pdf_file:
        files = {'input': pdf_file}
        response = requests.post(GROBID_URL + "/api/processFulltextDocument", files=files, params={"consolidate": "1"})

    if response.status_code == 200:
        return response.text
    return None

def extract_links(text):
    """Extrae enlaces (URLs) del texto usando expresiones regulares"""
    pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    return re.findall(pattern, text)

def save_links(pdf_name, links):
    """Guarda los enlaces en un archivo de texto"""
    output_dir = "/data/links/"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, pdf_name.replace(".pdf", "_links.txt"))
    
    with open(output_path, "w", encoding="utf-8") as f:
        for link in links:
            f.write(link + "\n")
    
    print(f"✅ Enlaces guardados en {output_path}")

if __name__ == "__main__":
    wait_for_grobid()

    pdf_files = [f for f in os.listdir("/data/papers/") if f.endswith(".pdf")]

    if not pdf_files:
        print("⚠️ No se encontraron PDFs en /data/papers/")
        exit(1)

    for pdf in pdf_files:
        print(f"📄 Procesando {pdf}...")
        text = extract_text(f"/data/papers/{pdf}")
        if text:
            links = extract_links(text)
            if links:
                save_links(pdf, links)
            else:
                print(f"⚠️ No se encontraron enlaces en {pdf}")
        else:
            print(f"❌ No se pudo extraer el texto de {pdf}")
