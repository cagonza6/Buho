import sqlite3
#import cfg


def query2dic(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

def saveuser(userdata,path2db = "../biblioteca/database/Main.db"):

	query = "INSERT INTO usuarios ( nombres, apellidos, rut, direccion, telefono, comentarios) VALUES ( ?, ?, ?, ?, ?, ?);"
	con              = sqlite3.connect(path2db)
	con.text_factory = str
	con.row_factory  = query2dic
	sth              = con.cursor()
	try:
		sth.execute(query,userdata)
	except sqlite3.Error as e:
		print e
		return False
	con.commit()
	Result = sth.fetchall()
	con.close()
	return True
