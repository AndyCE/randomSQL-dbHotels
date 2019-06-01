######################################################################
### Importante ### 

### Modulo a instalar:
## pip3 install pymysql     pip install pymysql

### Cambios en la creación de la base de datos:
## ALTER TABLE reserves CHANGE COLUMN hab_id hab_id mediumint(8) unsigned DEFAULT NULL; 


######################################################################


import pymysql as __pymysql # Libreria para realziar la conexión con MYSQL
import random as __random # Libreria para elegir valores aleatorios
import time as __time
import json as __json # Librerira que utilizo para leer el contenido de ficheros JSON
from calendar import monthrange as __monthrange # Libreria necesaria para tratar con fechas
import datetime as __datetime



### Función para realizar la conexión
def myConnection (host, user, passwd, db = 'db_hotels'):
    try:
        conexion = __pymysql.connect(host, user, passwd, db)
        return conexion
    except ValueError:
        print ('Conexión Fallida')

### Función que devulve una tabla aleatoriamente
def __random_table():
    num = __random.randint(0,5)
    options = {
        0 : 'clients',
        1 : 'habitacions',
        2 : 'hotels',
        3 : 'paisos',
        4 : 'poblacions',
        5 : 'reserves'
    }
    return options[num]

### Función que devolvera una columna aleatorio de una tabla 
def __random_column(table):
    if table == 'clients': # Tabla clients
        num = __random.randint(0,5)
        options = {
            0 : 'client_id',
            1 : 'nom',
            2 : 'cognom1',
            3 : 'sexe', 
            4 : 'data_naix',
            5 : 'pais_origen_id'
        }
    elif table == 'habitacions': # Tabla habitacions
        num = __random.randint(0,2)
        options = {
            0 : 'hab_id',
            1 : 'hotel_id',
            2 : 'num_hab'
        }
    elif table == 'hotels': # Tabla hotels
        num = __random.randint(0,5)
        options = {
            0 : 'hotel_id',
            1 : 'nom',
            2 : 'categoria',
            3 : 'habitacions', 
            4 : 'adreca',
            5 : 'poblacio_id'
        }
    elif table == 'paisos': # Tabla paisos
        num = __random.randint(0,1)
        options = {
            0 : 'pais_id',
            1 : 'nom'
        }
    elif table == 'poblacions': # Tabla poblacions
        num = __random.randint(0,1)
        options = {
            0 : 'poblacio_id',
            1 : 'nom'
        }
    elif table == 'reserves': # Tabla reserves
        num = __random.randint(0,4)
        options = {
            0 : 'reserva_id',
            1 : 'hab_id',
            2 : 'data_inici',
            3 : 'data_fi',
            4 : 'client_id'
        }

    return options[num]

### Función que construirá y devolverá una query completa en formato String
def __random_query():
    table = __random_table() # Selecciono una tabla random
    # Selecciono dos columnas random desiguales (2 columnas porque la tabla paisos/poblacions tiene solo 2 columnas)
    column1 = __random_column(table)
    column2 = __random_column(table)
    while column2 == column1: # Si son iguales, busco otra
        column2 = __random_column(table)
    # Función que devuelve un par de joins segun la tabla que sale random (está dentro de otra función porque es el unico sitio donde se utiliza)
    def join_switch(table):
        if table == 'clients' : return ' INNER JOIN paisos ON paisos.pais_id = clients.pais_origen_id INNER JOIN reserves ON clients.client_id = reserves.client_id INNER JOIN habitacions ON habitacions.hab_id = reserves.hab_id'
        elif table == 'habitacions' : return ' INNER JOIN reserves ON reserves.hab_id = habitacions.hab_id INNER JOIN hotels ON habitacions.hotel_id = hotels.hotel_id INNER JOIN clients ON clients.client_id = reserves.client_id'
        elif table == 'hotels' : return ' INNER JOIN poblacions ON poblacions.poblacio_id = hotels.poblacio_id INNER JOIN habitacions ON hotels.hotel_id = habitacions.hotel_id INNER JOIN reserves ON reserves.hab_id = habitacions.hab_id'
        elif table == 'paisos' : return ' INNER JOIN clients ON clients.pais_origen_id = paisos.pais_id'
        elif table == 'poblacions' : return ' INNER JOIN hotels ON hotels.poblacio_id = poblacions.poblacio_id'
        elif table == 'reserves' : return ' INNER JOIN clients ON clients.client_id = reserves.client_id INNER JOIN habitacions ON reserves.hab_id = habitacions.hab_id INNER JOIN hotels ON habitacions.hotel_id = hotels.hotel_id'
    join = join_switch(table) # Almaceno dichos join

    ## Creo una query, la imprimo por pantalla, y la devuelvo con un return
    query = 'SELECT {table}.{column1}, {table}.{column2} FROM {table} {join} WHERE 0=0;'.format(table = table, column1 = column1, column2 = column2, join = join)
    print('\n', query)
    return query

