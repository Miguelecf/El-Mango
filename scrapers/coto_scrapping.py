import requests
from bs4 import BeautifulSoup
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from entities.Product import Product

def get_coto_products():
    # URL de la página de Cotodigital
    url = 'https://www.cotodigital3.com.ar/sitios/cdigi/browse?_dyncharset=utf-8&Dy=1&Ntt=pan+dulce&Nty=1&Ntk=&siteScope=ok&_D%3AsiteScope=+&atg_store_searchInput=pan+dulce&idSucursal=200&_D%3AidSucursal=+&search=Ir&_D%3Asearch=+&_DARGS=%2Fsitios%2Fcartridges%2FSearchBox%2FSearchBox.jsp'  # Cambia esto a la URL exacta que necesitas

    # Definir los encabezados de la solicitud para evitar el error 403 (emular navegador)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Realizamos la solicitud HTTP con el encabezado adecuado
    response = requests.get(url, headers=headers)

    # Verificamos si la solicitud fue exitosa (código 200)
    if response.status_code == 200:
        # Parsear el contenido HTML de la respuesta
        soup = BeautifulSoup(response.text, 'html.parser')

        # Buscar el contenedor de los productos (ajusta según el HTML de la página real)
        products_list = soup.find("ul", id="products", class_="grid")

        # Crear una lista para almacenar los productos extraídos
        products = []

        # Extraer información de cada producto dentro del <ul id="products">
        if products_list:
            product_containers = products_list.find_all("li", class_="clearfix")  # Ajusta esta clase si es necesario

            for container in product_containers:
                # Buscar el nombre del producto dentro del <a> que tiene el enlace
                product_name_tag = container.find("span", class_="span_productName")
                if product_name_tag:
                    raw_name = product_name_tag.get_text(strip=True)
                    product_name = clean_product_name(raw_name)  # Esto extrae solo la primera instancia del nombre
                else:
                    product_name = 'Nombre no disponible'

                # Buscar el precio del producto
                price_tag = container.find("span", class_="atg_store_newPrice")
                price = price_tag.text.strip() if price_tag else 'Precio no disponible'

                # Buscar la imagen del producto
                image_tag = container.find("span", class_="atg_store_productImage").find("img")
                image_url = image_tag['src'] if image_tag else 'Imagen no disponible'

                # Buscar el enlace al producto
                link_tag = container.find("a", href=True)
                if link_tag:
                    link = link_tag['href']
                # Convertir enlaces relativos a absolutos si es necesario
                    if not link.startswith('http'):
                        base_url = "https://www.cotodigital3.com.ar"  # URL base del sitio
                        link = base_url + link
                else:
                    link = 'Enlace no disponible'

                # Verificar que la información esté disponible
                if product_name and price and image_url and link:
                    # Crear un objeto Product y agregarlo a la lista
                    product = Product(
                        name=product_name,
                        price=price,
                        image=image_url,
                        link=link
                    )
                    products.append(product)

        # Retornar los productos extraídos
        return products

    else:
        print(f"No se pudo acceder a la página web. Código de estado: {response.status_code}")
        return []


import re

def clean_product_name(raw_name):
    """
    Limpia y normaliza el nombre del producto para evitar repeticiones y formatos extraños.
    """
    # Quitar espacios redundantes y caracteres extraños
    cleaned_name = re.sub(r'\s+', ' ', raw_name)  # Reemplazar múltiples espacios por uno solo
    cleaned_name = cleaned_name.strip()  # Quitar espacios al inicio y final

    # Unificar unidades (e.g., "Grm" -> "G")
    cleaned_name = re.sub(r'\bGrm\b', 'G', cleaned_name, flags=re.IGNORECASE)

    # Quitar repeticiones del nombre (e.g., "XYZ ...XYZ" -> "XYZ")
    parts = cleaned_name.split(' . . .')
    if len(parts) > 1:
        cleaned_name = parts[0]  # Tomar sólo la primera parte antes de las repeticiones

    return cleaned_name
    