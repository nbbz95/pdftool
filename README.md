# pdftool

CLI en Python para trabajar con PDF desde la terminal: unir, partir, extraer páginas, rotar, sacar el texto y ver metadatos.

```bash
pdftool unir a.pdf b.pdf c.pdf -o todo.pdf
pdftool partir informe.pdf -d paginas/          # un PDF por página
pdftool extraer informe.pdf -p 2-4,7 -o resumen.pdf
pdftool rotar escaneo.pdf -g 90 -p 1,3 -o derecho.pdf
pdftool texto contrato.pdf -o contrato.txt
pdftool info contrato.pdf --json
```

Los rangos de páginas se escriben como los ve el usuario, desde 1: `1-3`, `5`, `8-` (de la 8 al final) o `-2` (las dos primeras), combinables con comas.

## Instalación

Con [pipx](https://pipx.pypa.io/), directo desde GitHub:

```bash
pipx install git+https://github.com/nbbz95/pdftool
```

O bajando la wheel de la última [release](https://github.com/nbbz95/pdftool/releases):

```bash
pip install pdftool-1.0.0-py3-none-any.whl
```

## Estructura

```
src/pdftool/
  cli.py          # argparse y salida por pantalla
  operaciones.py  # unir, partir, extraer, rotar, texto, info (sobre pypdf)
  rangos.py       # parser de rangos "1-3,5,8-"
tests/            # pytest; genera PDFs de prueba con fpdf2
```

La CLI solo traduce argumentos: toda la lógica está en `operaciones.py`, que se puede usar como librería.

## Desarrollo

```bash
pip install -e ".[dev]"
pytest -q
ruff check . && ruff format --check .
```

## CI/CD

- Cada push y PR corre lint y tests en Python 3.10 a 3.13 ([ci.yml](.github/workflows/ci.yml)).
- Al pushear un tag `v*` se construye la wheel y se publica una release en GitHub ([release.yml](.github/workflows/release.yml)).

## Licencia

MIT
