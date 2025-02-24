from flask import Flask, request, jsonify, send_file
import qrcode
import io

app = Flask(__name__)

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.json
    phone_number = data.get('phone_number')
    message = data.get('message')
    
    if not phone_number or not message:
        return jsonify({"error": "Por favor, forneça um número de telefone e uma mensagem"}), 400
    
    # Formatação do URL do WhatsApp
    whatsapp_url = f"https://wa.me/{phone_number}?text={message}"
    
    # Geração do QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(whatsapp_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    
    # Salvar a imagem em um objeto BytesIO
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
