import mysql.connector
import sys
import os





def insert(user,url):
    conn = mysql.connector.connect(
        host = 'bbvatjkgxodfj3ar8fsd-mysql.services.clever-cloud.com',
        user = 'ugruig9xosjpklaa',
        password = 'qPg7Iimt3Oq89pRG7yOL',
        database = 'bbvatjkgxodfj3ar8fsd'
    )
    
    if conn.is_connected():
            print("Connection to MySQL DB successful")
    
    else:
       sys.exit(1)
       
    cursor = conn.cursor()
    
    print("user : ",user)
    print("url : ",url)
    
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, user text, url text)''')
      
    cursor.execute('''INSERT INTO users (user, url) VALUES (%s, %s)''', (user, url))
     
    conn.commit()
    conn.close()

   
def retrive(user):
    try:
              print(user)
              conn = mysql.connector.connect(
                 host = 'bbvatjkgxodfj3ar8fsd-mysql.services.clever-cloud.com',
        user = 'ugruig9xosjpklaa',
        password = 'qPg7Iimt3Oq89pRG7yOL',
        database = 'bbvatjkgxodfj3ar8fsd'
              )
              
              if conn.is_connected():
                      print("Connection to MySQL DB successful")
              
              else:
                 print("faild to connect to MySQL")
                 return False
                 
              cursor = conn.cursor()
              
              cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, user text, url text)''')
              
              cursor.execute('''SELECT url FROM users WHERE user = %s''', (user,))
              row = cursor.fetchall()
              
              if not row :
                     cursor.execute('''INSERT INTO users (user, url) VALUES (%s, %s)''', (user, 'NULL'))
                     conn.commit()
                     return 'new'
                 
              print(row)
                 
              new_row=[]
              for i in row:
                  if i[0] != 'NULL':
                      print(i)
                      new_row.append(i[0])
                  
              print(new_row)
              return new_row
    except:
        print("Error")
        return False
    finally:
        cursor.close()
        conn.close()
   
def delete(user):
    conn = mysql.connector.connect(
       host = 'bbvatjkgxodfj3ar8fsd-mysql.services.clever-cloud.com',
        user = 'ugruig9xosjpklaa',
        password = 'qPg7Iimt3Oq89pRG7yOL',
        database = 'bbvatjkgxodfj3ar8fsd'
    )
    cursor = conn.cursor()
    
    if conn.is_connected():
            print("Connection to MySQL DB successful")
    
    else:
      return False
    
    cursor.execute('''DELETE FROM users WHERE user = %s''', (user,))
   
    conn.commit()
    
    cursor.close()
    conn.close()

def delete_file(user,file_name):
    conn = mysql.connector.connect(
        host = 'bbvatjkgxodfj3ar8fsd-mysql.services.clever-cloud.com',
        user = 'ugruig9xosjpklaa',
        password = 'qPg7Iimt3Oq89pRG7yOL',
        database = 'bbvatjkgxodfj3ar8fsd'
    )
    cursor = conn.cursor()
    
    print(user,file_name)
    
    if conn.is_connected():
            print("Connection to MySQL DB successful")
    
    else:
      return False
    
    cursor.execute('''DELETE FROM users WHERE user = %s and url = %s''', (user,file_name))

    conn.commit()
    
    cursor.close()
    conn.close()
    
    return True


