from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
from PIL import Image
import io
from deep_translator import GoogleTranslator

app = Flask(__name__)
CORS(app) # Permite que o HTML converse com este servidor Python

# ATENÇÃO: Se você usa Windows, remova o '#' da linha abaixo e verifique se o caminho está correto:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@app.route('/traduzir', methods=['POST'])
def traduzir_imagem():
    if 'imagem' not in request.files:
        return jsonify({'erro': 'Nenhuma imagem enviada'}), 400
    
    file = request.files['imagem']
    
    try:
        # 1. Abre a imagem recebida
        img = Image.open(io.BytesIO(file.read()))
        
        # 2. Extrai o texto da imagem (OCR)
        import re
        texto_original = pytesseract.image_to_string(img).replace('\n', ' ')
        texto_original = re.sub(r'\bI\b', 'eu', texto_original)
        
        if not texto_original.strip():
            return jsonify({'erro': 'Nenhum texto encontrado na imagem. Tente outra foto.'}), 400

        # 3. Traduz o texto para Português
        tradutor = GoogleTranslator(source='auto', target='pt')
        texto_traduzido = tradutor.translate(texto_original)
        
        # 4. Devolve o resultado para o site
        return jsonify({
            'original': texto_original,
            'traduzido': texto_traduzido
        })
        
    except Exception as e:
        return jsonify({'erro': f'Erro no processamento: {str(e)}'}), 500

if __name__ == '__main__':
    print("Servidor rodando! Não feche este terminal.")
    app.run(host='127.0.0.1', port=5001, debug=True)