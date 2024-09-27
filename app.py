from flask import Flask, render_template, request, redirect, jsonify, flash, url_for, session
from datetime import datetime
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = 'WBl7qpIdJN4K3m1j'

DB_CONFIG = {
    'user' : 'root',
    'password' : '',
    'host' : 'localhost',
    'database' : 'goat_project'
}

def check_credentials(email, password, user_type):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    query = f"SELECT * FROM {user_type} WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        
        user = check_credentials(email, password, user_type)
        
        if user:

            session['user_type'] = user_type
            
            if user_type == 'admin':
                return redirect(url_for('admin_page'))
            elif user_type == 'farmer':
                return redirect(url_for('farmer'))
            elif user_type == 'vet':
                return redirect(url_for('vet'))
        
        else:
            flash('Invalid email or password. Please try again.', 'error')
        
    return render_template('login.html')
            

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_type', None)
    session.clear()

    return redirect(url_for('login'))
    

def get_uid_details(uid):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    
    # Query to get data from the 'goat' table
    cursor.execute("SELECT * FROM goat WHERE uid = %s", (uid,))
    goat_result = cursor.fetchone()
    
    # Query to get data from the 'breeding' table
    cursor.execute("SELECT * FROM breeding WHERE uid = %s", (uid,))
    breeding_result = cursor.fetchone()
    
    cursor.execute("SELECT * FROM baby_goat WHERE uid = %s", (uid,))
    babyGoat_result = cursor.fetchone()
    
    # Combine the results if both queries return data
    result = {}
    
    if goat_result:
        result.update(goat_result)

    if breeding_result:
        result.update(breeding_result)
        
    if babyGoat_result:
        result.update(babyGoat_result)

    # Format datetime fields for the datetime-local input if they exist
    if 'register_time' in result and result['register_time']:
        result['register_time'] = result['register_time'].strftime('%Y-%m-%dT%H:%M')

    if 'treatment_time' in result and result['treatment_time']:
        result['treatment_time'] = result['treatment_time'].strftime('%Y-%m-%dT%H:%M')

    if 'program_date' in result and result['program_date']:
        result['program_date'] = result['program_date'].strftime('%Y-%m-%dT%H:%M')

    if 'pregnancy_check_date' in result and result['pregnancy_check_date']:
        result['pregnancy_check_date'] = result['pregnancy_check_date'].strftime('%Y-%m-%dT%H:%M')

    if 'expected_birth_date' in result and result['expected_birth_date']:
        result['expected_birth_date'] = result['expected_birth_date'].strftime('%Y-%m-%dT%H:%M')

    cursor.close()
    conn.close()

    return result



@app.route('/latest_uid')
def latest_uid_route():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT uid FROM goat ORDER BY rfid_scan_time DESC LIMIT 1")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    uid = result['uid'] if result else ''
    return jsonify({'uid': uid})    

@app.route('/uid_details/<uid>')
def uid_details(uid):
    details = get_uid_details(uid)
    return jsonify(details)


@app.route('/')
def main():
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/farmer')
def farmer():
    return render_template('farmer.html')

@app.route('/vet')
def vet():
    return render_template('vet.html')

@app.route('/goats')
def goats():
    return render_template('/admin/goats.html')

@app.route('/babyGoat')
def babyGoat():
    return render_template('/admin/babyGoat.html')

@app.route('/read_BabyGoat')
def read_babyGoat():
    return render_template('/admin/read_BabyGoat.html')

@app.route('/read_Goat')
def read_Goat():
    return render_template('/admin/read_Goat.html')

@app.route('/add_Goat')
def add_Goat():
    return render_template('/admin/add_Goat.html')

@app.route('/admin_page')
def admin_page():
    return render_template('admin/admin_page.html')

    
