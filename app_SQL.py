import pytz
import os

from flask import Flask, render_template,jsonify, request, session, redirect, url_for
from flask_session import Session
from dotenv import load_dotenv
from AppFuntions import *
from LoginFct import *
from threading import Thread
from urllib.parse import unquote
from datetime import datetime


app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY") 
app.config['SESSION_TYPE'] = 'filesystem'  

Session(app)




@app.route('/api/data', methods=["GET"])

def api():
    path = r'JsonFiles\AllProducts.json'
    jsonf = fct_read_json(path)
    d = {'resp' : jsonf}
    return d




@app.route('/api/fz', methods=["GET"])

def apifz():
    path = r'JsonFiles\Furnizori.json'
    jsonf = fct_read_json(path)
    d = {'resp' : jsonf}
    return d



@app.route('/api/customers', methods=["GET"])

def apicustomers():
    
    jsonf = fct_customers_list()
    jsonf = list(jsonf)
    d = {'resp' : jsonf}
    return d


@app.route('/', endpoint = 'home')
def home():
    global invaid_login
    return render_template('login.html', invaid_login=invaid_login)



@app.route('/login', methods = ['POST'])
def login():
    global bool_data_complete
    global invaid_login

    user = request.form.get('username')
    passw = request.form.get("password")
    resp_db = fct_verify_user(user)
    if resp_db == -1 and fct_get_pass(user) == None:
        return render_template('create_pass.html', username=user)
    
    elif resp_db == 1 or fct_hash_str(passw) != fct_get_pass(user) and fct_get_pass(user) != None:
        invaid_login = True
        return render_template('login.html', invaid_login=invaid_login)
    
    session['user_id'] = user

    if user == "admin":
        return render_template('index_admin.html')
    return render_template('main.html', bool_data_complete=bool_data_complete)



@app.route('/signup')
def signup():
    global invalid_sign_up
    return render_template('signup.html', invalid_sign_up=invalid_sign_up)



@app.route('/forgetpass')
def forgetpass():
    return render_template('forget_password.html')


        
@app.route('/add_user_db', methods = ["POST"])
def add_user_db():

    global invalid_sign_up
    global invaid_login

    username = request.form.get('username')
    email = request.form.get('email')


    new_user_reps = fct_validate_new_users(username, email)

    if username != '' and email != '' and new_user_reps == 1:
        emailwassent = True
        t = Thread(target=fct_sent_mail, args=(username,))
        t.start()
        return render_template('login.html', emailwassent=emailwassent)
    invalid_sign_up = True
    return render_template('signup.html', invalid_sign_up=invalid_sign_up, username=username, email=email)


@app.route('/add_user_password', methods = ['POST'])

def add_user_password():

    global bool_data_complete
    global passwords_match
    user = request.form.get('username')
    pasw = request.form.get('password')
    repass = request.form.get('repassword')
    session['user_id'] = user

    if pasw != repass:
        passwords_match = False
        return render_template('create_pass.html', passwords_match=passwords_match)
    print(user, pasw, repass)
    
    fct_update_pass(user, pasw)
    return render_template('index.html')



@app.route('/start')

def start():
    global bool_data_complete
    print(session['user_id'])
    return render_template('index.html')



@app.route('/add', methods=['POST'])

def add():
    user = session['user_id']
    
    global bool_data_complete
    bool_home = fct_path_bool_is_home(user)

    
    



    json_dict_all_prod = fct_path_dict_all_product(user)

    

    data = request.form.get('data')
    nrFac = request.form.get('nrFac')
    furnizor = request.form.get('Furnizor')
    delegat = request.form.get('Delegat')


    list_1 = []
    list_1.append(data)
    list_1.append(nrFac)
    list_1.append(furnizor)

    with open(json_dict_all_prod, 'w') as f:
        json.dump(list_1, f, indent=4)
    list_nir_products = fct_path_list_product(user)



    last_element = fct_read_json_all_d(list_nir_products)

    if not last_element:
        last_element = []
    else:
        last_element = fct_read_json(list_nir_products)

    data2 = fct_read_json_all_d(JSON_PATH_PRODUSE)
    
    l_factura = ''

    fct_append_list(2, furnizor)
    if data == '' or nrFac == '' or furnizor == '':
        bool_data_complete = False
        return render_template('main.html', bool_data_complete=bool_data_complete, data=data, nrFac=nrFac, furnizor=furnizor, delegat=delegat)
    else:
        data3 = fct_read_json_all_d(bool_home)
        data3.append('False')
        with open(bool_home, 'w') as jf:
            json.dump(data3, jf, indent=4)
        fct_create_excel_file(data, nrFac, furnizor, delegat, user=user)
        l_factura = fct_read_json_all_d(json_dict_all_prod)
        data4 = fct_read_json(JSON_PATH_PRODUSE)
    return render_template('main2.html', bool_data_complete=bool_data_complete, list_1=list_1, l_factura=l_factura, data=data4)

    # 
    # return render_template('add.html', data=data[0], l_factura=l_factura )



