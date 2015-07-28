/*
Contiene todos los libros en existencia
llave: id_libro unica para cada libro
*/
CREATE TABLE "main"."libros" (
    "id_libro" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "isbn" TEXT NOT NULL DEFAULT ('-'),
    "autor" TEXT NOT NULL DEFAULT ('-'),
    "titulo" TEXT NOT NULL DEFAULT ('-'),
    "comentarios" TEXT
);

/*
contiene todos los usuarios registrados
llave: id_usuario
*/
CREATE TABLE "main"."usuarios" (
    "id_usuario" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "nombres" TEXT NOT NULL DEFAULT ('Nombre'),
    "apellidos" TEXT NOT NULL DEFAULT ('Apellidos'),
    "rut" TEXT NOT NULL DEFAULT ('-'),
    "email" TEXT NOT NULL DEFAULT ('a@a.com'),
    "direccion" TEXT NOT NULL DEFAULT ('-'),
    "telefono" TEXT NOT NULL DEFAULT ('-'),
    "grade" INTEGER DEFAULT (1),
    "estado" INTEGER DEFAULT (1),
    "comentarios" TEXT
);


/*
Contiene los prestamos activos
llave: id_prestamo
*/
CREATE TABLE prestamos (
    "id_prestamo" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "id_libro" INTEGER NOT NULL,
    "id_usuario" INTEGER NOT NULL,
    "desde" INTEGER NOT NULL,
    "hasta" INTEGER NOT NULL,
    "comentarios" TEXT,
    "estado" INTEGER DEFAULT (1)
);
/*
Contiene el historial prestamos realizados
llave: id_prestamo
*/
CREATE TABLE historial (
    "id_prestamo" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "id_libro" INTEGER NOT NULL,
    "id_usuario" INTEGER NOT NULL,
    "desde" INTEGER NOT NULL,
    "hasta" INTEGER NOT NULL,
    "retorno" INTEGER NOT NULL,
    "comentarios" TEXT,
    "estado" INTEGER DEFAULT (1)
);
