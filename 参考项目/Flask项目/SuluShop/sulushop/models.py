from sulushop import db

db.Model.metadata.reflect(db.engine)


class Usuario(db.Model):
    __table__ = db.Model.metadata.tables['usuario']

    def get_id(self):
        return unicode(self.id)

    def is_active(self):
        """True, as all users are active."""
        return True

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


class Carro(db.Model):
    __table__ = db.Model.metadata.tables['carro']


class Foto(db.Model):
    __table__ = db.Model.metadata.tables['foto']


class Producto(db.Model):
    __table__ = db.Model.metadata.tables['producto']


class FotoProducto(db.Model):
    __table__ = db.Model.metadata.tables['foto_producto']


class Lista(db.Model):
    __table__ = db.Model.metadata.tables['lista']


class Puntuacion(db.Model):
    __table__ = db.Model.metadata.tables['puntuacion']

