from flask import render_template,flash, request, url_for, redirect, session, abort, g
from functools import wraps
from main.models.adm import *
from main.models.properties import *
from main.models.subscribers import *
from main.propertyForm import SeguridadForm,ComfortForm,PropertyForm
from main import app
from datetime import date,timedelta
import logging
import os
import random
import io
import base64
import math
import shutil
from PIL import Image
import cProfile, pstats, io



def profile(fnc):

    """A decorator that uses cProfile to profile a function"""

    def inner(*args, **kwargs):

        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats(.5)
        with open('C:/Users/Santi/Desktop/Inmobiliaria/main/p_optimize.log.txt', 'w+') as f:
            f.write(str(date.today()) + f'/n' + s.getvalue())
        print(s.getvalue())
        return retval

    return inner

#logging.basicConfig(filename='p_optimize.log', level=logging.DEBUG)
# from flask_mail import Mail, Message

# mail_data = MainMail.query.first()
# if mail_data != None:
#     app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
#     app.config['MAIL_PORT'] = 25
#     app.config['MAIL_USE_TLS'] = True
#     app.config['MAIL_USERNAME'] = str(mail_data.mail)  # enter your email here
#     app.config['MAIL_DEFAULT_SENDER'] = str(mail_data.mail) # enter your email here
#     app.config['MAIL_PASSWORD'] = str(mail_data.mail_password) # enter your password here
# else:
#     app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
#     app.config['MAIL_PORT'] = 25
#     app.config['MAIL_USE_TLS'] = True
#     app.config['MAIL_USERNAME'] = 'nomail@gmail.com'  # enter your email here
#     app.config['MAIL_DEFAULT_SENDER'] = 'nomail@gmail.com' # enter your email here
#     app.config['MAIL_PASSWORD'] = 'xxxx' # enter your password here

# print(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])

# mail = Mail(app)

# def sort_imgs():
#     os.chdir(imgs_dir)
#     properties = os.listdir()
#     for f in properties:
#         os.chdir(imgs_dir + '/' + f)
#         imgs = os.listdir()
#         imgs.sort(key=lambda x: x[1:])
#         print(imgs)
# @app.before_request
# def caca():
#     sort_imgs()
imgs_dir = os.getcwd() + '/inmobiliaria3/main/static/imgs/'
buffer_dir = imgs_dir + 'buffer/'
def properties_mtx(properties, columns):
    print(imgs_dir)
    aux = []
    p_show = []
    for i,propiedad in enumerate(properties):
        foto = get_img(propiedad.ref)
        aux.append([propiedad,foto])
        #print((i+1)%columns)
        if ((i+1)%columns) == 0:
            p_show.append(aux)
            aux = []
    if aux != []:
        p_show.append(aux)
    #print(p_show[0])
    return p_show

def store_imgs(ref,imgs):
    os.chdir(imgs_dir)
    os.mkdir(ref)
    os.chdir(ref)
    print(os.getcwd())
    for i,img in enumerate(imgs):
        fext = img.filename.split('.')
        im = Image.open(img).save(str(i+1) + '.' + fext[-1],quality=15,optimize=True)
        im.close()
def add_imgs(path_ref,img):
    id = len(os.listdir(path_ref)) + 1
    im = Image.open(img)
    im.save(path_ref + '/' + str(id) + '.' + im.format,quality=15,optimize=True)
    im.close()

# def del_imgs(ref,id):
#     id = [int(i) for i in id]
#     id.sort()
#     f = []
#     f_aux = []
#     wrk_path = imgs_dir + ref + '/'
#     imgs = os.listdir(wrk_path)
#     imgs.sort(key=lambda x: x[1:])
#     imgs = imgs[id[0]-1:]
#     init_imgs = len(imgs)
#     print(init_imgs,imgs,id)
#     for j in range(init_imgs):
#         f.append(os.path.splitext(wrk_path + imgs[j]))
#         print(f)
#     for delete_offset,i in enumerate(id):
#         idx_mapping = i-id[0]-delete_offset
#         print(idx_mapping,f[idx_mapping][0])
#         init_imgs -= 1
#         os.remove(f[idx_mapping][0]+f[idx_mapping][1])
#         for j in range(idx_mapping,init_imgs):
#             os.rename(f[j+1][0] + f[j+1][1], f[j][0] + f[j+1][1])
#     return True
def sort(files):
    return sorted(files,key=lambda x: int(os.path.splitext(x)[0]))
def del_imgs(ref,id):
    path_ref = imgs_dir + ref + '/'
    file_list = sort(os.listdir(path_ref))
    print(file_list)
    os.remove(path_ref + file_list[id])
    new_file_list = sort(os.listdir(path_ref))
    new_file_list_lenght = len(new_file_list)
    if (new_file_list_lenght == id or new_file_list_lenght == 0):
        #Si el largo es ==id entonces id era el ultimo elemento,
        #si es igual a 0 no hay nada, en ninguno de los casos hay que hacer algo mas
        return True
    else:
        files_to_rename = new_file_list[id:]
        for f in files_to_rename:
            fname, fext = os.path.splitext(f)
            os.rename(path_ref + fname + fext, path_ref + str(int(fname) - 1) + fext)
        return True
def get_imgs(ref):
    prop_phs = []
    os.chdir(imgs_dir + ref)
    imgs = sort(os.listdir())
    for i in (img for i,img in enumerate(imgs) if i<15):
        with open(i,'rb') as ph:
            im = base64.b64encode(ph.read()).decode('utf-8')
        prop_phs.append(im)
    os.chdir(imgs_dir)
    return prop_phs

def get_img(ref):
    os.chdir(imgs_dir + ref +'/')
    imgs = os.listdir()
    print(imgs)
    if (len(imgs) > 0):
        ph = open(imgs[0],'rb')
        im = base64.b64encode(ph.read()).decode('utf-8')
        ph.close()
    else:
        os.chdir(imgs_dir)
        ph = open('default.png','rb')
        im = base64.b64encode(ph.read()).decode('utf-8')
        ph.close()
    return im
def is_number(num_input):
    try:
        float(num_input)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(num_input)
        return True
    except (TypeError, ValueError):
        pass
    return False

