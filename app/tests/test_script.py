import pytest
import os
import sys
from unittest.mock import patch, mock_open, MagicMock
import requests

# Importa el script a testear
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from script import extract_abstract, clean_text, generate_wordcloud, wait_for_grobid

@pytest.fixture
def mock_grobid_response():
    """Simula una respuesta XML de Grobid con un abstract"""
    return """<tei><abstract>This is a test abstract with NLP processing and stopwords removal.</abstract></tei>"""

@patch("requests.get")
def test_wait_for_grobid(mock_get):
    """Test para verificar que espera correctamente a Grobid."""
    mock_get.return_value.status_code = 200
    wait_for_grobid()
    mock_get.assert_called_with("http://localhost:8070/api/isalive")

@patch("requests.post")
def test_extract_abstract(mock_post, mock_grobid_response):
    """Test para verificar la extracción del abstract desde Grobid."""
    mock_post.return_value.status_code = 200
    mock_post.return_value.text = mock_grobid_response

    with patch("builtins.open", mock_open(read_data="dummy pdf data")):
        abstract = extract_abstract("dummy.pdf")

    assert abstract == "This is a test abstract with NLP processing and stopwords removal."

def test_clean_text():
    """Test para verificar la limpieza del texto eliminando stopwords."""
    sample_text = "This is a test abstract with NLP processing and stopwords removal."
    
    with patch("nltk.corpus.stopwords.words", return_value={"is", "a", "and", "with"}):
        cleaned_text = clean_text(sample_text)

    assert cleaned_text == "this test abstract nlp processing stopwords removal."

@patch("matplotlib.pyplot.savefig")
def test_generate_wordcloud(mock_savefig):
    """Test para verificar que la nube de palabras se genera correctamente."""
    sample_text = "test test test abstract abstract"
    output_path = "wordcloud.png"

    generate_wordcloud(sample_text, output_path)

    # Verifica que se intentó guardar la imagen
    mock_savefig.assert_called_once_with(output_path)
