import requests
from bs4 import BeautifulSoup
import sys
import os

# Agregar el path para importar la entidad Product
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from entities.Product import Product

# Constantes
BASE_URL = "https://diaonline.supermercadosdia.com.ar"
SEARCH_URL = f"{BASE_URL}/pan%20dulce?_q=pan%20dulce&map=ft"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