@app.before_request
def get_current_user():
    g.user = None
    username = session.get('username')
    if username is not None:
        g.user = username

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login_page', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
#ROUTES -------------------------------
def assign_properties_to_from(form,get_properties):
    form.nombre.data = get_properties.propietario.nombre
    form.apellido.data = get_properties.propietario.apellido
    form.email.data = get_properties.propietario.email
    form.telefono.data = get_properties.propietario.telefono
    form.barrio.data = get_properties.barrio.barrio
    form.destacado.data = get_properties.destacado
    form.operacion.data = get_properties.operaciones.operacion
    form.tipo_propiedad.data = get_properties.tipo_propiedad.tipo_propiedad
    form.titulo.data = get_properties.titulo
    form.direccion.data = get_properties.direccion
    form.permuta.data = get_properties.permuta
    form.financia.data = get_properties.financia
    form.ref.data = get_properties.ref
    form.distancia_al_mar.data = get_properties.distancia_al_mar
    form.descripcion.data = get_properties.descripcion
    form.precio_dolares.data = get_properties.precio_dolares
    form.precio_pesos.data = get_properties.precio_pesos
    form.metraje_edificio.data = get_properties.metraje_edificio
    form.metraje_patio.data = get_properties.metraje_patio
    form.baños.data = get_properties.baños
    form.dormitorios.data = get_properties.dormitorios
    form.permuta.data = get_properties.permuta
    form.financia.data = get_properties.financia
    form.garaje.data = get_properties.garaje
    form.estado.data = get_properties.estado
    form.orientacion.data = get_properties.orientacion
    form.disposicion.data = get_properties.disposicion
    form.n_plantas.data = get_properties.n_plantas
    form.comfort.agua_caliente.data = get_properties.comfort[0].agua_caliente
    form.comfort.aire_acondicionado.data = get_properties.comfort[0].aire_acondicionado
    form.comfort.altillo.data = get_properties.comfort[0].altillo
    form.comfort.amueblada.data = get_properties.comfort[0].amueblada
    form.comfort.balcón.data = get_properties.comfort[0].balcón
    form.comfort.barbacoa.data = get_properties.comfort[0].barbacoa
    form.comfort.box.data = get_properties.comfort[0].box
    form.comfort.bungalow.data = get_properties.comfort[0].bungalow
    form.comfort.calefacción.data = get_properties.comfort[0].calefacción
    form.comfort.depósito.data = get_properties.comfort[0].depósito
    form.comfort.dormitorio_de_servicio.data = get_properties.comfort[0].dormitorio_de_servicio
    form.comfort.estufa_leña.data = get_properties.comfort[0].estufa_leña
    form.comfort.garaje.data = get_properties.comfort[0].garaje
    form.comfort.gas_por_cañería.data = get_properties.comfort[0].gas_por_cañería
    form.comfort.gym.data = get_properties.comfort[0].gym
    form.comfort.instalación_de_tv_cable.data = get_properties.comfort[0].instalación_de_tv_cable
    form.comfort.jacuzzi.data = get_properties.comfort[0].jacuzzi
    form.comfort.jardín.data = get_properties.comfort[0].jardín
    form.comfort.lavadero.data = get_properties.comfort[0].lavadero
    form.comfort.lavandería.data = get_properties.comfort[0].lavandería
    form.comfort.linea_blanca.data = get_properties.comfort[0].linea_blanca
    form.comfort.living_comedor.data = get_properties.comfort[0].living_comedor
    form.comfort.losa_radiante.data = get_properties.comfort[0].losa_radiante
    form.comfort.parrillero.data = get_properties.comfort[0].parrillero
    form.comfort.patio.data = get_properties.comfort[0].patio
    form.comfort.piscina.data = get_properties.comfort[0].piscina
    form.comfort.piso_porcelanato.data = get_properties.comfort[0].piso_porcelanato
    form.comfort.placard_en_la_cocina.data = get_properties.comfort[0].placard_en_la_cocina
    form.comfort.placard_en_dormitorio.data = get_properties.comfort[0].placard_en_dormitorio
    form.comfort.playroom.data = get_properties.comfort[0].playroom
    form.comfort.previsión_aa.data = get_properties.comfort[0].previsión_aa
    form.comfort.sauna.data = get_properties.comfort[0].sauna
    form.comfort.sótano.data = get_properties.comfort[0].sótano
    form.comfort.terraza.data = get_properties.comfort[0].terraza
    form.comfort.terraza_lavadero.data = get_properties.comfort[0].terraza_lavadero
    form.comfort.vista_al_mar.data = get_properties.comfort[0].vista_al_mar
    form.comfort.vestidor.data = get_properties.comfort[0].vestidor
    form.comfort.walkin_closet.data = get_properties.comfort[0].walkin_closet
    form.comfort.wifi.data = get_properties.comfort[0].wifi
    form.seguridad.alarma.data = get_properties.seguridad[0].alarma
    form.seguridad.cámaras_cctv.data = get_properties.seguridad[0].cámaras_cctv
    form.seguridad.cerca_perimetral.data = get_properties.seguridad[0].cerca_perimetral
    form.seguridad.portería_24hs.data = get_properties.seguridad[0].portería_24hs
    form.seguridad.portón_eléctrico.data = get_properties.seguridad[0].portón_eléctrico
    form.seguridad.rejas.data = get_properties.seguridad[0].rejas
    form.seguridad.guardia_de_seguridad.data = get_properties.seguridad[0].guardia_de_seguridad
    return form
def assign_form_to_properties(get_property,form):
    barrio = Barrios.query.filter_by(barrio = form.data['barrio']).first()
    operacion = Operaciones.query.filter_by(operacion = form.data['operacion']).first()
    tipo_propiedad = Tipo_propiedad.query.filter_by(tipo_propiedad = form.data['tipo_propiedad']).first()
    get_property.destacado = form.data['destacado']
    get_property.ref = form.data['ref']
    get_property.propietario.nombre = form.data['nombre']
    get_property.propietario.apellido = form.data['apellido']
    get_property.propietario.email = form.data['email']
    get_property.propietario.telefono = form.data['telefono']
    get_property.operacion_id = operacion.id
    get_property.fecha_publicacion = date.today()
    get_property.tipo_propiedad_id = tipo_propiedad.id
    get_property.barrio_id = barrio.id
    get_property.titulo = form.data['titulo']
    get_property.direccion = form.data['direccion']
    get_property.descripcion = form.data['descripcion']
    get_property.precio_dolares = abs(form.data['precio_dolares']) if form.data['precio_dolares'] else None
    get_property.precio_pesos = abs(form.data['precio_pesos']) if form.data['precio_pesos'] else None
    get_property.metraje_edificio = form.data['metraje_edificio']
    get_property.metraje_patio = form.data['metraje_patio']
    get_property.metraje_total = form.data['metraje_edificio'] if form.data['metraje_patio'] is None else form.data['metraje_edificio'] + form.data['metraje_patio']
    get_property.baños = form.data['baños']
    get_property.dormitorios = form.data['dormitorios']
    get_property.permuta = form.data['permuta'] if form.data['permuta'] != 2 else None
    get_property.financia = form.data['financia'] if form.data['financia'] != 2 else None
    get_property.garaje = form.data['garaje']
    get_property.estado = form.data['estado']
    get_property.orientacion = form.data['orientacion']
    get_property.disposicion = form.data['disposicion']
    get_property.n_plantas = form.data['n_plantas']
    get_property.comfort[0].agua_caliente = form.comfort.data['agua_caliente']
    get_property.comfort[0].aire_acondicionado = form.comfort.data['aire_acondicionado']
    get_property.comfort[0].altillo = form.comfort.data['altillo']
    get_property.comfort[0].amueblada = form.comfort.data['amueblada']
    get_property.comfort[0].balcón = form.comfort.data['balcón']
    get_property.comfort[0].barbacoa = form.comfort.data['barbacoa']
    get_property.comfort[0].box = form.comfort.data['box']
    get_property.comfort[0].bungalow =form.comfort.data['bungalow']
    get_property.comfort[0].calefacción = form.comfort.data['calefacción']
    get_property.comfort[0].depósito = form.comfort.data['depósito']
    get_property.comfort[0].dormitorio_de_servicio = form.comfort.data['dormitorio_de_servicio']
    get_property.comfort[0].estufa_leña = form.comfort.data['estufa_leña']
    get_property.comfort[0].garaje = form.comfort.data['garaje']
    get_property.comfort[0].gas_por_cañería = form.comfort.data['gas_por_cañería']
    get_property.comfort[0].gym = form.comfort.data['gym']
    get_property.comfort[0].instalación_de_tv_cable = form.comfort.data['instalación_de_tv_cable']
    get_property.comfort[0].jacuzzi = form.comfort.data['jacuzzi']
    get_property.comfort[0].jardín = form.comfort.data['jardín']
    get_property.comfort[0].lavadero = form.comfort.data['lavadero']
    get_property.comfort[0].lavandería = form.comfort.data['lavandería']
    get_property.comfort[0].linea_blanca = form.comfort.data['linea_blanca']
    get_property.comfort[0].living_comedor = form.comfort.data['living_comedor']
    get_property.comfort[0].losa_radiante = form.comfort.data['losa_radiante']
    get_property.comfort[0].parrillero = form.comfort.data['parrillero']
    get_property.comfort[0].patio = form.comfort.data['patio']
    get_property.comfort[0].piscina = form.comfort.data['piscina']
    get_property.comfort[0].piso_porcelanato = form.comfort.data['piso_porcelanato']
    get_property.comfort[0].placard_en_la_cocina = form.comfort.data['placard_en_la_cocina']
    get_property.comfort[0].placard_en_dormitorio = form.comfort.data['placard_en_dormitorio']
    get_property.comfort[0].playroom = form.comfort.data['playroom']
    get_property.comfort[0].previsión_aa = form.comfort.data['previsión_aa']
    get_property.comfort[0].sauna = form.comfort.data['sauna']
    get_property.comfort[0].sótano = form.comfort.data['sótano']
    get_property.comfort[0].terraza = form.comfort.data['terraza']
    get_property.comfort[0].terraza_lavadero = form.comfort.data['terraza_lavadero']
    get_property.comfort[0].vestidor = form.comfort.data['vestidor']
    get_property.comfort[0].walkin_closet = form.comfort.data['walkin_closet']
    get_property.comfort[0].wifi = form.comfort.data['wifi']
    get_property.seguridad[0].alarma = form.seguridad.data['alarma']
    get_property.seguridad[0].cámaras_cctv = form.seguridad.data['cámaras_cctv']
    get_property.seguridad[0].cerca_perimetral = form.seguridad.data['cerca_perimetral']
    get_property.seguridad[0].portería_24hs = form.seguridad.data['portería_24hs']
    get_property.seguridad[0].portón_eléctrico = form.seguridad.data['portón_eléctrico']
    get_property.seguridad[0].rejas = form.seguridad.data['rejas']
    get_property.seguridad[0].guardia_de_seguridad = form.seguridad.data['guardia_de_seguridad']
