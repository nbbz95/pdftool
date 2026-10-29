import json

import pytest
from pypdf import PdfReader

from pdftool import operaciones
from pdftool.cli import main
from pdftool.rangos import parsear_rangos


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [("1", [0]), ("1-3", [0, 1, 2]), ("2,4", [1, 3]), ("4-", [3, 4]), ("-2", [0, 1])],
)
def test_parsear_rangos(texto, esperado):
    assert parsear_rangos(texto, 5) == esperado


def test_parsear_rangos_fuera_de_limite():
    with pytest.raises(ValueError):
        parsear_rangos("6", 5)


def test_unir(crear_pdf, tmp_path):
    a = crear_pdf("a.pdf", ["uno", "dos"])
    b = crear_pdf("b.pdf", ["tres"])
    salida = tmp_path / "unido.pdf"
    assert operaciones.unir([a, b], salida) == 3
    assert "tres" in PdfReader(salida).pages[2].extract_text()


def test_partir(crear_pdf, tmp_path):
    a = crear_pdf("doc.pdf", ["uno", "dos", "tres"])
    archivos = operaciones.partir(a, tmp_path / "out", "2-3")
    assert [f.name for f in archivos] == ["doc_p2.pdf", "doc_p3.pdf"]


def test_extraer_paginas(crear_pdf, tmp_path):
    a = crear_pdf("doc.pdf", ["uno", "dos", "tres"])
    salida = tmp_path / "x.pdf"
    assert operaciones.extraer_paginas(a, salida, "1,3") == 2
    assert "tres" in PdfReader(salida).pages[1].extract_text()


def test_rotar(crear_pdf, tmp_path):
    a = crear_pdf("doc.pdf", ["uno", "dos"])
    salida = tmp_path / "r.pdf"
    operaciones.rotar(a, salida, 90, "2")
    paginas = PdfReader(salida).pages
    assert [p.rotation for p in paginas] == [0, 90]


def test_rotar_grados_invalidos(crear_pdf, tmp_path):
    with pytest.raises(ValueError):
        operaciones.rotar(crear_pdf("doc.pdf", ["uno"]), tmp_path / "r.pdf", 45)


def test_texto(crear_pdf):
    a = crear_pdf("doc.pdf", ["Hola mundo", "Chau"])
    assert "Hola mundo" in operaciones.texto(a, "1")
    assert "Chau" not in operaciones.texto(a, "1")


def test_cli_info_json(crear_pdf, capsys):
    a = crear_pdf("doc.pdf", ["uno", "dos"])
    assert main(["info", str(a), "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["paginas"] == 2


def test_cli_error_archivo_inexistente(capsys):
    assert main(["info", "no-existe.pdf"]) == 1
    assert "Error" in capsys.readouterr().err
