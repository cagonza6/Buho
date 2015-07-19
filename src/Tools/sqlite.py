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
		query  = "SELECT "
		query += "        libros.id_libro, libros.isbn, libros.autor, libros.titulo, libros.comentarios, "
		query += "        sum(prestamos.estado) as estado "
		query += "FROM libros "
		query += "LEFT OUTER JOIN prestamos "
		query += "        ON libros.id_libro = prestamos.id_libro "
		query += "group by libros.id_libro;"

	elif table =='usuarios':

		query  = "SELECT "
		query += "usuarios.id_usuario , usuarios.nombres , usuarios.apellidos , usuarios.rut , usuarios.direccion , usuarios.telefono , usuarios.estado , usuarios.comentarios,	count(prestamos.estado) as prestamos "
		query += "FROM usuarios "
		query += "LEFT OUTER JOIN prestamos ON usuarios.id_usuario = prestamos.id_usuario and prestamos.estado>0 "
		query += "group by usuarios.id_usuario; "

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

	data  =  [idlibro,idusuario,desde_,hasta_]
	query1 = "INSERT INTO prestamos ( id_libro , id_usuario, desde, hasta, comentarios) VALUES ( ?, ?, ?, ?, '');"
	query2 = "INSERT INTO historial ( id_libro , id_usuario, desde, hasta,retorno, comentarios) VALUES ( ?, ?, ?, ?,0,'');"

	con              = sqlite3.connect(path2db)
	con.text_factory = str
	con.row_factory  = query2dic
	sth              = con.cursor()

	try:
		sth.execute(query1,data)
		sth.execute(query2,data)
	except sqlite3.Error as e:
		Result = sth.fetchall()
		print "Fail al registrar pedido",Result
		print e
		return False

	con.commit()
	con.close()
	return True

def returnbook(idlibro,retorno, path2db = "../biblioteca/database/Main.db"):

#	Con esto sabremos cual es la ID del prestamo que se esta utilizando
	data0  =  [idlibro,]
	query0 = "SELECT id_prestamo FROM prestamos WHERE id_libro= ? LIMIT 1;"

#	Elimina de los prestamos activos el libro en cuestion
	data1  =  [idlibro,]
	query1 = "DELETE FROM prestamos WHERE id_libro= ?;"

#	actualiza la fecha de la devolucion en el historial y cierra el prestamo
#   data2 se genera a partir de la primera query, ver llamado a query3
	query2 = "UPDATE historial set estado = 0, retorno = ? WHERE id_prestamo= ? and id_libro = ?; "

	con              = sqlite3.connect(path2db)
	con.text_factory = str
	con.row_factory  = query2dic
	sth              = con.cursor()

	try:
		sth.execute(query0,data0)
		Result = sth.fetchone()
		idPrestamo = Result['id_prestamo']
		print idPrestamo
		sth.execute(query1,data1)
		data1  =  [idlibro,]

		data2  =  [retorno,idPrestamo,idlibro]
		sth.execute(query2,data2)
	except sqlite3.Error as e:
		print e
		return False


	con.commit()
	con.close()
	return True


def loadprestamo(idlibro,idusuario, path2db = "../biblioteca/database/Main.db"):

	data =  [idlibro,idusuario,desde_,hasta_]

	query1 = "Select id_prestamo,id_libro, id_usuario FROM prestamos WHERE id_libro = ? ;"

	con              = sqlite3.connect(path2db)
	con.text_factory = str
	con.row_factory  = query2dic
	sth              = con.cursor()

	try:
		sth.execute(query1,data)
		sth.execute(query2,data)
	except sqlite3.Error as e:
		return False

	con.commit()
	con.close()
	return True