### Función que ejecutará una query
## IN: established_connection, query
## OUT: myresult (fetchall), print del tiempo de ejecución
def __execute_query_fetchall(established_connection, query):
    try: # Compruebo que se ejecuta la query sin problemas
        with established_connection.cursor() as mycursor: # Usando with me aseguro de que puedo acceder al cursor
            start_time = __time.time() # Empieza el contador de tiempo usado más adelante
            mycursor.execute(query) # Ejecución de la query y posterior almacenamiento en el cursor
            print("--- {0} seconds ---".format(__time.time() - start_time), '\n') # Imprimo el tiempo de ejecución de la query en segundos
            data = mycursor.fetchall() # Guardo los datos en una variable
            mycursor.close() # Cierro el cursor
            return data
    except: # Imprimo 'ERROR' por pantalla si algo saliese mal durante la ejecución
        print('ERROR')
        print('\n')

### Función para ver el resultado de una query recorriendo el resultado
def __print_query_result(data):
    linea = 1
    for result in data:
        print('Linea ' + str(linea) + ' = ' + str(result))
        linea+=1

### Función que devolverá un insert random en formato String
def __random_insert():

    ## Funciones que utilizo para generar datos random
    # Función para sacar un nombre random de un fichero JSON que he sacado de GitHub
    # https://github.com/dominictarr/random-name/blob/master/first-names.json
    def __get_random_name():
        names = __json.load(open('JSON/first-names.json'))
        return __random.choice(names)

    # Función para sacar un apellido random de un fichero JSON que he sacado de GitHub
    # https://github.com/rossgoodwin/american-names/blob/master/surnames.json
    def __get_random_surname():
        surnames = __json.load(open('JSON/surnames.json'))
        return __random.choice(surnames)

    # Función para sacar un género random
    def __get_random_gender():
            num = __random.randint(0,1)
            if num == 0 : return 'M'
            if num == 1 : return 'F'

    # Función para sacar una fecha random formato 'AAA-MM-DD', 
    # tiene que ser mayor de edad y no puede tener mas de 120 años
    def __get_random_born_day():
        MM = __random.randint(1,12) # Mes random
        AAAA = __random.randint(1900,2001) # Año random
        max_day = __monthrange(AAAA, MM) # Saco el ultimo dia del mes para utilizarlo luego
        DD = __random.randint(1,max_day[1])
        born_day = '{año}-{MM}-{DD}'.format(año = str(AAAA), MM = str(MM), DD = str(DD))
        return born_day

    # Función para sacar un pais_origen_id random. Min 1 y Max 19
    def __get_random_country_id():
        return __random.randint(1,19)

    # Función para generar una dirección random
    def __get_random_address():
        address_types = ['Carrer', 'Avenida', 'Plaza', 'Carretera', 'Rambla', 'Via']
        address_to_return = '{0} de {1}, {2}'.format( __random.choice(address_types), __get_random_name(), str(__random.randint(1,1000)) )
        return address_to_return

    # Función para sacar un pais random de un fichero JSON que he sacado de GitHub
    # https://gist.github.com/keeguon/2310008
    def __get_random_country():
        countries = __json.load(open('JSON/countries.json'))
        countries_names = []
        for country in countries:
            countries_names.append(country['name'])
        return __random.choice(countries_names)

    # Función para sacar un municipio random de un fichero JSON que he sacado de una api y le he dado formato 
    # (quitar una gran cantidad de datos con regex y dejar solo el nombre del municipio)
    def __get_random_town():
        towns = __json.load(open('JSON/municipios.json', encoding='utf8'))
        return __random.choice(towns)

    # Función que devuelve una tupla que contiene dos strings, una data_inici y una data_fi formato 'YYYY-MM-DD'
    def __get_random_start_end_dates():
        data_inici_yyyy = __random.randint(2010,2019) # Año inicio
        data_inici_mm = __random.randint(1,12) # Mes inicio
        max_data_inici_dd = __monthrange(data_inici_yyyy, data_inici_mm) # Función que devuelve una tupla (weekday, num of days)
        data_inici_dd = __random.randint(1,max_data_inici_dd[1]) # Día random entre 1 y max dias del mes
        data_inici = '{0}-{1}-{2}'.format(str(data_inici_yyyy), str(data_inici_mm), str(data_inici_dd)) # Creo la fecha inicio
        data_fi_yyyy, data_fi_mm, data_fi_dd = 1900,1,1 # Inicializo fecha_fin de tal manera que entre en el bucle (La solución más correcta es usar un dowhile pero no está en Python)
        while __datetime.datetime(data_inici_yyyy, data_inici_mm, data_inici_dd) > __datetime.datetime(data_fi_yyyy, data_fi_mm, data_fi_dd): # Si fecha_inicio > fecha_fin busca otra fecha_inicio
            data_fi_yyyy = __random.randint(2010,2018) # Año fin
            data_fi_mm = __random.randint(1,12) # Mes fin
            max_data_fi_dd = __monthrange(data_fi_yyyy, data_fi_mm) # Saco el ultimo dia del mes
            data_fi_dd = __random.randint(1,max_data_fi_dd[1]) # Día random entre 1 y max dias del mes
            data_fi = '{0}-{1}-{2}'.format(str(data_fi_yyyy), str(data_fi_mm), str(data_fi_dd)) # Creo la fecha fin
        data_inici_fi = (data_inici, data_fi) # Creo una tupla con ambas fechas
        return data_inici_fi # Devuelvo la tupla

    table = __random_table() # Selecciono tabla random
    if table == 'clients' : 
        client_id = __random.randint(27945, 100000) # Selecciono un valor random entre los valores permitidos por la DB
        nom = __get_random_name()
        cognom1 = __get_random_surname()
        sexe = __get_random_gender()
        data_naix = __get_random_born_day()
        pais_origen_id = __get_random_country_id()
        #insert_clients = 'INSERT INTO clients(client_id, nom, cognom1, sexe, data_naix, pais_origen_id) VALUES (' + str(client_id) + ', "' + nom + '", "' + cognom1 + '", "' + sexe + '", "' + str(data_naix) + '", ' + str(pais_origen_id) + ');'
        insert_clients = 'INSERT INTO clients(client_id, nom, cognom1, sexe, data_naix, pais_origen_id) VALUES ({0}, "{1}", "{2}", "{3}", "{4}", {5});'.format(str(client_id), nom,cognom1, sexe, str(data_naix), str(pais_origen_id))
        insert_a_ejecutar =  insert_clients
        
    elif table == 'habitacions' : 
        hab_id = __random.randint(32726,8388606)
        hotel_id = __random.randint(11,111)
        num_hab =  __random.randint(233,2333)
        insert_habitacions = 'INSERT INTO habitacions(hab_id, hotel_id, num_hab) VALUES ({0}, {1}, {2});'.format(str(hab_id), str(hotel_id), str(num_hab))
        insert_a_ejecutar = insert_habitacions
        
    elif table == 'hotels' : 
        hotel_id = __random.randint(340,32766)
        nom = __get_random_name() + ' hotel'
        categoria = __random.randint(1,5)
        habitacions = __random.randint(4,623)
        adreca = __get_random_address()
        poblacio_id = __random.randint(1,97)
        insert_hotels = 'INSERT INTO hotels(hotel_id, nom, categoria, habitacions, adreca, poblacio_id) VALUES ({0}, "{1}", {2}, {3}, "{4}", {5});'.format(str(hotel_id), nom, str(categoria), str(habitacions), adreca, str(poblacio_id))
        insert_a_ejecutar = insert_hotels

    elif table == 'paisos' : 
        pais_id = __random.randint(20,127)
        nom = __get_random_country()
        insert_paisos = 'INSERT INTO paisos(pais_id, nom) VALUES({0}, "{1}");'.format(str(pais_id), nom)
        insert_a_ejecutar = insert_paisos
        
    elif table == 'poblacions' : 
        poblacio_id = __random.randint(98,32766)
        nom = __get_random_town()
        insert_poblacions = 'INSERT INTO poblacions(poblacio_id, nom) VALUES({0}, "{1}");'.format(str(poblacio_id), nom)
        insert_a_ejecutar = insert_poblacions
        
    elif table == 'reserves' : 
        reserva_id = __random.randint(182536,1000000)
        hab_id = __random.randint(32726,8388607)
        data_inici_fi = __get_random_start_end_dates()
        data_inici = data_inici_fi[0]
        data_fi = data_inici_fi[1]
        client_id = __random.randint(10001,27944)
        insert_reserves = 'INSERT INTO reserves(reserva_id, hab_id, data_inici, data_fi, client_id) VALUES({0}, {1}, "{2}", "{3}", {4});'.format(str(reserva_id), str(hab_id), str(data_inici), str(data_fi), str(client_id))
        insert_a_ejecutar = insert_reserves
    
    print (insert_a_ejecutar) # Imprimo el insert por pantalla
    return insert_a_ejecutar # Devuelvo un único insert dependiendo del switch anterior

