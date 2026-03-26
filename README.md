# 📦 Inventory Management System

A full-featured **Inventory Management System** built with **Django**, designed to manage products, categories, stock movements, and import/export orders efficiently.

---

## 🚀 Features

### 👤 User Management

* Authentication (Login / Logout)
* Role-based access control:

  * **ADMIN**
  * **MANAGER**
  * **ACCOUNTANT**
  * **STAFF**

---

### 📁 Category Management

* Hierarchical categories (Tree structure)
* Parent-child relationships using **MPTT**
* Manage category code and description

---

### 📦 Product Management

* SKU management (unique product code)
* Import & selling price tracking
* Real-time stock quantity tracking
* Minimum stock level alerts
* Product image support

---

### 🚚 Supplier Management

* Manage supplier information
* Phone, email, address, tax code

---

### 📥 Import Orders

* Create import orders from suppliers
* Automatic total calculation
* Upload invoice files

---

### 📤 Export Orders

* Create export orders
* Manage customer information
* Automatically deduct stock

---

### 🔄 Stock Movement Tracking

* Track all stock changes:

  * IMPORT
  * EXPORT
  * ADJUST
* Full audit trail of inventory changes

---

### 🏬 Warehouse Management

* Multi-warehouse support
* Track stock by warehouse

---

### 📊 Dashboard

* Key metrics:

  * Total products
  * Total stock
  * Total import/export orders
* Stock distribution by category (Chart.js)
* Top stocked products
* Recent activity logs

---

### 📝 Activity Log

* Track all system activities:

  * Create / Update / Delete
* Record user actions
* Display recent activity timeline

---

## 🛠️ Tech Stack

* **Backend:** Django
* **Database:** PostgreSQL / MySQL / SQLite
* **Frontend:** Django Templates + Bootstrap
* **Charts:** Chart.js
* **Tree Structure:** django-mptt

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-repo/inventory-management.git
cd inventory-management
```

---

### 2. Create virtual environment

```bash
python -m venv venv
```

Activate it:

```bash
# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 5. Create superuser

```bash
python manage.py createsuperuser
```

---

### 6. Run server

```bash
python manage.py runserver
```

---

## 🔐 Role Permissions (Example)

| Role       | Permissions                     |
| ---------- | ------------------------------- |
| ADMIN      | Full access                     |
| MANAGER    | View reports, manage operations |
| ACCOUNTANT | Manage financial data           |
| STAFF      | Manage products and orders      |

---

## 📂 Project Structure (Simplified)

```bash
inventory_management/
├── category/
├── product/
├── supplier/
├── importorder/
├── exportorder/
├── stock/
├── warehouse/
├── activity/
├── templates/
└── manage.py
```

---

## 📸 Screenshots

* Dashboard with charts
* Product management UI
* Import / Export order pages
* Activity log timeline

---

## 🧠 Future Improvements

* REST API (Django REST Framework)
* Angular / React frontend
* Real-time dashboard (WebSocket)
* Advanced reporting & analytics
* Barcode / QR code integration

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repo and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Developed by **Tran Thanh Tung**

---

⭐ If you find this project useful, please give it a star!
