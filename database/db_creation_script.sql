/*
Contiene todos los libros en existencia
llave: id_libro unica para cada libro
*/
CREATE TABLE items (
    itemID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    format TEXT NOT NULL REFERENCES item_formats (formatID) ON UPDATE CASCADE DEFAULT 'BK',
    ISBN TEXT,
    title TEXT,
    author TEXT,
    publisher TEXT DEFAULT ('?') NOT NULL,
    year INTEGER NOT NULL DEFAULT (1980),
    lang TEXT NOT NULL DEFAULT ('spa') REFERENCES languages (langIsoID) ON UPDATE CASCADE,
    location TEXT,
    comements TEXT
);


/*
contiene todos los usuarios registrados
llave: id_usuario
*/
CREATE TABLE users (
    userID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    password TEXT NOT NULL DEFAULT ('secretpassword'),
    name TEXT NOT NULL DEFAULT ('name'),
    familyname TEXT NOT NULL DEFAULT ('familyname'),
    IDN TEXT NOT NULL DEFAULT ('0'),
    email TEXT NOT NULL DEFAULT ('a@a.com'),
    address TEXT NOT NULL,
    phone TEXT NOT NULL DEFAULT ('0'),
    cellphone TEXT NOT NULL DEFAULT ('0'),
    grade INTEGER DEFAULT (0) REFERENCES grades (gradeID) ON UPDATE CASCADE,
    status INTEGER DEFAULT (1),
    comments TEXT,
    role TEXT NOT NULL REFERENCES roles (roleID) ON UPDATE CASCADE NOT NULL
    );

/*
*
*
*/
CREATE TABLE grades (
    gradeID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    gradeName TEXT NOT NULL DEFAULT (' ')
);
INSERT INTO grades (gradeID, gradeName) VALUES (-1," ");
INSERT INTO grades (gradeID, gradeName) VALUES (1,"1ro");
INSERT INTO grades (gradeID, gradeName) VALUES (2,"2do");
INSERT INTO grades (gradeID, gradeName) VALUES (3,"3ro");
INSERT INTO grades (gradeID, gradeName) VALUES (4,"4to");
INSERT INTO grades (gradeID, gradeName) VALUES (5,"5to");
INSERT INTO grades (gradeID, gradeName) VALUES (6,"6to");
INSERT INTO grades (gradeID, gradeName) VALUES (7,"7mo");
INSERT INTO grades (gradeID, gradeName) VALUES (8,"8vo");
INSERT INTO grades (gradeID, gradeName) VALUES (9,"1M");
INSERT INTO grades (gradeID, gradeName) VALUES (10,"2M");
INSERT INTO grades (gradeID, gradeName) VALUES (11,"3M");
INSERT INTO grades (gradeID, gradeName) VALUES (12,"4M");
INSERT INTO grades (gradeID, gradeName) VALUES (13,"Kinder");
INSERT INTO grades (gradeID, gradeName) VALUES (14,"Pre-Kinder");

/*
Contiene los prestamos activos
llave: id_prestamo
*/
-- Describe LOANS
DROP TABLE if exists loans;
CREATE TABLE loans (
    loanID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    itemID INTEGER NOT NULL REFERENCES items (itemID) ON UPDATE CASCADE UNIQUE,
    userID INTEGER NOT NULL REFERENCES users (userID) ON UPDATE CASCADE,
    loanDate INTEGER NOT NULL,
    dueDate INTEGER NOT NULL,
    renewals INTEGER default(0)
);
/*
Contiene el historial prestamos realizados
llave: id_prestamo
*/
-- Describe HISTORY
DROP TABLE if exists history;
CREATE TABLE history (
   loanID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
   itemID INTEGER NOT NULL REFERENCES items (itemID) ON UPDATE CASCADE,
   userID INTEGER NOT NULL REFERENCES users (userID) ON UPDATE CASCADE,
   loanDate INTEGER NOT NULL,
   dueDate INTEGER NOT NULL,
   returnDate INTEGER default 0,
   renewals INTEGER default(0)
);

