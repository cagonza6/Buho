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

/*
contiene los posibles cargos a ocupar por quienes
puedan pedir libros y los diferentes permisos de acceso (eventualmente)
Se llena al momento del registro.
Admin es el unico que pude registrar bibliotecarios.
*/
CREATE TABLE "main"."occupations" (
    "occupation_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "function_" text NOT NULL
);
INSERT INTO occupations (occupation_id, function_) VALUES (1,"Admin");
INSERT INTO occupations (occupation_id, function_) VALUES (2,"Bibliotecario(a)");
INSERT INTO occupations (occupation_id, function_) VALUES (3,"Profesor");
INSERT INTO occupations (occupation_id, function_) VALUES (4,"Estudiante");
INSERT INTO occupations (occupation_id, function_) VALUES (5,"Funcionario(a)");
INSERT INTO occupations (occupation_id, function_) VALUES (6,"Apoderado(a)");
INSERT INTO occupations (occupation_id, function_) VALUES (100,"Otro");

/*
Categorias de los items que pueden ser ingresados y prestados
Utiliza la misma clasificacion general de el sistema sibuc de la UC
*/
CREATE TABLE "main"."item_formats" (
    "format_id" text PRIMARY KEY NOT NULL,
    "format_name" text NOT NULL
);
INSERT INTO item_formats (format_id, format_name) VALUES ("BK","Libros");
INSERT INTO item_formats (format_id, format_name) VALUES ("SE","Revistas");
INSERT INTO item_formats (format_id, format_name) VALUES ("MU","Música (Incluye partituras, cassettes y CDs)");
INSERT INTO item_formats (format_id, format_name) VALUES ("MP","Mapas (Incluye planos)");
INSERT INTO item_formats (format_id, format_name) VALUES ("CF","Archivos (Incluye bases de datos en CD y en línea, diskettes)");
INSERT INTO item_formats (format_id, format_name) VALUES ("VM","Material Visual (Incluye DVD, videocassettes, CDs, diapositivas)");
INSERT INTO item_formats (format_id, format_name) VALUES ("MX","Material Mixto (Otros)");