@app.route('/create_nir_desk', methods=["POST"])

def create_nir_desk():
    user = session['user_id']
    bool_home = fct_path_bool_is_home(user)
    data_desk = request.form.get('date_desk')
    furnizor_desk = request.form.get('furnizor_desk')
    numar_factura_desk = request.form.get('numar_factura_desk')
    nume_delegat_desk = request.form.get('nume_delegat_desk')
    
    lista_furnizori = fct_read_json(JSON_PATH_FURIZORI)

    if furnizor_desk not in lista_furnizori:
        lista_furnizori.append(furnizor_desk)
        fct_write_JSON(JSON_PATH_FURIZORI, lista_furnizori)

    fct_make_new_directories(user, data_desk)
    fct_create_excel_file(data_desk, numar_factura_desk, furnizor_desk, nume_delegat_desk, user=user)

    json_dict_all_prod = fct_path_dict_all_product(user)
    
    list_furnizori = fct_read_json(JSON_PATH_FURIZORI)
    


    list_1 = []
    list_1.append(data_desk)
    list_1.append(numar_factura_desk)
    list_1.append(furnizor_desk)

    with open(json_dict_all_prod, 'w') as f:
        json.dump(list_1, f, indent=4)
    data3 = fct_read_json_all_d(bool_home)
    data3.append('False')
    with open(bool_home, 'w') as jf:
        json.dump(data3, jf, indent=4)
    
    list_nir_products = fct_path_list_product(user)
    l_factura = fct_read_json_all_d(json_dict_all_prod)
    list_1 = fct_read_json_all_d(json_dict_all_prod)
    data5 = fct_read_json(JSON_PATH_PRODUSE)
    d = fct_read_json_all_d(list_nir_products)
    
    return render_template('main2.html', bool_data_complete=bool_data_complete, list_1=list_1, data=data5, l_factura=l_factura, d=d)


@app.route('/add_desktop', methods=["POST"])
def add_desktop():
    user = session["user_id"]
    JSON_NR_NAME = fct_path_table(user)
    json_dict_all_prod = fct_path_dict_all_product(user)

    p_desk = request.form.get('p_desk')
    am_d = request.form.get('am_d')
    print(p_desk)

    all_p = fct_read_json(JSON_PATH_PRODUSE)
    

    if p_desk not in all_p:
        return render_template('add_prod_desk.html', pr = p_desk, am=am_d)

    list_1 = fct_read_json_all_d(json_dict_all_prod)
    
    list_prod_price = []




    tuple_all_Data = fct_get_data_db(p_desk)
    print(tuple_all_Data)
    tva = tuple_all_Data[1]
    um = tuple_all_Data[2]
    pf = tuple_all_Data[3]
    pv = tuple_all_Data[4]

    cant = fct_write_formated_price(am_d)
    pv = fct_write_formated_price(pv)

    total = float(pf) * float(cant)
    total = round(total, 2)
    total = fct_write_formated_price(str(total))

    nr_name = fct_read_json(JSON_NR_NAME)

    id_name = f'product{nr_name}'
    id_pf = f'pf{nr_name}'
    id_pv = f'pv{nr_name}'
    id_um = f'um{nr_name}'
    id_cant = f'cant{nr_name}'
    id_tva = f'tva{nr_name}'
    id_total = f'total{nr_name}'


    list_prod_price.append(p_desk)
    list_prod_price.append(pf)
    list_prod_price.append(pv)
    list_prod_price.append(um)
    list_prod_price.append(cant)
    list_prod_price.append(tva)
    list_prod_price.append(total)

    list_prod_price.append(id_name)
    list_prod_price.append(id_pf)
    list_prod_price.append(id_pv)
    list_prod_price.append(id_um)
    list_prod_price.append(id_cant)
    list_prod_price.append(id_tva)
    list_prod_price.append(id_total)

    fct_increment_nir_nr(JSON_NR_NAME)

    list_nir_products = fct_path_list_product(user)


    with open(list_nir_products, 'r') as file:
        json_content = file.read()
    data = json.loads(json_content)
    data.append(list_prod_price)
    with open(list_nir_products, 'w') as f:
        json.dump(data, f, indent=4)
    
    
    d = fct_read_json_all_d(list_nir_products)
    l_factura = fct_read_json_all_d(json_dict_all_prod)
    list_1 = fct_read_json_all_d(json_dict_all_prod)
    data5 = fct_read_json(JSON_PATH_PRODUSE)
    return render_template('main2.html', bool_data_complete=bool_data_complete, list_1=list_1, data=data5, l_factura=l_factura, d=d)


