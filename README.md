# Simulador Logístico: Curva de Hilbert vs. Orden X

Este proyecto es un prototipo interactivo desarrollado para una monografía académica de Matemática Aplicada. Compara la eficiencia de rutas logísticas utilizando el ordenamiento fractal (Curva de Hilbert) frente a un enfoque tradicional (ordenamiento por coordenada X), calculando distancias Manhattan en una cuadrícula urbana de $8 \times 8$.

## Requisitos de Instalación

El proyecto está construido en Python y utiliza el framework **Flask** para el servidor web. No requiere base de datos (PostgreSQL fue omitido para mantener la simulación en memoria temporal de manera simple y eficiente).

Asegúrate de tener instalado Python 3 y ejecuta el siguiente comando en tu terminal para instalar las dependencias:

```bash
pip install Flask
```

## Instrucciones para Iniciar el Servidor

1. Abre una terminal en el directorio raíz de este proyecto (`/Users/gabo/.gemini/antigravity/scratch/hilbert_logistics`).
2. Ejecuta el servidor Flask con el comando:
   ```bash
   python3 app.py
   ```
3. El servidor se iniciará localmente en el puerto `5001`. Abre tu navegador web y navega a:
   [http://127.0.0.1:5001](http://127.0.0.1:5001)

## Estructura del Proyecto

*   `app.py`: Servidor Flask. Contiene la función matemática pura `xy2hilbert(n, x, y)` y el endpoint de cálculo de rutas y distancias Manhattan.
*   `templates/index.html`: Interfaz web interactiva (HTML5 + CSS moderno + Vanilla JavaScript con gráficos en HTML5 Canvas).
*   `EXPLICACION.md`: Guion y material de soporte teórico para la exposición de la monografía.
