# 🐐 RFID Project Setup Guide

## 🛠️ Prerequisites

- Python 3.x
- MySQL Server
- MySQL Workbench (or similar GUI tool)
- Git

## 🚀 Installation Steps

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/NikPrivate/Goat-RFID-Prototype.git
```

cd Goat-RFID-Prototype

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up MySQL Database

Create a new database called goat_rfid_db (for example)

#### Import the SQL dump:

#### Using MySQL Workbench:

1. Go to Server > Data Import
2. Select "Import from Self-Contained File"
3. Find and Select goat_project.sql
4. Select your target schema
5. Click "Start Import"

### 4️⃣ Configure Environment Variables

Create .env file in root directory:

env

```bash
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=localhost
MYSQL_DB=goat_rfid_db
APP_SECRET_KEY=your_generated_secret_key
```

Replace based on your database information

### 5️⃣ Generate Secret Key

Run this command and copy the output to your .env for (APP_SECRET_KEY):

```bash
Copy
python -c "import secrets; print(secrets.token_hex(16))"
```

### 6️⃣ Launch Application

```bash
python app.py
```

🌐 Access the application at: http://127.0.0.1:5000

### 🔧 Troubleshooting Tips

#### Ensure MySQL service is running

#### Verify database credentials in .env

#### Check port 5000 is available

#### Confirm Python version with python --version