@app.route('/add_p_d', methods=["POST"])

def add_p_d():
    user = session["user_id"]

    list_nir_products = fct_path_list_product(user)
    JSON_NR_NAME = fct_path_table(user)
    json_dict_all_prod = fct_path_dict_all_product(user)
    

    pr = request.form.get('pr')
    am = request.form.get('am')
    um = request.form.get('um')
    tva = request.form.get('tva')
    pp = request.form.get('pp')
    sp = request.form.get('sp')

    if tva == '0.09':
        tva = '9'
    elif tva == '019':
        tva == '19'
    else:
        tva = 'UNDIFINED'

    data = fct_read_json(JSON_PATH_PRODUSE)
    print(data)
    pr = pr.upper()
    data.append(pr)

    fct_write_JSON(JSON_PATH_PRODUSE, data)

    list_prod_price = []

    print(pr, am, um, tva, pp, sp)

    cant = fct_write_formated_price(am)
    pv = fct_write_formated_price(sp)

    total = float(pp) * float(cant)
    total = round(total, 2)
    total = fct_write_formated_price(str(total))

    nr_name = fct_read_json(JSON_NR_NAME)

    id_name = f'product{nr_name}'
    id_pf = f'pf{nr_name}'
    id_pv = f'pv{nr_name}'
    id_um = f'um{nr_name}'
    id_cant = f'cant{nr_name}'
    id_tva = f'tva{nr_name}'
    id_total = f'total{nr_name}'


    list_prod_price.append(pr)
    list_prod_price.append(pp)
    list_prod_price.append(pv)
    list_prod_price.append(um)
    list_prod_price.append(cant)
    list_prod_price.append(tva)
    list_prod_price.append(total)

    list_prod_price.append(id_name)
    list_prod_price.append(id_pf)
    list_prod_price.append(id_pv)
    list_prod_price.append(id_um)
    list_prod_price.append(id_cant)
    list_prod_price.append(id_tva)
    list_prod_price.append(id_total)

    fct_increment_nir_nr(JSON_NR_NAME)

    


    with open(list_nir_products, 'r') as file:
        json_content = file.read()
    data = json.loads(json_content)
    data.append(list_prod_price)
    with open(list_nir_products, 'w') as f:
        json.dump(data, f, indent=4)
        


    fct_insert_db(pr, tva, um, pp, sp)


    l_factura = fct_read_json_all_d(json_dict_all_prod)
    list_1 = fct_read_json_all_d(json_dict_all_prod)
    data5 = fct_read_json(JSON_PATH_PRODUSE)
    d = fct_read_json_all_d(list_nir_products)
    
    return render_template('main2.html', bool_data_complete=bool_data_complete, list_1=list_1, data=data5, l_factura=l_factura, d=d)


@app.route('/add_product', methods=["POST"])
def add_product():
    user = session["user_id"]

    list_nir_products = fct_path_list_product(user)

    global is_complete
    product = request.form.get('produs')

    last_element = fct_read_json_all_d(list_nir_products)

    if not last_element:
        last_element = []
    else:
        last_element = fct_read_json_all_d(list_nir_products)
    print(last_element)
    response = fct_get_id_bool_elem_from_db(product)
    if response == 1:
        bool_is_in_db = True
        return render_template('add.html', bool_is_in_db=bool_is_in_db, product=product, last_element=last_element)
    elif response == -1:
        return render_template('add_to_db.html', product=product)

    return render_template('add_to_db.html', product=product, is_complete=is_complete)