__format = '---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'

### Función que si le pasamos una conexión y un insert, lo ejecutará ###
def __execute_insert(established_connection,insert):
    try:
        with established_connection.cursor() as mycursor:
            print(__format)
            start_time = __time.time() # Comienzo del temporizador
            mycursor.execute(insert) # Ejecución del insert 
            established_connection.commit() # Commit 
            print("--- %s seconds ---" % (__time.time() - start_time)) # Tiempo de ejecución de la query 
            print('OK','\n', __format, '\n')

    except:
        print(__format, 'NOT OK', '\n', __format, '\n')

### Función para realizar un número de transacciones pasadas por parametro
def num_sql(established_connection, num_sql):
    print("ESTABLISHED CONNECTION")
    for num in range(num_sql): # Ejecuto el número de transacciones
        # Decido la transacción a realizar de manera aleatoria
        # 0 = Query     1 = Insert
        transaction_type = __random.randint(0, 1)
        if transaction_type == 0: # Query
            __execute_query_fetchall(established_connection, __random_query())
            
            # SI QUEREMOS MOSTRAR EL RESULTADO, DESCOMENTAR EL SIGUIENTE FRAGMENTO
            '''
            # Guardo el resultado de la Query en una variable para recorrerlo
            myresult = __execute_query_fetchall(established_connection, __random_query())
            # Muestro el resultado de la query por pantalla 
            __print_query_result(myresult)
            '''

        elif transaction_type == 1: # Insert
            __execute_insert(established_connection, __random_insert())
    
    established_connection.close() # Cierro la conexión
    print("CLOSED CONNECTION")
