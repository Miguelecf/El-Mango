import requests
from bs4 import BeautifulSoup
import sys
import os

# Agregar ruta de importación
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from entities.Product import Product

# URL de la página de Cotodigital
def get_carrefour_products():
    url = 'https://www.carrefour.com.ar/pan%20dulce?_q=pan%20dulce&map=ft'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    products = []
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        products_list = soup.find("div", id="products", class_="valtech-carrefourar-search-result-3-x-gallery flex flex-row flex-wrap items-stretch bn ph1 na4 pl9-l")
        if products_list:
            product_containers = products_list.find_all("li", class_="clearfix")
            for container in product_containers:
                product_name_tag = container.find("div", class_="valtech-carrefourar-search-result-3-x-galleryItem valtech-carrefourar-search-result-3-x-galleryItem--normal pa4")
                product_name = product_name_tag.get_text(strip=True) if product_name_tag else 'Nombre no disponible'
                
                price_tag = container.find("span", class_="atg_store_newPrice")
                price = price_tag.text.strip() if price_tag else 'Precio no disponible'
                
                image_tag = container.find("span", class_="atg_store_productImage").find("img")
                image_url = image_tag['src'] if image_tag else 'Imagen no disponible'
                
                link_tag = container.find("a", href=True)
                if link_tag:
                    link = link_tag['href']
                    if not link.startswith('http'):
                        base_url = "https://www.carrefour.com.ar/"
                        link = base_url + link
                
                if product_name and price and image_url and link:
                    product = Product(
                        name=product_name,
                        price=price,
                        image=image_url,
                        link=link
                    )
                    products.append(product)
                    
        return products
    else:
        print(f"No se pudo acceder a la página web. Código de estado: {response.status_code}")
        return []

if __name__ == "__main__":
    products = get_carrefour_products()
    for product in products:
        print(product)