def paginacion(page,step,id,prop_query):
    print(page,step,id)
    destacados_count = prop_query.filter(Properties.pausado == False,Properties.destacado == 1).count()
    if (step == 1):
        if ((page-1)*9 < destacados_count):
            get_properties = prop_query.filter(Properties.pausado == False,Properties.destacado == 1,Properties.id > id).limit(9).all()
            properties_count = len(get_properties)
            if (properties_count < 9):
                get_properties_left = prop_query.filter(Properties.pausado == False,Properties.destacado == 0).limit(9-properties_count).all()
                for propiedades in get_properties_left:
                    get_properties.append(propiedades)
            return get_properties
        elif ((page-1)*9 == destacados_count):
            get_properties = prop_query.filter(Properties.pausado == False,Properties.destacado == 0).limit(9).all()
            return get_properties
        else:
            get_properties = prop_query.filter(Properties.pausado == False,Properties.destacado == 0,Properties.id > id).limit(9).all()
            return get_properties
    else :
        if ((page*9)+1 > destacados_count):
            properties_count = prop_query.filter(Properties.pausado == False,Properties.destacado == 0,Properties.id < id).count()
            if (properties_count < 9):
                get_properties_left = prop_query.order_by().filter(Properties.pausado == False,Properties.destacado == 0,Properties.id < id).all()
                get_properties = prop_query.order_by(Properties.id.desc()).filter(Properties.pausado == False,Properties.destacado == 1).limit(9-properties_count).all()
                get_properties = get_properties[::-1]
                for propiedades in get_properties_left:
                    get_properties.append(propiedades)
            return get_properties
        elif ((page*9)+1 == destacados_count):
            get_properties = prop_query.order_by(Properties.id.desc()).filter(Properties.pausado == False,Properties.destacado == 1).limit(9).all()
            get_properties = get_properties[::-1]
            return get_properties
        else:
            get_properties = prop_query.filter(Properties.pausado == False,Properties.destacado == 1,Properties.id < id).limit(9).all()
            return get_properties

@app.route('/testfotos')
#@profile
def testfotos():
    files = os.listdir(imgs_dir)
    print(files)
    for f in files:
        if (not (f == 'default.png')):
            imgs = os.listdir(imgs_dir + f + '/')
            print(imgs)
            for img in imgs:
                im = Image.open(imgs_dir + f + '/' + img)
                im.save(imgs_dir + f + '/' + img,quality=15,optimize=True)
                im.close()
    return url_for('index')

@app.route('/')
#@profile
def index():
    barrios_query = Barrios.query.all()
    p_show = []
    aux = []
    i = 0
    get_properties = Properties.query.filter(Properties.pausado == False,Properties.destacado == 1).limit(9).all()
    properties_count = len(get_properties) if get_properties is not None else 0
    if (properties_count < 9):
        get_properties_left = Properties.query.filter(Properties.pausado == False,Properties.destacado == 0).limit(9-properties_count).all()
        for propiedades in get_properties_left:
            get_properties.append(propiedades)
    #print(get_properties)
    paginas = Properties.query.count()
    p_show = properties_mtx(get_properties,3)
    #print(p_show[0])
    paginas = math.ceil(int(paginas)/9) if paginas != '0' else 1
    return render_template('index-premium.html', barrios = barrios_query,
    get_properties = p_show, paginas = paginas, pagina = 1)

@app.route('/imgsPost', methods=['POST','GET'])
def imgPost():
    added_imgs = request.files.getlist('imgs')
    print(request.json , request.files.getlist('imgs'))
    added_imgs_count = len(added_imgs)
    print(added_imgs[0].filename)
    #Condicional por si el input no trae ninguna imagen
    if added_imgs_count <= 15:
        for img in added_imgs:
            add_imgs(buffer_dir,img)
        return "1"
    else:
        return "0"
@app.route('/imgsDelete/<int:id>', methods=['DELETE'])
def imgDelete(id):
    del_check = del_imgs('buffer',id)
    if del_check is None:
        return "0"
    return "1"

@app.route('/imgsPostUpdate/<string:ref>', methods=['POST','GET'])
def imgPostUpdate(ref):
    print(os.listdir(imgs_dir + ref + '/'))
    added_imgs = request.files.getlist('imgs')
    print(request.json , request.files.getlist('imgs'))
    added_imgs_count = len(added_imgs)
    print(added_imgs[0].filename)
    #Condicional por si el input no trae ninguna imagen
    if added_imgs_count <= 15:
        for img in added_imgs:
            add_imgs(imgs_dir + ref + '/',img)
        return "1"
    else:
        return "0"
@app.route('/imgsDeleteUpdate/<string:ref>/<int:id>', methods=['DELETE'])
def imgDeleteUpdate(ref,id):
    del_check = del_imgs(ref,id)
    print(os.listdir(imgs_dir + ref + '/'))
    if del_check is None:
        return "0"
    return "1"

@app.route('/page')
#@profile
def page():
    barrios_query = Barrios.query.all()
    p_show = []
    aux = []
    i = 0
    get_properties = Properties.query.filter(Properties.pausado == False,Properties.destacado == 1).limit(9).all()
    properties_count = len(get_properties) if get_properties is not None else 0
    if (properties_count < 9):
        get_properties_left = Properties.query.filter(Properties.pausado == False,Properties.destacado == 0).limit(9-properties_count).all()
        for propiedades in get_properties_left:
            get_properties.append(propiedades)
    #print(get_properties)
    paginas = Properties.query.count()
    p_show = properties_mtx(get_properties,3)
    #print(p_show[0])
    paginas = math.ceil(int(paginas)/9) if paginas != '0' else 1
    return render_template('index-premium-pag.html', barrios = barrios_query,
    get_properties = p_show, paginas = paginas, pagina = 1,operacion_title = "Todas las propiedades")

@app.route('/administrar')
def admin_redirect():
    return redirect(url_for('admin', section="home"))

@app.route('/<int:page>/<int:step>/<int:id>')
def index_paginas(page,step,id):
    print(page,step,id)
    p_search = False
    p_show = []
    aux = []
    barrios_query = Barrios.query.all()
    destacados_count = Properties.query.filter(Properties.pausado == False,Properties.destacado == 1).count()
    print(destacados_count)
    get_properties = paginacion(page,step,id,Properties.query)
    paginas = Properties.query.count()
    p_show = properties_mtx(get_properties,3)
    #print(p_show)
    paginas = math.ceil(int(paginas)/9) if paginas != '0' else 1
    print('                      ' , p_show[0][0][0].id)
    #if (id == paginas)
    return render_template('index-premium-pag.html',
    get_properties = p_show, barrios = barrios_query, pagina = page,
    paginas = paginas, p_search = p_search,operacion_title = "Todas las propiedades")

@app.route('/delete/<id>', methods=['GET'])
def delete(id):
    com_deletes = Comfort.query.filter_by(id = id).delete()
    sec_deletes = Seguridad.query.filter_by(id = id).delete()
    prop_ref = Properties.query.filter_by(id = id).with_entities(Properties.ref).first()
    print(prop_ref[0])
    p_deletes = Properties.query.filter_by(id = id).delete()
    shutil.rmtree(imgs_dir + prop_ref.ref)
    db.session.commit()
    return redirect(url_for('admin',section = 'home'))

@app.route('/paused/<id>', methods=['GET'])
def pause(id):
    prop = Properties.query.filter_by(id = id).first()
    if prop.pausado == True:
        prop.pausado = False
        db.session.commit()
        return redirect(url_for('admin',section = 'paused'))
    else:
        prop.pausado = True
        db.session.commit()
        return redirect(url_for('admin',section = 'home'))