@app.route('/add_to_nir', methods=["POST"])
def add_to_nir():
    user = session["user_id"]

    global bool_is_in_db
    global all_products
    global bool_cant
    

    list_nir_products = fct_path_list_product(user)
    JSON_NR_NAME = fct_path_table(user)
    json_dict_all_prod = fct_path_dict_all_product(user)
    

    
    list_prod_price = []

    product = request.form.get('produs')
    cant = request.form.get('nrProd')
    all_p = fct_read_json(JSON_PATH_PRODUSE)
    
    if product not in all_p:
        return render_template('add_prod_desk.html', pr = product, am=cant)
    
    print(product)
    if cant == '':
        bool_cant = True
        bool_is_in_db = True
        return render_template('add.html', bool_is_in_db=bool_is_in_db, bool_cant=bool_cant, product=product, last_element=last_element)
    all_products.append(product)
    
    tuple_all_Data = fct_get_data_db(product)
    tva = tuple_all_Data[1]
    um = tuple_all_Data[2]
    pf = tuple_all_Data[3]
    pv = tuple_all_Data[4]

    cant = fct_write_formated_price(cant)
    pv = fct_write_formated_price(pv)

    total = float(pf) * float(cant)
    total = round(total, 2)
    total = fct_write_formated_price(str(total))

    nr_name = fct_read_json(JSON_NR_NAME)

    id_name = f'product{nr_name}'
    id_pf = f'pf{nr_name}'
    id_pv = f'pv{nr_name}'
    id_um = f'um{nr_name}'
    id_cant = f'cant{nr_name}'
    id_tva = f'tva{nr_name}'
    id_total = f'total{nr_name}'


    list_prod_price.append(product)
    list_prod_price.append(pf)
    list_prod_price.append(pv)
    list_prod_price.append(um)
    list_prod_price.append(cant)
    list_prod_price.append(tva)
    list_prod_price.append(total)

    list_prod_price.append(id_name)
    list_prod_price.append(id_pf)
    list_prod_price.append(id_pv)
    list_prod_price.append(id_um)
    list_prod_price.append(id_cant)
    list_prod_price.append(id_tva)
    list_prod_price.append(id_total)

    fct_increment_nir_nr(JSON_NR_NAME)

    


    with open(list_nir_products, 'r') as file:
        json_content = file.read()
    data = json.loads(json_content)
    data.append(list_prod_price)
    with open(list_nir_products, 'w') as f:
        json.dump(data, f, indent=4)
    
    bool_is_in_db = False
    last_element = fct_read_json_all_d(list_nir_products)

    if not last_element:
        last_element = []
    else:
        last_element = fct_read_json_all_d(list_nir_products)

    last_element = last_element[-1][0]
    list_nir_products = fct_path_list_product(user)
    l_factura = fct_read_json_all_d(json_dict_all_prod)
    list_1 = fct_read_json_all_d(json_dict_all_prod)
    data5 = fct_read_json(JSON_PATH_PRODUSE)
    d = fct_read_json_all_d(list_nir_products)
    
    return render_template('main2.html', bool_data_complete=bool_data_complete, list_1=list_1, data=data5, l_factura=l_factura, d=d)


@app.route('/add_to_db', methods=["POST"])

def add_to_db():
    user = session["user_id"]

    global is_complete
    global bool_is_in_db
    global all_products

    list_nir_products = fct_path_list_product(user)
    JSON_NR_NAME = fct_path_table(user)
    

    list_prod_price = []

    produs = request.form.get('product')
   
    nrProd = request.form.get('nrProd')
    tva_furnizor = request.form.get('tva_furnizor')
    u_m = request.form.get('u_m')
    pret_fz = request.form.get('pret_fz')
    pret_final = request.form.get('pret_final')
    if tva_furnizor == "0.09":
        tva_furnizor = '9'
    else:
        tva_furnizor = '19'
    produs = produs.upper()
    
    if produs == '' or nrProd == '' or pret_fz == '' or pret_final == '':
        is_complete = False
        return render_template('add_to_db.html', is_complete=is_complete, produs=produs,
                               nrProd=nrProd, pret_fz=pret_fz, pret_final=pret_final)


    tva = tva_furnizor
    um = u_m
    pf = pret_fz
    pv = pret_final

    pf = fct_write_formated_price(pf)
    cant = fct_write_formated_price(nrProd)
    pv = fct_write_formated_price(pv)

    total = float(pf) * float(cant)
    total = round(total, 2)
    total = fct_write_formated_price(str(total))

    nr_name = fct_read_json(JSON_NR_NAME)
   

    id_name = f'product{nr_name}'
    id_pf = f'pf{nr_name}'
    id_pv = f'pv{nr_name}'
    id_um = f'um{nr_name}'
    id_cant = f'cant{nr_name}'
    id_tva = f'tva{nr_name}'
    id_total = f'total{nr_name}'


    list_prod_price.append(produs)
    list_prod_price.append(pf)
    list_prod_price.append(pv)
    list_prod_price.append(um)
    list_prod_price.append(cant)
    list_prod_price.append(tva)
    list_prod_price.append(total)

    list_prod_price.append(id_name)
    list_prod_price.append(id_pf)
    list_prod_price.append(id_pv)
    list_prod_price.append(id_um)
    list_prod_price.append(id_cant)
    list_prod_price.append(id_tva)
    list_prod_price.append(id_total)


    fct_increment_nir_nr(JSON_NR_NAME)

    


    with open(list_nir_products, 'r') as file:
        json_content = file.read()
    data = json.loads(json_content)


    data.append(list_prod_price)
    with open(list_nir_products, 'w') as f:
        json.dump(data, f, indent=4)
    
    all_products.append(produs)
    fct_append_list(1, produs)
    fct_insert_db(produs, tva_furnizor, u_m, pret_fz, pret_final)
    
    list_prod_price.append(produs)
    list_prod_price.append(nrProd)

    

    return render_template('add.html', bool_is_in_db=bool_is_in_db)



