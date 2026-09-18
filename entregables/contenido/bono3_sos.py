# -*- coding: utf-8 -*-
"""
Bono 3 — SOS Antojo de Dulce.

Qué hacer en los primeros 10 minutos de un antojo fuerte.

La primera página no es el protocolo: es la separación entre "antojo" y
"azúcar baja". Tenía que ir ahí. Este bono se lee con prisa, en el
momento del antojo, y el mismo cuadro — ansiedad, hambre de golpe,
ganas de dulce — puede ser una hipoglucemia en alguien que usa
glibenclamida o insulina. Si esa lectora abre el bono y encuentra un
té de canela como primer consejo, el bono la perjudica.

Por eso: triaje primero, protocolo después.
"""

import libro as L

META = dict(
    slug="bono3",
    archivo="Bono-3-SOS-Antojo-de-Dulce.pdf",
    titulo_pdf="Bono 3 — SOS Antojo de Dulce",
    autor="Abuela Mei",
    asunto="Qué hacer en los primeros 10 minutos de un antojo fuerte de dulce, "
           "y cómo distinguirlo de una bajada de azúcar.",
    claves="antojo, dulce, ansiedad por comer, hipoglucemia, azúcar baja, "
           "rescate, glucosa",
    pie="SOS Antojo de Dulce",
)


def portada():
    return L.portada(
        sello="Bono 3 · Azúcar en Equilibrio",
        titulo_html="SOS<br><span>Antojo de Dulce</span>",
        sub="Qué hacer en los primeros 10 minutos, para que se te pase sin "
            "pan y sin refresco. Déjalo guardado en el celular.",
        cuenta="10 MINUTOS · 12 RESCATES",
        autor="de la Abuela Mei",
        hoja="&#9200;",
    )


# ------------------------------------------------------------------
def _triaje():
    h = ['<div style="padding-top:4mm">']
    h.append(L.caja(
        "Alto. Primero esto.",
        "<p>Antes de cualquier remedio de este cuaderno, contesta una sola "
        "pregunta: <b>¿esto es un antojo, o se te está bajando el azúcar?</b></p>"
        "<p>Se parecen. Los dos dan hambre de repente y ganas de dulce. "
        "Pero se atienden <b>al revés</b>: el antojo se pasa sin azúcar, "
        "y la bajada se atiende <b>con azúcar, ya</b>.</p>"
        "<p>Confundirlos es lo único de este cuaderno que puede hacerte daño. "
        "Por eso esta es la primera página y no la última.</p>",
        "alerta"))
    h.append(L.ancla("triaje", "¿Antojo o azúcar baja?", 0))
    h.append('<div class="dos">'
             '<div class="col-antojo"><h4>Suena a antojo</h4><ul>'
             "<li>Llega a una <b>hora fija</b>: casi siempre entre 4 y 6 de la tarde</li>"
             "<li>Se te antoja <b>algo en particular</b>: el pan de la esquina, "
             "ese chocolate, no cualquier cosa</li>"
             "<li>Comiste hace 2 o 3 horas y comiste bien</li>"
             "<li>Aparece con <b>aburrimiento, enojo o cansancio</b></li>"
             "<li>Se te olvida si te distraes con algo</li>"
             "<li>No traes temblor ni sudor frío</li>"
             "</ul></div>"
             '<div class="col-baja"><h4>Suena a azúcar baja</h4><ul>'
             "<li><b>Temblor</b> en las manos</li>"
             "<li><b>Sudor frío</b>, de repente, sin calor</li>"
             "<li>El corazón <b>acelerado</b> o golpeando</li>"
             "<li>Mareo, piernas débiles, ganas de sentarte</li>"
             "<li><b>Visión borrosa</b> o doble</li>"
             "<li>Te comerías <b>cualquier cosa</b>, con urgencia</li>"
             "<li>Te sientes <b>rara</b> y te cuesta explicar por qué</li>"
             "<li>Te saltaste una comida, caminaste de más o tomaste alcohol</li>"
             "</ul></div></div>")
    h.append(L.caja(
        "Si es o si dudas: azúcar baja se trata así",
        "<p><b>Mídete si puedes.</b> Menos de <b>70 mg/dL</b> es azúcar baja. "
        "<b>Si no tienes con qué medirte y dudas, trátalo como bajada.</b> "
        "Es mucho peor esperar a ver qué pasa.</p>"
        "<p><b>La regla del 15 y 15:</b> toma <b>15 gramos de azúcar rápida</b> "
        "— una cucharada de azúcar en medio vaso de agua, medio vaso de "
        "refresco <b>normal</b> (no de dieta), medio vaso de jugo, una cucharada "
        "de miel o 3 tabletas de glucosa. Siéntate y <b>espera 15 minutos</b>. "
        "Vuelve a medirte. Si sigue abajo de 70, repite. Cuando suba, come algo "
        "de verdad.</p>"
        "<p>Después avísale a tu médico, <b>aunque ya se te haya pasado</b>.</p>"
        "<p>Y si la persona <b>no puede tragar o está inconsciente</b>: nada a "
        "la boca, de lado en el piso, y al <b>911</b>.</p>",
        "alerta"))
    h.append(L.caja(
        "Si es antojo, entonces sí",
        "<p>Pasa a la página siguiente. Tienes diez minutos por delante y "
        "todo lo que necesitas está aquí.</p>",
        "verde"))
    h.append("</div>")
    return "".join(h)


