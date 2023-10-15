from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        qr_data = request.form.get("qr_data")
        if qr_data:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img_io = BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)
            return render_template('qr_display.html', qr_code_url=img_io)

    return render_template('index.html')

@app.route("/display_qr_code",methods=['GET', 'POST'])
def display_qr_code():
    qr_code_url = request.args.get('qr_code_url')
    return send_file(BytesIO(qr_code_url), mimetype='image/png')


@app.route("/api" , methods=["GET"])
def QR_Code_Generater():
    if request.method == "GET":
        try:
            qr_data = request.args.get("qr_data")
            qr=qrcode.QRCode(version=1, 
                             error_correction=qrcode.constants.ERROR_CORRECT_H,
                             box_size=10,border=4,)
            qr.add_data(qr_data)
            qr.make(fit=True)
            img=qr.make_image(fill_color="black",back_color="white")
            img_io = BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)
            return send_file(img_io, mimetype='image/png')


        except (ValueError,TypeError):
            return "Change the input"



if __name__ == "__main__":
    app.run(debug=False)
