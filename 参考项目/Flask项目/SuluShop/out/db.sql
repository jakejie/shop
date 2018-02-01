CREATE database IF NOT EXISTS sulushop;
	use sulushop;

CREATE TABLE IF NOT EXISTS usuario(
  id int unsigned AUTO_INCREMENT PRIMARY key,
  nombre varchar(140) NOT null,
  apellidos varchar(140) not null,
  fecha_nacimiento varchar(140) not null,
  direccion varchar(140) not null,
  email varchar(140) not null,
  telefono varchar(20) not null,
  contrasena varchar(300) not null,
  imagen varchar(140)
);

CREATE TABLE IF NOT EXISTS producto(
  id int unsigned AUTO_INCREMENT PRIMARY key,
  nombre varchar(140) not null,
	nombreVendedor varchar(140) not null,
  precio double not null,
  puntuacion double,
  descripcion varchar(500) not null,
  detalles varchar(1500) not null
);

CREATE TABLE IF NOT EXISTS foto(
  id int unsigned primary key auto_increment,
  url varchar(140) not null,
  principal boolean
);

CREATE TABLE IF NOT EXISTS foto_producto(
	id int unsigned primary key auto_increment,
	id_foto int unsigned,
	index (id_foto),
	foreign key (id_foto) references foto (id)
		on delete cascade on update no action,
	id_producto int unsigned,
	index (id_producto),
	foreign key (id_producto)
		references producto (id)
		on delete cascade on update no action
);

CREATE TABLE IF NOT EXISTS comentario(
	id int unsigned primary key auto_increment,
	comentario varchar(500) not null,
	fecha date not null,
	id_usuario int unsigned,
	index (id_usuario),
	foreign key (id_usuario)
		references usuario (id)
		on delete cascade on update no action,
	id_producto int unsigned,
	index (id_producto),
	foreign key (id_producto)
		references producto (id)
		on delete cascade on update no action
);

CREATE TABLE IF NOT EXISTS puntuacion(
	id int unsigned primary key auto_increment,
	puntuacion int unsigned,
	id_usuario int unsigned,
	index (id_usuario),
	foreign key (id_usuario)
		references usuario (id)
		on delete cascade on update no action,
	id_producto int unsigned,
	index (id_producto),
	foreign key (id_producto)
		references producto (id)
		on delete cascade on update no action
);

CREATE TABLE IF NOT EXISTS carro(
	id int unsigned primary key auto_increment,
	cantidad int unsigned,
	id_usuario int unsigned,
	index (id_usuario),
	foreign key (id_usuario)
		references usuario (id)
		on delete cascade on update no action,
	id_producto int unsigned,
	index (id_producto),
	foreign key (id_producto)
		references producto (id)
		on delete cascade on update no action
);

CREATE TABLE IF NOT EXISTS lista(
	id int unsigned primary key auto_increment,
	accion varchar(60) not null,
	fecha date not null,
	precio double,
  cantidad int;
	id_usuario int unsigned,
	index (id_usuario),
	foreign key (id_usuario)
		references usuario (id)
		on delete cascade on update no action,
	id_producto int unsigned,
	index (id_producto),
	foreign key (id_producto)
		references producto (id)
		on delete cascade on update no action
);



