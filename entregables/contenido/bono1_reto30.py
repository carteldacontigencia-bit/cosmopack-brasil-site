# -*- coding: utf-8 -*-
"""
Bono 1 — Reto de 30 Días: Azúcar Acompañada.

El calendario del primer mes, para que la lectora no tenga que escoger.

Tres cosas que se cuidaron al armarlo:

1. Se entra despacio. El día 1 no lleva ninguna hierba — lleva la caminata,
   que es lo más seguro y de lo que más sirve. Cada remedio nuevo entra a
   media dosis y solo de día, como manda la regla 2 del ebook.
2. Nunca hay dos remedios nuevos el mismo día, y los días 7, 14, 21 y 30
   no estrenan nada: son de repaso.
3. Los preparados que tardan se ponen a macerar con anticipación: el aceite
   de romero el día 3 (necesita 2 semanas y se usa el día 17), la mistela
   el día 23 (necesita 48 horas y se prueba el día 25). Si no, la lectora
   llega al día y no tiene el remedio listo.
"""

import libro as L

META = dict(
    slug="bono1",
    archivo="Bono-1-Reto-de-30-Dias.pdf",
    titulo_pdf="Bono 1 — Reto de 30 Días: Azúcar Acompañada",
    autor="Abuela Mei",
    asunto="Calendario de 30 días para acompañar el cuidado del azúcar, "
           "con dosis y horario. Complemento del ebook Azúcar en Equilibrio.",
    claves="reto 30 días, rutina, azúcar, glucosa, remedios naturales, hábito",
    pie="Reto de 30 Días",
)


def portada():
    return L.portada(
        sello="Bono 1 · Azúcar en Equilibrio",
        titulo_html="Reto de<br><span>30 Días</span>",
        sub="Azúcar Acompañada — tu primer mes ya organizado, día por día, "
            "con la dosis y la hora de cada remedio.",
        cuenta="4 SEMANAS · 30 DÍAS",
        autor="de la Abuela Mei",
        hoja="&#9728;",
    )


