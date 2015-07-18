UPDATE usuarios SET estado= abs(random()) % 2  where 1;
UPDATE usuarios SET comentarios= 'Comentatios- ' ||id_usuario where 1;
UPDATE usuarios SET direccion= 'Direccion- ' ||id_usuario where 1;
UPDATE usuarios SET rut= 'Rut- ' ||id_usuario where 1;
UPDATE usuarios SET apellidos= 'Apellido- ' ||id_usuario where 1;
UPDATE usuarios SET nombres= 'Nombre- ' ||id_usuario where 1;


UPDATE libros SET isbn   = 'isbn- '||(abs(random()) % 100+id_libro) where 1;
UPDATE libros SET autor  = 'Autor- ' ||id_libro where 1;
UPDATE libros SET titulo = 'Titulo- ' ||id_libro where 1;
UPDATE libros SET comentarios= 'Comentatios- ' ||id_libro where 1;
UPDATE libros SET estado = abs(random()) % 2  where 1;
