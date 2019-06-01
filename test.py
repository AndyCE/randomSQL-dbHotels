import myfunctions # Archivo que almacena las funciones

# Establecer conexión
myconnection = myfunctions.myConnection (
    host='192.168.162.3',
    user='asix', 
    passwd='patata', 
    #db='db_hotels' # Se puede cambiar o no definir, ya que tiene default value
)

myfunctions.num_sql(myconnection, 5) # Hago 5 transacciones