# ------------------------------------------------------------------
def _como():
    h = [L.capitulo("Antes de empezar", "Cómo funciona este reto",
                    sub="Cinco minutos de lectura y ya no tienes que decidir "
                        "nada por treinta días.",
                    token="como", nivel=0)]
    h.append(L.entrada(
        "El problema no es que no haya remedios. Es que hay demasiados, y "
        "una termina probando una hierba distinta cada semana sin saber "
        "cuál le hizo qué."))
    h.append(L.parrafo(
        "Así que yo te lo ordené. Treinta días, cuatro semanas, y cada día "
        "te dice qué tomar en la mañana, con la comida y en la tarde-noche. "
        "Tú nada más sigues."))

    h.append(L.seccion("Las reglas del reto", token="reglas_reto"))
    h.append(L.numerada([
        "<b>Tu medicina no cambia.</b> Ni un día, ni una dosis. El reto se "
        "monta encima de tu tratamiento, no en lugar de él.",
        "<b>Un remedio nuevo por día, y ninguno de noche.</b> Ya está armado "
        "así: fíjate que los días de estrenar están marcados.",
        "<b>Lo nuevo entra a media dosis.</b> El primer día de cada remedio "
        "va la mitad; al día siguiente, completo.",
        "<b>Los días 7, 14, 21 y 30 no se estrena nada.</b> Son de repaso, "
        "para que el cuerpo asiente lo anterior.",
        "<b>Si un día te sientes rara, ese día se para.</b> No se recupera "
        "ni se adelanta. Se anota y se sigue al día siguiente.",
        "<b>Si te saltas un día, sigues donde ibas.</b> No empieces de cero. "
        "Esto no es un castigo.",
    ]))

    h.append(L.caja(
        "Lo que necesitas tener a la mano",
        "<ul class='lista lista-pt'>"
        "<li>El ebook <b>Azúcar en Equilibrio</b>, para consultar cada ficha "
        "completa — aquí solo va el número, la dosis y la hora</li>"
        "<li>Tu medidor, si tienes, y tu libreta o el diario de la última "
        "página del ebook</li>"
        "<li><b>Azúcar de verdad a la mano</b>: un sobre de azúcar, un jugo "
        "chico o tabletas de glucosa. Por si acaso, todos los días</li>"
        "<li>Una olla chica, un colador y dos frascos de vidrio con tapa</li>"
        "</ul>",
        "suave"))

    h.append(L.caja(
        "La parte que no se salta",
        "<p>Varios de los remedios de este mes <b>bajan el azúcar</b> — la "
        "canela, el nopal, la hoja de guayaba. Se <b>suman</b> a tu metformina, "
        "a tu glibenclamida o a tu insulina.</p>"
        "<p>Por eso este reto entra despacio y por eso te pido que, si puedes "
        "medirte, lo hagas <b>más seguido las primeras dos semanas</b>: en "
        "ayunas y dos horas después del remedio nuevo.</p>"
        "<p>Y si te da <b>temblor, sudor frío, mareo o visión borrosa</b>: "
        "azúcar primero, la regla del 15 y 15 del ebook, y después me cuentas. "
        "Antes de empezar el reto, léete esa página. Es la única tarea "
        "que te dejo de hoy.</p>",
        "alerta"))

    h.append(L.seccion("Marca aquí tus 30 días", token="tablero"))
    h.append(L.parrafo(
        "Una palomita por día. No para presumir — para que veas, el día 12, "
        "que ya llevas once."))
    casillas = "".join(
        f'<div class="sem{min((d - 1) // 7 + 1, 4)}">{d}</div>' for d in range(1, 31))
    h.append(f'<div class="tablero">{casillas}</div>')

    h.append(L.seccion("Lo que vas a comprar, por semana", token="compras"))
    h.append(L.parrafo(
        "No compres todo hoy. La hierba seca pierde fuerza y lo fresco se "
        "echa a perder. Compra al principio de cada semana lo de esa semana."))
    h.append(L.tabla(
        ["Semana", "Lo que hace falta"],
        [
            ["<b>1 — Digestión</b>",
             "Canela de Ceilán en raja · 1 nopal · limones · hierbabuena · anís en grano"],
            ["<b>2 — Riñón y sed</b>",
             "Pepino · apio · chía · flor de jamaica · manzanilla · toronjil"],
            ["<b>3 — Circulación</b>",
             "Manzanilla (más) · sal de grano · romero fresco · aceite de oliva · "
             "col (repollo) · jengibre · cúrcuma"],
            ["<b>4 — Costumbre</b>",
             "Clavo de olor · 1 manzana · lo que hayas decidido dejar fijo"],
        ]))
    h.append(L.caja(
        "Cuánto debe costarte",
        "<p>En el <b>Bono 2 — Guía del Mercado de la Abuela Mei</b> viene el "
        "precio justo de cada cosa, dónde conseguirla y cómo distinguir la "
        "canela buena de la que casi siempre te venden. Léelo antes de ir "
        "al mercado la primera vez.</p>",
        "suave"))
    return "".join(h)


# ------------------------------------------------------------------
def _semana(num, etiqueta, titulo, texto, compra, token):
    return (f'<section class="semana">{L.ancla(token, f"Semana {num} — {titulo}", 0)}'
            f'<div class="eti">{etiqueta}</div><h2>{titulo}</h2>'
            f'<p>{texto}</p>'
            f'<div class="compra"><b>Para esta semana:</b> {compra}</div>'
            f'</section>')


def _repaso(num, preguntas, token):
    filas = "".join("<tr><td></td><td></td><td></td><td></td></tr>" for _ in range(7))
    tabla = ('<table class="registro"><thead><tr>'
             '<th>Día</th><th>¿Lo hice?</th><th>Azúcar</th><th>Cómo me sentí</th>'
             "</tr></thead><tbody>" + filas + "</tbody></table>")
    lst = "".join(f"<li>{p}</li>" for p in preguntas)
    return (f'<div class="caja no-cortar">{L.ancla(token, f"Repaso de la semana {num}", 1)}'
            f"<h4>Repaso de la semana {num}</h4>"
            f"<ul class='lista lista-pt'>{lst}</ul>{tabla}</div>")


