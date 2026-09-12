from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

ADMIN_HESAPLARI = {
    "Devil": "0553",
    "Azrail": "0553"
}

urunler = [
    {"id": 1, "ad": "Medine İpeği Elbise", "fiyat": 3450, "resim": "https://via.placeholder.com/250x350"},
    {"id": 2, "ad": "Kemerli Yazlık Tunik", "fiyat": 2250, "resim": "https://via.placeholder.com/250x350"},
    {"id": 3, "ad": "Siyah Abiye Elbise", "fiyat": 5800, "resim": "https://via.placeholder.com/250x350"}
]

siparisler = []

@app.route('/')
def ana_sayfa():
    return render_template('index.html', urunler=urunler)

@app.route('/siparis-ver', methods=['POST'])
def siparis_ver():
    musteri_ad = request.form.get('ad_soyad')
    telefon = request.form.get('telefon')
    urun_ad = request.form.get('urun_ad')
    fiyat = request.form.get('fiyat')
    
    yeni_siparis = {
        "id": len(siparisler) + 1001,
        "musteri": musteri_ad,
        "telefon": telefon,
        "urun": urun_ad,
        "tutar": fiyat,
        "durum": "Havale/EFT Bekliyor",
        "onaylayan": "-"
    }
    siparisler.append(yeni_siparis)
    return redirect(url_for('ana_sayfa'))

@app.route('/admin', methods=['GET', 'POST'])
def admin_paneli():
    mesaj = ""
    giris_yapildi = False
    aktif_admin = ""

    if request.method == 'POST':
        kullanici = request.form.get('kullanici_adi')
        sifre = request.form.get('sifre')

        if kullanici in ADMIN_HESAPLARI and ADMIN_HESAPLARI[kullanici] == sifre:
            giris_yapildi = True
            aktif_admin = kullanici
        else:
            mesaj = "Hatalı kullanıcı adı veya şifre!"

    return render_template('admin.html', siparisler=siparisler, giris_yapildi=giris_yapildi, mesaj=mesaj, aktif_admin=aktif_admin)

@app.route('/odeme-onayla/<int:siparis_id>/<admin_adi>')
def odeme_onayla(siparis_id, admin_adi):
    for siparis in siparisler:
        if siparis["id"] == siparis_id:
            siparis["durum"] = "Ödeme Onaylandı ✅"
            siparis["onaylayan"] = admin_adi
    return redirect(url_for('admin_paneli'))

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/admin/urun-ekle', methods=['POST'])
def urun_ekle():
    urun_adi = request.form.get('urun_adi')
    fiyat = request.form.get('fiyat')
    resim_url = request.form.get('resim_url')
    
    yeni_urun = {
        'id': len(urunler) + 1,
        'ad': urun_adi,
        'fiyat': fiyat,
        'resim': resim_url
    }
    urunler.append(yeni_urun)
    
    return redirect(url_for('admin'))