# ------------------------------------------------------------------
def _protocolo():
    h = [L.capitulo("El método", "Los primeros diez minutos",
                    sub="Un antojo fuerte dura menos de lo que crees. Lo que "
                        "hay que hacer es atravesarlo, no vencerlo.",
                    token="protocolo", nivel=0)]
    h.append(L.entrada(
        "Un antojo no es una línea recta que sube y sube. Es una ola: sube, "
        "se queda arriba unos minutos y <b>baja sola</b>. El chiste no es "
        "aguantar toda la tarde. Es aguantar la ola."))
    h.append(L.parrafo(
        "Casi siempre son <b>entre siete y diez minutos</b>. Por eso este "
        "cuaderno se llama así y no «cómo dejar el azúcar para siempre»: "
        "diez minutos sí se pueden."))

    pasos = [
        ("0:00", "Ponte de pie y sal de la cocina",
         "No decidas nada todavía. Solo cambia de cuarto. La mitad del antojo "
         "de la tarde se sostiene porque estás viendo el pan."),
        ("0:30", "Toma agua, un vaso entero",
         "Despacio, de pie. La sed y el antojo de dulce se confunden más de lo "
         "que uno cree, sobre todo con el azúcar alta."),
        ("1:00", "Pon a hervir el agua",
         "Este paso es el que de verdad funciona, y no por la planta: "
         "<b>preparar algo ocupa las manos y toma minutos</b>. Son minutos "
         "que el antojo está pasando."),
        ("2:00", "Escoge tu rescate",
         "De la lista de las páginas que siguen. El que tengas a la mano — "
         "el mejor rescate es el que sí puedes hacer hoy, no el ideal."),
        ("5:00", "Siéntate a tomarlo. Sin teléfono y sin tele",
         "En taza, sentada, oliéndolo. Si te lo tomas de pie y viendo el "
         "celular, tu cabeza no registra que comiste algo."),
        ("8:00", "Pregúntate qué pasó hoy",
         "¿Fue la hora? ¿Te saltaste la comida? ¿Te enojaste? ¿Estás cansada? "
         "Apúntalo en una línea. En una semana vas a ver tu patrón."),
        ("10:00", "Ya pasó",
         "Casi siempre ya pasó. Si no pasó del todo pero bajó, también cuenta: "
         "no es todo o nada."),
    ]
    for minuto, titulo, texto in pasos:
        h.append(f'<div class="paso"><div class="paso-min">{minuto}</div>'
                 f'<div class="paso-cuerpo"><h4>{titulo}</h4><p>{texto}</p></div></div>')

    h.append(L.caja(
        "Lo que no funciona",
        "<ul class='lista lista-no'>"
        "<li><b>Aguantar a fuerza de voluntad</b>, sin hacer nada. Aguantar "
        "sola diez minutos viendo el reloj hace el antojo más grande.</li>"
        "<li><b>«Nada más un pedacito.»</b> Con el pan dulce casi nunca es un "
        "pedacito, y tú ya lo sabes.</li>"
        "<li><b>Castigarte después.</b> La culpa no baja el azúcar y sí hace "
        "que mañana comas más.</li>"
        "<li><b>Saltarte la cena</b> para compensar. Eso te trae otro antojo "
        "más fuerte en la noche — y si usas insulina o glibenclamida, "
        "una bajada.</li>"
        "</ul>",
        ""))
    return "".join(h)


