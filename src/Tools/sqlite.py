import sqlite3
#import cfg


def query2dic(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d


#
#           Insert New Data
#

def save_new(userdata,type_,path2db = "../biblioteca/database/Main.db"):

	if type_=='book':
		query = "INSERT INTO libros ( isbn, autor, titulo, comentarios) VALUES ( ?, ?, ?, ?);"
	elif type_=='user':
		query = "INSERT INTO usuarios ( nombres, apellidos, rut, direccion, telefono, comentarios) VALUES ( ?, ?, ?, ?, ?, ?);"
	else:
		return False

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

def load_table(table, path2db = "../biblioteca/database/Main.db"):

	if table   =='libros':
		query  = "SELECT * FROM libros ;"
	elif table =='usuarios':
		query  = "SELECT * FROM usuarios ;"
	else:
		return False

	con              = sqlite3.connect(path2db)
	con.text_factory = str
	con.row_factory  = query2dic
	sth              = con.cursor()

	try:
		sth.execute(query)
	except sqlite3.Error as e:
		print e
		return False

	Result = sth.fetchall()
	con.close()
	return Result


def loanbook(idlibro,idusuario,desde_,hasta_, path2db = "../biblioteca/database/Main.db"):

	data =  [idlibro,idusuario,desde_,hasta_]

	query1 = "INSERT INTO prestamos ( id_libro , id_usuario, desde, hasta,retorno, comentarios) VALUES ( ?, ?, ?, ?,0,'');"
	query2 = "UPDATE libros SET estado = 0 WHERE id_libro = ? ;"
	query3 = "UPDATE usuarios SET prestamos = (prestamos+1) WHERE id_usuario = ? ;"

	con              = sqlite3.connect(path2db)
	con.text_factory = str
	con.row_factory  = query2dic
	sth              = con.cursor()

	try:
		sth.execute(query1,data)
	except sqlite3.Error as e:
		return False
	try:
		sth.execute(query2, [idlibro,])
	except sqlite3.Error as e:
		return False
	try:
		sth.execute(query3, [idusuario,])
	except sqlite3.Error as e:
		return False

	con.commit()
	con.close()
	return True