@app.route('/p_search', methods=['POST', 'GET'])
def search_page():
    barrios_query = Barrios.query.all()
    querys = Properties.query
    errores = {}
    print('asdasdasd',request.form)
    currency = request.form['currency']
    precio_min = request.form['precio_min']
    precio_max = request.form['precio_max']
    metraje_min = request.form['metraje_min']
    metraje_max = request.form['metraje_max']

    if  request.form['ref'] != '':
        flag = True
        querys = querys.filter_by(ref = request.form['ref'])
    if request.form['dormitorios'] != '':
        flag = True
        querys = querys.filter_by(dormitorios = request.form['dormitorios'])
    if request.form['baños'] != '':
        flag = True
        querys = querys.filter_by(baños = request.form['baños'])
    if request.form['barrio'] != '':
        flag = True
        querys = querys.filter(Properties.barrio.has(barrio=request.form['barrio']))

    if request.form['operacion']:
        flag = True
        querys = querys.filter(Properties.operaciones.has(operacion=request.form['operacion']))
    if request.form['tipo_propiedad']:
        flag = True
        querys = querys.filter(Properties.tipo_propiedad.has(tipo_propiedad=request.form['tipo_propiedad']))

    #....PRECIOS QUERY & erroresHANDLING...........................
    query1 = querys
    if(currency == 'precio_dolares'):
        query_precio = False
        query_precio1 = False
        if precio_min != '':
            if not is_number(precio_min):
                errores["precio_min"] = "No es un numero"
            else:
                flag = True
                query_precio = True
                query1 = query1.filter(Properties.precio_dolares >= precio_min)
        if precio_max != '':
            if not is_number(precio_max):
                errores["precio_max"] = "No es un numero"
            else:
                flag = True
                query_precio1 = True
                query1 = query1.filter(Properties.precio_dolares <= precio_max)
        if query_precio and query_precio1 and precio_min > precio_max:
            query1 = querys
            errores["precio_min"] = "Diferencia invalida"
            errores["precio_max"] = "Diferencia invalida"
    else:
        query_precio = False
        query_precio1 = False
        if precio_min != '':
            query_precio = False
            if not is_number(precio_min):
                errores["precio_min"] = "No es un numero"
            else:
                flag = True
                query_precio = True
                query1 = query1.filter(Properties.precio_pesos >= precio_min)
        if precio_max != '':
            query_precio1 = False
            if not is_number(precio_max):
                errores["precio_max"] = "No es un numero"
            else:
                flag = True
                query_precio1 = True
                query1 = query1.filter(Properties.precio_pesos <= precio_max)
        if query_precio and query_precio1 and precio_min > precio_max:
            query1 = querys
            errores["precio_min"] = "Diferencia invalida"
            errores["precio_max"] = "Diferencia invalida"


    #....METRAJE QUERY & erroresHANDLING...........................
    query2 = query1
    query_metraje = False
    query_metraje1 = False
    if metraje_min != '':
        if not is_number(metraje_min):
            errores["metraje_min"] = "No es un numero"
        else:
            flag = True
            query_metraje = True
            query2 = query2.filter(Properties.metraje_edificio >= metraje_min)
    if metraje_max != '':
        if not is_number(metraje_max):
            errores["metraje_max"] = "No es un numero"
        else:
            flag = True
            query_metraje1 = True
            query2 = query2.filter(Properties.metraje_edificio <= metraje_max)

    if query_metraje and query_metraje1 and metraje_min > metraje_max:
        query2 = querys
        errores["metraje_min"] = "Diferencia invalida"
        errores["metraje_max"] = "Diferencia invalida"
    print(query2)
    search_results = query2 if flag==True else False
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%4', search_results)
    if (search_results):
        paginas = search_results.count()
        if(paginas == 0):
            flash("Sin resultados")
            return redirect(url_for('page'))
        get_properties = search_results.filter(Properties.pausado == False,Properties.destacado == 1).limit(9).all()
        properties_count = len(get_properties) if get_properties is not None else 0
        if (properties_count < 9):
            search_results_left = search_results.filter(Properties.pausado == False,Properties.destacado == 0).limit(9-properties_count).all()
            for propiedades in search_results_left:
                get_properties.append(propiedades)
        session['busqueda'] = request.form
    else:
        #p_show = Properties.query.limit(30).all()
        return redirect(url_for('page'))
    print(errores,[e for e in errores])
    print(get_properties)
    p_show = properties_mtx(get_properties,3)
    paginas = math.ceil(int(paginas)/9)
    return render_template('index-premium-pag.html', barrios = barrios_query,
    paginas = paginas, pagina = 1,
    get_properties=p_show, errores=errores, p_search = True)


@app.route('/p_search/<int:page>/<int:step>/<int:id>', methods=['POST', 'GET'])
def search(page,step,id):
    barrios_query = Barrios.query.all()
    querys = Properties.query
    flag = False
    errores = {}
    print('asdasdasd',session.get('busqueda'))
    currency = session.get('busqueda')['currency']
    precio_min = session.get('busqueda')['precio_min']
    precio_max = session.get('busqueda')['precio_max']
    metraje_min = session.get('busqueda')['metraje_min']
    metraje_max = session.get('busqueda')['metraje_max']
    if  session.get('busqueda')['ref'] != '':
        flag = True
        querys = querys.filter_by(ref = session.get('busqueda')['ref'])
    if session.get('busqueda')['dormitorios'] != '':
        flag = True
        querys = querys.filter_by(dormitorios = session.get('busqueda')['dormitorios'])
    if session.get('busqueda')['baños'] != '':
        flag = True
        querys = querys.filter_by(baños = session.get('busqueda')['baños'])
    if session.get('busqueda')['barrio'] != '':
        flag = True
        querys = querys.filter(Properties.barrio.has(barrio=session.get('busqueda')['barrio']))
    if session.get('busqueda')['operacion']:
        flag = True
        querys = querys.filter(Properties.operaciones.has(operacion=session.get('busqueda')['operacion']))
    if session.get('busqueda')['tipo_propiedad']:
        flag = True
        querys = querys.filter(Properties.tipo_propiedad.has(tipo_propiedad=session.get('busqueda')['tipo_propiedad']))
    #....PRECIOS QUERY & erroresHANDLING...........................
    query1 = querys
    if(currency == 'precio_dolares'):
        query_precio = False
        query_precio1 = False
        if precio_min != '':
            if not is_number(precio_min):
                errores["precio_min"] = "No es un numero"
            else:
                flag = True
                query_precio = True
                query1 = query1.filter(Properties.precio_dolares >= precio_min)
        if precio_max != '':
            if not is_number(precio_max):
                errores["precio_max"] = "No es un numero"
            else:
                flag = True
                query_precio1 = True
                query1 = query1.filter(Properties.precio_dolares <= precio_max)
        if query_precio and query_precio1 and precio_min > precio_max:
            query1 = querys
            errores["precio_min"] = "Diferencia invalida"
            errores["precio_max"] = "Diferencia invalida"
    else:
        query_precio = False
        query_precio1 = False
        if precio_min != '':
            if not is_number(precio_min):
                errores["precio_min"] = "No es un numero"
            else:
                flag = True
                query_precio = True
                query1 = query1.filter(Properties.precio_pesos >= precio_min)
        if precio_max != '':
            if not is_number(precio_max):
                errores["precio_max"] = "No es un numero"
            else:
                flag = True
                query_precio1 = True
                query1 = query1.filter(Properties.precio_pesos <= precio_max)
        if query_precio and query_precio1 and precio_min > precio_max:
            query1 = querys
            errores["precio_min"] = "Diferencia invalida"
            errores["precio_max"] = "Diferencia invalida"
    #....METRAJE QUERY & erroresHANDLING...........................
    query2 = query1
    query_metraje = False
    query_metraje1 = False
    if metraje_min != '':
        if not is_number(metraje_min):
            errores["metraje_min"] = "No es un numero"
        else:
            flag = True
            query_metraje = True
            query2 = query2.filter(Properties.metraje_edificio >= metraje_min)
    if metraje_max != '':
        if not is_number(metraje_max):
            errores["metraje_max"] = "No es un numero"
        else:
            flag = True
            query_metraje1 = True
            query2 = query2.filter(Properties.metraje_edificio <= metraje_max)

    if query_metraje and query_metraje1 and metraje_min > metraje_max:
        query2 = querys
        errores["metraje_min"] = "Diferencia invalida"
        errores["metraje_max"] = "Diferencia invalida"
    print(query2)
    search_results = query2 if flag==True else False
    if (search_results != False):
        paginas = search_results.count()
        if(paginas == 0):
            return redirect(url_for('page'))
        search_results = paginacion(page,step,id,search_results)
    else:
        return redirect(url_for('page'))
    print(errores,[e for e in errores])
    print(search_results)
    p_show = properties_mtx(search_results,3)
    paginas = math.ceil(int(paginas)/9)
    return render_template('index-premium-pag.html', barrios = barrios_query,
    paginas = paginas, pagina = page, get_properties=p_show,
    errores=errores, p_search = True)