# ------------------------------------------------------------------
DIAS = [
    # ---------- SEMANA 1 · DIGESTIÓN ----------
    (1, "Semana 1 · Digestión", "Hoy no se toma nada nuevo", [
        ("Mañana", "Tu medicina como siempre. Nada más."),
        ("Después de comer", "<b>R-43 · La caminata de los diez minutos.</b> "
                             "Revisa el zapato por dentro antes de salir."),
        ("Noche", "Apunta cómo dormiste y cómo te sentiste después de comer."),
    ], "Empezamos por lo más seguro y lo que más sirve. Si hoy solo haces la "
       "caminata, el reto ya arrancó bien."),

    (2, "Semana 1 · Digestión", "Entra la canela — media taza", [
        ("Mañana", "Tu medicina. Compra la canela de Ceilán si aún no la tienes."),
        ("Después de comer", "<b>R-01 · Té de canela de Ceilán, MEDIA taza.</b> "
                             "Mídete 2 horas después si puedes."),
        ("Noche", "R-43 · La caminata, si no la hiciste al mediodía."),
    ], "Media taza el primer día, siempre. Hoy estrenas: si te sientes rara, "
       "para y anótalo."),

    (3, "Semana 1 · Digestión", "Canela completa y pones el aceite a macerar", [
        ("Mañana", "<b>Pon a macerar el aceite de romero (R-21):</b> romero "
                   "bien seco en un frasco con aceite de oliva. Lo vas a usar "
                   "el día 17 — tarda dos semanas."),
        ("Después de comer", "<b>R-01 · Té de canela, taza completa.</b>"),
        ("Tarde", "R-43 · La caminata."),
    ], "Hoy no estrenas hierba nueva: subes la canela a dosis completa. "
       "Y dejas listo lo que tarda."),

    (4, "Semana 1 · Digestión", "Entra el nopal — medio vaso", [
        ("Antes de comer", "<b>R-05 · Agua de nopal con limón, MEDIO vaso.</b> "
                           "Deja 1 hora entre tu pastilla y este vaso."),
        ("Después de comer", "R-01 · Té de canela."),
        ("Tarde", "R-43 · La caminata."),
    ], "El nopal es fibra: puede darte gases los primeros días. Es normal y se pasa."),

    (5, "Semana 1 · Digestión", "Nopal completo", [
        ("Antes de comer", "<b>R-05 · Agua de nopal, vaso completo.</b>"),
        ("Después de comer", "R-01 · Té de canela."),
        ("Tarde", "R-43 · La caminata."),
    ], "Fíjate en el sueño de la tarde. ¿Sigue igual de pesado que el lunes?"),

    (6, "Semana 1 · Digestión", "Entra el té de la noche", [
        ("Antes de comer", "R-05 · Agua de nopal."),
        ("Después de comer", "R-01 · Té de canela."),
        ("Después de cenar", "<b>R-09 · Té de hierbabuena con anís.</b> "
                             "Si tienes reflujo, cámbialo por manzanilla."),
    ], "Este es suave, por eso lo dejo para la noche del sexto día."),

    (7, "Semana 1 · Digestión", "Repaso — no se estrena nada", [
        ("Todo el día", "Lo mismo de ayer: nopal, canela y el té de la noche."),
        ("Tarde", "R-43 · La caminata."),
        ("Noche", "Llena el repaso de la semana, en la página siguiente."),
    ], "Una semana. Ya tienes tres remedios en su lugar y una caminata al día."),

    # ---------- SEMANA 2 · RIÑÓN Y SED ----------
    (8, "Semana 2 · Riñón y sed", "Entra el agua del día", [
        ("Mañana", "<b>R-12 · Agua de pepino, apio y limón.</b> Prepara la jarra "
                   "y tómala hasta las 6 de la tarde, no después."),
        ("Comida", "Sigue el nopal y la canela."),
        ("Noche", "R-09 · Té de hierbabuena con anís."),
    ], "Si tomas medicina para la presión, empieza con medio litro: el apio la baja."),

    (9, "Semana 2 · Riñón y sed", "Entra la chía", [
        ("Mañana", "R-12 · Agua del día."),
        ("Media tarde", "<b>R-13 · Agua de chía con limón.</b> Déjala 20 minutos "
                        "en remojo. Nunca la tomes seca."),
        ("Noche", "R-09 · Té de la noche."),
    ], "Separa la chía 1 hora de tus pastillas y 4 horas de la levotiroxina."),

    (10, "Semana 2 · Riñón y sed", "Sin novedades — se asienta", [
        ("Todo el día", "Lo mismo de ayer. No entra nada nuevo."),
        ("Tarde", "R-43 · La caminata."),
        ("Noche", "Apunta: ¿te levantaste menos veces al baño esta semana?"),
    ], "Dos remedios nuevos en dos días es el tope. Hoy descansa de estrenar."),

    (11, "Semana 2 · Riñón y sed", "Entra la jamaica", [
        ("Comida", "<b>R-14 · Agua de jamaica sin azúcar.</b> Si te cuesta el "
                   "sabor, échale una raja de canela — engaña bonito."),
        ("Tarde", "R-13 · Agua de chía."),
        ("Noche", "R-09 · Té de la noche."),
    ], "La jamaica baja la presión. Si te mareas al levantarte, bájale a un vaso."),

    (12, "Semana 2 · Riñón y sed", "Entra el té para dormir", [
        ("Mañana", "R-12 · Agua del día."),
        ("Comida", "R-14 · Jamaica · y el nopal antes de comer."),
        ("Una hora antes de dormir", "<b>R-19 · Té de manzanilla con toronjil.</b> "
                                     "Una hora antes, no en la cama."),
    ], "Este sustituye al de hierbabuena si el que quieres es dormir mejor."),

    (13, "Semana 2 · Riñón y sed", "Se sostiene", [
        ("Todo el día", "Agua del día, nopal, canela, jamaica."),
        ("Tarde", "R-43 · La caminata."),
        ("Noche", "R-19 · Té de manzanilla con toronjil."),
    ], "Trece días. Fíjate si la sed de la noche cambió algo."),

    (14, "Semana 2 · Riñón y sed", "Repaso — no se estrena nada", [
        ("Todo el día", "Lo mismo."),
        ("Tarde", "Compra lo de la semana 3: sal de grano, col, jengibre, cúrcuma."),
        ("Noche", "Llena el repaso de la semana."),
    ], "Dos semanas. Aquí es donde la mayoría afloja — y donde se empieza a notar."),

    # ---------- SEMANA 3 · CIRCULACIÓN ----------
    (15, "Semana 3 · Circulación", "Los tobillos y las piernas en alto", [
        ("Mañana", "R-12 · Agua del día."),
        ("Media tarde", "<b>R-28 · La bomba de tobillos</b> y 15 minutos con "
                        "las piernas en alto."),
        ("Noche", "R-19 · Té para dormir."),
    ], "Empezamos la semana de las piernas por lo que no cuesta un peso."),

    (16, "Semana 3 · Circulación", "Primer baño de pies", [
        ("Tarde-noche", "<b>R-20 · Baño de pies templado de manzanilla y sal.</b> "
                        "<b>10 minutos, agua tibia probada con el codo.</b> "
                        "Nunca caliente."),
        ("Al terminar", "Seca muy bien <b>entre cada dedo</b>."),
        ("Noche", "R-28 · Piernas en alto."),
    ], "Si tienes cualquier herida, ampolla o grieta en el pie: HOY no hay baño. "
       "Hoy hay médico."),

    (17, "Semana 3 · Circulación", "El aceite de romero ya está listo", [
        ("Mañana", "Cuela el aceite que pusiste el día 3 y guárdalo en su frasco."),
        ("Noche", "<b>R-21 · Masaje de pies con el aceite de romero.</b> "
                  "Del tobillo hacia la rodilla. <b>No entre los dedos.</b>"),
        ("Mientras te lo untas", "Revísate los pies: planta, talón, uñas, entre los dedos."),
    ], "El masaje es la excusa; la revisión diaria del pie es lo que de verdad "
       "estamos construyendo."),

    (18, "Semana 3 · Circulación", "Entra la cataplasma de col", [
        ("Tarde", "<b>R-22 · Cataplasma de hoja de col</b> en las pantorrillas, "
                  "30 minutos con las piernas en alto. A temperatura ambiente."),
        ("Noche", "R-19 · Té para dormir."),
        ("Antes de dormir", "Revisión de pies."),
    ], "No amarres apretado. En una pierna con mala circulación, apretar hace daño."),

    (19, "Semana 3 · Circulación", "Entra el té de jengibre con cúrcuma", [
        ("Mañana", "<b>R-24 · Té de jengibre con cúrcuma.</b> Si tomas "
                   "anticoagulante, <b>este te lo saltas</b> hasta hablar con tu médico."),
        ("Tarde", "R-28 · Bomba de tobillos."),
        ("Noche", "R-21 · Masaje de pies."),
    ], "El único remedio del reto que de plano no es para todas. Lee la ficha completa."),

    (20, "Semana 3 · Circulación", "Segundo baño de pies", [
        ("Mañana", "R-24 · Té de jengibre con cúrcuma."),
        ("Tarde-noche", "R-20 · Baño de pies, 10 minutos, tibio. Y a secar bien."),
        ("Noche", "R-28 · Piernas en alto."),
    ], "Tres baños por semana es el tope. Más no es mejor: reblandece la piel."),

    (21, "Semana 3 · Circulación", "Repaso — no se estrena nada", [
        ("Todo el día", "Lo mismo."),
        ("Tarde", "Compra lo de la semana 4: clavo de olor y una manzana."),
        ("Noche", "Llena el repaso de la semana."),
    ], "Tres semanas. ¿Los pies se sienten distintos en la noche?"),

    # ---------- SEMANA 4 · COSTUMBRE ----------
    (22, "Semana 4 · Costumbre", "Entra el remedio de las cinco", [
        ("Mañana", "Lo de siempre."),
        ("5 de la tarde", "<b>R-29 · Agua de canela con clavo.</b> Prepárala "
                          "ANTES de que llegue el antojo, no cuando ya llegó."),
        ("Noche", "R-19 · Té para dormir."),
    ], "Tener algo listo a las cinco es medio trabajo hecho. El otro medio es tomárselo."),

    (23, "Semana 4 · Costumbre", "Pon la mistela a macerar", [
        ("Mañana", "<b>Prepara la mistela R-44</b> (manzana y canela) y métela al "
                   "refrigerador. Estará lista el día 25."),
        ("Tarde", "R-29 · Agua de canela con clavo."),
        ("Noche", "Revisión de pies."),
    ], "Frasco de vidrio limpio y seco, y siempre en el refrigerador — nunca fuera."),

    (24, "Semana 4 · Costumbre", "Sin novedades", [
        ("Todo el día", "Lo que ya traes."),
        ("Tarde", "R-43 · La caminata."),
        ("Noche", "Apunta cuáles remedios de verdad estás haciendo y cuáles no."),
    ], "Ese apunte de la noche es el más importante del mes. Sé honesta."),

    (25, "Semana 4 · Costumbre", "Pruebas la mistela", [
        ("Tarde", "<b>R-44 · Mistela de canela y manzana: 30 ml</b> rebajados en "
                  "medio vaso de agua. No a tragos puros."),
        ("Tarde", "R-28 · Bomba de tobillos."),
        ("Noche", "R-19 · Té para dormir."),
    ], "Una mistela dura cinco días en el refrigerador. Si huele agrio, se tira."),

    (26, "Semana 4 · Costumbre", "Escoge tus cinco fijos", [
        ("Mañana", "Abre tu diario y subraya los <b>cinco remedios</b> que sí "
                   "hiciste casi todos los días."),
        ("Tarde", "Esos cinco son tu rutina. Los demás quedan de repuesto."),
        ("Noche", "Escríbelos en un papel y pégalo en la cocina."),
    ], "Cinco que haces valen más que veinte que te sabes."),

    (27, "Semana 4 · Costumbre", "La lista para tu médico", [
        ("Mañana", "Anota en una hoja <b>todo</b> lo que estás tomando: "
                   "medicinas y remedios, con dosis y hora."),
        ("Tarde", "Guárdala en la bolsa o tómale foto con el celular."),
        ("Noche", "Lo de siempre."),
    ], "Esa hoja es la regla 4 del ebook. Llévala a tu próxima consulta."),

    (28, "Semana 4 · Costumbre", "Arma la despensa de la semana", [
        ("Mañana", "Revisa qué hierba se te acabó y apúntala."),
        ("Tarde", "Deja lista el agua del día y la jarra en el refrigerador."),
        ("Noche", "R-19 · Té para dormir."),
    ], "Dejar preparado hoy lo de mañana es lo que hace que esto no se caiga "
       "en la semana ocupada."),

    (29, "Semana 4 · Costumbre", "Tu rutina en tres renglones", [
        ("Mañana", "Escribe tu rutina en <b>tres renglones</b>: uno para la "
                   "mañana, uno para la comida, uno para la noche."),
        ("Tarde", "Si no cabe en tres renglones, es demasiado. Quita."),
        ("Noche", "Pégala en el refrigerador."),
    ], "Lo que no cabe en tres renglones no se sostiene un año."),

    (30, "Semana 4 · Costumbre", "Último día — no se estrena nada", [
        ("Todo el día", "Tu rutina de tres renglones. Nada más."),
        ("Tarde", "Palomea el día 30 en el tablero."),
        ("Noche", "Lee la última página de este bono."),
    ], "Treinta días. Ya no estás improvisando tu cuidado todos los días — "
       "y eso era todo el punto."),
]