@app.route('/finish')

def finish():
    global bool_data_complete
    global all_products
    global bool_home
    fz = fct_read_json_all_d(JSON_PATH_DICT_ALL_DATA)[-1]

    user = session['user_id']

    all_products = []

    return render_template('main.html', bool_data_complete=bool_data_complete)



@app.route('/invite/<username>', methods=['GET'])
def registration(username):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('SELECT email FROM temporary_users WHERE username = ?', (username, ))
    email_l = cur.fetchall()
    email = fct_get_fine_data(email_l)

    fct_accept_user_into_DB(username, email)
    fct_make_dir(username)
    
    return 'user accepted'



@app.route('/receiving_note')

def receiving_note():
    user = session['user_id']

    global bool_data_complete
    global bool_is_in_db

    bool_home = fct_path_bool_is_home(user)

    list_nir_products = fct_path_list_product(user)
    data = fct_read_json_all_d(JSON_PATH_PRODUSE)
    json_dict_all_prod = fct_path_dict_all_product(user)

    data3 = fct_read_json(bool_home)
    l_factura = fct_read_json_all_d(json_dict_all_prod)
    # nr_nir = fct_read_json(JSON_PATH_NIR_NUMBER)
    nr_nir = 2222
    

    if data3 == "True":
        return render_template('main.html', bool_data_complete=bool_data_complete, nr_nir=nr_nir)
    else:
        l_factura = fct_read_json_all_d(json_dict_all_prod)
        list_1 = fct_read_json_all_d(json_dict_all_prod)
        data5 = fct_read_json(JSON_PATH_PRODUSE)
        d = fct_read_json_all_d(list_nir_products)
        
        return render_template('main2.html', bool_data_complete=bool_data_complete, list_1=list_1, data=data5, l_factura=l_factura, d=d)




@app.route('/product_info')

def product_info():
    return render_template('product_info.html')



@app.route('/product_info_2/<product>')

def product_infoo(product):
    user = session['user_id']
    json_product_name = fct_path_product_modify_name(user)
    id = fct_get_id_elem_from_db(product)

    data = []
    data.append(id)
    data.append(product)
    print(data)
    with open(json_product_name, 'w') as f:
        json.dump(data, f, indent=4)

    r = fct_get_data_db(product)
    
    return render_template('searchresult.html', product=r[0], vat=r[1], pp=r[3], sp=r[4], r=r)



@app.route('/search', methods = ['POST'])

def search():
    user = session['user_id']

    product = request.form.get('product')

    ids = fct_get_id_elem_from_db(product)

    data = []
    data.append(ids)
    data.append(product)
    
    json_mod = fct_path_product_modify_name(user)

    with open(json_mod, 'w') as file:
        json.dump(data, file, indent = 4)
    r = fct_get_data_db(product)
    
    return render_template('searchresult.html', product=r[0], vat=r[1], pp=r[3], sp=r[4], r=r)



@app.route('/edit_product')
def edit_product():

    user = session['user_id']
    print(user)
    json_product_name = fct_path_product_modify_name(user)
    modify_product = fct_read_json(json_product_name)
    r = fct_get_data_db(modify_product)
    return render_template('modify_product.html', product=r[0], vat=r[1], pp=r[3], sp=r[4])



@app.route('/save', methods = ['POST'])

def save():
    user = session["user_id"]
    global succes_mod

    json_product_name = fct_path_product_modify_name(user)
    modify_product_id = fct_read_json_all_d(json_product_name)[0]
    modify_product = fct_read_json_all_d(json_product_name)[1] 
    list_nir_products = fct_path_list_product(user)
    print(modify_product_id)




    p = request.form.get('product')
    p = p.upper()
    tva = request.form.get('vat')
    print(tva)
    pp = request.form.get('pp')
    sp = request.form.get('sp')
    p2 = p
    id = modify_product_id
    succes_mod = True


    modify_product_LIST(modify_product, p, user)

    data = fct_read_json_all_d(list_nir_products)
    for element in data:
        if p in element:
            element[0] = p2
            element[1] = pp
            element[2] = sp
    fct_write_JSON(list_nir_products, [])

    with open(list_nir_products, 'w') as jf:
        json.dump(data, jf, indent=4)
    fct_update_product_info_id(p, tva, pp, sp, id)
    return render_template('modify_product.html', product=p, vat=tva, pp=pp, sp=sp, succes_mod=succes_mod)



@app.route('/add_product_db', methods = ['POST'])

