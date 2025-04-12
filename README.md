# 🐐 RFID Project Setup Guide

## 🛠️ Prerequisites
- Python 3.x
- MySQL Server
- MySQL Workbench (or similar GUI tool)
- Git

## 🚀 Installation Steps

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/goat_rfid.git
cd goat_rfid
2️⃣ Install Dependencies
bash
Copy
pip install -r requirements.txt
3️⃣ Set Up MySQL Database
Create a new database called goat_rfid_db

Import the SQL dump:

Using MySQL Workbench:

Go to File > Open SQL Script

Select goat_rfid.sql

Click the lightning bolt icon to execute

Command Line:

bash
Copy
mysql -u root -p goat_rfid_db < goat_rfid.sql
4️⃣ Configure Environment Variables
Create .env file in root directory:

env
Copy
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=localhost
MYSQL_DB=goat_rfid_db
APP_SECRET_KEY=your_generated_secret_key
5️⃣ Generate Secret Key
Run this command and copy the output to your .env:

bash
Copy
python -c "import secrets; print(secrets.token_hex(16))"
6️⃣ Launch Application
bash
Copy
python app.py
🌐 Access the application at: http://127.0.0.1:5000

🔧 Troubleshooting Tips
Ensure MySQL service is running

Verify database credentials in .env

Check port 5000 is available

Confirm Python version with python --version

