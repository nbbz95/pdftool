def parsear_rangos(texto, total):
    """Convierte '1-3,5,8-' en índices base 0. Las páginas se numeran desde 1, como las ve el usuario."""
    indices = []
    for parte in texto.split(","):
        parte = parte.strip()
        if not parte:
            continue
        if "-" in parte:
            ini, fin = parte.split("-", 1)
            ini = int(ini) if ini else 1
            fin = int(fin) if fin else total
        else:
            ini = fin = int(parte)
        if not (1 <= ini <= fin <= total):
            raise ValueError(f"Rango fuera de límites: '{parte}' (el PDF tiene {total} páginas)")
        indices.extend(range(ini - 1, fin))
    return indices
