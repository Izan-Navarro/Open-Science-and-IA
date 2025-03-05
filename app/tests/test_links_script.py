import pytest
import os
import sys
from unittest.mock import patch, mock_open, MagicMock
import requests

# Importa el script a testear
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from links_script import extract_text, extract_links, save_links, wait_for_grobid

@pytest.fixture
def mock_grobid_response():
    """Simula una respuesta XML de Grobid con texto que contiene enlaces."""
    return """<tei><text>
                Here is a link: https://example.com
                Another one: http://test.com
                And a www.testsite.com
              </text></tei>"""

@patch("requests.get")
def test_wait_for_grobid(mock_get):
    """Test para verificar que espera correctamente a Grobid."""
    mock_get.return_value.status_code = 200
    wait_for_grobid()
    mock_get.assert_called_with("http://localhost:8070/api/isalive")

@patch("requests.post")
def test_extract_text(mock_post, mock_grobid_response):
    """Test para verificar la extracción de texto desde Grobid."""
    mock_post.return_value.status_code = 200
    mock_post.return_value.text = mock_grobid_response

    with patch("builtins.open", mock_open(read_data="dummy pdf data")):
        text = extract_text("dummy.pdf")

    assert "https://example.com" in text  # Verifica que el texto contiene un enlace simulado

def test_extract_links():
    """Test para verificar la extracción de enlaces desde texto."""
    sample_text = "Visit https://example.com and http://test.com or www.testsite.com for more info."
    links = extract_links(sample_text)

    expected_links = [
        "https://example.com",
        "http://test.com",
        "www.testsite.com"
    ]
    
    assert links == expected_links  # Verifica que los enlaces extraídos sean los esperados

@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
def test_save_links(mock_makedirs, mock_file):
    """Test para verificar que los enlaces se guardan en un archivo."""
    pdf_name = "sample.pdf"
    links = ["https://example.com", "http://test.com"]

    save_links(pdf_name, links)

    # Verifica que se intentó crear la carpeta de salida
    mock_makedirs.assert_called_once_with("/data/links/", exist_ok=True)

    # Verifica que los enlaces fueron escritos en el archivo
    mock_file().write.assert_any_call("https://example.com\n")
    mock_file().write.assert_any_call("http://test.com\n")
