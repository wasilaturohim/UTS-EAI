from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Koneksi ke database MySQL
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'pariwisata'
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Endpoint untuk melayani review.html
@app.route('/review')
def serve_review():
    return render_template('review.html')

@app.route('/review/add', methods=['POST'])
def add_review():
    try:
        data = request.get_json()  # Mengambil data JSON dari permintaan
        if data is None:
            return jsonify({'error': 'Invalid data format'}), 400
        
        id_tempat = data.get('id_tempat')
        ulasan = data.get('ulasan')
        rating = data.get('rating')
        
        # Membuat koneksi ke database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Menjalankan query untuk menambahkan ulasan ke tabel `review`
        query = "INSERT INTO review (id_tempat, ulasan, rating) VALUES (%s, %s, %s)"
        cursor.execute(query, (id_tempat, ulasan, rating))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Ulasan berhasil ditambahkan'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/review', methods=['GET'])
def get_reviews():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Menjalankan query untuk mengambil semua ulasan
    cursor.execute("SELECT * FROM review")
    
    column_names = [desc[0] for desc in cursor.description]
    reviews = cursor.fetchall()

    reviews_list = []
    for review in reviews:
        review_dict = dict(zip(column_names, review))
        reviews_list.append(review_dict)

    cursor.close()
    conn.close()

    return jsonify(reviews_list)

@app.route('/review/product/<int:id_tempat>', methods=['GET'])
@app.route('/review/product/<int:id_tempat>', methods=['GET'])
def get_reviews_by_product(id_tempat):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Menjalankan query untuk mengambil ulasan berdasarkan id_tempat
    query = "SELECT * FROM review WHERE id_tempat = %s"
    cursor.execute(query, (id_tempat,))
    
    column_names = [desc[0] for desc in cursor.description]
    reviews = cursor.fetchall()
    
    reviews_list = []
    for review in reviews:
        review_dict = dict(zip(column_names, review))
        reviews_list.append(review_dict)
    
    cursor.close()
    conn.close()
    
    # Jika tidak ada ulasan, kembalikan JSON kosong
    if not reviews_list:
        return jsonify([])  # Kembalikan list kosong
    
    return jsonify(reviews_list)

@app.route('/review/delete/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Menjalankan query untuk menghapus ulasan berdasarkan review_id
    query = "DELETE FROM review WHERE user_id = %s"
    cursor.execute(query, (review_id,))
    
    conn.commit()
    
    # Periksa apakah ada baris yang dihapus
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({'error': 'Ulasan tidak ditemukan!'}), 404
    
    cursor.close()
    conn.close()
    
    return jsonify({'message': 'Ulasan sudah dihapus!'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