/*
contiene los nombres de los idiomas en Iso, usables para clasificar.
Los idiomas mas comunes para hispanohablantes son los primeros de la lista
el resto viene posteriormente en orden alfabetico
*/
CREATE TABLE "main"."languages" (
    "isoname" text PRIMARY KEY NOT NULL,
    "lang" TEXT NOT NULL DEFAULT ('-')
);
INSERT INTO languages VALUES ("es","español - castellano");
INSERT INTO languages VALUES ("en","inglés");
INSERT INTO languages VALUES ("it","italiano");
INSERT INTO languages VALUES ("fr","francés");
INSERT INTO languages VALUES ("de","alemán");
INSERT INTO languages VALUES ("pt","portugués");
INSERT INTO languages VALUES ("la","latín");
INSERT INTO languages VALUES ("el","griego");
INSERT INTO languages VALUES ("aa","afar");
INSERT INTO languages VALUES ("ab","abjasio - abjasiano");
INSERT INTO languages VALUES ("ae","avéstico");
INSERT INTO languages VALUES ("af","afrikáans");
INSERT INTO languages VALUES ("ak","akano");
INSERT INTO languages VALUES ("am","amhárico");
INSERT INTO languages VALUES ("an","aragonés");
INSERT INTO languages VALUES ("ar","árabe");
INSERT INTO languages VALUES ("as","asamés");
INSERT INTO languages VALUES ("av","avar - ávaro");
INSERT INTO languages VALUES ("ay","aimara");
INSERT INTO languages VALUES ("az","azerí");
INSERT INTO languages VALUES ("ba","baskir");
INSERT INTO languages VALUES ("be","bielorruso");
INSERT INTO languages VALUES ("bg","búlgaro");
INSERT INTO languages VALUES ("bh","bhoyapurí");
INSERT INTO languages VALUES ("bi","bislama");
INSERT INTO languages VALUES ("bm","bambara");
INSERT INTO languages VALUES ("bn","bengalí");
INSERT INTO languages VALUES ("bo","tibetano");
INSERT INTO languages VALUES ("br","bretón");
INSERT INTO languages VALUES ("bs","bosnio");
INSERT INTO languages VALUES ("ca","catalán");
INSERT INTO languages VALUES ("ce","checheno");
INSERT INTO languages VALUES ("ch","chamorro");
INSERT INTO languages VALUES ("co","corso");
INSERT INTO languages VALUES ("cr","cree");
INSERT INTO languages VALUES ("cs","checo");
INSERT INTO languages VALUES ("cu","eslavo eclesiástico antiguo");
INSERT INTO languages VALUES ("cv","chuvasio");
INSERT INTO languages VALUES ("cy","galés");
INSERT INTO languages VALUES ("da","danés");
INSERT INTO languages VALUES ("dv","maldivo - dhivehi");
INSERT INTO languages VALUES ("dz","dzongkha");
INSERT INTO languages VALUES ("ee","ewé");
INSERT INTO languages VALUES ("eo","esperanto");
INSERT INTO languages VALUES ("et","estonio");
INSERT INTO languages VALUES ("eu","euskera");
INSERT INTO languages VALUES ("fa","persa");
INSERT INTO languages VALUES ("ff","fula");
INSERT INTO languages VALUES ("fi","finés - finlandés");
INSERT INTO languages VALUES ("fj","fiyiano - fiyi");
INSERT INTO languages VALUES ("fo","feroés");
INSERT INTO languages VALUES ("fy","frisón - frisio");
INSERT INTO languages VALUES ("ga","irlandés - gaélico");
INSERT INTO languages VALUES ("gd","gaélico escocés");
INSERT INTO languages VALUES ("gl","gallego");
INSERT INTO languages VALUES ("gn","guaraní");
INSERT INTO languages VALUES ("gu","guyaratí - guyaratí");
INSERT INTO languages VALUES ("gv","manés - gaélico manés o de Isla de Man");
INSERT INTO languages VALUES ("ha","hausa");
INSERT INTO languages VALUES ("he","hebreo");
INSERT INTO languages VALUES ("hi","hindi - hindú");
INSERT INTO languages VALUES ("ho","hiri motu");
INSERT INTO languages VALUES ("hr","croata");
INSERT INTO languages VALUES ("ht","haitiano");
INSERT INTO languages VALUES ("hu","húngaro");
INSERT INTO languages VALUES ("hy","armenio");
INSERT INTO languages VALUES ("hz","herero");
INSERT INTO languages VALUES ("ia","interlingua");
INSERT INTO languages VALUES ("id","indonesio");
INSERT INTO languages VALUES ("ie","occidental");
INSERT INTO languages VALUES ("ig","igbo");
INSERT INTO languages VALUES ("ii","yi de Sichuán");
INSERT INTO languages VALUES ("ik","iñupiaq");
INSERT INTO languages VALUES ("io","ido");
INSERT INTO languages VALUES ("is","islandés");
INSERT INTO languages VALUES ("iu","inuktitut - inuit");
INSERT INTO languages VALUES ("ja","japonés");
INSERT INTO languages VALUES ("jv","javanés");
INSERT INTO languages VALUES ("ka","georgiano");
INSERT INTO languages VALUES ("kg","kongo - kikongo");
INSERT INTO languages VALUES ("ki","kikuyu");
INSERT INTO languages VALUES ("kj","kuanyama");
INSERT INTO languages VALUES ("kk","kazajo - kazajio");
INSERT INTO languages VALUES ("kl","groenlandés - kalaallisut");
INSERT INTO languages VALUES ("km","camboyano - jemer");
INSERT INTO languages VALUES ("kn","canarés");
INSERT INTO languages VALUES ("ko","coreano");
INSERT INTO languages VALUES ("kr","kanuri");
INSERT INTO languages VALUES ("ks","cachemiro - cachemir");
INSERT INTO languages VALUES ("ku","kurdo");
INSERT INTO languages VALUES ("kv","komi");
INSERT INTO languages VALUES ("kw","córnico");
INSERT INTO languages VALUES ("ky","kirguís");
INSERT INTO languages VALUES ("lb","luxemburgués");
INSERT INTO languages VALUES ("lg","luganda");
INSERT INTO languages VALUES ("li","limburgués");
INSERT INTO languages VALUES ("ln","lingala");
INSERT INTO languages VALUES ("lo","lao");
INSERT INTO languages VALUES ("lt","lituano");
INSERT INTO languages VALUES ("lu","luba-katanga - chiluba");
INSERT INTO languages VALUES ("lv","letón");
INSERT INTO languages VALUES ("mg","malgache - malagasy");
INSERT INTO languages VALUES ("mh","marshalés");
INSERT INTO languages VALUES ("mi","maorí");
INSERT INTO languages VALUES ("mk","macedonio");
INSERT INTO languages VALUES ("ml","malayalam");
INSERT INTO languages VALUES ("mn","mongol");
INSERT INTO languages VALUES ("mr","maratí");
INSERT INTO languages VALUES ("ms","malayo");
INSERT INTO languages VALUES ("mt","maltés");
INSERT INTO languages VALUES ("my","birmano");
INSERT INTO languages VALUES ("na","nauruano");
INSERT INTO languages VALUES ("nb","noruego bokmål");
INSERT INTO languages VALUES ("nd","ndebele del norte");
INSERT INTO languages VALUES ("ne","nepalí");
INSERT INTO languages VALUES ("ng","ndonga");
INSERT INTO languages VALUES ("nl","neerlandés - holandés");
INSERT INTO languages VALUES ("nn","nynorsk");
INSERT INTO languages VALUES ("no","noruego");
INSERT INTO languages VALUES ("nr","ndebele del sur");
INSERT INTO languages VALUES ("nv","navajo");
INSERT INTO languages VALUES ("ny","chichewa");
INSERT INTO languages VALUES ("oc","occitano");
INSERT INTO languages VALUES ("oj","ojibwa");
INSERT INTO languages VALUES ("om","oromo");
INSERT INTO languages VALUES ("or","oriya");
INSERT INTO languages VALUES ("os","osético - osetio - oseta");
INSERT INTO languages VALUES ("pa","panyabí - penyabi");
INSERT INTO languages VALUES ("pi","pali");
INSERT INTO languages VALUES ("pl","polaco");
INSERT INTO languages VALUES ("ps","pastú - pastún - pashto");
INSERT INTO languages VALUES ("qu","quechua");
INSERT INTO languages VALUES ("rm","romanche");
INSERT INTO languages VALUES ("rn","kirundi");
INSERT INTO languages VALUES ("ro","rumano");
INSERT INTO languages VALUES ("ru","ruso");
INSERT INTO languages VALUES ("rw","ruandés - kiñaruanda");
INSERT INTO languages VALUES ("sa","sánscrito");
INSERT INTO languages VALUES ("sc","sardo");
INSERT INTO languages VALUES ("sd","sindhi");
INSERT INTO languages VALUES ("se","sami septentrional");
INSERT INTO languages VALUES ("sg","sango");
INSERT INTO languages VALUES ("si","cingalés");
INSERT INTO languages VALUES ("sk","eslovaco");
INSERT INTO languages VALUES ("sl","esloveno");
INSERT INTO languages VALUES ("sm","samoano");
INSERT INTO languages VALUES ("sn","shona");
INSERT INTO languages VALUES ("so","somalí");
INSERT INTO languages VALUES ("sq","albanés");
INSERT INTO languages VALUES ("sr","serbio");
INSERT INTO languages VALUES ("ss","suazi - swati - siSwati");
INSERT INTO languages VALUES ("st","sesotho");
INSERT INTO languages VALUES ("su","sundanés - sondanés");
INSERT INTO languages VALUES ("sv","sueco");
INSERT INTO languages VALUES ("sw","suajili");
INSERT INTO languages VALUES ("ta","tamil");
INSERT INTO languages VALUES ("te","télugu");
INSERT INTO languages VALUES ("tg","tayiko");
INSERT INTO languages VALUES ("th","tailandés");
INSERT INTO languages VALUES ("ti","tigriña");
INSERT INTO languages VALUES ("tk","turcomano");
INSERT INTO languages VALUES ("tl","tagalo");
INSERT INTO languages VALUES ("tn","setsuana");
INSERT INTO languages VALUES ("to","tongano");
INSERT INTO languages VALUES ("tr","turco");
INSERT INTO languages VALUES ("ts","tsonga");
INSERT INTO languages VALUES ("tt","tártaro");
INSERT INTO languages VALUES ("tw","twi");
INSERT INTO languages VALUES ("ty","tahitiano");
INSERT INTO languages VALUES ("ug","uigur");
INSERT INTO languages VALUES ("uk","ucraniano");
INSERT INTO languages VALUES ("ur","urdu");
INSERT INTO languages VALUES ("uz","uzbeko");
INSERT INTO languages VALUES ("ve","venda");
INSERT INTO languages VALUES ("vi","vietnamita");
INSERT INTO languages VALUES ("vo","volapük");
INSERT INTO languages VALUES ("wa","valón");
INSERT INTO languages VALUES ("wo","wolof");
INSERT INTO languages VALUES ("xh","xhosa");
INSERT INTO languages VALUES ("yi","yídish - yidis - yiddish");
INSERT INTO languages VALUES ("yo","yoruba");
INSERT INTO languages VALUES ("za","chuan - chuang - zhuang");
INSERT INTO languages VALUES ("zh","chino");
INSERT INTO languages VALUES ("zu","zulú");

