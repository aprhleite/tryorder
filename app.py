from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Data Menu
coffee_menu = [
    {"id": 1, "nama": "Americano", "harga": 13636},
    {"id": 2, "nama": "Cappucino", "harga": 22727},
    {"id": 3, "nama": "Cafe Latte", "harga": 18181},
    {"id": 4, "nama": "Espresso", "harga": 11818},
    {"id": 5, "nama": "Mocha", "harga": 20000},
    {"id": 6, "nama": "Caramel Macchiato", "harga": 24545}
]

non_coffee_menu = [
    {"id": 7, "nama": "White Chocolate", "harga": 18181},
    {"id": 8, "nama": "Chocolate", "harga": 18181},
    {"id": 9, "nama": "Green Tea", "harga": 15454},
    {"id": 10, "nama": "Matcha Latte", "harga": 15454},
    {"id": 11, "nama": "Caramel milk", "harga": 22727},
    {"id": 12, "nama": "Black Tea", "harga": 10909},
    {"id": 13, "nama": "Lemon Tea", "harga": 9090}
]

menu_items = coffee_menu + non_coffee_menu

HARGA_MENU = {item["nama"]: item["harga"] for item in menu_items}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html', 
                           coffee_menu=coffee_menu, 
                           non_coffee_menu=non_coffee_menu)

@app.route('/bayar', methods=['POST'])
def bayar():
    nama = request.form.get('nama_pelanggan')
    nomor_meja = request.form.get('nomor_meja')
    catatan = request.form.get('catatan')
    
    daftar_pesanan = []
    total_harga_bruto = 0 

    for item in menu_items:
        try:
            jumlah_key = f'jumlah_{item["id"]}'
            jumlah = int(request.form.get(jumlah_key, 0))
        except ValueError:
            jumlah = 0

        if jumlah > 0:
            harga_satuan = HARGA_MENU.get(item["nama"], 0)
            subtotal = harga_satuan * jumlah
            
            daftar_pesanan.append({
                "nama": item["nama"],
                "jumlah": jumlah,
                "harga_satuan": harga_satuan,
                "subtotal": subtotal
            })
            total_harga_bruto += subtotal
            
    if not daftar_pesanan:
        return redirect(url_for('menu')) 

    PAJAK_RATE = 0.10
    nilai_pajak = round(total_harga_bruto * PAJAK_RATE) 
    total_pembayaran_final = total_harga_bruto + nilai_pajak
    
    detail_header = {
        "Nama": nama if nama else "Pelanggan",
        "Nomor Meja": nomor_meja if nomor_meja else "-",
        "Catatan": catatan if catatan else "-"
    }

    return render_template('bayar.html', 
                           daftar_pesanan=daftar_pesanan, 
                           detail_header=detail_header, 
                           total_harga_bruto=total_harga_bruto, 
                           nilai_pajak=nilai_pajak, 
                           total_pembayaran_final=total_pembayaran_final)

@app.route('/result', methods=['POST'])
def result():
    metode_pembayaran = request.form.get('metode')

    try:
        total_pembayaran_final = float(request.form.get('total_pembayaran_final', 0)) 
        nilai_pajak = float(request.form.get('nilai_pajak', 0))
        total_harga_bruto = float(request.form.get('total_harga_bruto', 0))
    except ValueError:
        total_pembayaran_final = 0
        nilai_pajak = 0
        total_harga_bruto = 0

    detail_header = {
        "Nama": request.form.get('nama_pelanggan'),
        "Nomor Meja": request.form.get('nomor_meja'),
        "Catatan": request.form.get('catatan')
    }

    item_nama_list = request.form.getlist('item_nama')
    item_jumlah_list = request.form.getlist('item_jumlah')
    item_harga_satuan_list = request.form.getlist('item_harga_satuan')
    
    daftar_pesanan = []
    for nama, jumlah_str, harga_str in zip(item_nama_list, item_jumlah_list, item_harga_satuan_list):
        try:
            jumlah = int(jumlah_str)
            harga_satuan = float(harga_str)
            subtotal = jumlah * harga_satuan
            daftar_pesanan.append({
                "nama": nama,
                "jumlah": jumlah,
                "harga_satuan": harga_satuan,
                "subtotal": subtotal
            })
        except ValueError:
            continue 

    return render_template('result.html', 
                           daftar_pesanan=daftar_pesanan, 
                           detail_header=detail_header, 
                           total_pembayaran_final=total_pembayaran_final,
                           nilai_pajak=nilai_pajak,
                           total_harga_bruto=total_harga_bruto,
                           metode_pembayaran=metode_pembayaran)

if __name__ == '__main__':
    app.run(debug=True)