/*
contiene los posibles cargos a ocupar por quienes
puedan pedir libros y los diferentes permisos de acceso (eventualmente)
Se llena al momento del registro.
Admin es el unico que pude registrar bibliotecarios.
*/
CREATE TABLE roles (
    roleID text NOT NULL PRIMARY KEY UNIQUE,
    roleName text NOT NULL UNIQUE,
    roleHasGrade int
);

INSERT INTO roles (roleID, roleName,roleHasGrade) VALUES ("AM","Admin"            ,0);
INSERT INTO roles (roleID, roleName,roleHasGrade) VALUES ("LB","Bibliotecario(a)" ,0);
INSERT INTO roles (roleID, roleName,roleHasGrade) VALUES ("HP","Ayudante"         ,0);
INSERT INTO roles (roleID, roleName,roleHasGrade) VALUES ("TC","Profesor"         ,0);
INSERT INTO roles (roleID, roleName,roleHasGrade) VALUES ("ST","Estudiante"       ,1);
INSERT INTO roles (roleID, roleName,roleHasGrade) VALUES ("EY","Funcionario(a)"   ,0);
INSERT INTO roles (roleID, roleName,roleHasGrade) VALUES ("GD","Apoderado(a)"     ,1);
INSERT INTO roles (roleID, roleName,roleHasGrade) VALUES ("OT","Otro"             ,0);

/*
Categorias de los items que pueden ser ingresados y prestados
Utiliza la misma clasificacion general de el sistema sibuc de la UC
*/
CREATE TABLE item_formats (
    formatID text NOT NULL PRIMARY KEY UNIQUE,
    formatName text NOT NULL,
    formatNameShort text NOT NULL
    );

INSERT INTO item_formats (formatID, formatName, formatNameShort) VALUES ("BK","Libros","Libros");
INSERT INTO item_formats (formatID, formatName, formatNameShort) VALUES ("SE","Revistas","Revistas");
INSERT INTO item_formats (formatID, formatName, formatNameShort) VALUES ("MU","Música (Incluye partituras, cassettes y CDs)","Música");
INSERT INTO item_formats (formatID, formatName, formatNameShort) VALUES ("MP","Mapas (Incluye planos)","Mapas");
INSERT INTO item_formats (formatID, formatName, formatNameShort) VALUES ("CF","Archivos (Incluye bases de datos en CD y en línea, diskettes)","Archivos");
INSERT INTO item_formats (formatID, formatName, formatNameShort) VALUES ("VM","Material Visual (Incluye DVD, videocassettes, CDs, diapositivas)","Material Visual");
INSERT INTO item_formats (formatID, formatName, formatNameShort) VALUES ("MX","Material Mixto (Otros)","Otros");

/*
contiene los nombres de los idiomas en Iso, usables para clasificar.
Los idiomas mas comunes para hispanohablantes son los primeros de la lista
el resto viene posteriormente en orden alfabetico
*/
CREATE TABLE languages (
    langIsoID TEXT PRIMARY KEY NOT NULL UNIQUE,
    Part2B TEXT NOT NULL,
    Part2T TEXT NOT NULL DEFAULT ('-'),
    Part1 TEXT NOT NULL DEFAULT ('-'),
    Ref_Name TEXT NOT NULL DEFAULT ('-')
);

INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("aar","aar","aar","aa","Afar");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("abk","abk","abk","ab","Abkhazian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ace","ace","ace","","Achinese");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ach","ach","ach","","Acoli");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ada","ada","ada","","Adangme");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ady","ady","ady","","Adyghe");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("afh","afh","afh","af","Afrihili");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("afr","afr","afr","af","Afrikaans");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ain","ain","ain","ak","Ainu (Japan)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("aka","aka","aka","ak","Akan");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("akk","akk","akk","sq","Akkadian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("sqi","alb","sqi","sq","Albanian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ale","ale","ale","","Aleut");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("alt","alt","alt","am","Southern Altai");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("amh","amh","amh","am","Amharic");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ang","ang","ang","","Old English (ca. 450-1100)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("anp","anp","anp","ar","Angika");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ara","ara","ara","ar","Arabic");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("arc","arc","arc","an","Official Aramaic (700-300 BCE)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("arg","arg","arg","an","Aragonese");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("hye","arm","hye","hy","Armenian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("arn","arn","arn","","Mapudungun");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("arp","arp","arp","","Arapaho");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("arw","arw","arw","as","Arawak");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("asm","asm","asm","as","Assamese");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ast","ast","ast","av","Asturian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ava","ava","ava","av","Avaric");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ave","ave","ave","ae","Avestan");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("awa","awa","awa","ay","Awadhi");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("aym","aym","aym","ay","Aymara");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("aze","aze","aze","az","Azerbaijani");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("bak","bak","bak","ba","Bashkir");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("bal","bal","bal","bm","Baluchi");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("bam","bam","bam","bm","Bambara");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ban","ban","ban","eu","Balinese");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("eus","baq","eus","eu","Basque");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("bas","bas","bas","","Basa (Cameroon)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("bej","bej","bej","be","Beja");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("bel","bel","bel","be","Belarusian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("bem","bem","bem","bn","Bemba (Zambia)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ben","ben","ben","bn","Bengali");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("bho","bho","bho","","Bhojpuri");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("bik","bik","bik","","Bikol");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("bin","bin","bin","bi","Bini");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("bis","bis","bis","bi","Bislama");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("bla","bla","bla","bs","Siksika");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("bos","bos","bos","bs","Bosnian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("bra","bra","bra","br","Braj");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("bre","bre","bre","br","Breton");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("bua","bua","bua","","Buriat");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("bug","bug","bug","bg","Buginese");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("bul","bul","bul","bg","Bulgarian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mya","bur","mya","my","Burmese");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("byn","byn","byn","","Bilin");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("cad","cad","cad","","Caddo");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("car","car","car","ca","Galibi Carib");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("cat","cat","cat","ca","Catalan");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ceb","ceb","ceb","ch","Cebuano");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("cha","cha","cha","ch","Chamorro");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("chb","chb","chb","ce","Chibcha");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("che","che","che","ce","Chechen");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("chg","chg","chg","zh","Chagatai");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("zho","chi","zho","zh","Chinese");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("chk","chk","chk","","Chuukese");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("chm","chm","chm","","Mari (Russia)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("chn","chn","chn","","Chinook jargon");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("cho","cho","cho","","Choctaw");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("chp","chp","chp","","Chipewyan");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("chr","chr","chr","cu","Cherokee");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("chu","chu","chu","cu","Church Slavic");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("chv","chv","chv","cv","Chuvash");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("chy","chy","chy","","Cheyenne");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("cop","cop","cop","kw","Coptic");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("cor","cor","cor","kw","Cornish");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("cos","cos","cos","co","Corsican");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("cre","cre","cre","cr","Cree");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("crh","crh","crh","","Crimean Tatar");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("csb","csb","csb","cs","Kashubian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ces","cze","ces","cs","Czech");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("dak","dak","dak","da","Dakota");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("dan","dan","dan","da","Danish");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("dar","dar","dar","","Dargwa");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("del","del","del","","Delaware");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("den","den","den","","Slave (Athapascan)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("dgr","dgr","dgr","","Dogrib");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("din","din","din","dv","Dinka");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("div","div","div","dv","Dhivehi");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("doi","doi","doi","","Dogri (macrolanguage)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("dsb","dsb","dsb","","Lower Sorbian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("dua","dua","dua","","Duala");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("dum","dum","dum","nl","Middle Dutch (ca. 1050-1350)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("nld","dut","nld","nl","Dutch");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("dyu","dyu","dyu","dz","Dyula");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("dzo","dzo","dzo","dz","Dzongkha");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("efi","efi","efi","","Efik");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("egy","egy","egy","","Egyptian (Ancient)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("eka","eka","eka","","Ekajuk");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("elx","elx","elx","en","Elamite");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("eng","eng","eng","en","English");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("enm","enm","enm","eo","Middle English (1100-1500)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("epo","epo","epo","eo","Esperanto");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("est","est","est","et","Estonian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ewe","ewe","ewe","ee","Ewe");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ewo","ewo","ewo","","Ewondo");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("fan","fan","fan","fo","Fang (Equatorial Guinea)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("fao","fao","fao","fo","Faroese");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("fat","fat","fat","fj","Fanti");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("fij","fij","fij","fj","Fijian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("fil","fil","fil","fi","Filipino");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("fin","fin","fin","fi","Finnish");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("fon","fon","fon","fr","Fon");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("fra","fre","fra","fr","French");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("frm","frm","frm","","Middle French (ca. 1400-1600)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("fro","fro","fro","","Old French (842-ca. 1400)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("frr","frr","frr","","Northern Frisian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("frs","frs","frs","fy","Eastern Frisian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("fry","fry","fry","fy","Western Frisian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ful","ful","ful","ff","Fulah");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("fur","fur","fur","","Friulian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("gaa","gaa","gaa","","Ga");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("gay","gay","gay","","Gayo");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("gba","gba","gba","ka","Gbaya");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kat","geo","kat","ka","Georgian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("deu","ger","deu","de","German");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("gez","gez","gez","","Geez");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("gil","gil","gil","gd","Gilbertese");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("gla","gla","gla","gd","Scottish Gaelic");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("gle","gle","gle","ga","Irish");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("glg","glg","glg","gl","Galician");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("glv","glv","glv","gv","Manx");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("gmh","gmh","gmh","","Middle High German (ca. 1050-1500)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("goh","goh","goh","","Old High German (ca. 750-1050)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("gon","gon","gon","","Gondi");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("gor","gor","gor","","Gorontalo");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("got","got","got","","Gothic");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("grb","grb","grb","","Grebo");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("grc","grc","grc","el","Ancient Greek (to 1453)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ell","gre","ell","el","Modern Greek (1453-)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("grn","grn","grn","gn","Guarani");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("gsw","gsw","gsw","gu","Swiss German");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("guj","guj","guj","gu","Gujarati");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("gwi","gwi","gwi","","Gwichʼin");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("hai","hai","hai","ht","Haida");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("hat","hat","hat","ht","Haitian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("hau","hau","hau","ha","Hausa");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("haw","haw","haw","he","Hawaiian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("heb","heb","heb","he","Hebrew");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("her","her","her","hz","Herero");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("hil","hil","hil","hi","Hiligaynon");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("hin","hin","hin","hi","Hindi");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("hit","hit","hit","","Hittite");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("hmn","hmn","hmn","ho","Hmong");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("hmo","hmo","hmo","ho","Hiri Motu");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("hrv","hrv","hrv","hr","Croatian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("hsb","hsb","hsb","hu","Upper Sorbian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("hun","hun","hun","hu","Hungarian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("hup","hup","hup","","Hupa");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("iba","iba","iba","ig","Iban");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ibo","ibo","ibo","ig","Igbo");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("isl","ice","isl","is","Icelandic");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ido","ido","ido","io","Ido");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("iii","iii","iii","ii","Sichuan Yi");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("iku","iku","iku","iu","Inuktitut");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ile","ile","ile","ie","Interlingue");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ilo","ilo","ilo","ia","Iloko");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ina","ina","ina","ia","Interlingua");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ind","ind","ind","id","Indonesian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("inh","inh","inh","ik","Ingush");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ipk","ipk","ipk","ik","Inupiaq");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ita","ita","ita","it","Italian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("jav","jav","jav","jv","Javanese");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("jbo","jbo","jbo","ja","Lojban");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("jpn","jpn","jpn","ja","Japanese");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("jpr","jpr","jpr","","Judeo-Persian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("jrb","jrb","jrb","","Judeo-Arabic");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kaa","kaa","kaa","","Kara-Kalpak");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kab","kab","kab","","Kabyle");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kac","kac","kac","kl","Kachin");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kal","kal","kal","kl","Kalaallisut");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kam","kam","kam","kn","Kamba (Kenya)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kan","kan","kan","kn","Kannada");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kas","kas","kas","ks","Kashmiri");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kau","kau","kau","kr","Kanuri");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kaw","kaw","kaw","kk","Kawi");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kaz","kaz","kaz","kk","Kazakh");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kbd","kbd","kbd","","Kabardian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kha","kha","kha","km","Khasi");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("khm","khm","khm","km","Central Khmer");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kho","kho","kho","ki","Khotanese");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kik","kik","kik","ki","Kikuyu");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kin","kin","kin","rw","Kinyarwanda");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kir","kir","kir","ky","Kirghiz");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kmb","kmb","kmb","","Kimbundu");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kok","kok","kok","kv","Konkani (macrolanguage)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kom","kom","kom","kv","Komi");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kon","kon","kon","kg","Kongo");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kor","kor","kor","ko","Korean");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kos","kos","kos","","Kosraean");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kpe","kpe","kpe","","Kpelle");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("krc","krc","krc","","Karachay-Balkar");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("krl","krl","krl","","Karelian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kru","kru","kru","kj","Kurukh");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kua","kua","kua","kj","Kuanyama");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kum","kum","kum","ku","Kumyk");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kur","kur","kur","ku","Kurdish");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("kut","kut","kut","","Kutenai");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("lad","lad","lad","","Ladino");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("lah","lah","lah","","Lahnda");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("lam","lam","lam","lo","Lamba");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("lao","lao","lao","lo","Lao");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("lat","lat","lat","la","Latin");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("lav","lav","lav","lv","Latvian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("lez","lez","lez","li","Lezghian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("lim","lim","lim","li","Limburgan");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("lin","lin","lin","ln","Lingala");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("lit","lit","lit","lt","Lithuanian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("lol","lol","lol","","Mongo");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("loz","loz","loz","lb","Lozi");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ltz","ltz","ltz","lb","Luxembourgish");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("lua","lua","lua","lu","Luba-Lulua");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("lub","lub","lub","lu","Luba-Katanga");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("lug","lug","lug","lg","Ganda");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("lui","lui","lui","","Luiseno");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("lun","lun","lun","","Lunda");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("luo","luo","luo","","Luo (Kenya and Tanzania)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("lus","lus","lus","mk","Lushai");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mkd","mac","mkd","mk","Macedonian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mad","mad","mad","","Madurese");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mag","mag","mag","mh","Magahi");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mah","mah","mah","mh","Marshallese");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mai","mai","mai","","Maithili");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mak","mak","mak","ml","Makasar");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mal","mal","mal","ml","Malayalam");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("man","man","man","mi","Mandingo");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mri","mao","mri","mi","Maori");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mar","mar","mar","mr","Marathi");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mas","mas","mas","ms","Masai");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("msa","may","msa","ms","Malay (macrolanguage)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mdf","mdf","mdf","","Moksha");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mdr","mdr","mdr","","Mandar");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("men","men","men","","Mende (Sierra Leone)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mga","mga","mga","","Middle Irish (900-1200)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mic","mic","mic","","Mi'kmaq");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("min","min","min","","Minangkabau");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mis","mis","mis","mg","Uncoded languages");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mlg","mlg","mlg","mg","Malagasy");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mlt","mlt","mlt","mt","Maltese");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mnc","mnc","mnc","","Manchu");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mni","mni","mni","","Manipuri");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("moh","moh","moh","mn","Mohawk");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mon","mon","mon","mn","Mongolian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mos","mos","mos","","Mossi");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mul","mul","mul","","Multiple languages");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mus","mus","mus","","Creek");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mwl","mwl","mwl","","Mirandese");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("mwr","mwr","mwr","","Marwari");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("myv","myv","myv","","Erzya");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("nap","nap","nap","na","Neapolitan");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("nau","nau","nau","na","Nauru");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("nav","nav","nav","nv","Navajo");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("nbl","nbl","nbl","nr","South Ndebele");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("nde","nde","nde","nd","North Ndebele");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ndo","ndo","ndo","ng","Ndonga");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("nds","nds","nds","ne","Low German");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("nep","nep","nep","ne","Nepali (macrolanguage)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("new","new","new","","Newari");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("nia","nia","nia","","Nias");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("niu","niu","niu","nn","Niuean");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("nno","nno","nno","nn","Norwegian Nynorsk");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("nob","nob","nob","nb","Norwegian Bokmål");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("nog","nog","nog","","Nogai");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("non","non","non","no","Old Norse");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("nor","nor","nor","no","Norwegian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("nqo","nqo","nqo","","N'Ko");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("nso","nso","nso","","Pedi");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("nwc","nwc","nwc","ny","Classical Newari");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("nya","nya","nya","ny","Nyanja");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("nym","nym","nym","","Nyamwezi");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("nyn","nyn","nyn","","Nyankole");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("nyo","nyo","nyo","","Nyoro");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("nzi","nzi","nzi","oc","Nzima");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("oci","oci","oci","oc","Occitan (post 1500)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("oji","oji","oji","oj","Ojibwa");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ori","ori","ori","or","Oriya (macrolanguage)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("orm","orm","orm","om","Oromo");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("osa","osa","osa","os","Osage");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("oss","oss","oss","os","Ossetian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ota","ota","ota","","Ottoman Turkish (1500-1928)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("pag","pag","pag","","Pangasinan");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("pal","pal","pal","","Pahlavi");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("pam","pam","pam","pa","Pampanga");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("pan","pan","pan","pa","Panjabi");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("pap","pap","pap","Part1","Papiamento");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("pau","pau","pau","","Palauan");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("peo","peo","peo","fa","Old Persian (ca. 600-400 B.C.)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("fas","per","fas","fa","Persian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("phn","phn","phn","pi","Phoenician");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("pli","pli","pli","pi","Pali");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("pol","pol","pol","pl","Polish");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("pon","pon","pon","pt","Pohnpeian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("por","por","por","pt","Portuguese");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("pro","pro","pro","ps","Old Provençal (to 1500)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("pus","pus","pus","ps","Pushto");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("que","que","que","qu","Quechua");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("raj","raj","raj","","Rajasthani");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("rap","rap","rap","","Rapanui");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("rar","rar","rar","rm","Rarotongan");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("roh","roh","roh","rm","Romansh");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("rom","rom","rom","ro","Romany");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ron","rum","ron","ro","Romanian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("run","run","run","rn","Rundi");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("rup","rup","rup","ru","Macedo-Romanian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("rus","rus","rus","ru","Russian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("sad","sad","sad","sg","Sandawe");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("sag","sag","sag","sg","Sango");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("sah","sah","sah","","Yakut");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("sam","sam","sam","sa","Samaritan Aramaic");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("san","san","san","sa","Sanskrit");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("sas","sas","sas","","Sasak");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("sat","sat","sat","","Santali");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("scn","scn","scn","","Sicilian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("sco","sco","sco","","Scots");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("sel","sel","sel","","Selkup");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("sga","sga","sga","","Old Irish (to 900)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("shn","shn","shn","","Shan");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("sid","sid","sid","si","Sidamo");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("sin","sin","sin","si","Sinhala");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("slk","slo","slk","sk","Slovak");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("slv","slv","slv","sl","Slovenian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("sma","sma","sma","se","Southern Sami");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("sme","sme","sme","se","Northern Sami");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("smj","smj","smj","","Lule Sami");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("smn","smn","smn","sm","Inari Sami");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("smo","smo","smo","sm","Samoan");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("sms","sms","sms","sn","Skolt Sami");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("sna","sna","sna","sn","Shona");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("snd","snd","snd","sd","Sindhi");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("snk","snk","snk","","Soninke");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("sog","sog","sog","so","Sogdian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("som","som","som","so","Somali");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("sot","sot","sot","st","Southern Sotho");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("spa","spa","spa","es","Spanish");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("srd","srd","srd","sc","Sardinian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("srn","srn","srn","sr","Sranan Tongo");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("srp","srp","srp","sr","Serbian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("srr","srr","srr","ss","Serer");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ssw","ssw","ssw","ss","Swati");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("suk","suk","suk","su","Sukuma");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("sun","sun","sun","su","Sundanese");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("sus","sus","sus","","Susu");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("sux","sux","sux","sw","Sumerian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("swa","swa","swa","sw","Swahili (macrolanguage)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("swe","swe","swe","sv","Swedish");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("syc","syc","syc","","Classical Syriac");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("syr","syr","syr","ty","Syriac");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tah","tah","tah","ty","Tahitian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tam","tam","tam","ta","Tamil");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tat","tat","tat","tt","Tatar");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tel","tel","tel","te","Telugu");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tem","tem","tem","","Timne");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ter","ter","ter","","Tereno");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tet","tet","tet","tg","Tetum");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tgk","tgk","tgk","tg","Tajik");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tgl","tgl","tgl","tl","Tagalog");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tha","tha","tha","th","Thai");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("bod","tib","bod","bo","Tibetan");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tig","tig","tig","ti","Tigre");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tir","tir","tir","ti","Tigrinya");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tiv","tiv","tiv","","Tiv");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tkl","tkl","tkl","","Tokelau");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tlh","tlh","tlh","","Klingon");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tli","tli","tli","","Tlingit");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tmh","tmh","tmh","","Tamashek");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tog","tog","tog","to","Tonga (Nyasa)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ton","ton","ton","to","Tonga (Tonga Islands)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tpi","tpi","tpi","","Tok Pisin");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tsi","tsi","tsi","tn","Tsimshian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tsn","tsn","tsn","tn","Tswana");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tso","tso","tso","ts","Tsonga");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tuk","tuk","tuk","tk","Turkmen"); 
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tum","tum","tum","tr","Tumbuka");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tur","tur","tur","tr","Turkish");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tvl","tvl","tvl","tw","Tuvalu");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("twi","twi","twi","tw","Twi");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("tyv","tyv","tyv","","Tuvinian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("udm","udm","udm","","Udmurt");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("uga","uga","uga","ug","Ugaritic");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("uig","uig","uig","ug","Uighur");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ukr","ukr","ukr","uk","Ukrainian");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("umb","umb","umb","","Umbundu");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("und","und","und","ur","Undetermined");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("urd","urd","urd","ur","Urdu");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("uzb","uzb","uzb","uz","Uzbek");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("vai","vai","vai","ve","Vai");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("ven","ven","ven","ve","Venda");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("vie","vie","vie","vi","Vietnamese");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("vol","vol","vol","vo","Volapük");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("vot","vot","vot","","Votic");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("wal","wal","wal","","Wolaytta");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("war","war","war","","Waray (Philippines)");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("was","was","was","cy","Washo");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("cym","wel","cym","cy","Welsh");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("wln","wln","wln","wa","Walloon");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("wol","wol","wol","wo","Wolof");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("xal","xal","xal","xh","Kalmyk");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("xho","xho","xho","xh","Xhosa");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("yao","yao","yao","","Yao");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("yap","yap","yap","yi","Yapese");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("yid","yid","yid","yi","Yiddish");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("yor","yor","yor","yo","Yoruba");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("zap","zap","zap","","Zapotec");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("zbl","zbl","zbl","","Blissymbols");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("zen","zen","zen","","Zenaga");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("zgh","zgh","zgh","za","Standard Moroccan Tamazight");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("zha","zha","zha","za","Zhuang");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("zul","zul","zul","zu","Zulu");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("zun","zun","zun","","Zuni");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("zxx","zxx","zxx","","No linguistic content");
INSERT INTO languages ("langIsoID","Part2B","Part2T","Part1","Ref_Name") VALUES ("zza","zza","zza","","Zaza");