# ------------------------------------------------------------------
RESCATES = [
    ("Agua caliente con canela y clavo", "2 minutos",
     "Si ya la tienes hecha en el termo, <b>30 segundos</b>. Es el R-29 del "
     "libro. El más parecido a un postre sin serlo."),
    ("Agua fría con limón y hierbabuena", "1 minuto",
     "Cuando el antojo viene con calor y con sed. Ten la jarra hecha desde "
     "la mañana."),
    ("Té de cáscara de manzana con canela", "12 minutos",
     "El R-35. Tarda, y eso es parte de por qué sirve: los doce minutos son "
     "el remedio."),
    ("Un vaso de agua y lavarte los dientes", "3 minutos",
     "Suena tonto y es de los que mejor funcionan. Con la boca a menta, "
     "el pan deja de antojarse."),
    ("Mistela de canela y manzana", "30 segundos",
     "El R-44, si la tienes lista en el refrigerador. <b>30 ml</b> en medio "
     "vaso de agua, no a tragos."),
    ("Té verde con hierbabuena", "5 minutos",
     "El R-32. Para el antojo con sueño. <b>No después de las 6</b> o no duermes."),
    ("Jamaica fría sin azúcar", "1 minuto",
     "El R-14, del jarro que ya tienes hecho. Para el antojo de refresco."),
    ("Un puño chico de nueces o cacahuates sin sal", "0 minutos",
     "Diez o doce, contados y servidos <b>en un plato</b> — nunca de la bolsa. "
     "La grasa y la proteína cortan el antojo mejor que la fruta."),
    ("Jícama con limón y chile en polvo", "3 minutos",
     "Cuando lo que quieres es <b>masticar</b>, no tomar. Déjala picada "
     "desde la mañana."),
    ("Pepino con limón y sal", "2 minutos",
     "Lo mismo: cruje, dura y no te mueve el azúcar."),
    ("Un cuadrito de chocolate amargo, del de 70% o más", "0 minutos",
     "Un cuadrito, no la barra. Sirve cuando el antojo es de sabor y no de hambre. "
     "Si sabes que no te vas a quedar en uno, este no es tu rescate."),
    ("Salir a caminar a la cuadra", "10 minutos",
     "Es el R-43 usado de otro modo. Sales, das la vuelta y vuelves: "
     "los diez minutos del antojo se te fueron caminando."),
]


def _rescates():
    h = [L.capitulo("Escoge uno", "Los doce rescates",
                    sub="Ordenados por lo que tardan. El mejor es el que "
                        "tengas a la mano ahorita.",
                    token="rescates", nivel=0)]
    h.append(L.parrafo(
        "No necesitas los doce. Necesitas <b>tres</b> que puedas hacer sin "
        "pensar: uno caliente, uno frío y uno que se mastique. Subráyalos ahora "
        "y deja de escoger cada tarde."))
    filas = []
    for i, (nombre, tiempo, texto) in enumerate(RESCATES, 1):
        filas.append(
            f'<div class="paso">{L.ancla(f"res{i:02d}")}'
            f'<div class="paso-min">{tiempo}</div>'
            f'<div class="paso-cuerpo"><h4>{i}. {nombre}</h4><p>{texto}</p></div></div>')
    h.append("".join(filas))
    h.append(L.caja(
        "Los que se preparan de antes",
        "<p>Cuatro de estos doce solo sirven <b>si ya están hechos</b>: la "
        "jamaica, el agua de limón, la mistela y la jícama picada. "
        "Déjalos listos en la mañana del domingo y te resuelven la semana.</p>"
        "<p>El antojo de las cinco no se gana a las cinco. Se gana el domingo "
        "en la mañana.</p>",
        "verde"))
    return "".join(h)


