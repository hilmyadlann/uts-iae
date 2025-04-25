# 📝 Final Report UTS EAI — Sistem Terintegrasi Antar Layanan

## NAMA ANGGOTA KELOMPOK 
1. Aldo Wardana Ramdo	( 1202213375 )
2. Aditya Rizky Syahputra 	( 1202220008 )
3. Hilmy Adlan Ahmad Ghifari	( 1202210138 )
4. Pricilia Vercelly T	( 1202194004 )

## 1. Deskripsi Umum
Proyek ini bertujuan untuk membangun sistem integrasi antar layanan tanpa menggunakan API Gateway, dengan pendekatan service-to-service communication. Setiap service berfungsi sebagai provider dan consumer, dan berkomunikasi menggunakan protokol HTTP serta format data JSON. Sistem ini mencakup layanan untuk mengelola pesanan yang melibatkan interaksi dengan layanan User dan Product, serta menyediakan fitur seperti deteksi suspicious order, dan pemberian status Refund. Layanan yang dibangun terdiri dari **UserService**, **ProductService**, dan **OrderService**.

---

## 2. Arsitektur Layanan

- **UserService** (Port 5000): Menyediakan data pengguna melalui endpoint `GET /users/{user_id}`.
- **ProductService** (Port 5001): Menyediakan data produk melalui endpoint `GET /products/{product_id}`.
- **OrderService** (Port 5002): OrderService (Port 5002): Bertindak sebagai consumer dan provider, memproses order, memberikan status pesanan, mendeteksi pesanan mencurigakan, dan pemberian status refund/no refund.

---

## 3. Alur Komunikasi Antar Layanan

1. Client mengirim permintaan POST /orders ke OrderService.
2. **OrderService** sebagai **consumer**:
   - Mengambil data pengguna dari **UserService** (menggunakan `GET /users/{user_id}`).
   - Mengambil data produk dari **ProductService** (menggunakan `GET /products/{product_id}`).
3. **OrderService** melakukan perhitungan harga, mendeteksi apakah order mencurigakan (suspicious), dan pemberian status refund/no refund.
4. Response pesanan dikembalikan dalam format JSON, dan **OrderService** juga bertindak sebagai provider untuk histori pesanan.

---

## 4. Fitur Inovatif

| Fitur                        | Deskripsi                                                                 |
|-----------------------------|---------------------------------------------------------------------------|
| **Suspicious Order Detection**  | Order dengan quantity lebih dari 10 ditandai sebagai mencurigakan (`suspicious: true`) |
| **Status Refund/No Refund**  | Order dengan status failed akan diberikan status refund, jika order success diberikan status no refund |

---

## 5. Contoh Pengujian Endpoint

### **`POST /orders`**
**Request:**
`http://localhost:5002/orders`

```json
{
  "user_id": 4,
  "product_id": 10,
  "quantity": 15
}
```

### **Response :**
```json
{
  "order_id": 1,
  "user": {
    "id": 1,
    "name": "Hilmy",
    "email": "hilmy@mail.com"
  },
  "product": {
    "id": 10,
    "name": "Laptop",
    "price": 7000000
  },
  "quantity": 15,
  "total_price": 105000000,
  "status": "Failed",
  "suspicious": true,
  "refund_status": "Refund"
}
```
## 6. Dokumentasi Swagger (OpenAPI)

Setiap service memiliki dokumentasi otomatis berbasis Swagger UI:

| Service         | URL Swagger Docs                 | Keterangan                                        |
|----------------|-----------------------------------|---------------------------------------------------|
| UserService     | `http://127.0.0.1:5000/docs/`      | Endpoint `GET /users/{user_id}`                   |
| ProductService  | `http://127.0.0.1:5001/docs/`      | Endpoint `GET /products/{product_id}`             |
| OrderService    | `http://127.0.0.1:5002/docs/`      | Endpoint POST /orders & GET /orders/{order_id}    |

**File Skema OpenAPI JSON:**
- `http://127.0.0.1:5000/openapi.json`
- `http://127.0.0.1:5001/openapi.json`
- `http://127.0.0.1:5002/openapi.json`

---

## 7. Teknologi yang Digunakan

- **Bahasa**: Python 3.9
- **Framework**: Flask
- **HTTP Client**: Requests
- **Testing Tool**: Postman
- **Editor**: Visual Studio Code
- **Dokumentasi API**: Dokumentasi API: Swagger UI (OpenAPI)
---

## 9. Kesimpulan
Sistem Order Service ini berhasil mengintegrasikan beberapa layanan untuk pengelolaan pesanan yang melibatkan interaksi dengan layanan UserService dan ProductService. Dengan menggunakan pendekatan service-to-service communication, aplikasi ini dapat memproses pesanan secara efisien. Fitur-fitur seperti deteksi pesanan mencurigakan (jika jumlah pesanan lebih dari 10), dan status refund telah berhasil diimplementasikan dengan baik. Selain itu, dokumentasi API menggunakan Swagger UI memungkinkan pengujian dan pemahaman API menjadi lebih mudah dan interaktif.

Dengan adanya Swagger UI, pengembang dapat dengan mudah mengakses dokumentasi API dan melakukan pengujian pada setiap endpoint. Sistem ini dapat berkembang lebih lanjut dengan penambahan database, sistem autentikasi pengguna, dan pemanfaatan machine learning untuk meningkatkan fitur deteksi kecurangan.

## 10. Referensi

1. Flask Documentation. (n.d.). Flask Web Framework. Diakses dari: https://flask.palletsprojects.com/en/2.1.x/
2. Swagger UI & OpenAPI. (n.d.). API Documentation Tools. Diakses dari: https://swagger.io/tools/swagger-ui
3. Python Requests Library. (n.d.). Python HTTP for Humans. Diakses dari: https://docs.python-requests.org/en/master/
4. JSON. (n.d.). JavaScript Object Notation. Diakses dari: https://www.json.org/json-en.html