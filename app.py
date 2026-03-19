import os
from flask import Flask, render_template
from fpdf import FPDF
from flask import send_file

app = Flask(__name__)

# Esta es la ruta hacia tu carpeta de fotos
CARPETA_FOTOS = os.path.join('static', 'productos')

@app.route('/')
def index():
    lista_fotos = os.listdir(CARPETA_FOTOS)
    
    # FILTRO INTELIGENTE:
    # 1. Que sea imagen (jpg, png)
    # 2. QUE NO EMPIECE CON 'X_' (esto oculta el producto)
    fotos = [f for f in lista_fotos if f.lower().endswith(('.png', '.jpg', '.jpeg')) and not f.upper().startswith('X_')]
    
    return render_template('index.html', fotos=fotos)

@app.route('/descargar-pdf')
def descargar_pdf():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    lista_fotos = os.listdir(CARPETA_FOTOS)
    # Usamos el mismo filtro de la "X" para el PDF
    fotos = [f for f in lista_fotos if f.lower().endswith(('.png', '.jpg', '.jpeg')) and not f.upper().startswith('X_')]

    for foto in fotos:
        pdf.add_page()
        # Fondo claro (gris muy suave)
        pdf.set_fill_color(245, 245, 245)
        pdf.rect(0, 0, 210, 297, 'F')
        
        # Insertar la Imagen del producto
        ruta_foto = os.path.join(CARPETA_FOTOS, foto)
        pdf.image(ruta_foto, x=10, y=20, w=190)
        
        # Barra Azul Oscuro abajo
        pdf.set_fill_color(0, 31, 63) # Tu azul Ferreagro
        pdf.rect(0, 250, 210, 47, 'F')
        
        # Texto Amarillo
        pdf.set_text_color(255, 219, 88) # Tu amarillo Ferreagro
        pdf.set_font("Arial", 'B', 24)
        nombre = foto.split('.')[0].replace('_', ' ').upper()
        pdf.set_y(265)
        pdf.cell(0, 10, nombre, align='C')

    nombre_pdf = "Catalogo_Ferreagro_Emmanuel.pdf"
    pdf.output(nombre_pdf)
    return send_file(nombre_pdf, as_attachment=True)
if __name__ == '__main__':
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
