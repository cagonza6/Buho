UPDATE usuarios SET estado= abs(random()) % 2  where 1;
UPDATE usuarios SET comentarios= 'Comentatios- ' ||id_usuario where 1;
UPDATE usuarios SET direccion= 'Direccion- ' ||id_usuario where 1;
UPDATE usuarios SET rut= 'Rut- ' ||id_usuario where 1;
UPDATE usuarios SET apellidos= 'Apellido- ' ||id_usuario where 1;
UPDATE usuarios SET nombres= 'Nombre- ' ||id_usuario where 1;
UPDATE usuarios SET email= 'a@a.com' where 1;


UPDATE libros SET isbn   = 'isbn- '||(abs(random()) % 100+id_libro) where 1;
UPDATE libros SET autor  = 'Autor- ' ||id_libro where 1;
UPDATE libros SET titulo = 'Titulo- ' ||id_libro where 1;
UPDATE libros SET comentarios= 'Comentatios- ' ||id_libro where 1;


UPDATE prestamos SET id_usuario = abs(random()) % 4095 where 1;
UPDATE prestamos SET comentarios= 'Comentatios- ' ||id_prestamo where 1;
UPDATE prestamos SET desde      = (201500000+abs(random() %500)+100    +abs(random()% 28))  where 1;
UPDATE prestamos SET hasta      = (201500000+abs(random() %500)+600+abs(random()% 27))  where 1;
UPDATE prestamos SET retorno    = (201500000+abs(random() %500)+600+abs(random()% 27))  where 1;


UPDATE prestamos SET retorno    = 1 where desde >hasta ;
UPDATE prestamos SET retorno    = 1 where retorno >hasta ;
UPDATE prestamos SET estado     = 1 where desde < hasta ;


