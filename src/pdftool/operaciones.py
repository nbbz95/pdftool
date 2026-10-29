from pathlib import Path

from pypdf import PdfReader, PdfWriter

from pdftool.rangos import parsear_rangos


def unir(entradas, salida):
    writer = PdfWriter()
    for ruta in entradas:
        writer.append(str(ruta))
    with open(salida, "wb") as f:
        writer.write(f)
    return len(writer.pages)


def partir(entrada, carpeta, paginas=None):
    """Una página por archivo, o solo las del rango indicado."""
    reader = PdfReader(str(entrada))
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    indices = parsear_rangos(paginas, len(reader.pages)) if paginas else range(len(reader.pages))
    generados = []
    for i in indices:
        writer = PdfWriter()
        writer.add_page(reader.pages[i])
        destino = carpeta / f"{Path(entrada).stem}_p{i + 1}.pdf"
        with open(destino, "wb") as f:
            writer.write(f)
        generados.append(destino)
    return generados


def extraer_paginas(entrada, salida, paginas):
    reader = PdfReader(str(entrada))
    writer = PdfWriter()
    for i in parsear_rangos(paginas, len(reader.pages)):
        writer.add_page(reader.pages[i])
    with open(salida, "wb") as f:
        writer.write(f)
    return len(writer.pages)


def rotar(entrada, salida, grados, paginas=None):
    if grados % 90:
        raise ValueError("Los grados tienen que ser múltiplo de 90")
    reader = PdfReader(str(entrada))
    writer = PdfWriter(clone_from=reader)
    indices = set(parsear_rangos(paginas, len(reader.pages))) if paginas else set(range(len(reader.pages)))
    for i, pagina in enumerate(writer.pages):
        if i in indices:
            pagina.rotate(grados)
    with open(salida, "wb") as f:
        writer.write(f)
    return len(indices)


def texto(entrada, paginas=None):
    reader = PdfReader(str(entrada))
    indices = parsear_rangos(paginas, len(reader.pages)) if paginas else range(len(reader.pages))
    return "\n\f".join(reader.pages[i].extract_text() or "" for i in indices)


def info(entrada):
    reader = PdfReader(str(entrada))
    meta = reader.metadata or {}
    return {
        "archivo": str(entrada),
        "paginas": len(reader.pages),
        "encriptado": reader.is_encrypted,
        "titulo": meta.get("/Title"),
        "autor": meta.get("/Author"),
        "creador": meta.get("/Creator"),
    }