@app.route('/admin-search', methods=['POST', 'GET'])
def admin_search():
    barrios_query = Barrios.query.all()
    querys = Properties.query
    flag = False
    errores = {}
    print('asdasdasd',request.form)
    currency = request.form['currency']
    precio_min = request.form['precio_min']
    precio_max = request.form['precio_max']
    metraje_min = request.form['metraje_min']
    metraje_max = request.form['metraje_max']
    if  request.form['ref'] != '':
        flag = True
        querys = querys.filter_by(ref = request.form['ref'])
    if request.form['dormitorios'] != '':
        flag = True
        querys = querys.filter_by(dormitorios = request.form['dormitorios'])
    if request.form['baños'] != '':
        flag = True
        querys = querys.filter_by(baños = request.form['baños'])
    if request.form['barrio'] != '':
        flag = True
        querys = querys.filter(Properties.barrio.has(barrio=request.form['barrio']))
    if request.form['operacion']:
        flag = True
        querys = querys.filter(Properties.operaciones.has(operacion=request.form['operacion']))
    if request.form['tipo_propiedad']:
        flag = True
        querys = querys.filter(Properties.tipo_propiedad.has(tipo_propiedad=request.form['tipo_propiedad']))
    #....PRECIOS QUERY & erroresHANDLING...........................
    query1 = querys
    if(currency == 'precio_dolares'):
        query_precio = False
        query_precio1 = False
        if precio_min != '':
            if not is_number(precio_min):
                errores["precio_min"] = "No es un numero"
            else:
                flag = True
                query_precio = True
                query1 = query1.filter(Properties.precio_dolares >= precio_min)
        if precio_max != '':
            if not is_number(precio_max):
                errores["precio_max"] = "No es un numero"
            else:
                flag = True
                query_precio1 = True
                query1 = query1.filter(Properties.precio_dolares <= precio_max)
        if query_precio and query_precio1 and precio_min > precio_max:
            query1 = querys
            errores["precio_min"] = "Diferencia invalida"
            errores["precio_max"] = "Diferencia invalida"
    else:
        query_precio = False
        query_precio1 = False
        if precio_min != '':
            if not is_number(precio_min):
                errores["precio_min"] = "No es un numero"
            else:
                flag = True
                query_precio = True
                query1 = query1.filter(Properties.precio_pesos >= precio_min)
        if precio_max != '':
            if not is_number(precio_max):
                errores["precio_max"] = "No es un numero"
            else:
                flag = True
                query_precio1 = True
                query1 = query1.filter(Properties.precio_pesos <= precio_max)
        if query_precio and query_precio1 and precio_min > precio_max:
            query1 = querys
            errores["precio_min"] = "Diferencia invalida"
            errores["precio_max"] = "Diferencia invalida"
    #....METRAJE QUERY & erroresHANDLING...........................
    query2 = query1
    query_metraje = False
    query_metraje1 = False
    if metraje_min != '':
        if not is_number(metraje_min):
            errores["metraje_min"] = "No es un numero"
        else:
            flag = True
            query_metraje = True
            query2 = query2.filter(Properties.metraje_edificio >= metraje_min)
    if metraje_max != '':
        if not is_number(metraje_max):
            errores["metraje_max"] = "No es un numero"
        else:
            flag = True
            query_metraje1 = True
            query2 = query2.filter(Properties.metraje_edificio <= metraje_max)

    if query_metraje is not None and query_metraje1 is not None and metraje_min > metraje_max:
        query2 = querys
        errores["metraje_min"] = "Diferencia invalida"
        errores["metraje_max"] = "Diferencia invalida"
    print(query2)
    search_results = query2 if flag==True else False
    if (search_results != False):
        paginas = search_results.count()
        if(paginas == 0):
            flash('No se encontro ninguna propiedad')
            return redirect(url_for('admin', section="home"))
        search_results = search_results.order_by(Properties.destacado).all()
    else:
        return redirect(url_for('admin', section="home"))
    print(errores,[e for e in errores])
    print(query2)
    properties_fotos_concat = []
    for p in search_results:
        foto = get_img(p.ref)
        properties_fotos_concat.append([p,foto])
    barrios_query = Barrios.query.all()
    form = PropertyForm()
    contactquestions_amount = Contactquestions.query.filter_by(read=False).count()
    return render_template('admin.html', questions_amount=contactquestions_amount, barrios = barrios_query,
    get_properties=properties_fotos_concat, errores=errores, form=form)

@app.route('/ventas', methods=['GET'])
def ventas():
    ventas = True
    barrios_query = Barrios.query.all()
    p_show = []
    get_properties = Properties.query.filter(Properties.pausado == False,Properties.destacado == 1,Properties.operacion_id == 1).limit(9).all()
    properties_count = len(get_properties) if get_properties is not None else 0
    if (properties_count < 9):
        get_properties_left = Properties.query.filter(Properties.pausado == False,Properties.destacado == 0,Properties.operacion_id == 1).limit(9-properties_count).all()
        for propiedades in get_properties_left:
            get_properties.append(propiedades)
    paginas =Properties.query.filter_by(operacion_id = 1).count()
    print([propiedad.id for propiedad in get_properties])
    p_show = properties_mtx(get_properties,3)
    paginas = math.ceil(int(paginas)/9) if paginas != '0' else 1
    return render_template('index-premium-pag.html', barrios = barrios_query,
    get_properties = p_show, paginas = paginas, pagina = 1,ventas = ventas,operacion_title = "Propiedades en venta")

@app.route('/ventas/<int:page>/<int:step>/<int:id>', methods=['GET'])
def ventas_pag(page,step,id):
    ventas = True
    barrios_query = Barrios.query.all()
    p_show = []
    get_properties = paginacion(page,step,id,Properties.query.filter(Properties.operacion_id==1))
    if (get_properties == []):
        return redirect(url_for('ventas'))
    paginas = Properties.query.filter_by(operacion_id = 1).count()
    p_show = properties_mtx(get_properties,3)
    paginas = math.ceil(int(paginas)/9) if paginas != '0' else 1
    return render_template('index-premium-pag.html', barrios = barrios_query,
    get_properties = p_show, paginas = paginas, pagina = page,  ventas = ventas,operacion_title = "Propiedades en venta")

@app.route('/alquiler', methods=['GET'])
def alquiler():
    alquiler = True
    barrios_query = Barrios.query.all()
    p_show = []
    get_properties = Properties.query.filter(Properties.pausado == False,Properties.destacado == 1,Properties.operacion_id == 2).limit(9).all()
    properties_count = len(get_properties) if get_properties is not None else 0
    if (properties_count < 9):
        get_properties_left = Properties.query.filter(Properties.pausado == False,Properties.destacado == 0,Properties.operacion_id == 2).limit(9-properties_count).all()
        for propiedades in get_properties_left:
            get_properties.append(propiedades)
    paginas = Properties.query.filter_by(operacion_id = 2).count()
    p_show = properties_mtx(get_properties,3)
    paginas = math.ceil(int(paginas)/9) if paginas != '0' else 1
    return render_template('index-premium-pag.html', barrios = barrios_query,
    get_properties = p_show, paginas = paginas, pagina = 1, alquiler = alquiler,operacion_title = "Propiedades en alquiler")

@app.route('/alquiler/<int:page>/<int:step>/<int:id>', methods=['GET'])
def alquiler_pag(page,step,id):
    alquiler = True
    barrios_query = Barrios.query.all()
    p_show = []
    get_properties = paginacion(page,step,id,Properties.query.filter(Properties.pausado == False,Properties.operacion_id==2))
    print('asdasdas',get_properties)
    if (get_properties == []):
        return redirect(url_for('alquiler'))
    paginas = Properties.query.filter_by(operacion_id = 2).count()
    p_show = properties_mtx(get_properties,3)
    paginas = math.ceil(int(paginas)/9) if paginas != '0' else 1
    return render_template('index-premium-pag.html', barrios = barrios_query,
    get_properties = p_show, paginas = paginas, pagina = page ,alquiler = alquiler,operacion_title = "Propiedades en alquiler")

