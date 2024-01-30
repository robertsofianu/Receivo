from AppFuntions import fct_get_fine_data
import os
import sqlite3
import hashlib
import smtplib
import ssl
from email.message import EmailMessage
import json



DB_PATH = r'db\produse.db'





def fct_verify_user(uS):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('SELECT id FROM userinfo WHERE username = ?', (uS, ))
    resp = cur.fetchall()
    if resp:
        r = -1 #user in DB
    else:
        r = 1 #user is not in DB
    return r

def fct_verify_email(uS):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('SELECT id FROM userinfo WHERE email = ?', (uS, ))
    resp = cur.fetchall()
    if resp:
        r = -1 #user in DB
    else:
        r = 1 #user is not in DB
    return r

def fct_verify_user_pass(uS, pS):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('SELECT password FROM userinfo WHERE username = ?', (uS, ))
    resp = cur.fetchall()
    db_pass = fct_get_fine_data(resp)

    if db_pass == pS:
        r = 1 #user introduced the correct password
    else:
        r = -1 #wrong password
    return r
    
    

def fct_insert_user_signup(uN, pS):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    pS = fct_hash_str(pS)
    cur.execute("INSERT INTO userinfo (username, password) VALUES (?, ?)", (uN, pS,))
    con.commit()




def fct_accept_user_into_DB(uN, email):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("INSERT INTO userinfo (username, email) VALUES (?, ?)", (uN, email))
    con.commit()


def fct_make_dir(uN):
    try:
        directory_path = f"\users\\{uN}"
        os.mkdir(directory_path)
    except FileExistsError:
        print('a')



    json_path = f"\\users\\{uN}\\list_nir_products.json"
    data = []
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)



    json_path2 = f'users\\{uN}\\table_final_nr.json'
    data2 = [1]
    with open(json_path2, 'w') as f:
        json.dump(data2, f, indent=4)



    json_path3 = f'users\\{uN}\\dict_all_product.json'
    with open(json_path3, 'w') as f:
        json.dump(data, f, indent=4)



    json_path4 = f'users\\{uN}\\ExcelNumber.json'
    with open(json_path4, 'w') as f:
        json.dump(data, f, indent=4)


    json_path5 = f'users\\{uN}\\NumberRowExcel.json'
    data3 = [9]
    with open(json_path5, 'w') as f:
        json.dump(data3, f, indent=4)


    json_path6 = f'users\\{uN}\\product_modify_name.json'
    with open(json_path6, 'w') as f:
        json.dump(data, f, indent=4)

    json_path7 = f'users\\{uN}\\json_is_hame_bool.json'
    with open(json_path7, 'w') as f:
        json.dump(['True'], f, indent=4)



def fct_make_new_directories(uN, year = '2024-12-05'):
    sp_y = year.split('-')
    print(sp_y)
    try:
        directory_path = f"users\\{uN}\\{sp_y[0]}"
        os.mkdir(directory_path)

        directory_path1 = f"users\\{uN}\\{sp_y[0]}\\1_January"
        os.mkdir(directory_path1) 

        directory_path2 = f"users\\{uN}\\{sp_y[0]}\\2_February"
        os.mkdir(directory_path2)

        directory_path3 = f"users\\{uN}\\{sp_y[0]}\\3_March"
        os.mkdir(directory_path3) 

        directory_path4 = f"users\\{uN}\\{sp_y[0]}\\4_April"
        os.mkdir(directory_path4)

        directory_path5 = f"users\\{uN}\\{sp_y[0]}\\5_May"
        os.mkdir(directory_path5) 

        directory_path6 = f"users\\{uN}\\{sp_y[0]}\\6_June"
        os.mkdir(directory_path6)

        directory_path7 = f"users\\{uN}\\{sp_y[0]}\\7_July"
        os.mkdir(directory_path7) 

        directory_path8 = f"users\\{uN}\\{sp_y[0]}\\8_August"
        os.mkdir(directory_path8)

        directory_path9 = f"users\\{uN}\\{sp_y[0]}\\9_September"
        os.mkdir(directory_path9) 

        directory_path10 = f"users\\{uN}\\{sp_y[0]}\\10_October"
        os.mkdir(directory_path10)

        directory_path11 = f"users\\{uN}\\{sp_y[0]}\\11_November"
        os.mkdir(directory_path11) 

        directory_path12 = f"users\\{uN}\\{sp_y[0]}\\12_December"
        os.mkdir(directory_path12) 
    except FileExistsError:
        pass



def fct_hash_str(str):
    input_string = str
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode('utf-8'))
    hashed_string = sha256_hash.hexdigest()

    return hashed_string

def fct_get_pass(user):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('SELECT password FROM userinfo WHERE username = ?', (user,))
    passw = cur.fetchall()
    f_pasw = fct_get_fine_data(passw)
    return f_pasw
    
    
def fct_sent_mail(user: str, rec_email= 'robertsofianu@gmail.com'):
    email_sender = 'listofmovie.robert@gmail.com'
    email_password = 'ynmzzzoavfmwpdmr'
    email_receiver = rec_email
    subject = 'Sign Up NIR'
    body = f"""
Dear Administrator,

I hope this message finds you well.

We have received a registration request from a new user, {user}, who wishes to join our platform. As the administrator of our community, you play a crucial role in ensuring the integrity and security of our user base.

{user} has expressed an interest in becoming a valued member of our community. We kindly request your attention to review and approve their registration.

To proceed with the user's registration approval, please follow the link provided below:

[Approve {user}'s Registration](http://127.0.0.1:5000/invite/{user})

We understand the importance of careful consideration in admitting new users to our platform. By clicking the link above, you will grant access to {user}, allowing them to enjoy the benefits of our community.

However, if you have any reservations or concerns regarding this registration request, we respect your discretion, and you may choose to ignore this email.

Please be assured that our team is committed to maintaining the highest standards of security and user experience, and we appreciate your diligence in this regard.

Thank you for your time and attention to this matter. Your dedication to the well-being of our community is greatly appreciated.

If you have any questions or require further assistance, please do not hesitate to reach out to us.

Best regards,

Robert Sofianu
Creator
Vanso
robertsofianu@gmail.com
    """
    body = body.strip()

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())






def fct_update_pass(uS, pS):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    pS = fct_hash_str(pS)
    cur.execute("""
    UPDATE userinfo SET password = ? WHERE username = ?
    """, (pS, uS))
    con.commit()


if __name__ == "__main__":
    print()