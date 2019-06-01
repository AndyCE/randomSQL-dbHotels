# randomSQL-dbHotels
Python script to create random sql transactions.
Used database:
#### [db_hotels](https://github.com/robertventura/databases/tree/master/db_hotels)

##### Modified schema:

```sql
ALTER TABLE reserves CHANGE COLUMN hab_id hab_id mediumint(8) unsigned DEFAULT NULL;
```

##### Basic usage example:

Connection (not using SSL) and 5 random SQL

```python
import myfunctions

myconnection = myfunctions.myConnection (
    host='192.168.162.3',
    user='asix', 
    passwd='patata', 
    #db='db_hotels' # Se puede cambiar o no definir, ya que tiene default value
)

myfunctions.num_sql(myconnection, 5)
```
##### Result:

![5 random SQL](https://github.com/AndyCE/randomSQL-dbHotels/blob/master/img/5SQL.png "5 random SQL")

