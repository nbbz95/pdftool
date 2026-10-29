import argparse
import json
import sys

from pdftool import __version__, operaciones


def construir_parser():
    p = argparse.ArgumentParser(prog="pdftool", description="Herramientas para PDF desde la terminal.")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(dest="comando", required=True)

    s = sub.add_parser("unir", help="Une varios PDF en uno")
    s.add_argument("entradas", nargs="+")
    s.add_argument("-o", "--salida", required=True)

    s = sub.add_parser("partir", help="Genera un PDF por página")
    s.add_argument("entrada")
    s.add_argument("-d", "--carpeta", default=".")
    s.add_argument("-p", "--paginas", help="Rango, ej: 1-3,5")

    s = sub.add_parser("extraer", help="Copia un rango de páginas a un PDF nuevo")
    s.add_argument("entrada")
    s.add_argument("-p", "--paginas", required=True, help="Rango, ej: 2-4,7")
    s.add_argument("-o", "--salida", required=True)

    s = sub.add_parser("rotar", help="Rota páginas")
    s.add_argument("entrada")
    s.add_argument("-g", "--grados", type=int, default=90)
    s.add_argument("-p", "--paginas")
    s.add_argument("-o", "--salida", required=True)

    s = sub.add_parser("texto", help="Extrae el texto")
    s.add_argument("entrada")
    s.add_argument("-p", "--paginas")
    s.add_argument("-o", "--salida", help="Archivo .txt (por defecto, la pantalla)")

    s = sub.add_parser("info", help="Muestra metadatos y cantidad de páginas")
    s.add_argument("entrada")
    s.add_argument("--json", action="store_true")
    return p


def main(argv=None):
    args = construir_parser().parse_args(argv)
    try:
        if args.comando == "unir":
            n = operaciones.unir(args.entradas, args.salida)
            print(f"Listo: {args.salida} ({n} páginas)")
        elif args.comando == "partir":
            archivos = operaciones.partir(args.entrada, args.carpeta, args.paginas)
            print(f"Listo: {len(archivos)} archivos en {args.carpeta}")
        elif args.comando == "extraer":
            n = operaciones.extraer_paginas(args.entrada, args.salida, args.paginas)
            print(f"Listo: {args.salida} ({n} páginas)")
        elif args.comando == "rotar":
            n = operaciones.rotar(args.entrada, args.salida, args.grados, args.paginas)
            print(f"Listo: {n} páginas rotadas {args.grados}° en {args.salida}")
        elif args.comando == "texto":
            contenido = operaciones.texto(args.entrada, args.paginas)
            if args.salida:
                with open(args.salida, "w", encoding="utf-8") as f:
                    f.write(contenido)
                print(f"Listo: {args.salida}")
            else:
                print(contenido)
        elif args.comando == "info":
            datos = operaciones.info(args.entrada)
            if args.json:
                print(json.dumps(datos, ensure_ascii=False, indent=2))
            else:
                for k, v in datos.items():
                    print(f"{k:>11}: {v if v is not None else '-'}")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
