import math
from operator import itemgetter

def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def distancia_total(ruta, coord, almacen):
    total = distancia(almacen, coord[ruta[0]])
    for i in range(len(ruta) - 1):
        total += distancia(coord[ruta[i]], coord[ruta[i + 1]])
    total += distancia(coord[ruta[-1]], almacen)
    return total

def peso_ruta(ruta, pedidos):
    return sum([pedidos[c] for c in ruta])

def en_ruta(rutas, c):
    for r in rutas:
        if c in r:
            return r
    return None

def vrp_voraz(coord, pedidos, almacen, max_carga, max_clientes):
    s = {}
    for c1 in coord:
        for c2 in coord:
            if c1 != c2 and (c2, c1) not in s:
                d_c1_c2 = distancia(coord[c1], coord[c2])
                d_c1_almacen = distancia(coord[c1], almacen)
                d_c2_almacen = distancia(coord[c2], almacen)
                s[(c1, c2)] = d_c1_almacen + d_c2_almacen - d_c1_c2

    s = sorted(s.items(), key=itemgetter(1), reverse=True)
    rutas = []

    for k, _ in s:
        c1, c2 = k
        rc1 = en_ruta(rutas, c1)
        rc2 = en_ruta(rutas, c2)

        def cumple_restricciones(r):
            peso_ok = peso_ruta(r, pedidos) <= max_carga
            clientes_ok = len(r) <= max_clientes
            return peso_ok and clientes_ok

        if rc1 is None and rc2 is None:
            nueva_ruta = [c1, c2]
            if cumple_restricciones(nueva_ruta):
                rutas.append(nueva_ruta)
        elif rc1 is not None and rc2 is None:
            if rc1[0] == c1:
                nueva = [c2] + rc1
                if cumple_restricciones(nueva):
                    rutas[rutas.index(rc1)] = nueva
            elif rc1[-1] == c1:
                nueva = rc1 + [c2]
                if cumple_restricciones(nueva):
                    rutas[rutas.index(rc1)] = nueva
        elif rc1 is None and rc2 is not None:
            if rc2[0] == c2:
                nueva = [c1] + rc2
                if cumple_restricciones(nueva):
                    rutas[rutas.index(rc2)] = nueva
            elif rc2[-1] == c2:
                nueva = rc2 + [c1]
                if cumple_restricciones(nueva):
                    rutas[rutas.index(rc2)] = nueva
        elif rc1 != rc2:
            if rc1[-1] == c1 and rc2[0] == c2:
                nueva = rc1 + rc2
                if cumple_restricciones(nueva):
                    rutas.remove(rc1)
                    rutas.remove(rc2)
                    rutas.append(nueva)
            elif rc2[-1] == c2 and rc1[0] == c1:
                nueva = rc2 + rc1
                if cumple_restricciones(nueva):
                    rutas.remove(rc1)
                    rutas.remove(rc2)
                    rutas.append(nueva)

    return rutas

if __name__ == "__main__":
    coord = {
        'EDO.MEX': (19.29379546003528, -99.65370007457237),
        'QRO': (20.285934613275167, -100.0305177136275),
        'CDMX': (19.432652099495538, -99.13321421505111),
        'SLP': (22.151090482894386, -100.97400123008491),
        'MTY': (25.672389939722347, -100.2979069652517),
        'PUE': (19.0630252455807, -98.3078707414849),
        'GDL': (20.677174509247386, -103.34700546105012),
        'MICH': (19.702524985126907, -101.19233198226928),
        'SON': (29.07517004365961, -110.95964623200271)
    }

    pedidos = {
        'EDO.MEX': 10,
        'QRO': 13,
        'CDMX': 7,
        'SLP': 11,
        'MTY': 15,
        'PUE': 8,
        'GDL': 6,
        'MICH': 7,
        'SON': 8
    }

    almacen = (19.29379546003528, -99.65370007457237)
    max_carga = 40
    max_clientes = 4

    rutas = vrp_voraz(coord, pedidos, almacen, max_carga, max_clientes)

    print(f"\nNúmero total de rutas generadas: {len(rutas)}\n")

    for i, ruta in enumerate(rutas):
        carga = peso_ruta(ruta, pedidos)
        distancia_ruta = distancia_total(ruta, coord, almacen)
        print(f"Ruta {i+1}: {ruta} (Carga: {carga}, Distancia: {distancia_ruta:.2f} km, Clientes: {len(ruta)})")
