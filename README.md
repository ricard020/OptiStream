# OptiStream | Compresor de Video

![OptiStream Banner](assets/logo/banner.png)

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

OptiStream es una aplicacion de escritorio construida con Python y Tkinter que permite comprimir archivos de video utilizando FFmpeg, con una interfaz grafica intuitiva y barra de progreso en tiempo real.

## Caracteristicas Principales

- **Compresion con FFmpeg:** Reduce el peso de archivos de video manteniendo una calidad profesional.
- **Barra de Progreso:** Seguimiento visual preciso del avance de la compresion.
- **Interfaz Moderna:** Diseño oscuro optimizado para una mejor experiencia de usuario.
- **Procesamiento Asincrono:** Ejecucion en segundo plano para evitar que la interfaz se congele.

## Requisitos

- Python 3.8 o superior.
- FFmpeg instalado y configurado en el PATH del sistema.

## Instalacion

1. Clona el repositorio o descarga los archivos.
2. Abre una terminal en la carpeta del proyecto.
3. Asegurate de tener FFmpeg instalado:
   ```bash
   ffmpeg -version
   ```

## Uso

1. Ejecuta el archivo principal:
   ```bash
   python main.py
   ```
2. Selecciona el archivo de video que deseas comprimir.
3. Configura las opciones de compresion deseadas.
4. Haz clic en el boton de comprimir y espera a que finalice el proceso.

## Estructura del Proyecto

```text
Compresor video/
├── main.py                    # Punto de entrada principal
├── requirements.txt           # Dependencias del proyecto
├── assets/                    # Recursos estaticos
│   └── logo/                  # Iconos y logos de la aplicacion
├── src/                       # Codigo fuente principal
│   ├── core/                  # Logica de negocio (FFmpeg handler)
│   ├── ui/                    # Interfaz grafica y estilos
│   └── utils/                 # Utilidades generales
```

## Tecnologias Utilizadas

- [Python](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - Interfaz grafica
- [FFmpeg](https://ffmpeg.org/) - Procesamiento de video

## Licencia

Este proyecto es de uso libre para propositos educativos y personales.

## Autor

- **Ricardo** - [GitHub](https://github.com/[tu-usuario])
