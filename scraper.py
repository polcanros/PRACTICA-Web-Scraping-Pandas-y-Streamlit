import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def hacer_scraping_estructura_real():
    url = "https://es.wikipedia.org/wiki/Anexo:Personajes_de_South_Park"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        respuesta = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        
        contenido = soup.find('div', class_='mw-parser-output')
        
        personajes = []
        detalles = []
        id_counter = 1
        
        categoria_actual = "General"
        personaje_actual = None
        descripcion_actual = ""
        
        for tag in contenido.find_all(['h2', 'h3', 'p']):
            
            # H2: Cambio de categoría
            if tag.name == 'h2':
                # ¡AQUÍ ESTABA EL ERROR! Guardamos el último personaje antes de limpiar la variable
                if personaje_actual:
                    desc_limpia = descripcion_actual.strip()
                    if not desc_limpia: desc_limpia = "Sin descripción detallada."
                    
                    personajes.append({"id_personaje": id_counter, "nombre": personaje_actual, "categoria": categoria_actual})
                    detalles.append({"id_personaje": id_counter, "longitud_descripcion": len(desc_limpia), "descripcion": desc_limpia})
                    id_counter += 1
                    personaje_actual = None
                
                titulo_h2 = tag.text.replace('[editar]', '').strip()
                if titulo_h2.lower() in ['véase también', 'referencias', 'enlaces externos', 'notas']:
                    break
                categoria_actual = titulo_h2
                descripcion_actual = ""
                
            # H3: Nombre del personaje
            elif tag.name == 'h3':
                if personaje_actual:
                    desc_limpia = descripcion_actual.strip()
                    if not desc_limpia: desc_limpia = "Sin descripción detallada."
                    
                    personajes.append({"id_personaje": id_counter, "nombre": personaje_actual, "categoria": categoria_actual})
                    detalles.append({"id_personaje": id_counter, "longitud_descripcion": len(desc_limpia), "descripcion": desc_limpia})
                    id_counter += 1
                
                personaje_actual = tag.text.replace('[editar]', '').strip()
                descripcion_actual = ""
                
            # P: Párrafos de descripción
            elif tag.name == 'p' and personaje_actual:
                texto_p = tag.text.strip()
                if texto_p:
                    descripcion_actual += texto_p + " "

        # Guardar el último personaje de toda la página
        if personaje_actual:
            desc_limpia = descripcion_actual.strip()
            if not desc_limpia: desc_limpia = "Sin descripción detallada."
            personajes.append({"id_personaje": id_counter, "nombre": personaje_actual, "categoria": categoria_actual})
            detalles.append({"id_personaje": id_counter, "longitud_descripcion": len(desc_limpia), "descripcion": desc_limpia})

        # Generar CSVs
        df_p = pd.DataFrame(personajes)
        df_d = pd.DataFrame(detalles)

        os.makedirs('datos', exist_ok=True)
        df_p.to_csv('datos/personajes.csv', index=False)
        df_d.to_csv('datos/detalles_personajes.csv', index=False)
        
        print(f"Scraping completado. ¡Kenny recuperado! Se extrajeron {len(df_p)} personajes en total.")

    except Exception as e:
        print(f"Error durante el scraping: {e}")

if __name__ == "__main__":
    hacer_scraping_estructura_real()