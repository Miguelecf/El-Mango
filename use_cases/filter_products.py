

def filter_products_by_name(products, keyword):
    # Convertir la palabra clave a minúsculas para una búsqueda insensible a mayúsculas
    keyword_lower = keyword.lower()

    # Filtrar los productos cuyo nombre contenga la palabra clave
    filtered_products = [
        product for product in products
        if keyword_lower in product.name.lower()
    ]

    return filtered_products
