from main import db
from .subscribers import *
from .adm import *
class Properties(db.Model):
    __bind_key__ = 'admin_db'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(40), nullable = False)
    fecha_publicacion = db.Column(db.String(10), nullable = False)
    #cargar en us$ o en $ y usar CurrencyConverter para cargar el otro
    precio_dolares = db.Column(db.Integer)
    precio_pesos = db.Column(db.Integer)
    barrio_id = db.Column(db.Integer,db.ForeignKey('barrios.id'), nullable = False)
    operacion_id = db.Column(db.Integer,db.ForeignKey('operaciones.id'), nullable = False)
    tipo_propiedad_id = db.Column(db.Integer,db.ForeignKey('tipo_propiedad.id'), nullable = False)
    metraje_edificio = db.Column(db.Integer, nullable = False)
    metraje_patio = db.Column(db.Integer)
    #agregar un trigger para autosuma de metrajes
    metraje_total = db.Column(db.Integer, nullable = False)
    ref = db.Column(db.String(5), nullable = False,unique = True)
    baños = db.Column(db.String(2), nullable = False)
    dormitorios = db.Column(db.String(2), nullable = False)
    permuta = db.Column(db.Boolean)
    financia = db.Column(db.Boolean)
    garaje = db.Column(db.String(2), nullable = False)
    estado = db.Column(db.String(30))
    sobre = db.Column(db.String(30))
    orientacion = db.Column(db.String(1), nullable = False)
    ######
    n_plantas = db.Column(db.String(2))
    destacado = db.Column(db.Boolean)
    pausado = db.Column(db.Boolean)
    ######
    disposicion = db.Column(db.String(30), nullable = False)
    ######
    distancia_al_mar = db.Column(db.Integer)
    descripcion = db.Column(db.String(600), nullable = False)
    direccion = db.Column(db.String(30))
    propietario_id = db.Column(db.Integer, db.ForeignKey('propietarios.id'), nullable = False)
    #phone = db.Column(db.Integer, nullable = False, unique = True)
    propietario = db.relationship('Propietarios',backref='properties',lazy = 'joined')
    operaciones = db.relationship('Operaciones',backref='properties',lazy = 'joined')
    tipo_propiedad = db.relationship('Tipo_propiedad',backref='properties',lazy = 'joined')
    barrio = db.relationship('Barrios',backref='properties',lazy = 'joined')