@app.route('/update_Goat/<uid>', methods=['POST'])
def update_Goat_submit(uid):
    gender = request.form['gender']
    breed = request.form['breed']
    age = request.form['age']
    register_time = request.form['register_time']
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE goat SET gender=%s, breed=%s, age=%s, register_time=%s WHERE uid=%s
        """, (gender, breed, age, register_time, uid))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('read_Goat'))

@app.route('/add_BabyGoat', methods=['POST'])
def add_BabyGoat():
    uid = request.form['uid']
    mom_uid = request.form['mom_uid']
    dad_uid = request.form['dad_uid']
    breed = request.form['breed']
    register_time = request.form['register_time']
    health_status = request.form['health_status']
    treatment_time = request.form['treatment_time']
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO baby_goat (uid, mom_uid, dad_uid, breed, register_time, health_status, treatment_time) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (uid, mom_uid, dad_uid, breed, register_time, health_status, treatment_time))
        
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return redirect (url_for('babyGoat'))
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "An error occured while inserting the baby goat details", 500
    
@app.route('/view_BabyGoat')
def view_BabyGoat():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM baby_goat")
        results = cursor.fetchall()
        
        for result in results:
            if result['register_time']:
                result['register_time'] = result['register_time'].strftime('%Y-%m-%dT%H:%M')
            
            if result['treatment_time']:
                result['treatment_time'] = result['treatment_time'].strftime('%Y-%m-%dT%H:%M')
        
        cursor.close()
        conn.close()
        return render_template('admin/view_BabyGoat.html', babygoats = results)
        
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "An error is occurred while viewing the baby goat details"
    
@app.route('/edit_BabyGoat/<string:id>', methods=['GET', 'POST'])
def edit_BabyGoat(id):
    try:
        conn  = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        if request.method == 'POST':
            
            mom_uid = request.form['mom_uid']
            dad_uid = request.form['dad_uid']
            breed = request.form['breed']
            register_time = request.form['register_time']
            health_status = request.form['health_status']
            treatment_time = request.form['treatment_time']
            
            cursor.execute("""
                UPDATE baby_goat
                SET mom_uid=%s, dad_uid=%s, breed=%s, register_time=%s, health_status=%s, treatment_time=%s WHERE uid=%s
            """, (mom_uid, dad_uid, breed, register_time, health_status, treatment_time, id))
            
            conn.commit()

            cursor.close()
            conn.close()
            
            return redirect(url_for('view_BabyGoat'))
        
        cursor.execute("SELECT * FROM baby_goat WHERE uid=%s",(id,))
        babygoats = cursor.fetchall()
        
        for baby_goat in babygoats:
            if baby_goat['register_time']:
                baby_goat['register_time'] = baby_goat['register_time'].strftime('%Y-%m-%dT%H:%M')
            
            if baby_goat['treatment_time']:
                baby_goat['treatment_time'] = baby_goat['treatment_time'].strftime('%Y-%m-%dT%H:%M')
                
        cursor.close()
        conn.close()
        
        return render_template('admin/edit_BabyGoat.html', baby_goat=babygoats)
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "An error occured while updating the baby goat details", 500
    
@app.route('/delete_BabyGoat/<string:id>', methods=['POST', 'GET'])
def delete_BabyGoat(id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM baby_goat WHERE uid=%s",(id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return redirect(url_for('view_BabyGoat'))
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "An error occured while trying to delete the baby goat details", 500

@app.route('/update_Goat_treatment/<uid>', methods=['POST'])
def update_Goat_submit_treatment(uid):
    gender = request.form['gender']
    breed = request.form['breed']
    age = request.form['age']
    register_time = request.form['register_time']
    health_status = request.form['health_status']
    treatment_time = request.form['treatment_time']
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE goat SET gender=%s, breed=%s, age=%s, register_time=%s, health_status=%s, treatment_time=%s WHERE uid=%s
        """, (gender, breed, age, register_time, health_status,treatment_time, uid))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('read_Goat'))


@app.route('/update_health', methods=['POST'])
def update_health():
    uid = request.form['uid']
    health_status = request.form['health_status']
    treatment_form = request.form['treatment_form']
    vaccination_form = request.form['vaccination_form']
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
    
        cursor.execute("""
            UPDATE goat SET health_status=%s WHERE uid=%s
        """,(health_status,uid))
    
        cursor.execute("""
            INSERT INTO health_tracker (uid, treatment_form, vaccination_form)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE treatment_form=%s, vaccination_form=%s
        """,(uid, treatment_form, vaccination_form, treatment_form, vaccination_form))
    
        conn.commit()
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()
        
    return redirect(url_for('view_health'))

@app.route('/view_health', methods=['GET','POST'])
def view_health():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor= conn.cursor(dictionary=True)
        
        
        cursor.execute("SELECT * FROM health_tracker")
        results = cursor.fetchall()
    
        cursor.close()
        conn.close()
        
        return render_template('admin/view_health.html', healths=results)
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "An error occurred while fetching the details.", 500
    
