/*
Contiene todos los libros en existencia
llave: id_libro unica para cada libro
*/
CREATE TABLE "main"."libros" (
    "id_libro" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "isbn" TEXT NOT NULL DEFAULT ('-'),
    "autor" TEXT NOT NULL DEFAULT ('-'),
    "titulo" TEXT NOT NULL DEFAULT ('-'),
    "estado" INTEGER DEFAULT (1),
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
    "direccion" TEXT NOT NULL DEFAULT ('-'),
    "telefono" TEXT NOT NULL DEFAULT ('-'),
    "estado" INTEGER DEFAULT (1),
    "comentarios" TEXT
);


/*
Contiene los prestamos realizados
*/
-- Describe PRESTAMOS
CREATE TABLE prestamos (
    "id_prestamo" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "id_libro" INTEGER NOT NULL,
    "id_usuario" INTEGER NOT NULL,
    "desde" INTEGER NOT NULL,
    "hasta" INTEGER NOT NULL,
    "retorno" INTEGER NOT NULL,
    "comentarios" TEXT,
    "estado" INTEGER DEFAULT (1)
);