class Propietarios(db.Model):
    __bind_key__ = 'admin_db'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(40), nullable = False)
    apellido = db.Column(db.String(40), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    telefono = db.Column(db.Integer, nullable = False, unique = True)

class Barrios(db.Model):
    __bind_key__ = 'admin_db'
    id = db.Column(db.Integer, primary_key=True)
    barrio = db.Column(db.String(60), nullable = False, unique = True)

class Operaciones(db.Model):
    __bind_key__ = 'admin_db'
    id = db.Column(db.Integer, primary_key=True)
    operacion = db.Column(db.String(10), nullable = False, unique = True)
   


class Tipo_propiedad(db.Model):
    __bind_key__ = 'admin_db'
    id = db.Column(db.Integer, primary_key=True)
    tipo_propiedad = db.Column(db.String(30), nullable = False, unique = True)

class Seguridad(db.Model):
    __bind_key__ = 'admin_db'
    id = db.Column(db.Integer,db.ForeignKey('properties.id'), primary_key = True, autoincrement=True)
    alarma = db.Column(db.Boolean)
    cámaras_cctv = db.Column(db.Boolean)
    cerca_perimetral = db.Column(db.Boolean)
    portería_24hs = db.Column(db.Boolean)
    portón_eléctrico = db.Column(db.Boolean)
    rejas = db.Column(db.Boolean)
    guardia_de_seguridad = db.Column(db.Boolean)
    propiedad = db.relationship('Properties',backref='seguridad',lazy = 'select')

class Comfort(db.Model):
    __bind_key__ = 'admin_db'
    id = db.Column(db.Integer,db.ForeignKey('properties.id'), primary_key = True, autoincrement=True)
    agua_caliente = db.Column(db.Boolean)
    aire_acondicionado = db.Column(db.Boolean)
    altillo = db.Column(db.Boolean)
    amueblada = db.Column(db.Boolean)
    balcón = db.Column(db.Boolean)
    barbacoa = db.Column(db.Boolean)
    box = db.Column(db.Boolean)
    bungalow = db.Column(db.Boolean)
    calefacción = db.Column(db.Boolean)
    depósito = db.Column(db.Boolean)
    dormitorio_de_servicio = db.Column(db.Boolean)
    estufa_leña = db.Column(db.Boolean)
    garaje = db.Column(db.Boolean)
    gas_por_cañería = db.Column(db.Boolean)
    gym = db.Column(db.Boolean)
    instalación_de_tv_cable = db.Column(db.Boolean)
    jacuzzi = db.Column(db.Boolean)
    jardín = db.Column(db.Boolean)
    lavadero = db.Column(db.Boolean)
    lavandería = db.Column(db.Boolean)
    linea_blanca = db.Column(db.Boolean)
    living_comedor = db.Column(db.Boolean)
    losa_radiante = db.Column(db.Boolean)
    parrillero = db.Column(db.Boolean)
    patio = db.Column(db.Boolean)
    piscina = db.Column(db.Boolean)
    piso_porcelanato = db.Column(db.Boolean)
    placard_en_la_cocina = db.Column(db.Boolean)
    placard_en_dormitorio = db.Column(db.Boolean)
    playroom = db.Column(db.Boolean)
    previsión_aa = db.Column(db.Boolean)
    sauna = db.Column(db.Boolean)
    sótano = db.Column(db.Boolean)
    terraza = db.Column(db.Boolean)
    terraza_lavadero = db.Column(db.Boolean)
    vestidor = db.Column(db.Boolean)
    vista_al_mar = db.Column(db.Boolean)
    walkin_closet = db.Column(db.Boolean)
    wifi = db.Column(db.Boolean)
    propiedad = db.relationship('Properties',backref='comfort',lazy = 'select')

# db.drop_all()
# db.create_all()

# array = ('Aguada','Aires Puros','Arroyo Seco','Atahualpa','Bañados de Carrasco','Barra de Carrasco','Barrio Sur','Bella Italia','Bella Vista','Belvedere','Bolivar','Brazo Oriental','Buceo','Camino Maldonado','Capurro','Capurro Bella Vista','Carrasco','Carrasco Barrios con seguridad privada','Carrasco Este','Carrasco Norte','Casabó','Casabó Pajas Blancas','Casavalle','Centro','Cerrito','Cerro','Ciudad Vieja','Colón','Conciliación','Cordón','Flor de maroñas','Goes','Golf','Ituzango','Jacinto Vera','Jardines del Hipódromo','La Blanqueada','La Caleta','La Colorada','La Comercial','La Figurita ','La Paloma Tomkinson','La Teja','Larrañaga','Las Acacias','Las Canteras','Lezica','Malvín ','Malvín Norte','Manga ','Marconi','Maroñas','Melilla','Mercado Modelo','Montevideo (en general)','Nuevo Paris','Pajas Blancas','Palermo','Parque Batlle','Parque Miramar','Parque Rodó','Paso de la Arena','Paso Molino','Peñarol','Peñarol Lavalleja','Perez Castellanos ','Piedras Blancas','Pocitos','Pocitos Nuevo','Prado','Prado Nueva Savona','Puerto','Puerto Buceo','Punta Carretas','Punta Espinillo','Punta Gorda','Punta de Rieles','Reducto','Santiago Vazquez','Sayago','Tres Cruces','Tres Ombues','Unión','Villa Biattitz','Villa Dolores','Villa Española','Villa Garcia Manga Rural','Villa Muñoz','Zona Rural')
# operaciones = ('Venta','Alquiler')
# tipo_propiedad = ('Casa','Apartamento','Oficina')

# for arr in array:
#    caca = Barrios(barrio = arr)
#    db.session.add(caca)
#    db.session.commit()

# for arr in operaciones:
#    caca = Operaciones(operacion = arr)
#    db.session.add(caca)
#    db.session.commit()

# for arr in tipo_propiedad:
#    caca = Tipo_propiedad(tipo_propiedad = arr)
#    db.session.add(caca)
#    db.session.commit()