# ------------------------------------------------------------------
def _kit():
    h = [L.capitulo("Ten esto listo", "Tu kit de los diez minutos",
                    sub="Lo que debe estar en la cocina y lo que debe estar "
                        "en la bolsa. Sin esto, el cuaderno no sirve.",
                    token="kit", nivel=0)]
    h.append(L.seccion("En la cocina, a la vista"))
    h.append(L.lista([
        "Un <b>termo</b> con agua de canela y clavo, hecho en la mañana",
        "Una <b>jarra</b> de jamaica o de agua de limón con hierbabuena en el refrigerador",
        "Un <b>frasco</b> con nueces o cacahuates sin sal — y un platito chico al lado",
        "Jícama o pepino <b>ya picado</b>, en tóper, al frente del refrigerador",
        "Tu <b>taza favorita</b>, limpia y a la mano. Esto no es adorno: "
        "la taza bonita hace que te sientes a tomártelo",
    ]))
    h.append(L.caja(
        "Y lo que NO debe estar a la vista",
        "<p>El pan dulce, las galletas y el refresco, <b>en el mueble de "
        "arriba y hasta atrás</b>. No se trata de tirarlos — se trata de que "
        "cueste tres movimientos en vez de uno.</p>"
        "<p>En esos tres movimientos te da tiempo de acordarte de este cuaderno.</p>",
        ""))
    h.append(L.seccion("En la bolsa, siempre"))
    h.append(L.lista([
        "<b>Azúcar de rescate</b>: un sobre de azúcar, un jugo chico de caja "
        "o tabletas de glucosa. Esto no es para el antojo — <b>es para una "
        "bajada</b>, y no debe faltar nunca",
        "Una bolsita con <b>nueces</b> o cacahuates",
        "Una botella de agua",
        "La <b>tarjeta</b> de la página siguiente, o su foto en el celular",
    ]))
    h.append(L.caja(
        "La diferencia, otra vez",
        "<p>El azúcar de la bolsa <b>no se toca</b> para un antojo. Es para "
        "una bajada de verdad. Si te la acabas en los antojos, el día que la "
        "necesites no va a estar.</p>",
        "alerta"))
    return "".join(h)


# ------------------------------------------------------------------
def _disparadores():
    h = [L.capitulo("Para que vuelva menos", "Los cinco disparadores",
                    sub="El antojo de las cinco casi nunca empieza a las cinco. "
                        "Empieza antes, y casi siempre en el mismo lugar.",
                    token="disparadores", nivel=0)]
    h.append(L.tabla(
        ["Si el antojo viene de", "Se nota en que", "Qué hacer distinto"],
        [["<b>Saltarte comidas</b>",
          "Llegas a la tarde con hambre de verdad y te comerías lo que sea",
          "Come tu comida completa, con proteína. El antojo de las cinco "
          "casi siempre se armó al mediodía."],
         ["<b>Un desayuno de puro pan</b>",
          "El antojo te da a media mañana y otra vez a media tarde",
          "Mete huevo, frijol o queso al desayuno. La mañana sostiene la tarde."],
         ["<b>La hora y la costumbre</b>",
          "Llega puntual, a la misma hora, aunque no tengas hambre",
          "Ten el rescate <b>preparado a las 4:30</b>, antes de que llegue. "
          "A la costumbre se le gana con otra costumbre."],
         ["<b>El cansancio</b>",
          "Viene con sueño y con ganas de algo rápido",
          "Diez minutos sentada con los pies en alto, y el té. El cuerpo "
          "pide descanso y tú le estabas dando pan."],
         ["<b>El coraje o la tristeza</b>",
          "Llega después de un disgusto, y quieres algo dulce específico",
          "Este no se quita con té, y no te voy a decir que sí. Sal a caminar, "
          "háblale a alguien. Y si es todos los días, eso se platica con "
          "el médico: no es glotonería."]]))
    h.append(L.caja(
        "Una semana de apuntes",
        "<p>Durante siete días, cada vez que te dé el antojo apunta tres cosas: "
        "<b>la hora, qué habías comido y cómo andabas de ánimo</b>.</p>"
        "<p>Al séptimo día vas a ver tu patrón escrito, y ahí se acaba el "
        "misterio. Casi siempre son las mismas dos cosas.</p>",
        "suave"))
    return "".join(h)