@app.route('/contact-mail', methods=['POST', 'GET'])
def contact_questions():
    new_question = Contactquestions(complete_name = request.form['contact-name'],
    mail = request.form['contact-email'], phone = request.form['contact-phone'],
    question = request.form['contact-question'])
    db.session.add(new_question)
    db.session.commit()
    flash("Pregunta enviada correctamente!")
    return redirect(url_for('index'))

@app.route('/question-mail', methods=['POST', 'GET'])
def property_questions():
    id = request.form['contact-property_id']
    new_question = Contactquestions(property_id=request.form['contact-property_id'],complete_name = "Buscando propiedad",
    mail = request.form['contact-email'], phone = request.form['contact-phone'],
    question = request.form['contact-question'])
    db.session.add(new_question)
    db.session.commit()
    flash("Pregunta enviada correctamente!")
    return redirect(url_for('profile', id=id))

@profile
@app.route('/admin/<section>')
@login_required
def admin(section):
    test = []
    form = PropertyForm()
    barrios_query = Barrios.query.all()
    propietarios = Propietarios.query.all()
    contactquestions_amount = Contactquestions.query.filter_by(read=False).count()
    if section == "insert":
        get_properties = Properties.query.with_entities(Properties.ref).all()
        print(get_properties)
        return render_template('insert.html',form=form,get_properties = get_properties,propietarios=propietarios)
    if section == "home":
        get_properties = Properties.query.filter_by(pausado=0).all()
        for propiedades in get_properties:
            foto = get_img(propiedades.ref)
            test.append([propiedades,foto])
        print(get_properties)
        section="home"
        return render_template('admin.html', barrios = barrios_query, propietarios=propietarios,get_properties=test,
        form=form, questions_amount=contactquestions_amount, section=section)
    if section == "sale":
        get_properties = Properties.query.filter_by(operacion_id = 1, pausado = 0).all()#THE ONE THAT CHANGES
        for propiedades in get_properties:
            foto = get_img(propiedades.ref)
            test.append([propiedades,foto])
        print(get_properties)
        section="sale"
        return render_template('admin.html', propietarios=propietarios,barrios = barrios_query, get_properties = test,
        form=form, questions_amount=contactquestions_amount, base64=base64, section=section)
    if section == "rent":
        get_properties = Properties.query.filter_by(operacion_id = 2, pausado = 0).all()#THE ONE THAT CHANGES
        for propiedades in get_properties:
            foto = get_img(propiedades.ref)
            test.append([propiedades,foto])
        print(get_properties)
        section="rent"
        return render_template('admin.html', barrios = barrios_query, get_properties = test,
        form=form, propietarios=propietarios,questions_amount=contactquestions_amount, base64=base64, section=section)
    if section == "paused":
        get_properties = Properties.query.filter_by(pausado = 1).all()#THE ONE THAT CHANGES
        for propiedades in get_properties:
            foto = get_img(propiedades.ref)
            test.append([propiedades,foto])
        print(get_properties)
        section="paused"
        return render_template('admin.html', propietarios=propietarios,barrios = barrios_query, get_properties = test,
        form=form, questions_amount=contactquestions_amount, section=section)

@profile
@app.route('/update/<id>', methods=['GET', 'POST'])
@login_required
def update(id):
    contactquestions_amount = Contactquestions.query.filter_by(read=False).count()
    get_properties = Properties.query.get(id)
    form = PropertyForm()
    assign_properties_to_from(form,get_properties)
    propietarios = Propietarios.query.all()
    barrios = Barrios.query.all()
    print(form.data,get_properties.titulo)
    return render_template('asdasd.html',
    form = form,fotos = get_imgs(get_properties.ref),ref=get_properties.ref, propietarios = propietarios,questions_amount=contactquestions_amount,id = id,barrios = barrios, base64=base64)

@app.route('/about')
def about():
    return render_template('about.html')

@profile
@app.route('/edit-property/<int:id>', methods=['POST'])
@login_required
def edit_property(id):
    form = PropertyForm()
    flag = True
    get_property = Properties.query.get(id)
    path_to_ref = imgs_dir + '/' + get_property.ref
    all_imgs = os.listdir(path_to_ref)
    # Check when a pic is re-changed (if is pushed to change_pic array or changed content within same index)
    #Condicional por si el input no trae ninguna imagen
    if form.validate_on_submit() and flag:
        ref_check = Properties.query.filter_by(ref = form.data['ref']).first()
        if (form.data['precio_dolares'] == '' and form.data['precio_dolares'] == ''):
            flag = False
            flash("La propiedad necesita un precio")
        if (ref_check is not None and ref_check.id != get_property.id):
            flag = False
            flash("La referencia tiene que ser unica")
        if not flag:
            contactquestions_amount = Contactquestions.query.filter_by(read=False).count()
            propietarios = Propietarios.query.all()
            barrios = Barrios.query.all()
            fotos = get_imgs(get_property.ref)
            print(form.errors)
            for error in form.errors:
                form.errors[error][0] = 'Valor no valido'
                print(error)
            return render_template('asdasd.html',
            form = form,fotos = fotos ,ref=get_property.ref,propietarios = propietarios,questions_amount=contactquestions_amount,id = id,barrios = barrios, base64=base64)
        else:
            if get_property.ref != form.data['ref']:
                os.rename(imgs_dir + get_property.ref, imgs_dir + form.data['ref'])
            assign_form_to_properties(get_property,form)
            db.session.commit()
    else:
        contactquestions_amount = Contactquestions.query.filter_by(read=False).count()
        propietarios = Propietarios.query.all()
        barrios = Barrios.query.all()
        fotos = get_imgs(get_property.ref)
        print(form.errors)
        for error in form.errors:
            form.errors[error][0] = 'Valor no valido'
            print(error)
        return render_template('asdasd.html',
        form = form,fotos = fotos, propietarios = propietarios,ref=get_property.ref,questions_amount=contactquestions_amount,id = id,barrios = barrios, base64=base64)
    return redirect(url_for('admin', section='home'))


@app.route('/profile/<id>')
def profile(id):
    get_property = Properties.query.filter_by(id = id).first()
    comodidades = Comfort.query.filter_by(id = id).first()
    seguridad = Seguridad.query.filter_by(id = id).first()
    fotos = get_imgs(get_property.ref)
    return render_template('profile.html',
    get_property = get_property, fotos = fotos,
    comfort = comodidades,
    seguridad = seguridad)
