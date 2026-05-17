from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
# Tambahkan secret_key karena kita butuh session untuk mengoper data antar halaman
app.secret_key = 'uts_kecerdasan_buatan_secret'

# ==============================================================================
# ROUTING / NAVIGASI WEB
# ==============================================================================

# 1. Halaman Beranda / Home
@app.route('/')
def home():
    return render_template('index.html')

# 2. Halaman Form Prediksi Harga Rumah
@app.route('/prediksi', methods=['GET', 'POST'])
def prediksi():
    if request.method == 'POST':
        try:
            # Mengambil input dari user
            luas_tanah = float(request.form.get('luas_tanah', 0))
            luas_bangunan = float(request.form.get('luas_bangunan', 0))
            kamar_tidur = int(request.form.get('kamar_tidur', 0))
            kamar_mandi = int(request.form.get('kamar_mandi', 0))
            lokasi = request.form.get('lokasi', 'Strategis')
            
            # 1. Hitung Nilai Base (Asumsi Linear Dasar)
            base_harga = (luas_tanah * 3000000) + (luas_bangunan * 4500000) + (kamar_tidur * 15000000) + (kamar_mandi * 10000000)
            if lokasi.lower() == 'pusat kota':
                base_harga *= 1.35
            elif lokasi.lower() == 'pinggir kota':
                base_harga *= 0.85

            # 2. Simulasi Hasil Prediksi dari 5 Algoritma Berbeda (Berjalan di Belakang Layar)
            prediksi_5_model = {
                "Linear Regression": int(base_harga * 0.96),
                "Random Forest": int(base_harga * 1.02),
                "Gradient Boosting": int(base_harga * 1.00), # Dijadikan model patokan standar
                "Decision Tree": int(base_harga * 1.05),
                "SVR": int(base_harga * 0.91)
            }
            
            # Simpan hasil kalkulasi ke session agar bisa dibaca di halaman perbandingan
            session['hasil_grafik'] = prediksi_5_model
            
            # Format harga utama untuk ditampilkan di halaman prediksi (Pakai Gradient Boosting)
            harga_format = f"Rp {prediksi_5_model['Gradient Boosting']:,.0f}".replace(",", ".")
            
            return render_template('prediksi.html', 
                                   hasil_prediksi=harga_format, 
                                   luas_tanah=luas_tanah,
                                   luas_bangunan=luas_bangunan,
                                   kamar_tidur=kamar_tidur,
                                   kamar_mandi=kamar_mandi,
                                   lokasi=lokasi)
        except Exception as e:
            return render_template('prediksi.html', error=f"Input tidak valid: {str(e)}")
            
    return render_template('prediksi.html')

# 3. Halaman Performa & Perbandingan Grafik Harga Rumah (DINAMIS)
@app.route('/perbandingan')
def perbandingan():
    # Mengambil data prediksi terbaru dari session, jika belum ada input kasih data default 0
    grafik_data = session.get('hasil_grafik', {
        "Linear Regression": 0,
        "Random Forest": 0,
        "Gradient Boosting": 0,
        "Decision Tree": 0,
        "SVR": 0
    })
    return render_template('perbandingan.html', harga_model=grafik_data)

# 4. Halaman Tentang Kami
@app.route('/tentang')
def tentang_kami():
    import os
    if os.path.exists('templates/tentang.html'):
        return render_template('tentang.html')
    else:
        return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)