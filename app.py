from flask import Flask, render_template, request
import os  # Necesario para acceder a las variables de entorno

app = Flask(__name__)

# Función vrp_voraz (algoritmo voraz simplificado)
def vrp_voraz(coord, pedidos, almacen, max_carga, max_clientes):
    rutas = []
    clientes = list(coord.keys())
    
    # Ejemplo de asignación de clientes a rutas
    for i in range(0, len(clientes), max_clientes):
        ruta = [almacen]  # Comienza desde el almacén
        carga_total = 0
        
        # Recorre los clientes de la ruta
        for j in range(i, min(i + max_clientes, len(clientes))):
            lugar = clientes[j]
            carga_total += pedidos[lugar]
            if carga_total <= max_carga:
                ruta.append(lugar)
            else:
                break
        ruta.append(almacen)  # Regresar al almacén
        rutas.append(ruta)
    
    return rutas

# Función para calcular la carga total de una ruta
def peso_ruta(ruta, pedidos):
    return sum(pedidos[lugar] for lugar in ruta if lugar in pedidos)

# Función para calcular la distancia total de una ruta
def distancia_total(ruta, coord, almacen):
    distancia = 0.0
    for i in range(len(ruta) - 1):
        lugar1 = ruta[i]
        lugar2 = ruta[i + 1]
        if lugar1 in coord and lugar2 in coord:
            lat1, lon1 = coord[lugar1]
            lat2, lon2 = coord[lugar2]
            distancia += ((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) ** 0.5
    return distancia

@app.route('/', methods=['GET', 'POST'])
def index():
    rutas = []
    if request.method == 'POST':
        lugares = request.form.getlist('lugar')
        latitudes = request.form.getlist('latitud')
        longitudes = request.form.getlist('longitud')
        pedidos_lista = request.form.getlist('pedido')

        if not lugares or not latitudes or not longitudes or not pedidos_lista:
            return render_template('formulario.html', error="Por favor complete todos los campos.", submitted=False)

        # Procesamiento de los datos recibidos
        coord = {}
        pedidos = {}
        for i in range(len(lugares)):
            lugar = lugares[i].strip()
            try:
                lat = float(latitudes[i].strip()) if latitudes[i].strip() else None
                lon = float(longitudes[i].strip()) if longitudes[i].strip() else None
                if lat is not None and lon is not None:
                    coord[lugar] = (lat, lon)
                    pedidos[lugar] = int(pedidos_lista[i])
                else:
                    raise ValueError(f"Latitud o longitud vacía para {lugar}")
            except ValueError as e:
                return render_template('formulario.html', error=f"Error en los datos: {e}", submitted=False)

        almacen = (19.29379546003528, -99.65370007457237)  # Ubicación del almacén (fijo)

        # Restricciones de carga y número de clientes
        max_carga = 100
        max_clientes = 10

        # Calculando las rutas
        rutas = vrp_voraz(coord, pedidos, almacen, max_carga, max_clientes)

        # Mostrando el resumen de las rutas calculadas
        resumen = []
        for i, ruta in enumerate(rutas):
            carga = peso_ruta(ruta, pedidos)
            dist = distancia_total(ruta, coord, almacen)
            resumen.append({
                'id': i + 1,
                'ruta': ruta,
                'carga': carga,
                'distancia': round(dist, 2),
                'clientes': len(ruta)
            })

        # Retornar los resultados
        return render_template('formulario.html', rutas=resumen, submitted=True)

    return render_template('formulario.html', submitted=False)

if __name__ == "__main__":
    # Usamos el puerto proporcionado por el entorno de Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)  # Asegúrate de estar usando '0.0.0.0' en producción