@app.route('/insertation', methods=['POST','GET'])
@login_required
def insertation():
    form = PropertyForm()
    path_to_buffer = imgs_dir + '/' + 'buffer'
    fotos_count = len(os.listdir(path_to_buffer))
    flag = True
    print('asd',form.fotos.data)
    if form.validate_on_submit():
        ref_check = Properties.query.filter_by(ref = request.form['ref']).first()
        ref_check = Properties.query.filter_by(ref = request.form['ref'].upper()).first() if ref_check is None else ref_check
        print(ref_check,request.form['ref'])
        if (form.data['precio_pesos'] == '' and form.data['precio_dolares'] == ''):
            flag = False
            flash("La propiedad necesita un precio")
        if (fotos_count > 15):
            flag = False
            flash("Demasiadas fotos, maximo 15")
        if (ref_check is not None):
            flag = False
            flash("La referencia tiene que ser unica")
        if flag:
            barrio = Barrios.query.filter_by(barrio = form.data['barrio']).first()
            operacion = Operaciones.query.filter_by(operacion = form.data['operacion']).first()
            tipo_propiedad = Tipo_propiedad.query.filter_by(tipo_propiedad = form.data['tipo_propiedad']).first()
            print(form.fotos.data)
            path_to_ref = imgs_dir + '/' + request.form['ref']
            os.rename(path_to_buffer,path_to_ref)
            os.mkdir(path_to_buffer)
            propietario_query = Propietarios.query.filter_by(telefono = form.data['telefono']).first()
            if propietario_query is None:
                propietario_add = Propietarios(nombre = form.data['nombre'], apellido = form.data['apellido'], email = form.data['email'], telefono = form.data['telefono'])
                db.session.add(propietario_add)
                db.session.commit()
                propietario_query = Propietarios.query.filter_by(telefono = form.data['telefono']).first()
                print(propietario_query.id)
            property_data = Properties(operacion_id = operacion.id,
            pausado = 0,
            fecha_publicacion = date.today(),
            tipo_propiedad_id = tipo_propiedad.id,
            propietario_id = propietario_query.id,
            barrio_id = barrio.id,
            destacado = form.data['destacado'],
            ref = request.form['ref'],
            distancia_al_mar = form.data['distancia_al_mar'],
            titulo = request.form['titulo'],
            direccion = request.form['direccion'],
            descripcion = form.data['descripcion'],
            precio_dolares = abs(form.data['precio_dolares']) if form.data['precio_dolares'] else None,
            precio_pesos = abs(form.data['precio_pesos']) if form.data['precio_pesos'] else None,
            metraje_edificio = form.data['metraje_edificio'],
            metraje_patio = form.data['metraje_patio'],
            metraje_total = form.data['metraje_edificio'] if form.data['metraje_patio'] is None else form.data['metraje_edificio'] + form.data['metraje_patio'],
            baños = form.data['baños'],
            dormitorios = form.data['dormitorios'],
            permuta = form.data['permuta'] if form.data['permuta'] != 2 else None,
            financia = form.data['financia'] if form.data['financia'] != 2 else None,
            garaje = form.data['garaje'],
            estado = form.data['estado'],
            orientacion = form.data['orientacion'],
            disposicion = form.data['disposicion'],
            n_plantas = form.data['n_plantas'])
            db.session.add(property_data)
            db.session.commit()
            comfort = Comfort(agua_caliente = form.comfort.data['agua_caliente'],
                        aire_acondicionado = form.comfort.data['aire_acondicionado'],
                        altillo = form.comfort.data['altillo'],
                        amueblada = form.comfort.data['amueblada'],
                        balcón = form.comfort.data['balcón'],
                        barbacoa = form.comfort.data['barbacoa'],
                        box = form.comfort.data['box'],
                        bungalow = form.comfort.data['bungalow'],
                        calefacción = form.comfort.data['calefacción'],
                        depósito = form.comfort.data['depósito'],
                        dormitorio_de_servicio = form.comfort.data['dormitorio_de_servicio'],
                        estufa_leña = form.comfort.data['estufa_leña'],
                        garaje = form.comfort.data['garaje'],
                        gas_por_cañería = form.comfort.data['gas_por_cañería'],
                        gym = form.comfort.data['gym'],
                        instalación_de_tv_cable = form.comfort.data['instalación_de_tv_cable'],
                        jacuzzi = form.comfort.data['jacuzzi'],
                        jardín = form.comfort.data['jardín'],
                        lavadero = form.comfort.data['lavadero'],
                        lavandería = form.comfort.data['lavandería'],
                        linea_blanca = form.comfort.data['linea_blanca'],
                        living_comedor = form.comfort.data['living_comedor'],
                        losa_radiante = form.comfort.data['losa_radiante'],
                        parrillero = form.comfort.data['parrillero'],
                        patio = form.comfort.data['patio'],
                        piscina = form.comfort.data['piscina'],
                        piso_porcelanato = form.comfort.data['piso_porcelanato'],
                        placard_en_la_cocina = form.comfort.data['placard_en_la_cocina'],
                        placard_en_dormitorio = form.comfort.data['placard_en_dormitorio'],
                        playroom = form.comfort.data['playroom'],
                        previsión_aa = form.comfort.data['previsión_aa'],
                        sauna = form.comfort.data['sauna'],
                        sótano = form.comfort.data['sótano'],
                        terraza = form.comfort.data['terraza'],
                        terraza_lavadero = form.comfort.data['terraza_lavadero'],
                        vestidor = form.comfort.data['vestidor'],
                        vista_al_mar = form.comfort.data['vista_al_mar'],
                        walkin_closet = form.comfort.data['walkin_closet'],
                        wifi = form.comfort.data['wifi'])
            seguridad = Seguridad( alarma = form.seguridad.data['alarma'],
                        cámaras_cctv = form.seguridad.data['cámaras_cctv'],
                        cerca_perimetral = form.seguridad.data['cerca_perimetral'],
                        portería_24hs = form.seguridad.data['portería_24hs'],
                        portón_eléctrico = form.seguridad.data['portón_eléctrico'],
                        rejas = form.seguridad.data['rejas'],
                        guardia_de_seguridad = form.seguridad.data['guardia_de_seguridad'])
            db.session.add_all([comfort,seguridad])
            db.session.commit()
            flash('Ingreso completado con exito')
            return redirect(url_for('admin',section='home'))
    barrios_query = Barrios.query.all()
    propietarios = Propietarios.query.all()
    contactquestions_amount = Contactquestions.query.filter_by(read=False).count()
    get_properties = Properties.query.all()
    return render_template('insert.html', barrios = barrios_query, propietarios=propietarios,get_properties = get_properties,
    form=form, questions_amount=contactquestions_amount, section="home")


@app.route('/insert-propietario', methods=['POST','GET'])
@login_required
def insert_propietario():
    propietario_mail  = request.form['email']
    propietario_check = Propietarios.query.filter_by(email=propietario_mail).first()
    if propietario_check:
        return redirect(url_for('owners'))
        flash("Propietario ya esta ingresado")
    else:
        propietario_add = Propietarios(nombre = request.form['nombre'], apellido = request.form['apellido'], email = request.form['email'], telefono = request.form['telefono'])
        db.session.add(propietario_add)
        db.session.commit()
        return redirect(url_for('owners'))

@app.route('/update-owner', methods=['POST', 'GET'])
@login_required
def update_owner():
    owner_id = request.form['id']
    get_owner = Propietarios.query.filter_by(id=owner_id).first()
    get_owner.nombre = request.form['nombre']
    get_owner.apellido = request.form['apellido']
    get_owner.email = request.form['email']
    get_owner.telefono = request.form['telefono']
    try:
        db.session.commit()
    except Exception as e:
        flash("Error! Hay otro propietario con esos datos")
        print(e)
    return redirect(url_for('owners'))

@app.route('/propietarios')
@login_required
def owners():
    contactquestions_amount = Contactquestions.query.filter_by(read=False).count()
    form = PropertyForm()
    propietarios = Propietarios.query.all()
    return render_template('owners.html', questions_amount=contactquestions_amount, form=form, propietarios=propietarios,base64 = base64)

@app.route('/propietarios/<id>')
@login_required
def owner_profile(id):
    contactquestions_amount = Contactquestions.query.filter_by(read=False).count()
    form = PropertyForm()
    propietario = Propietarios.query.filter_by(id=id).first()
    for propiedades in propietario.properties:
        foto = get_img(propiedades.ref)
        setattr(propiedades,'foto',foto)
    return render_template('owner-profile.html', questions_amount=contactquestions_amount, form=form, propietario=propietario)

@app.route('/delete-prop/<id>', methods=['GET'])
@login_required
def delete_prop(id):
    # try:
        p_deletes = Properties.query.filter_by(id = id).delete()
        com_deletes = Comfort.query.filter_by(id = id).delete()
        sec_deletes = Seguridad.query.filter_by(id = id).delete()
        db.session.commit()
    # except Exception:
    #     flash('No es posible eliminar esta propiedad')
        return redirect(url_for('owner_profile', id=id))

@app.route('/remove_owner/<id>', methods=['POST'])
@login_required
def remove_owner(id):
    db.session.query(Propietarios).filter_by(id=id).delete()
    db.session.commit()
    flash("Propietario eliminado.")
    return redirect(url_for('owners'))

@app.route('/contact-page')
def contactus():
    return render_template('contact.html')

@app.route('/subscribed', methods=['GET', 'POST'])
def subscribers():
    client_mail = request.form['email']
    new_subscriber = Subscribers( mail=client_mail)
    try:
        db.session.add(new_subscriber)
        db.session.commit()
        flash("Te has suscripto correctamente")
    except Exception as e:
        flash("Este mail ya esta ingresado")
        print(e)
    return redirect(url_for('index'))

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    admin_check = Admins.query.all()
    username = request.form['username']
    password = request.form['userpass']
    if admin_check != []:
        i = 0
        while username != admin_check[i].user and password != admin_check[i].password:
            i+=1
        if username == admin_check[i].user and password == admin_check[i].password:
            session['username'] = username
            print(g.user)
            return redirect(url_for('admin', section="home"))
        else:
            flash("Usuario incorrecto")
            return redirect(url_for('login_page'))
    else:
        if username == "admin" and password == "pass":
            session['username'] = username
            print(g.user)
            return redirect(url_for('admin', section="home"))
        else:
            flash("Usuario incorrecto")
            return redirect(url_for('login_page'))


    # if request.form['username'] == username and request.form['userpass'] == userpass:
    #     session['username'] = request.form['username']
    #     print(g.user)
    #     return redirect(url_for('admin', section="home"))
    # else:
    #     flash("Usuario incorrecto")
    #     return redirect(url_for('login_page'))

