import sqlite3
#import cfg


def query2dic(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

#
#    This class 
# source: http://stackoverflow.com/questions/4610791/can-i-put-my-sqlite-connection-and-cursor-in-a-function
class DatabaseManager(object):
	def __init__(self, db= "../biblioteca/database/Main.db"):
		self.conn = sqlite3.connect(db)
		self.conn.row_factory  = query2dic
		self.cur = self.conn.cursor()

	def __del__(self):
		self.conn.close()

	#
	#		   Insert New Data
	#

	def save_new(self,userdata,type_):

		if type_=='book':
			query = "INSERT INTO libros ( isbn, titulo, autor, comentarios) VALUES ( ?, ?, ?, ?);"
		elif type_=='user':
			query = "INSERT INTO usuarios ( nombres, apellidos, rut, direccion, telefono, comentarios) VALUES ( ?, ?, ?, ?, ?, ?);"
		else:
			return False

		try:
			self.cur.execute(query,userdata)
		except sqlite3.Error as e:
			return False
		self.conn.commit()
		return True

	def load_table(self,table):

		if table   =='libros':
			query  = "SELECT "
			query += "		libros.id_libro, libros.isbn, libros.autor, libros.titulo, libros.comentarios, prestamos.id_prestamo, "
			query += "		sum(prestamos.estado) as estado "
			query += "FROM libros "
			query += "LEFT OUTER JOIN prestamos "
			query += "		ON libros.id_libro = prestamos.id_libro "
			query += "group by libros.id_libro;"

		elif table =='usuarios':

			query  = "SELECT "
			query += "usuarios.id_usuario , usuarios.nombres , usuarios.apellidos , usuarios.rut , usuarios.direccion , usuarios.telefono , usuarios.estado , usuarios.comentarios,	count(prestamos.estado) as prestamos "
			query += "FROM usuarios "
			query += "LEFT OUTER JOIN prestamos ON usuarios.id_usuario = prestamos.id_usuario and prestamos.estado>0 "
			query += "group by usuarios.id_usuario; "


		else:
			return False

		try:
			self.cur.execute(query)
		except sqlite3.Error as e:

			return False
		self.Result = self.cur.fetchall()

		return self.Result

	def load_single_from_prestamos(self,table,id_):

		if table   =='libro':
			return False
		elif table =='usuario':

			query   = "SELECT  "
			query  += "		usuarios.id_usuario , usuarios.nombres , usuarios.apellidos , usuarios.rut , usuarios.direccion , "
			query  += "		usuarios.telefono , usuarios.estado , usuarios.comentarios, prestamos.id_prestamo, count(prestamos.estado) as prestamos, "
			query  += "		prestamos.desde,prestamos.hasta,prestamos.comentarios "
			query  += "FROM usuarios "
			query  += "LEFT OUTER JOIN prestamos ON usuarios.id_usuario = prestamos.id_usuario and prestamos.estado>0 "
			query  += "WHERE  prestamos.id_prestamo = ? "
			query  += "group by prestamos.id_usuario;"

		else:
			return False

		try:
			self.cur.execute(query,[id_,])
		except sqlite3.Error as e:

			return False
		if len (self.Result)>0:
			self.Result = self.cur.fetchall()[0]
			return self.Result
		return False

	def loanbook(self,idlibro,idusuario,desde_,hasta_):

		self.data  =  [idlibro,idusuario,desde_,hasta_]
		self.query1 = "INSERT INTO prestamos ( id_libro , id_usuario, desde, hasta, comentarios) VALUES ( ?, ?, ?, ?, '');"
		self.query2 = "INSERT INTO historial ( id_libro , id_usuario, desde, hasta,retorno, comentarios) VALUES ( ?, ?, ?, ?,0,'');"

		try:
			self.cur.execute(self.query1,self.data)
			self.cur.execute(self.query2,self.data)
		except sqlite3.Error as e:

			return False
		self.conn.commit()
		return True

	def returnbook(self,idprestamo,retorno, path2db = "../biblioteca/database/Main.db"):

	#	Elimina de los prestamos activos el libro en cuestion
		self.data1 =  [idprestamo,]
		self.query1 = "DELETE FROM prestamos WHERE id_prestamo= ?;"

		self.data2  =  [retorno,idprestamo]
		self.query2 = "UPDATE historial set estado = 0, retorno = ? WHERE id_prestamo= ? ; "

		try:
			self.cur.execute(self.query1,self.data1)
			self.cur.execute(self.query2,self.data2)
		except sqlite3.Error as e:

			return False
		self.conn.commit()
		return True

	#aun no usado ni implementado
	'''
	def loadprestamo(idlibro,idusuario, path2db = "../biblioteca/database/Main.db"):

		data =  [idlibro,idusuario,desde_,hasta_]

		query1 = "Select id_prestamo,id_libro, id_usuario FROM prestamos WHERE id_libro = ? ;"

		con			  = sqlite3.connect(path2db)
		con.text_factory = str
		con.row_factory  = query2dic
		self.cur			  = con.cursor()

		try:
			self.cur.execute(query1,data)
			self.cur.execute(query2,data)
		except sqlite3.Error as e:
			return False

		self.conn.commit()
		con.close()
		return True
	'''
