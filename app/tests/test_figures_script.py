import pytest
import os
import sys
from unittest.mock import patch, mock_open, MagicMock
import requests
import matplotlib.pyplot as plt

# Importa el script a testear
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from figures_script import extract_figures_count, generate_figures_chart, wait_for_grobid

@pytest.fixture
def mock_grobid_response():
    """Simula una respuesta XML de Grobid con figuras."""
    return """<tei><text>
                <figure>Figura 1</figure>
                <figure>Figura 2</figure>
                <figure>Figura 3</figure>
              </text></tei>"""

@patch("requests.get")
def test_wait_for_grobid(mock_get):
    """Test para verificar que espera correctamente a Grobid."""
    mock_get.return_value.status_code = 200
    wait_for_grobid()
    mock_get.assert_called_with("http://localhost:8070/api/isalive")

@patch("requests.post")
def test_extract_figures_count(mock_post, mock_grobid_response):
    """Test para verificar la extracción de figuras desde Grobid."""
    mock_post.return_value.status_code = 200
    mock_post.return_value.text = mock_grobid_response

    with patch("builtins.open", mock_open(read_data="dummy pdf data")):
        count = extract_figures_count("dummy.pdf")

    assert count == 3  # Esperamos que cuente 3 figuras

@patch("matplotlib.pyplot.savefig")
def test_generate_figures_chart(mock_savefig):
    """Test para verificar que la gráfica se genera correctamente."""
    figures_data = {"paper1.pdf": 2, "paper2.pdf": 5}

    output_path = "test_chart.png"
    generate_figures_chart(figures_data, output_path)

    # Verifica que matplotlib intentó guardar la imagen
    mock_savefig.assert_called_once_with(output_path)
