from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

# Layanan tempat
def get_tempat(id_tempat):
    response = requests.get(f'http://localhost:5001/tempat/{id_tempat}')
    return response.json()

# Layanan review
def get_reviews(id_tempat):
    response = requests.get(f'http://localhost:5003/review/product/{id_tempat}')
    try:
        data = response.json()
        return data
    except requests.exceptions.JSONDecodeError:
        print("JSONDecodeError: Respons tidak valid atau kosong")
        return []  

@app.route('/tempat/<int:id_tempat>')
def get_info_tempat(id_tempat):
    info_tempat = get_tempat(id_tempat)
    reviews = get_reviews(id_tempat)
    return render_template('index.html', info=info_tempat, reviews=reviews)

if __name__ == "__main__":
    app.run(debug=True, port=5004)