# ------------------------------------------------------------------
def _ya_comi():
    h = [L.capitulo("Y si ya te lo comiste", "No pasa nada. En serio.",
                    token="ya_comi", nivel=0)]
    h.append(L.entrada(
        "Porque va a pasar. A todas nos pasa, y la parte que hace daño no es "
        "el pan: es lo que viene después del pan."))
    h.append(L.seccion("Qué hacer"))
    h.append(L.numerada([
        "<b>Nada de castigos.</b> No te saltes la cena ni te pongas a "
        "caminar una hora para «compensar». Eso desordena más.",
        "<b>Tómate un vaso de agua</b> y, si puedes, sal a caminar "
        "<b>diez minutos</b>. Es el R-43, y es lo que de verdad ayuda "
        "después de algo dulce.",
        "<b>Mídete a las 2 horas</b> si tienes con qué, y apúntalo. "
        "No para regañarte: para saber.",
        "<b>La siguiente comida, normal.</b> No más chica, no más grande. Normal.",
        "<b>Apunta qué pasó antes.</b> Ahí está la información que sirve.",
    ]))
    h.append(L.caja(
        "Lo que sí importa",
        "<p>Un pan un martes no descompone nada. <b>Lo que descompone es "
        "el pan de todos los días</b> — y eso no se arregla con voluntad, "
        "se arregla con tener otra cosa lista a las cinco.</p>"
        "<p>Por eso el kit de la página anterior es lo más importante de "
        "este cuaderno.</p>",
        "verde"))
    h.append(L.caja(
        "Cuándo dejar de verlo como antojo",
        "<p>Si comes a escondidas, si no puedes parar cuando empiezas, si "
        "después te sientes muy mal contigo o si esto te pasa casi todos "
        "los días: <b>eso ya no es un antojo y no se arregla con un té</b>.</p>"
        "<p>Díselo a tu médico. Se atiende, es más común de lo que crees "
        "y no es falta de carácter.</p>",
        "alerta"))
    return "".join(h)


# ------------------------------------------------------------------
def _tarjeta():
    h = [L.capitulo("Recórtala", "La tarjeta del refrigerador",
                    sub="Córtala por la línea y pégala donde la veas. O tómale "
                        "foto y déjala en el celular — ahí la vas a encontrar "
                        "más rápido.",
                    token="tarjeta", nivel=0)]
    h.append('<div class="tarjeta">'
             '<div class="tijera">— — — — recorta por aquí — — — —</div>'
             "<h4>SOS Antojo · 10 minutos</h4>"
             "<ol>"
             "<li><b>¿Tiemblo o sudo frío?</b> → No es antojo. "
             "<b>Azúcar ya</b> (15 g) y espera 15 min.</li>"
             "<li>Si no: <b>ponte de pie y sal de la cocina</b>.</li>"
             "<li><b>Un vaso de agua</b>, despacio.</li>"
             "<li><b>Pon el agua a hervir.</b></li>"
             "<li>Tu rescate: ____________________</li>"
             "<li><b>Siéntate a tomarlo.</b> Sin teléfono.</li>"
             "<li>¿Qué pasó hoy? ¿Hora, hambre o coraje?</li>"
             "</ol>"
             "<p style='margin-top:3mm;font-size:10pt;color:#6B6355'>"
             "<b>Ya pasó.</b> Casi siempre dura menos de diez minutos.</p>"
             '<div class="tijera" style="margin-top:4mm">— — — — — — — — — —</div>'
             "</div>")
    h.append(L.caja(
        "Llena el renglón en blanco",
        "<p>Escribe ahí <b>tus tres rescates</b>, los que de verdad vas a "
        "hacer. Una tarjeta con doce opciones no sirve a las cinco de la "
        "tarde: a esa hora nadie escoge entre doce.</p>",
        "suave"))
    return "".join(h)


def cuerpo(paginas):
    return (_triaje() + _protocolo() + _rescates() + _kit()
            + _disparadores() + _ya_comi() + _tarjeta())


def final():
    return L.cierre(
        "Diez minutos.<br>Nada más",
        "<p>No es fuerza de voluntad. Es tener algo listo y saber que "
        "<strong>la ola baja sola</strong>.</p>"
        "<p>Prepara tu kit el domingo, escoge tus tres rescates y pega la "
        "tarjeta en el refrigerador. Con eso ya no llegas a las cinco "
        "a improvisar.</p>"
        "<p>Y no se te olvide lo de la primera página: <strong>si tiemblas "
        "o sudas frío, no es antojo</strong> — es azúcar y es ahora.</p>"
        '<p class="firma">— Abuela Mei</p>')