def add_product_db():

    p = request.form.get('product')
    tva = request.form.get('tva_furnizor')
    um = request.form.get('u_m')
    pp = request.form.get('pret_fz')
    sp = request.form.get('pret_final')
    r = fct_get_id_elem_from_db(p)

    print(type(sp))
    if p == '' or pp == '' or sp == '' or r == 1:
        empty_spaces = True
        return render_template('add_new_product.html', empty_spaces=empty_spaces, p=p,
                                tva=tva, um=um, pp=pp, sp=sp) 

    if tva == '0.09':
        tva = '9'
    else:
        tva = '19'
    try:
        pp = fct_write_formated_price(pp)
        sp = fct_write_formated_price(sp)
        fct_append_list(1, p)
        p = p.upper()
        fct_insert_db(p, tva, um, pp, sp)
        return render_template('product_info.html')
    except:
        return ''



@app.route('/test')

def test():
    return render_template('test.html')
    



@app.route('/clients')

def clients():
    data =  fct_customers_list()
    return render_template('clienti.html', data=data)



@app.route('/final_preview')

def final_preview():

    user = session["user_id"]

    list_nir_products = fct_path_list_product(user)

    with open(list_nir_products, 'r') as file:
        json_content = file.read()
    data = json.loads(json_content)

    nr = len(data)
    
    return render_template('final_mod.html', data=data, nr=nr)



@app.route('/preview')

def preview():

    global all_products
    return render_template('preview.html', all_products=all_products)



@app.route('/add_new_info')

def add_new_info():
    return render_template('add_new_product.html')



@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('login.html')



@app.route('/final_mod')

def final_mod():
    user = session["user_id"]

    list_nir_products = fct_path_list_product(user)
    
    with open(list_nir_products, 'r') as file:
        json_content = file.read()
    data = json.loads(json_content)
    print(data)
    nr = len(data)
    return render_template('final_mod.html', data=data, nr=nr)



@app.route('/fini', methods = ["POST"])

def fini():
    user = session['user_id']

    global bool_data_complete
    fz = fct_read_json_all_d(JSON_PATH_DICT_ALL_DATA)[-1]
    bool_home = fct_path_bool_is_home(user)


    list_nir_products = fct_path_list_product(user)

    JSON_NR_NAME = fct_path_table(user)
    
    with open(list_nir_products, 'r') as f:
        json_c = f.read()
    data = json.loads(json_c)

    for a in range(1, len(data) + 1):

        print(a)
        denumire = request.form.get(f'product{a}')
        pf = request.form.get(f'pf{a}')
        pv = request.form.get(f'pv{a}')
        um = request.form.get(f'um{a}')
        cant = request.form.get(f'cant{a}')
        tva = request.form.get(f'tva{a}')
        print(denumire, pf, pv, um, cant, tva)
        fct_create_excel_tables([denumire, tva, um, pf, pv], cantitate=cant, user=user, furnizor=fz)

    fct_terminare(user, fz)
    data = []
    with open(list_nir_products, 'w') as f:
        json.dump(data, f, indent=4)

    data2 = [1]
    with open(JSON_NR_NAME, 'w') as f:
        json.dump(data2, f, indent=4)

    data3 = fct_read_json_all_d(bool_home)
    data3.append('True')
    with open(bool_home, 'w') as jf:
        json.dump(data3, jf, indent=4)

    return render_template('main.html', bool_data_complete=bool_data_complete)



@app.route('/fini_desk', methods=["POST"])

def fini_desk():
    user = session["user_id"]
    bool_home = fct_path_bool_is_home(user)
    global bool_data_complete


    list_nir_products = fct_path_list_product(user)
    JSON_NR_NAME = fct_path_table(user)
    JSON_PATH_DICT_ALL_DATA = fct_path_dict_all_product(user)
    
    fz = fct_read_json_all_d(JSON_PATH_DICT_ALL_DATA)[-1]
    with open(list_nir_products, 'r') as f:
        json_c = f.read()
    data = json.loads(json_c)

    for a in range(1, len(data) * 10):

        denumire = request.form.get(f'product{a}')
        pf = request.form.get(f'pf{a}')
        pv = request.form.get(f'pv{a}')
        um = request.form.get(f'um{a}')
        cant = request.form.get(f'cant{a}')
        tva = request.form.get(f'tva{a}')

        if denumire is None:
            continue
        else:
            fct_create_excel_tables([denumire, tva, um, pf, pv], cantitate=cant, user=user, furnizor=fz)


    fct_terminare(user, fz)
    data = []
    with open(list_nir_products, 'w') as f:
        json.dump(data, f, indent=4)

    data2 = [1]
    with open(JSON_NR_NAME, 'w') as f:
        json.dump(data2, f, indent=4)

    data3 = fct_read_json_all_d(bool_home)
    data3.append('True')
    with open(bool_home, 'w') as jf:
        json.dump(data3, jf, indent=4)

    return render_template('main.html', bool_data_complete=bool_data_complete)