SEMANAS = [
    (1, "Semana 1 · Días 1 al 7", "Digestión",
     "Empezamos por la sobremesa: ese sueño que te tumba en el sillón después "
     "de comer. Entran <strong>la caminata, la canela, el nopal</strong> y un té "
     "para la noche — de uno en uno, y ninguno de golpe.",
     "canela de Ceilán en raja, 1 nopal, limones, hierbabuena, anís en grano, "
     "y romero fresco con aceite de oliva para dejar macerando el día 3.",
     "sem1"),
    (2, "Semana 2 · Días 8 al 14", "Riñón y sed",
     "Ahora la sed de la noche y tanta ida al baño. Entran <strong>las aguas "
     "del día</strong> y el té de dormir. Regla de esta semana: todo lo que hace "
     "orinar se toma <strong>antes de las 6 de la tarde</strong>.",
     "pepino, apio, chía, flor de jamaica, manzanilla y toronjil.",
     "sem2"),
    (3, "Semana 3 · Días 15 al 21", "Circulación",
     "La semana de los pies y las piernas. Aquí va lo de fuera: baños "
     "<strong>tibios y cortos</strong>, masaje y cataplasma. Y empieza la "
     "costumbre que más vale de todo el reto: <strong>revisarte los pies todas "
     "las noches</strong>.",
     "manzanilla, sal de grano, col (repollo), jengibre y cúrcuma. El aceite "
     "de romero ya lo tienes macerando desde el día 3.",
     "sem3"),
    (4, "Semana 4 · Días 22 al 30", "Costumbre",
     "Nueve días para que esto deje de ser un reto y se vuelva lo normal. "
     "Entran el remedio de las cinco y la primera mistela — y sobre todo, "
     "<strong>escoges los cinco que te vas a quedar</strong>.",
     "clavo de olor, una manzana, y lo que hayas decidido dejar fijo.",
     "sem4"),
]

