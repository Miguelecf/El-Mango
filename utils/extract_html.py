import requests

url = 'https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n/_/N-8pub5z'

if __name__ == '__main__':
    try:
        # Definir los headers para simular una solicitud de un navegador real
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # Hacer la solicitud con los headers
        response = requests.get(url, headers=headers)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            content = response.text  # Guardar el contenido HTML como cadena

            # Guardar el contenido en un archivo local
            with open('coto.html', 'w+', encoding='utf-8') as file:
                file.write(content)
            print("El archivo HTML se ha guardado correctamente como 'coto.html'.")
        else:
            print(f"Error al obtener la página. Código de estado: {response.status_code}")
    except Exception as e:
        print(f"Ocurrió un error al realizar la solicitud: {e}")