@app.route('/logout')
def logout():
    session['username'] = None
    return redirect(url_for('index'))

# ADMIN/SOCIAL ######################################################
@app.route('/social/<section>')
@login_required
def social_page(section):
    saved_amount = Contactquestions.query.filter_by(saved=True).count()
    trash_amount = Contactquestions.query.filter_by(erased=True).count()
    form = PropertyForm()
    contactquestions_amount = Contactquestions.query.filter_by(read=False).count()
    get_subscribers = Subscribers.query.all()
    subscribers_amount = Subscribers.query.count()
    subscribers = Subscribers.query.all()
    if section == "home":
        get_questions = Contactquestions.query.filter_by(erased=False).all()#THE ONE THAT CHANGES
        return render_template('social.html', form=form,
        subscribers_amount = subscribers_amount, subscribers=subscribers,
        questions = get_questions, section="home", trash_amount=trash_amount, saved_amount=saved_amount, questions_amount=contactquestions_amount, subscriber = get_subscribers)
    if section == "saved":
        get_questions = Contactquestions.query.filter_by(saved=True).all()#THE ONE THAT CHANGES
        form = PropertyForm()
        return render_template('social.html', form=form,
        subscribers_amount = subscribers_amount,  subscribers=subscribers,
        questions = get_questions, section="saved", trash_amount=trash_amount, saved_amount=saved_amount, questions_amount=contactquestions_amount, subscriber = get_subscribers)
    if section == "trash":
        get_questions = Contactquestions.query.filter_by(erased=True).all()#THE ONE THAT CHANGES
        return render_template('social.html', form=form,
        subscribers_amount = subscribers_amount,  subscribers=subscribers,
        questions = get_questions, section="trash", trash_amount=trash_amount, saved_amount=saved_amount, questions_amount=contactquestions_amount, subscriber = get_subscribers)

@app.route('/readed/<id>', methods=['POST'])
@login_required
def readed(id):
    get_question = Contactquestions.query.filter_by(id=id).first()
    get_question.read = True
    db.session.commit()
    return redirect(url_for('social_page', section="home"))

@app.route('/answered/<id>', methods=['POST'])
@login_required
def answered(id):
    get_question = Contactquestions.query.filter_by(id=id).first()
    get_question.answered = True
    get_question.read = True
    db.session.commit()
    return redirect(url_for('social_page', section="home"))

@app.route('/remove_question/<id>', methods=['POST'])
@login_required
def removed(id):
    get_question = Contactquestions.query.filter_by(id=id).first()
    if get_question.erased == False:
        get_question.erased = True
        get_question.saved = False
        db.session.commit()
        section = "home"
    else:
        db.session.query(Contactquestions).filter_by(id=id).delete()
        db.session.commit()
        section="trash"
    return redirect(url_for('social_page', section=section))

@app.route('/save_question/<id>', methods=['POST'])
@login_required
def saved(id):
    path = request.path
    get_question = Contactquestions.query.filter_by(id=id).first()
    if get_question.saved == True and get_question.erased==False:
        get_question.saved = False
        db.session.commit()
        return redirect(url_for('social_page', section="home"))
    if get_question.saved == True and get_question.erased==True:
        get_question.saved = False
        db.session.commit()
        return redirect(url_for('social_page', section="trash"))
    if get_question.saved == False and get_question.erased ==True:
        get_question.saved = True
        get_question.erased = False
        db.session.commit()
        return redirect(url_for('social_page', section="trash"))
    if get_question.saved == False:
        get_question.saved = True
        get_question.erased = False
        db.session.commit()
        return redirect(url_for('social_page', section="home"))

@app.route('/send-mail-subscribers')
@login_required
def mail_send():
    auto_send = False
    property_id = 1
    property_description = Properties.query.filter_by(id=property_id).first()
    message = property_description.descripcion
    subscribers = Subscribers.query.all()
    subscribers_mail = []
    for subscriber in subscribers:
        subscriber.mail
    subscribers_mail.append(subscriber.mail)
    print(subscribers)
    msg = Message("Nueva propiedad ingresada!",
                  recipients=subscribers_mail)
    msg.html = '<div style="border-style:solid;border-width:thin;border-color:#dadce0;border-radius:8px;padding:40px 20px"><div style="font-family:''Google Sans'',Roboto,RobotoDraft,Helvetica,Arial,sans-serif;border-bottom:thin solid #dadce0;color:rgba(0,0,0,0.87);line-height:32px;padding-bottom:24px;text-align:center;word-break:break-word"><img alt=Pallaresyasociados aria-hidden=true class=CToWUd width=50 src="https://scontent.fmvd4-1.fna.fbcdn.net/v/t1.0-9/16473247_262488650849599_8347533623051414236_n.jpg?_nc_cat=105&ccb=2&_nc_sid=09cbfe&_nc_eui2=AeG32RxTx024IYxCbpOzxz-1-3zJOy680pX7fMk7LrzSlYUv26nRqU1xX8N6KgvjcljdMNMVh_R061esq01RqNwe&_nc_ohc=Zps9IjZhHekAX9DH0kL&_nc_ht=scontent.fmvd4-1.fna&oh=e9b1d6a35f896795c3e791fc5cbbcff5&oe=5FD115BF" style=margin-bottom:16px width=74> <div style=font-size:24px> Descubre mas detalles sobre esta propiedad! </div> <div style=font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-size:14px;color:rgba(0,0,0,0.87);line-height:20px;padding-top:20px;text-align:center>' + message + '<div style=padding-top:32px;text-align:center><a href=http://127.0.0.1:3000/profile/1 style="font-family:''Google Sans'',Roboto,RobotoDraft,Helvetica,Arial,sans-serif;line-height:16px;color:#ffffff;font-weight:400;text-decoration:none;font-size:14px;display:inline-block;padding:10px 24px;background-color:rgb(1, 167, 1);border-radius:5px;min-width:90px" target=_blank> Ver la casa </a></div></div></div></div>'
    if auto_send==True:
        mail.send(msg)

    return render_template('mail.html')

@app.route('/insert-miemail', methods=['POST']) #Función sin terminar
@login_required
def my_email():
    existent_mail = MainMail.query.all()
    verify_user = request.form['miemail-email']
    verify_pass = request.form['miemail-pass']
    # Exist?
    if existent_mail == []:
        try:
            myemail_add = MainMail(mail = request.form['miemail-email'],
            mail_password = request.form['miemail-pass'])
            db.session.add(myemail_add)
            db.session.commit()
            flash("Correo registrado con éxito")
            return redirect(url_for('config'))
        except expression as identifier:
            flash("Error, ese correo ya esta registrado")
            return redirect(url_for('config'))
    # = mail & != pass
    elif existent_mail.mail == verify_user and existent_mail.mail_password != verify_pass:
        try:
            existent_mail.mail = request.form['miemail-email']
            existent_mail.mail_password = request.form['miemail-pass']
            db.session.commit()
            flash("Contraseña cambiada con éxito")
            return redirect(url_for('config'))
        except expression as identifier:
            flash("Error, ese correo ya esta registrado")
            return redirect(url_for('config'))
    # = mail & = pass
    elif existent_mail.mail == verify_user and existent_mail.mail_password == verify_pass:
        flash("Error, correo y contraseña ya estan registradas")
        return redirect(url_for('config'))

@app.route('/config')
def config():
    contactquestions_amount = Contactquestions.query.filter_by(read=False).count()
    return render_template("config.html", questions_amount=contactquestions_amount)

@app.route('/regist-admin', methods=['POST'])
@login_required
def regist_admin():
    try:
        admin_add = Admins(user = request.form['admin-user'],
        password = request.form['admin-pass'])
        db.session.add(admin_add)
        db.session.commit()
        flash("Administrador registrado con éxito")
        return redirect(url_for('config'))
    except Exception as e:
        print(e)
        flash("Error, ese administrador ya esta registrado")
        return redirect(url_for('config'))

@app.route('/profile-admin/<id>')
@login_required
def profileforadmin(id):
    get_property = Properties.query.filter_by(id = id).first()
    comodidades = Comfort.query.filter_by(id = id).first()
    seguridad = Seguridad.query.filter_by(id = id).first()

    return render_template('profileforadmin.html',
    get_property = get_property,
    comfort = comodidades,
    seguridad = seguridad, base64 = base64)