@app.route('/edit_health/<string:id>', methods=['GET','POST'])
def edit_health(id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        
        treatment_form = request.form['treatment_form']
        vaccination_form = request.form['vaccination_form']
        
        cursor.execute("""
            UPDATE health_tracker SET treatment_form=%s, vaccination_form=%s WHERE uid=%s
        """, (treatment_form, vaccination_form, id))

        conn.commit()
        
        cursor.close()
        conn.close()
        
        return redirect(url_for('view_health'))
    
    cursor.execute("SELECT * FROM health_tracker WHERE uid=%s",(id,))
    health_tracker = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return render_template('admin/edit_health.html', health = health_tracker)

@app.route('/delete_health/<string:id>', methods=['GET', 'POST'])
def delete_health(id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM health_tracker WHERE uid=%s",(id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('view_health'))
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "An error occurred while trying to delete the goat health status", 500


@app.route('/view_slaughter')
def view_slaughter():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)  # Ensure that the cursor returns dictionaries
        cursor.execute("SELECT * FROM slaughter")
        results = cursor.fetchall()  # Use fetchall() for multiple rows

        for result in results:
            if result['register_time']:
                result['register_time'] = result['register_time'].strftime('%Y-%m-%dT%H:%M')

        cursor.close()
        conn.close()
        return render_template('admin/view_slaughter.html', slaughters=results)
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "An error occurred while fetching the details.", 500



@app.route('/submit_slaughter', methods=['POST'])
def submit_slaughter():
    weight = request.form['weight']
    sold_amount = request.form['sold_amount']
    buyer = request.form['buyer']
    cause_of_death = request.form['cause_of_death']
    slaughter_cost = request.form['slaughter_cost']
    uid = request.form['uid']  # Only get UID from the form
    

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Insert into slaughter table using data from goat table
        cursor.execute("""
            INSERT INTO slaughter (uid, gender, register_time, weight, sold_amount, buyer, cause_of_death, slaughter_cost)
            SELECT uid, gender, register_time, %s, %s, %s, %s, %s
            FROM goat
            WHERE uid = %s
        """, (weight, sold_amount, buyer, cause_of_death, slaughter_cost, uid))
        
        conn.commit()
        
        cursor.close()
        conn.close()

        return redirect(url_for('view_slaughter'))
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "An error occurred while submitting the slaughter details.", 500

@app.route('/edit_slaughter/<string:id>', methods=['GET','POST'])
def edit_slaughter(id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        
        gender = request.form['gender']
        register_time = request.form['register_time']
        weight = request.form['weight']
        sold_amount = request.form['sold_amount']
        buyer = request.form['buyer']
        cause_of_death = request.form['cause_of_death']
        slaughter_cost = request.form['slaughter_cost']
        
        cursor.execute("""
            UPDATE slaughter SET gender=%s, register_time=%s, weight=%s, sold_amount=%s, buyer=%s, cause_of_death=%s, slaughter_cost=%s
        """, (gender, register_time, weight, sold_amount, buyer, cause_of_death, slaughter_cost))
        
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return redirect(url_for('view_slaughter'))
    
    cursor.execute("SELECT * FROM slaughter WHERE uid=%s", (id,))
    slaughter = cursor.fetchone()
    
    if slaughter and slaughter['register_time']:
        slaughter['register_time'] = slaughter['register_time'].strftime('%Y-%m-%dT%H:%M')
    
    cursor.close()
    conn.close()

    return render_template('admin/edit_slaughter.html', slaughter=slaughter)

@app.route('/delete_slaughter/<string:id>', methods=['POST', 'GET'])
def delete_slaughter(id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM slaughter WHERE uid=%s",(id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return redirect(url_for('view_slaughter'))
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "An error occured while trying to delete the slaughter details", 500
    
@app.route('/breeding')
def breeding():
    return render_template('admin/breeding.html')

@app.route('/add_breeding', methods=['POST'])
def add_breeding():
    uid = request.form['uid']
    partner_uid = request.form['partner_uid']
    program_date = request.form['program_date']
    pregnancy_check_date = request.form['pregnancy_check_date']
    expected_birth_date = request.form['expected_birth_date']
    breeding_method = request.form['breeding_method']
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO breeding (uid, partner_uid, program_date, pregnancy_check_date, expected_birth_date, breeding_method) VALUES (%s, %s, %s, %s, %s, %s)
        """, (uid, partner_uid, program_date, pregnancy_check_date, expected_birth_date, breeding_method))
        
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return redirect (url_for('breeding'))
        
        
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error on inserting breeding progran details into database", 500
    
@app.route('/view_breeding')
def view_breeding():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM breeding")
        results = cursor.fetchall()
        
        for result in results:
            if result['program_date']:
                result['program_date'] = result['program_date'].strftime('%Y-%m-%dT%H:%M')
                
            if result['pregnancy_check_date']:
                result['pregnancy_check_date'] = result['pregnancy_check_date'].strftime('%Y-%m-%dT%H:%M')
            
            if result['expected_birth_date']:
                result['expected_birth_date'] = result['expected_birth_date'].strftime('%Y-%m-%dT%H:%M')
                
        cursor.close()
        conn.close()
        return render_template('admin/view_breeding.html', breedings=results )
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "An error is occurred while viewing the breeding program"
    

@app.route('/edit_breeding/<string:id>', methods=['GET', 'POST'])
def edit_breeding(id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        if  request.method == 'POST':
            
            partner_uid = request.form['partner_uid']
            program_date = request.form['program_date']
            pregnancy_check_date = request.form['pregnancy_check_date']
            expected_birth_date = request.form['expected_birth_date']
            breeding_method = request.form['breeding_method']
            
            cursor.execute("""
                UPDATE breeding 
                SET partner_uid=%s, program_date=%s, pregnancy_check_date=%s, expected_birth_date=%s, breeding_method=%s
                WHERE uid=%s
            """, (partner_uid, program_date, pregnancy_check_date, expected_birth_date, breeding_method, id))
            
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return redirect(url_for('view_breeding'))
        
        cursor.execute("SELECT * FROM breeding WHERE uid=%s",(id,))
        breedings = cursor.fetchall()
        
        for breeding in breedings:
            if breeding['program_date']:
                breeding['program_date'] = breeding['program_date'].strftime('%Y-%m-%dT%H:%M')
                
            if breeding['pregnancy_check_date']:
                breeding['pregnancy_check_date'] = breeding['pregnancy_check_date'].strftime('%Y-%m-%dT%H:%M')
                
            if breeding['expected_birth_date']:
                breeding['expected_birth_date'] = breeding['expected_birth_date'].strftime('%Y-%m-%dT%H:%M')
        
        cursor.close()
        conn.close()
        
        return render_template('admin/edit_breeding.html', breeding=breedings)            
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "An error occured while updating the breeding program"
    
    
@app.route('/delete_breeding/<string:id>', methods=['POST', 'GET'])
def delete_breeding(id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM breeding WHERE uid=%s",(id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return redirect(url_for('view_breeding'))
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "An error occured while trying to delete the breeding program date", 500
    

@app.route('/feedPriceCalc', methods=['GET','POST'])
def feedPriceCalc():
    result = numgoat = feedpergoat = priceperkg = months = None
    if request.method == 'POST':
        try:
            # Get the form inputs
            numgoat = float(request.form['numgoat'])
            feedpergoat = float(request.form['feedpergoat'])
            priceperkg = float(request.form['priceperkg'])
            months = float(request.form['months'])
            
            result = (numgoat * feedpergoat) / 1000 * priceperkg * (months * 31)
        
        except ValueError:
            result = "Invalid input. Please enter numbers only"
    
    return render_template('admin/feedPriceCalc.html', result=result, numgoat=numgoat, feedpergoat=feedpergoat, priceperkg=priceperkg, months=months)

@app.route('/addPrice', methods=['POST'])
def addPrice():
    
    time = request.form['time']
    total_spend = request.form['total_spend']
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO feed_price (time, total_spend) VALUES (%s, %s)
        """, (time, total_spend))
        
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return redirect(url_for('feedPriceCalc'))
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "An error is occured encountering when tracking the price", 500
    
@app.route('/viewPrice')
def viewPrice():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor =  conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM feed_price")
        results = cursor.fetchall()
        
        for result in results:
            if result['time']:
                result['time'] = result['time'].strftime('%Y-%m-%d %H:%M')
        
        cursor.close()
        conn.close()
        return render_template('admin/viewPrice.html', feedPrice=results)
        
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "An error occured while fetching the details", 500

@app.route('/editPrice/<int:id>', methods=['GET', 'POST'])
def editPrice(id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        
        time = request.form['time']
        total_spend = request.form['total_spend']
        
        cursor.execute("""
            UPDATE feed_price SET time=%s, total_spend=%s
        """, (time, total_spend))
        
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return redirect(url_for('viewPrice'))
    
    cursor.execute("SELECT * FROM feed_price WHERE Id=%s",(id,))
    feed_price = cursor.fetchone()
    
    if feed_price and feed_price['time']:
        feed_price['time'] = feed_price['time'].strftime('%Y-%m-%d T %H:%M')
        
    cursor.close()
    conn.close()
    
    return render_template('admin/editPrice.html', feed_price=feed_price)

@app.route('/deletePrice/<int:id>', methods=['GET','POST'])
def deletePrice(id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM feed_price WHERE Id=%s",(id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return redirect(url_for('viewPrice'))
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "An error occured while trying to delete the record details", 500
    

@app.route('/feedCalc', methods=['GET', 'POST'])
def feedCalc():
    weight = dmi = freshfodder = valueHay = konsentrat = None
    content = {}
    
    pembesaran = 0.04
    maintenance = 0.03
    pembiakan = 0.036
    menyusu = 0.043
    
    if request.method == 'POST':
        try:
            weight = float(request.form['weight'])
            stage = request.form['stage']
            hay = request.form['hay']
            
            if stage == 'pembesaran':
                dmi = round(weight * 0.04,2)
            elif stage == 'maintenance':
                dmi = round(weight * 0.03,2)
            elif stage == 'pembiakan':
                dmi = round(weight * 0.036,2)
            elif stage == 'menyusu':
                dmi = round(weight * 0.043,2)
                
            freshfodder = round(dmi * 0.7 * 5.3,2)
            if hay == 'yesHay':
                valueHay = round(dmi * 0.1,2)
            else:
                valueHay = 0.0
            konsentrat = round(dmi * 0.2,2)   
            
            content = {
                'dmi' : dmi,
                'freshfodder' : freshfodder,
                'valueHay' : valueHay,
                'konsentrat' : konsentrat
            }
            
        
        except ValueError:
            result = "Invalid input"
    
    return render_template('admin/feedCalc.html',weight=weight, dmi=dmi, freshfodder=freshfodder, valueHay=valueHay, konsentrat=konsentrat, content=content)

@app.route('/health_stats', methods=['GET','POST'])
def health_stats():
    return render_template('admin/health_stats.html')

@app.route('/treatment_time', methods=['GET','POST'])
def treatment_time():
    return render_template('admin/treatment_time.html')
    
    
@app.route('/slaughter')
def slaughter():
    return render_template('admin/slaughter.html')

@app.route('/users')
def users():
    return render_template('admin/users.html')

@app.route('/farmer_register')
def farmer_register():
    return render_template('admin/farmer_register.html')

@app.route('/add_farmer', methods=['POST'])
def add_farmer():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    date_time =  request.form.get('date_time')
    
    # hash the password for purpose of security
    # hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO farmer (name, email, password, date_time) VALUES (%s, %s, %s, %s) 
        """, (name, email, password, date_time))
        
        conn.commit()
        
        cursor.close()
        conn.close()
        
        
        return redirect(url_for('view_Farmer'))
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "An error is occured while registering the farmer.", 500
    
@app.route('/view_Farmer')
def view_Farmer():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM farmer")
    result = cursor.fetchall()  # Fetch all rows from the farmer table
    
    for row in result:
        if row['date_time']:
            row['date_time'] = row['date_time'].strftime('%Y-%m-%dT%H:%M')
    
    cursor.close()
    conn.close()
    return render_template('admin/view_Farmer.html', farmers=result)

@app.route('/edit_Farmer/<int:id>', methods=['GET','POST'])
def edit_Farmer(id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        date_time = request.form['date_time']
        
        cursor.execute("""
            UPDATE farmer SET name=%s, email=%s, password=%s, date_time=%s WHERE Id=%s
        """, (name, email, password, date_time, id))
        
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return redirect(url_for('view_Farmer'))
    
    cursor.execute("SELECT * FROM farmer WHERE Id=%s", (id,))
    farmer = cursor.fetchone()
    
    if farmer and farmer['date_time']:
        farmer['date_time'] = farmer['date_time'].strftime('%Y-%m-%dT%H:%M')
    
    cursor.close()
    conn.close()
    
    return render_template('admin/edit_Farmer.html', farmer=farmer)

@app.route('/delete_Farmer/<int:id>', methods=['POST', 'GET'])
def delete_Farmer(id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM farmer WHERE Id=%s",(id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return redirect(url_for('view_Farmer'))
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "An error occurred while trying to delete the veterinarian.", 500

@app.route('/vet_register')
def vet_register():
    return render_template('admin/vet_register.html')

@app.route('/add_Vet', methods=['POST'])
def add_Vet():
    
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    date_time = request.form.get('date_time')
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
                INSERT INTO vet (name, email, password, date_time) VALUES (%s, %s, %s, %s)
        """, (name, email, password, date_time))
        
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return redirect(url_for('view_Vet'))
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "An error is occured while registering the farmer.", 500
    
@app.route('/view_Vet')
def view_Vet():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vet")
    result = cursor.fetchall()
    
    for row in result:
        if row['date_time']:
            row['date_time'] = row['date_time'].strftime('%Y-%m-%dT%H:%M')
    
    cursor.close()
    conn.close()
    return render_template('admin/view_Vet.html', vets=result)

@app.route('/edit_Vet/<int:id>', methods=['GET', 'POST'])
def edit_Vet(id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        date_time = request.form['date_time']
        
        cursor.execute("""
            UPDATE vet SET name=%s, email=%s, password=%s, date_time=%s WHERE Id=%s 
        """, (name, email, password, date_time, id))
        
        conn.commit()
        
        cursor.close()
        conn.close()

        return redirect(url_for('view_Vet'))
    
    #Fetch the veterinarian details for the given id
    cursor.execute("SELECT * FROM vet WHERE Id=%s", (id,))
    vet = cursor.fetchone()
    
    if vet and vet['date_time']:
        vet['date_time'] = vet['date_time'].strftime('%Y-%m-%dT%H:%M')
        
    cursor.close()
    conn.close()
    
    return render_template('admin/edit_Vet.html', vet=vet)

@app.route('/delete_Vet/<int:id>', methods=['POST', 'GET'])
def delete_Vet(id):
    
    try: 
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
    
        cursor.execute("DELETE FROM vet WHERE Id=%s",(id,))
        conn.commit()
    
        conn.close()
        cursor.close()
        
        return redirect(url_for('view_Vet'))
        
    except mysql.connector.Error as err:
        print(f"Error : {err}")
        return "An error occured while deteling the veterinarian details",500


@app.route('/number_of_workers')
def number_of_workers():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(Id) FROM farmer")
    farmers_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(Id) FROM vet")
    vets_count = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    return jsonify({
        'farmers_count': farmers_count,
        'vets_count': vets_count
    })
    
@app.route('/num_GoatGender')
def num_GoatGender():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(gender) FROM goat WHERE gender = 'Male'")
    goatGender_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(gender) FROM goat WHERE gender = 'Female'")
    goatGender2_count = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    return jsonify({
        'goatGender_count': goatGender_count,
        'goatGender2_count': goatGender2_count
    })

@app.route('/num_GoatBreed')
def num_GoatBreed():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(breed) FROM goat WHERE breed = 'Alpine'")
    goatBreed_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(breed) FROM goat WHERE breed = 'Boer'")
    goatBreed2_count = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    return jsonify({
        'goatBreed_count' : goatBreed_count,
        'goatBreed2_count' : goatBreed2_count
    })
    
@app.route('/recordPrice')
def recordPrice():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Query to group the total spend by month
    cursor.execute("""
        SELECT DATE_FORMAT(time, '%M-%Y') as month, SUM(total_spend) as total_amount
        FROM feed_price
        GROUP BY month
        ORDER BY month(time) ASC
    """)

    # Fetch results from the cursor
    results = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Format the results into a dictionary or JSON-friendly format
    monthly_data = [{"month": row[0], "total_amount": float(row[1])} for row in results]

    # Return the data as JSON
    return jsonify(monthly_data)







if __name__ == "__main__":
    app.run(debug=True)