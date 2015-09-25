UPDATE users SET status     = abs(random()) % 2  where 1;
UPDATE users SET comments   = 'Comentatios- ' ||userID where 1;
UPDATE users SET address    = 'Direccion- ' ||userID where 1;
UPDATE users SET IDN        = ((1000000+abs(random() %10000000))||('-'||userID%10)) where 1;
UPDATE users SET phone      = 1000000+abs(random()%8000000) where 1;
UPDATE users SET cellphone  = 10000000+abs(random()%80000000) where 1;
UPDATE users SET familyname = 'Apellido- ' ||userID where 1;
UPDATE users SET name       = 'Nombre- ' ||userID where 1;
UPDATE users SET role       = 'ST' where 1;
UPDATE users SET email      = 'a@a.com' where 1;
UPDATE users SET grade      = 1+abs(random()%11) where 1;


UPDATE items SET ISBN      = 'isbn- '||(abs(random()) % 100+itemID) where itemID>4;
UPDATE items SET author    = 'Autor- ' ||itemID where itemID>4;
UPDATE items SET title     = 'Titulo- ' ||itemID where itemID>4;
UPDATE items SET publisher = 'publiher- ' ||itemID where itemID>4;
UPDATE items SET year      = 1700+abs(random()%315) where itemID>4;
UPDATE items SET coments   = 'Comentatios- ' ||itemID where itemID>4;
UPDATE items SET lang   = 'spa' where itemID>4;

UPDATE loans SET userID     =  abs(random()) % 4095 where 1;
UPDATE loans SET comments   = 'Comentatios- ' ||loanID where 1;
UPDATE loans SET loanDate   = (20150000+abs(random() %500)+10    +abs(random()% 28))  where 1;
UPDATE loans SET dueDate    = (20150000+abs(random() %500)+60+abs(random()% 27))  where 1;
UPDATE loans SET returnDate = (20150000+abs(random() %500)+60+abs(random()% 27))  where 1;

