#app.py

from flask import Flask, render_template, request
from scrapers.coto_scrapping import get_coto_products
from use_cases.filter_products import filter_products_by_name
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Obtener todos los productos del scraper
    productos = get_coto_products()

    # Verificar si se envió un término de búsqueda
    keyword = request.form.get('keyword', '').strip()
    
    if keyword:
        # Filtrar productos por la palabra clave
        productos = filter_products_by_name(productos, keyword)

    # Pasar los productos (filtrados o no) a la plantilla
    return render_template('index.html', productos=productos, keyword=keyword)

if __name__ == '__main__':
    app.run(debug=True)