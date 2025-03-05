import requests
import os
import matplotlib.pyplot as plt
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

def extract_figures_count(pdf_path):
    """Envía un PDF a Grobid y cuenta las figuras en el XML"""
    with open(pdf_path, 'rb') as pdf_file:
        files = {'input': pdf_file}
        response = requests.post(GROBID_URL + "/api/processFulltextDocument", files=files, params={"consolidate": "1"})

    if response.status_code == 200:
        xml_content = response.text
        return xml_content.count("<figure")  # Cuenta las etiquetas <figure>
    return None

def generate_figures_chart(figures_data, output_path):
    """Genera una gráfica de figuras por artículo"""
    articles = list(figures_data.keys())
    figure_counts = list(figures_data.values())

    plt.figure(figsize=(10, 5))
    plt.bar(articles, figure_counts, color='skyblue')
    plt.xlabel("Artículo")
    plt.ylabel("Número de Figuras")
    plt.title("Número de Figuras por Artículo")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"✅ Gráfica guardada en {output_path}")

if __name__ == "__main__":
    wait_for_grobid()

    os.makedirs("/data/figures/", exist_ok=True)

    pdf_files = [f for f in os.listdir("/data/papers/") if f.endswith(".pdf")]
    if not pdf_files:
        print("⚠️ No se encontraron PDFs en /data/papers/")
        exit(1)

    figures_data = {}
    for pdf in pdf_files:
        print(f"📄 Procesando {pdf}...")
        figures_count = extract_figures_count(f"/data/papers/{pdf}")
        if figures_count is not None:
            figures_data[pdf] = figures_count
        else:
            print(f"❌ No se pudo extraer información de figuras en {pdf}")

    if figures_data:
        output_path = "/data/figures/figures_per_article.png"
        generate_figures_chart(figures_data, output_path)