@app.route('/modify/<parameter1>', methods = ["GET"])

def modify_page(parameter1):
    user = session['user_id']

    json_product_name = fct_path_product_modify_name(user)
    id = fct_get_id_elem_from_db(parameter1)

    data = []
    data.append(id)
    data.append(parameter1)

    with open(json_product_name, 'w') as f:
        json.dump(data, f, indent=4)
    
    p_info = fct_get_data_db(parameter1)

    return render_template('mod_prod.html', product=parameter1, tva = p_info[1], pp=p_info[3], sp=p_info[4])



@app.route('/edit_cust/<p1>')

def edit_cust(p1):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('SELECT amout FROM customers WHERE nume = ?', (p1, ))
    amount = fct_get_fine_data(cur.fetchall())
    return render_template('add_cust_amount.html', p1=p1, amount=amount)
    

@app.route('/add_client')

def add_client():
    return render_template('add_customer.html')


@app.route('/add_client_db', methods = ['POST'])

def add_client_db():
    user = session['user_id']

    first_name = request.form.get('prenume')
    last_name = request.form.get('nume')
    amount = request.form.get('bani')
    amount = fct_write_formated_price(amount)
    complete_name = f'{last_name} {first_name}'
    complete_name = complete_name.upper()

    data = fct_read_json_all_d(JSON_PATH_CUSTOMERS)

    utc_now = datetime.utcnow()
    desired_timezone = pytz.timezone('Europe/Bucharest')
    localized_time = utc_now.replace(tzinfo=pytz.utc).astimezone(desired_timezone)
    formatted_datetime = localized_time.strftime('%d-%m-%Y %H:%M:%S %Z')

    dictionar = {
        "user" : user,
        "amount" : amount,
        "data" : formatted_datetime
    }

    list_all = [complete_name, dictionar]

    data.append(list_all)

    with open(JSON_PATH_CUSTOMERS, 'w') as file:
        json.dump(data, file, indent=4)
    
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('INSERT INTO customers (nume, amout) VALUES (?, ?)', (complete_name, amount))
    con.commit()
    
    data =  fct_customers_list()
    return render_template('clienti.html', data=data)


@app.route('/search_customers')

def search_customers(): 
    
    data = fct_customers_list()
    print(data)
    
    return render_template('search_customers.html', data=data)



@app.route('/add_button')
def add_button():
    p1 = ''
    return render_template('prod_amount.html', p1=p1)



@app.route('/back/<param>')
def back(param):
    user = session['user_id']

    data = fct_read_json_all_d(JSON_PATH_PRODUSE)
    json_dict_all_prod = fct_path_dict_all_product(user)

    l_factura = fct_read_json_all_d(json_dict_all_prod)

    if param == '1':
        list_nir_products = fct_path_list_product(user)
        d = fct_read_json_all_d(list_nir_products)
        l_factura = fct_read_json_all_d(json_dict_all_prod)
        list_1 = fct_read_json_all_d(json_dict_all_prod)
        data5 = fct_read_json(JSON_PATH_PRODUSE)
        return render_template('main2.html', bool_data_complete=bool_data_complete, list_1=list_1, data=data5, l_factura=l_factura, d=d)
    
    elif param == '2':
        return render_template('main.html')
    
    elif param == '3':
        data =  fct_customers_list()
        return render_template('clienti.html', data=data)
    
    elif param == '4':
         return render_template('search_cust_date.html') 



    print(param)



@app.route('/test1', methods = ["POST"])

def test1():
    data = request.form.get('data')
    print(data)
    return '' 



@app.route('/delete/<parameter1>', methods = ["GET"])

def delete(parameter1):
    user = session["user_id"]

    list_nir_products = fct_path_list_product(user)
    json_dict_all_prod = fct_path_dict_all_product(user)
    list_1 = fct_read_json_all_d(json_dict_all_prod)
 
    data = fct_read_json_all_d(list_nir_products)

    data2 = []
    for l in data:
        for p_infi in l:
            if parameter1 in p_infi:
                print(l)
                index = data.index(l)
                data.pop(index)
                break

    with open(list_nir_products, 'w') as f:
        json.dump(data2, f, indent=4)
    
    with open(list_nir_products, 'w') as f:
        json.dump(data, f, indent=4)

    d = fct_read_json_all_d(list_nir_products)
    l_factura = fct_read_json_all_d(json_dict_all_prod)
    list_1 = fct_read_json_all_d(json_dict_all_prod)
    data5 = fct_read_json(JSON_PATH_PRODUSE)
    return render_template('main2.html', bool_data_complete=bool_data_complete, list_1=list_1, data=data5, l_factura=l_factura, d=d)

