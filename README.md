# 🛠️ Back-End API

Backend untuk sistem **Employee Attendance & Admin Panel** — menyediakan API server dengan fitur autentikasi, manajemen user/karyawan, dan pengolahan data absensi.

---

## 📌 Fitur Utama

- 🔐 Autentikasi **Login / Register**
- 👤 CRUD data Karyawan
- 📅 Absensi (Check-in / Check-out)
- 📸 Integrasi dengan Face Recognition (opsional)
- 📡 RESTful API endpoints
- 🗃️ Database untuk penyimpanan data

---

## 🧰 Teknologi yang Digunakan

| Teknologi | Keterangan |
|-----------|------------|
| Node.js / Express | Backend server |
| JWT | Autentikasi Token |
| Database (MySQL / PostgreSQL / MongoDB) | Penyimpanan data |
| ORM / Query Builder | (Sequelize / Mongoose / TypeORM) |

---


---

## ⚙️ Instalasi

Pastikan sudah terinstall **Node.js** (14+), **npm** atau **yarn**, dan database yang digunakan.

### 1. Clone repo

```bash
git clone https://github.com/joketoyou24/Back-End.git
cd Back-End
```

### 2. Install dependencies
```
npm install


atau

yarn install
```
### 3. Setup Environment Variables
```
Buat file .env di root:

PORT=5000
DB_HOST=localhost
DB_USER=root
DB_PASS=your_db_password
DB_NAME=your_db_name
JWT_SECRET=your_secret_key
```

Sesuaikan dengan konfigurasi database kamu.

### ▶️ Menjalankan Server
```
npm run dev


atau

yarn dev

Production
npm start


atau

yarn start

```
Server akan berjalan di:
```
http://localhost:5000
```
## 🗂️ Struktur Direktori (Contoh)

