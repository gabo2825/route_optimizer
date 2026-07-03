import random
from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder='templates')

def xy2hilbert(n: int, x: int, y: int) -> int:
    """
    Convierte coordenadas 2D (x, y) a un índice 1D de la curva de Hilbert.
    
    Parámetros:
        n: Orden de la curva de Hilbert (la cuadrícula es de tamaño 2^n x 2^n).
        x, y: Coordenadas del punto.
    
    Retorna:
        El índice 1D (distancia a lo largo de la curva) correspondiente al punto.
    """
    d = 0
    s = 1 << (n - 1)
    
    # Iterar sobre cada nivel (bit) de la cuadrícula
    while s > 0:
        rx = 1 if (x & s) > 0 else 0
        ry = 1 if (y & s) > 0 else 0
        
        # Incrementar el índice según el cuadrante actual
        d += s * s * ((3 * rx) ^ ry)
        
        # Rotar y reflejar la subcuadrícula según el cuadrante
        if ry == 0:
            if rx == 1:
                x = s - 1 - x
                y = s - 1 - y
            # Intercambiar x e y (rotación)
            x, y = y, x
            
        s >>= 1
        
    return d

def calculate_manhattan_distance(route) -> int:
    """
    Calcula la distancia Manhattan total de una ruta de puntos (x, y).
    """
    distance = 0
    for i in range(len(route) - 1):
        p1 = route[i]
        p2 = route[i + 1]
        distance += abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    return distance

@app.route('/')
def index():
    """Sirve la interfaz principal de la simulación."""
    return render_template('index.html')

@app.route('/api/generate_routes')
def generate_routes():
    """
    Endpoint de la API que genera ubicaciones aleatorias de clientes
    y calcula las rutas bajo los dos enfoques (Hilbert vs. Orden X).
    """
    # Obtener y validar el número de clientes
    try:
        n_clients = int(request.args.get('n', 5))
        n_clients = max(3, min(15, n_clients))
    except ValueError:
        n_clients = 5

    # El depósito siempre está en (0, 0)
    depot = (0, 0)
    
    # Generar coordenadas aleatorias únicas en cuadrícula 8x8 (excluyendo el depósito)
    possible_coords = [(x, y) for x in range(8) for y in range(8) if not (x == 0 and y == 0)]
    selected_clients = random.sample(possible_coords, n_clients)
    
    # 1. Enfoque Hilbert:
    # Calcular índice Hilbert de orden 3 (para cuadrícula 8x8) para cada cliente
    clients_with_hilbert = []
    for client in selected_clients:
        h_idx = xy2hilbert(3, client[0], client[1])
        clients_with_hilbert.append({
            'x': client[0],
            'y': client[1],
            'hilbert_idx': h_idx
        })
        
    # Ordenar por el índice Hilbert
    sorted_hilbert_clients = sorted(clients_with_hilbert, key=lambda c: c['hilbert_idx'])
    hilbert_coords = [(c['x'], c['y']) for c in sorted_hilbert_clients]
    
    # 2. Enfoque Tradicional (Orden X):
    # Ordenar por la coordenada X (primario) y luego por la coordenada Y (secundario)
    sorted_traditional_clients = sorted(selected_clients, key=lambda c: (c[0], c[1]))
    
    # Construir las rutas completas de viaje redondo (inician y terminan en depósito)
    hilbert_route = [depot] + hilbert_coords + [depot]
    traditional_route = [depot] + sorted_traditional_clients + [depot]
    
    # Calcular distancias Manhattan totales
    hilbert_dist = calculate_manhattan_distance(hilbert_route)
    traditional_dist = calculate_manhattan_distance(traditional_route)
    
    # Calcular mejora de eficiencia
    efficiency_gain = 0.0
    if traditional_dist > 0:
        efficiency_gain = ((traditional_dist - hilbert_dist) / traditional_dist) * 100
        
    return jsonify({
        'clients': clients_with_hilbert,
        'hilbert_route': [{'x': p[0], 'y': p[1]} for p in hilbert_route],
        'traditional_route': [{'x': p[0], 'y': p[1]} for p in traditional_route],
        'hilbert_distance': hilbert_dist,
        'traditional_distance': traditional_dist,
        'efficiency_gain_pct': round(efficiency_gain, 1)
    })

if __name__ == '__main__':
    # Escucha localmente en el puerto 5001
    app.run(debug=True, port=5001)