@app.route('/delete2/<parameter1>', methods = ["GET"])

def delete2(parameter1):
    user = session["user_id"]

    list_nir_products = fct_path_list_product(user)
    json_dict_all_prod = fct_path_dict_all_product(user)
    list_1 = fct_read_json_all_d(json_dict_all_prod)
 
    data = fct_read_json_all_d(list_nir_products)

    data2 = []
    for l in data:
        for p_infi in l:
            if parameter1 in p_infi:
                print(l)
                index = data.index(l)
                data.pop(index)
                break

    with open(list_nir_products, 'w') as f:
        json.dump(data2, f, indent=4)
    
    with open(list_nir_products, 'w') as f:
        json.dump(data, f, indent=4)


    list_nir_products = fct_path_list_product(user)

    with open(list_nir_products, 'r') as file:
        json_content = file.read()

    dataa = json.loads(json_content)
    nr = len(data)
    return render_template('final_mod.html', data=dataa, nr=nr)




@app.route('/add_subtract_customer_amout/<param>/<param2>/<param3>')

def add_subtract_customer_amout(param, param2, param3):
    user = session['user_id']

    

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('SELECT amout FROM customers WHERE nume = ?', (param,))
    amount = float(fct_get_fine_data(cur.fetchall()))
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%d-%m-%Y %H:%M:%S")

    if param3 == '1':
        sum = amount + float(param2)
        dictionar = {
            "user" : user,
            "amount" : float(param2),
            "data" : formatted_datetime
        }
    elif param3 == '2':
        sum = amount - float(param2)
        dictionar = {
            "user" : user,
            "amount" : f'-{float(param2)}',
            "data" : formatted_datetime
        }
    
    data = fct_read_json_all_d(JSON_PATH_CUSTOMERS)



    

    list_all = [param, dictionar]

    data.append(list_all)

    with open(JSON_PATH_CUSTOMERS, 'w') as file:
        json.dump(data, file, indent=4)
    


    cur.execute('UPDATE customers SET amout = ? WHERE nume = ? ', (sum, param))
    con.commit()

    print(param, param2, param3, sum)
    # SOFIANU MIHAELA 10 1 12.0
    data =  fct_customers_list()
    return render_template('clienti.html', data=data)




@app.route('/show_more_details_cust/<customer>')
def show_more_details_cust(customer):
    print(customer)
    list_serched_customer_details = []

    list_all_data_cust = fct_read_json_all_d(JSON_PATH_CUSTOMERS)
    for list in list_all_data_cust:
        if list[0] == customer:
            list_serched_customer_details.append(list)
    print(list_serched_customer_details[0][1]["user"])

    return render_template('more_details_cust.html', list=list_serched_customer_details, customer=customer)



@app.route('/add_product_everywhere/<p1>')
def add_product_everywhere(p1):
    return render_template('prod_amount.html', p1=p1)




@app.route('/search_date')
def search_date():
    return render_template('search_cust_date.html') 




@app.route('/sent_data', methods = ['POST'])
def sent_data():
    date = request.form.get('data')
    sp_date = date.split("-")
    final_date = f'{sp_date[2]}-{sp_date[1]}-{sp_date[0]}'

    cust_list = fct_read_json_all_d(JSON_PATH_CUSTOMERS)
    data_all_cust = []
    for el in cust_list:
        if final_date in el[1]['data']:
            data_all_cust.append(el)

    all_cust = set()
    for elem in data_all_cust:
        all_cust.add(elem[0])

    all_cust = list(all_cust)

    d = {}

    for name in all_cust:
        list_all_amount = []
        total = 0
        for lista in data_all_cust:
            if name in lista:
                list_all_amount.append(lista[1])
                # print(lista[1]['amount'])
                total += float(lista[1]['amount'])

        list_all_amount.append(total)     
        d[name] = list_all_amount

    for value in d.values():
        for element in value:
            if type(element) is dict:
                print(element)

    return render_template("date_cust_search.html", d=d, final_date=final_date) 


@app.route('/finish_rec_notes_cl', methods = ['POST'])
def finish_rec_notes_cl():
    user = session['user_id']
    end_date = request.form.get('end_date')
    resp = fct_trasfer_files(user, end_date)

    return render_template('main.html', bool_data_complete=bool_data_complete, resp = resp)


@app.route('/download_page', methods = ['POST'])
def download_page():
    down_date = request.form.get('dowload_date')
    fct_download_to_local(down_date)
    return render_template('main.html', bool_data_complete=bool_data_complete)
    



if __name__ == "__main__":
    app.run(debug=True)