REPASOS = {
    7: (1, ["¿Cuántos días hiciste la caminata?",
            "¿El sueño de después de comer cambió algo?",
            "¿Algún día te sentiste rara? ¿Qué habías tomado?",
            "¿Qué remedio te costó más trabajo hacer?"]),
    14: (2, ["¿Te levantaste menos veces en la noche?",
             "¿Cómo va la sed de la tarde?",
             "¿Se te olvidó alguna agua? ¿A qué hora se te olvida siempre?",
             "¿Cuánto te dio el azúcar en ayunas esta semana?"]),
    21: (3, ["¿Los pies se sienten distintos en la noche?",
             "¿Cuántos días te revisaste los pies?",
             "¿Encontraste algo en el pie que no habías notado?",
             "¿Las piernas pesan menos al final del día?"]),
    30: (4, ["¿Cuáles cinco remedios sí hiciste casi todos los días?",
             "¿Cuál te hizo la diferencia más clara?",
             "¿Cuál vas a dejar de hacer, con toda honestidad?",
             "¿Ya tienes tu hoja para el médico?"]),
}


def _dias():
    h = []
    semana_actual = 0
    for n, etiqueta, titulo, momentos, gesto in DIAS:
        sem = min((n - 1) // 7 + 1, 4)
        if sem != semana_actual:
            s = SEMANAS[sem - 1]
            h.append(_semana(s[0], s[1], s[2], s[3], s[4], s[5]))
            semana_actual = sem
        h.append(L.dia(n, etiqueta, titulo, momentos, gesto, token=f"d{n:02d}"))
        if n in REPASOS:
            num, preguntas = REPASOS[n]
            h.append(_repaso(num, preguntas, f"repaso{num}"))
    return "".join(h)


# ------------------------------------------------------------------
def _despues():
    h = [L.capitulo("Después del día 30", "Y ahora, ¿qué sigue?",
                    sub="Lo que hace que el mes 2 no sea volver a empezar.",
                    token="despues", nivel=0)]
    h.append(L.entrada(
        "El reto terminó, pero la idea nunca fue que hicieras treinta días y ya. "
        "La idea era que salieras con una rutina que puedas sostener sin "
        "acordarte de este cuaderno."))
    h.append(L.seccion("Las tres cosas que se quedan"))
    h.append(L.numerada([
        "<b>Tus cinco fijos.</b> Los que escogiste el día 26. Esos se hacen "
        "todos los días, y son los únicos que tienen que ser de diario.",
        "<b>La revisión del pie.</b> Un minuto, todas las noches, para siempre. "
        "De todo el reto, esta es la que más te puede ahorrar.",
        "<b>La caminata de los diez minutos.</b> Después de la comida fuerte. "
        "Es gratis y es de lo que más sirve.",
    ]))
    h.append(L.seccion("Cómo rotar sin hacerte bolas"))
    h.append(L.parrafo(
        "Varias hierbas de este libro <b>no se toman todo el año</b>: la "
        "tronadora, la cola de caballo, el boldo, el muicle. Cada ficha te "
        "dice cuántos días y cuánto se descansa. Respétalo."))
    h.append(L.tabla(
        ["Si quieres trabajar", "Cambia de capítulo a"],
        [["El sueño de después de comer", "Capítulo 1 — hay 10 y ya conoces 2"],
         ["La sed y la noche", "Capítulo 2 — prueba el de linaza o el de diente de león"],
         ["Los pies y las piernas", "Capítulo 3 — te faltan la compresa fresca y la ortiga"],
         ["El antojo de la tarde", "Capítulo 4 y el <b>Bono 3</b>, completo"],
         ["La digestión pesada", "Capítulo 5 — el de boldo, máximo 10 días"],
         ["Tener algo listo toda la semana", "Capítulo 6 — las otras cinco mistelas"]]))
    h.append(L.caja(
        "Repite el reto en tres meses",
        "<p>Cuando sientas que se te cayó la rutina — y se te va a caer alguna "
        "semana, a todas se nos cae — vuelve a empezar este cuaderno desde el "
        "día 1. Con lo que ya sabes, la segunda vuelta se hace sola.</p>",
        "suave"))
    return "".join(h)


def cuerpo(paginas):
    return _como() + _dias() + _despues()


def final():
    return L.cierre(
        "Treinta días<br>acompañada",
        "<p>Cuando empezaste, cuidarte era tomar la pastilla y medirte. "
        "Hoy tienes una rutina de mañana, comida y noche, y sabes por qué "
        "hace cada cosa.</p>"
        "<p>No te quedes con los treinta días. Quédate con <strong>tus cinco "
        "fijos</strong>, con <strong>la revisión del pie</strong> y con "
        "<strong>la caminata</strong>. Lo demás está en el libro cuando lo necesites.</p>"
        "<p>Y no se te olvide lo único que no cambia: <strong>la pastilla no "
        "se toca</strong>, y lo que tomas todos los días se le dice al médico.</p>"
        '<p class="firma">— Abuela Mei</p>')
