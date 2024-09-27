import serial
import mysql.connector
import time

class SerialReader():
    
    #initialize a constructor
    def __init__(self, port, baudrate, db_config):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        self.db_config = db_config
        self.running = True
        self.conn = mysql.connector.connect(**db_config)
        self.cursor = self.conn.cursor() 

    #method for insertion data
    def insert_uid(self, uid):
        try:
            query = "INSERT INTO goat (uid) values (%s) ON DUPLICATE KEY UPDATE rfid_scan_time = CURRENT_TIMESTAMP"
            self.cursor.execute(query, (uid,))
            self.conn.commit()
            
        except Exception as e:
            print(f"Error Inserting UID into database {e}")
            
    #display the result on terminal
    def read_serial(self):
        while self.running:
            if self.ser.in_waiting:
                data = self.ser.readline().decode('utf-8').strip()
                if data.startswith("UID:"):
                    uid = data[len("UID:"):].strip()
                    self.insert_uid(uid)
                    print(f"UID inserted INTO database: {uid}")
                    
    def start(self):
        self.read_serial()
        
    def stop(self):
        self.running = False
        self.conn.close()
        self.cursor.close()
        self.ser.close()



if __name__ == ("__main__"):
    db_config = {
        'user' : 'root',
        'password' : '',
        'host' : 'localhost',
        'database' : 'goat_project'
    }
    
    reader = SerialReader('COM4', 9600, db_config)
    
    try:
        reader.start()
    except KeyboardInterrupt:
        reader.stop()