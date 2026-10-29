import pytest
from fpdf import FPDF


@pytest.fixture
def crear_pdf(tmp_path):
    """Genera un PDF de prueba con una línea de texto por página."""

    def _crear(nombre, textos):
        pdf = FPDF()
        pdf.set_font("Helvetica", size=14)
        for t in textos:
            pdf.add_page()
            pdf.cell(text=t)
        ruta = tmp_path / nombre
        pdf.output(str(ruta))
        return ruta

    return _crear
