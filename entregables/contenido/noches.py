# -*- coding: utf-8 -*-
"""
Las Noches de la Abuela — sueño.

Order bump de Azúcar en Equilibrio. Va con el libro del azúcar por una
razón que la lectora reconoce enseguida: la noche mala le arruina el día
siguiente, y el día siguiente se le nota en el número.

Criterios propios de este libro:
  · Levantarse tres veces a orinar NO es "vejiga de vieja": puede ser el
    azúcar alta o la próstata. Va en el triaje, antes de cualquier té,
    porque si no, este bono la entretiene en vez de ayudarla.
  · Fuera la kava, por famosa que sea: hígado.
  · Toda planta que da sueño lleva escrito que se suma a las pastillas
    para dormir y para los nervios. Es el accidente probable de aquí.
  · Los ronquidos con pausas al respirar tienen su propio recuadro. Eso
    no se arregla con tila.
"""

import libro as L

META = dict(
    slug="noches",
    archivo="Las-Noches-de-la-Abuela.pdf",
    titulo_pdf="Las Noches de la Abuela — Para dormir",
    autor="Abuela Mei",
    asunto="18 remedios y gestos de uso tradicional para acompañar el descanso. "
           "No sustituye tratamiento médico.",
    claves="dormir, insomnio, sueño, tila, pasiflora, azahar, despertares, "
           "remedios caseros, México",
    pie="Las Noches de la Abuela",
)


def portada():
    return L.portada(
        sello="Recetario de la Abuela Mei",
        titulo_html="Las Noches<br><span>de la Abuela</span>",
        sub="Dieciocho remedios y gestos para la hora de acostarse y para la "
            "madrugada, cuando el sueño se va y no vuelve.",
        cuenta="18 REMEDIOS · 3 CAPÍTULOS",
        autor="de la Abuela Mei",
        hoja="&#9790;",
    )


# ══════════════════════════════════════════════════════════════════
CAPITULOS = [
    dict(
        num="Capítulo 1", token="c1",
        titulo="Para cuando el sueño no llega",
        sub="Lo de la hora antes de acostarse. Se toman tibios, despacio y con la "
            "luz ya baja — el té solo hace la mitad del trabajo.",
        cuantos="7 remedios",
        intro=[
            "Te acuestas cansada y en cuanto apagas la luz, la cabeza se prende. La lista "
            "del mandado, lo que dijo tu nuera, la cuenta de la luz.",
            "Estos tés ayudan, pero no te van a noquear. Lo que los hace funcionar es la "
            "<b>media hora de antes</b>: luz baja, teléfono abajo, y el té tibio a sorbos. "
            "Si te lo tomas de un jalón viendo la novela, no cuentes con él.",
        ],
        remedios=[
            dict(n=1, nombre="Té de tila de la Abuela",
                 tipo="Té · caliente",
                 para="Para las noches en que la cabeza no se calla.",
                 ingredientes=["1 cucharadita de <b>flor de tila</b>", "1 taza de agua (250 ml)"],
                 preparacion=["Hierve el agua y apágala.",
                              "Echa la tila, tapa y deja 8 minutos. Tapada, siempre.",
                              "Cuela y tómalo tibio, a sorbos, en 15 minutos."],
                 dosis="1 taza. No más de 2 al día.",
                 hora="45 minutos antes de acostarte.",
                 advertencia="Da sueño de verdad: no lo tomes si vas a manejar o a salir. "
                             "Si usas <b>clonazepam, alprazolam, pastillas para dormir o "
                             "antihistamínicos</b>, se suman y amaneces atontada — no los "
                             "juntes sin preguntarle a tu médico. En embarazo, mejor no."),
            dict(n=2, nombre="Agua de azahar",
                 tipo="Agua · tibia",
                 para="Para los nervios de la noche, cuando el corazón anda apurado.",
                 ingredientes=["½ cucharadita de <b>flor de azahar</b>", "1 taza de agua"],
                 preparacion=["Calienta el agua sin dejarla hervir fuerte.",
                              "Echa el azahar, tapa y deja 7 minutos.",
                              "Cuela. Se toma tibia, casi al tiempo."],
                 dosis="1 taza.",
                 hora="Media hora antes de dormir, o en el momento del susto.",
                 advertencia="Se suma a las pastillas de los nervios y a las de dormir. "
                             "Si el corazón acelerado viene con <b>dolor de pecho, falta de "
                             "aire o mareo</b>, eso no es nervios: es urgencia, llama al 911."),
            dict(n=3, nombre="Té de pasiflora",
                 tipo="Té · caliente",
                 para="Para la noche del día difícil, cuando el cuerpo no se suelta.",
                 ingredientes=["1 cucharadita de <b>pasiflora</b> (flor de la pasión)",
                               "1 taza de agua"],
                 preparacion=["Hierve el agua, apaga y echa la planta.",
                              "Tapa 10 minutos. Cuela.",
                              "Tómalo tibio, sin azúcar."],
                 dosis="1 taza. Máximo 2 semanas seguidas, luego descansa una.",
                 hora="Una hora antes de acostarte.",
                 advertencia="De los que más sueño dan. No con alcohol, ni con pastillas "
                             "para dormir o para los nervios: se potencian. No en embarazo "
                             "ni lactancia. Suspéndela dos semanas antes de una cirugía, "
                             "porque se suma a la anestesia."),
            dict(n=4, nombre="Té de toronjil con manzanilla",
                 tipo="Té · caliente",
                 para="Para cuando el estómago no deja dormir.",
                 ingredientes=["1 cucharadita de <b>toronjil</b> (melisa)",
                               "1 cucharadita de <b>manzanilla</b>", "1 taza de agua"],
                 preparacion=["Hierve el agua y apágala.",
                              "Echa las dos plantas, tapa 8 minutos.",
                              "Cuela y tómalo tibio."],
                 dosis="1 taza. Hasta 2 al día.",
                 hora="Después de la cena, o antes de acostarte.",
                 advertencia="No si eres alérgica a la manzanilla, al girasol o a la "
                             "ambrosía. El toronjil puede interferir con la medicina de la "
                             "<b>tiroides</b>: si tomas levotiroxina, consulta antes. Da "
                             "sueño: se suma a las pastillas de dormir."),
            dict(n=5, nombre="Leche tibia con nuez moscada",
                 tipo="Bebida · caliente",
                 para="Para la noche fría, y para quien no quiere tomar té.",
                 ingredientes=["1 taza de leche o bebida vegetal sin azúcar",
                               "Una <b>pizca muy chica</b> de nuez moscada recién rallada"],
                 preparacion=["Calienta la leche sin dejarla hervir.",
                              "Ralla apenas la nuez moscada encima. Una pizca, no más.",
                              "Tómala tibia, despacio."],
                 dosis="1 taza.",
                 hora="20 minutos antes de acostarte.",
                 advertencia="<b>Una pizca y ya.</b> La nuez moscada en cantidad "
                             "—una cucharadita o más— es tóxica de verdad: da alucinaciones "
                             "y taquicardia. Nunca en embarazo. Si tomas medicina del "
                             "azúcar, recuerda que la leche también la sube: cuéntala."),
            dict(n=6, nombre="Té de lavanda",
                 tipo="Té · caliente",
                 para="Para las noches de dolor de cabeza tensional.",
                 ingredientes=["½ cucharadita de <b>flor de lavanda</b>", "1 taza de agua"],
                 preparacion=["Hierve el agua y apágala.",
                              "Echa la lavanda, tapa 6 minutos. No más, o amarga.",
                              "Cuela y tómalo tibio."],
                 dosis="1 taza al día.",
                 hora="En la noche.",
                 advertencia="Poca cantidad: es intensa. Da sueño y se suma a las pastillas "
                             "de dormir. En embarazo, no. Si el dolor de cabeza es nuevo, "
                             "muy fuerte o distinto a los de siempre, eso se revisa hoy."),
            dict(n=7, nombre="Miel y limón en agua tibia",
                 tipo="Bebida · tibia",
                 para="Para la garganta seca que despierta de madrugada.",
                 ingredientes=["1 cucharadita de <b>miel</b>", "Jugo de ¼ de limón",
                               "1 taza de agua tibia"],
                 preparacion=["Entibia el agua — que la aguantes, no que queme.",
                              "Disuelve la miel y agrega el limón.",
                              "Tómalo despacio."],
                 dosis="1 taza.",
                 hora="Antes de acostarte.",
                 advertencia="<b>La miel es azúcar.</b> Si tomas medicina del azúcar, "
                             "cuéntala como lo que es y no la hagas costumbre diaria. Nada "
                             "de miel para menores de un año. Si la garganta seca es de "
                             "todas las noches y tomas mucha agua y orinas mucho, dilo en "
                             "la consulta: eso puede ser el azúcar."),
        ]),
    dict(
        num="Capítulo 2", token="c2",
        titulo="Para los despertares de madrugada",
        sub="Las tres de la mañana con los ojos abiertos. Lo que sí se hace, y "
            "sobre todo lo que no.",
        cuantos="6 remedios",
        intro=[
            "Te duermes bien y a las tres estás despierta. Y lo peor no es despertarse: "
            "es la hora y media peleando con la almohada.",
            "La regla de este capítulo es rara pero es la que funciona: <b>si llevas veinte "
            "minutos despierta, levántate</b>. Quedarse en la cama peleando le enseña al "
            "cuerpo que la cama es el lugar donde uno se desespera.",
        ],
        remedios=[
            dict(n=8, nombre="La regla de los veinte minutos",
                 tipo="Gesto · sin ingredientes",
                 para="Para no pasar hora y media peleando con la almohada.",
                 ingredientes=["Una silla fuera de la recámara", "Luz bajita"],
                 preparacion=["Si llevas como veinte minutos despierta, levántate. Sin ver el reloj.",
                              "Vete a otro cuarto, con luz bajita. Nada de teléfono ni televisión.",
                              "Siéntate. Toma agua o un té tibio del capítulo 1.",
                              "Regresa a la cama <b>hasta que traigas sueño otra vez</b>."],
                 dosis="Las veces que haga falta.",
                 hora="En la madrugada.",
                 advertencia="Cuidado al levantarte a oscuras: prende una luz. Una caída de "
                             "madrugada a los sesenta años es de las cosas que más cambian "
                             "una vida. Si tomas pastillas para dormir, siéntate en la "
                             "orilla de la cama un minuto antes de pararte."),
            dict(n=9, nombre="Té de valeriana, el de emergencia",
                 tipo="Té · caliente · fuerte",
                 para="Para la madrugada en que ya sabes que no vas a volver a dormir.",
                 ingredientes=["1 cucharadita de <b>raíz de valeriana</b>", "1 taza de agua"],
                 preparacion=["Hierve el agua, apaga y echa la raíz.",
                              "Tapa 10 minutos. Huele feo; así es.",
                              "Cuela y tómalo tibio."],
                 dosis="1 taza. <b>Máximo 2 semanas seguidas</b>, luego descansa dos.",
                 hora="En la madrugada, o una hora antes de acostarte.",
                 advertencia="Es el más fuerte de este recetario. <b>Nunca con alcohol, con "
                             "pastillas para dormir, con clonazepam o alprazolam</b>: se "
                             "potencian y eso sí es peligroso. No manejes al día siguiente "
                             "si amaneces pesada. No en embarazo ni lactancia. Suspéndela "
                             "dos semanas antes de cirugía. A algunas personas les hace lo "
                             "contrario y las despierta: si te pasa, déjala."),
            dict(n=10, nombre="Agua tibia sola, a sorbos",
                 tipo="Agua · tibia",
                 para="Para la boca seca de las cuatro de la mañana.",
                 ingredientes=["Un vaso de agua tibia en el buró"],
                 preparacion=["Déjalo listo antes de acostarte, tapado.",
                              "A sorbos. No de un jalón, o te levanta al baño."],
                 dosis="Medio vaso.",
                 hora="Cuando despiertes con la boca seca.",
                 advertencia="Si te despiertas con <b>mucha sed casi todas las noches</b> y "
                             "orinas más de lo normal, apúntalo y dilo en tu próxima "
                             "consulta. Con diabetes eso suele significar que el azúcar "
                             "anda alta, y eso no se arregla con agua."),
            dict(n=11, nombre="Respiración de cuatro tiempos",
                 tipo="Gesto · sin ingredientes",
                 para="Para bajar el cuerpo cuando la cabeza ya arrancó.",
                 ingredientes=["Nada"],
                 preparacion=["Acostada, una mano en la panza.",
                              "Inhala por la nariz contando cuatro. La panza sube.",
                              "Aguanta contando cuatro.",
                              "Suelta por la boca contando <b>seis</b>. Lo importante es que la salida sea más larga.",
                              "Diez rondas. Si pierdes la cuenta, empieza de nuevo sin regañarte."],
                 dosis="10 rondas. Las que quieras.",
                 hora="En la cama, en cuanto despiertes.",
                 advertencia="Si te marea, vuelve a respirar normal: vas muy rápido o muy "
                             "profundo. Si te falta el aire al estar acostada y tienes que "
                             "sentarte para respirar, <b>eso no es nervios</b>: se revisa."),
            dict(n=12, nombre="Compresa tibia en la nuca",
                 tipo="Externo · compresa",
                 para="Para la nuca dura que no deja acomodarse.",
                 ingredientes=["Un lienzo", "Agua tibia", "Opcional: unas hojas de romero"],
                 preparacion=["Entibia el agua, con el romero si quieres.",
                              "Empapa el lienzo y escúrrelo bien.",
                              "Póntelo en la nuca 10 minutos, acostada de lado."],
                 dosis="10 minutos.",
                 hora="En la madrugada o antes de dormir.",
                 advertencia="Tibia, no caliente. <b>Si tienes diabetes</b>, prueba el agua "
                             "con el codo: con la sensibilidad cambiada puedes quemarte sin "
                             "sentirlo. Nunca sobre piel rota."),
            dict(n=13, nombre="Té de manzanilla suave de madrugada",
                 tipo="Té · tibio",
                 para="Para volver a dormir sin cargar el estómago.",
                 ingredientes=["½ cucharadita de <b>manzanilla</b>", "1 taza de agua"],
                 preparacion=["Agua caliente, no hirviendo.",
                              "Manzanilla, tapa 5 minutos.",
                              "Cuela y tómalo tibio, medio taza si es tarde."],
                 dosis="Media taza a 1 taza.",
                 hora="En la madrugada.",
                 advertencia="No si eres alérgica a la manzanilla, al girasol o a la "
                             "ambrosía. Si tomas warfarina, la manzanilla seguido puede "
                             "sumarse: consulta. No te tomes una taza entera a las cuatro "
                             "o te levanta al baño a las cinco."),
        ]),
    dict(
        num="Capítulo 3", token="c3",
        titulo="Lo que se hace antes de acostarse",
        sub="Sin ingredientes y sin gastar un peso. Es la parte que casi todo el "
            "mundo se salta, y la que más cambia las cosas.",
        cuantos="5 gestos",
        intro=[
            "Te lo digo derecho: si te tomas el té y luego te acuestas con el teléfono en la "
            "mano, el té no tiene la culpa.",
            "Lo de este capítulo no cuesta nada y es lo que sostiene todo lo demás. "
            "<b>Escoge dos</b> y hazlos toda una semana antes de juzgar.",
        ],
        remedios=[
            dict(n=14, nombre="La misma hora, también el domingo",
                 tipo="Gesto · diario",
                 para="Para que el cuerpo sepa cuándo toca. Es el más aburrido y el más efectivo.",
                 ingredientes=["Una hora fija para levantarte"],
                 preparacion=["Escoge la hora de <b>levantarte</b>, no la de acostarte. Esa es la que manda.",
                              "Mantenla los siete días. Sí, también el domingo.",
                              "Si dormiste mal, levántate igual. Ese día vas a estar cansada y esa noche vas a dormir.",
                              "Dale dos semanas antes de opinar."],
                 dosis="Todos los días.",
                 hora="En la mañana.",
                 advertencia="Si trabajas por turnos esto no aplica igual; acomódalo a tu "
                             "turno con la misma idea. Si llevas meses durmiendo mal aunque "
                             "hagas todo bien, eso se consulta: hay causas que no son "
                             "costumbre."),
            dict(n=15, nombre="La última hora sin pantalla",
                 tipo="Gesto · noche",
                 para="Para que la cabeza entienda que ya es de noche.",
                 ingredientes=["Un cargador fuera de la recámara"],
                 preparacion=["Deja el teléfono a cargar en otro cuarto.",
                              "Si lo usas de despertador, compra uno de a veinte pesos.",
                              "Esa última hora: baja las luces, recoge la cocina, plancha, reza, lo que sea.",
                              "Nada de noticias ni de discutir por mensajes."],
                 dosis="Una hora.",
                 hora="La hora antes de acostarte.",
                 advertencia="Si vives sola y necesitas el teléfono cerca por seguridad, "
                             "déjalo boca abajo y en silencio del otro lado del cuarto. La "
                             "idea no es quedarte incomunicada."),
            dict(n=16, nombre="Baño de pies tibio de la noche",
                 tipo="Externo · noche",
                 para="Para jalar el calor de la cabeza a los pies. Suena raro y funciona.",
                 ingredientes=["Agua tibia", "Una cubeta",
                               "Opcional: un puño de <b>lavanda</b> o <b>manzanilla</b>"],
                 preparacion=["Llena la cubeta con agua tibia. Si quieres, echa la hierba.",
                              "Mete los pies 10 minutos, sentada y sin teléfono.",
                              "Sécalos bien, sobre todo entre los dedos.",
                              "Ponte calcetines y vete derecho a la cama."],
                 dosis="10 minutos.",
                 hora="Media hora antes de acostarte.",
                 advertencia="<b>Con diabetes: tibia, nunca caliente</b>, y pruébala con el "
                             "codo. Revisa que no tengas heridas ni uñas encarnadas antes de "
                             "meter los pies, y sécalos muy bien: la humedad entre los dedos "
                             "es donde empiezan los problemas."),
            dict(n=17, nombre="Apuntar lo que da vueltas",
                 tipo="Gesto · noche",
                 para="Para la cabeza que repasa pendientes en cuanto apagas la luz.",
                 ingredientes=["Un cuaderno y un lápiz en el buró"],
                 preparacion=["Antes de acostarte, escribe los pendientes de mañana. Todos.",
                              "No los ordenes ni los resuelvas. Solo sácalos.",
                              "Cierra el cuaderno y déjalo ahí.",
                              "Si despiertas con uno nuevo, préndelo, apúntalo y vuelve a acostarte."],
                 dosis="Cinco minutos.",
                 hora="Antes de acostarte.",
                 advertencia="Si lo que da vueltas es angustia y no pendientes —si traes "
                             "meses de tristeza, o de despertar a las cuatro con el pecho "
                             "apretado— eso no es falta de sueño: <b>eso se habla con un "
                             "médico</b>, y tiene tratamiento."),
            dict(n=18, nombre="La cena de tres horas antes",
                 tipo="Gesto · diario",
                 para="Para no acostarte con el estómago trabajando.",
                 ingredientes=["Una cena ligera"],
                 preparacion=["Cena al menos <b>tres horas</b> antes de acostarte.",
                              "Ligera: nada de frito, nada de picante fuerte, nada de refresco.",
                              "Si te da hambre después, media fruta o un puño de nueces.",
                              "Café y refresco de cola: el último, a las cuatro de la tarde."],
                 dosis="Todos los días.",
                 hora="Tres horas antes de dormir.",
                 advertencia="<b>Si usas insulina o glibenclamida, no te saltes la cena</b> "
                             "para cumplir esta regla: una hipoglucemia de madrugada es "
                             "mucho peor que una noche regular. Habla con tu médico sobre el "
                             "horario que te toca a ti. Si despiertas sudando, temblando o "
                             "con hambre de golpe, mídete el azúcar antes que nada."),
        ]),
]


# ══════════════════════════════════════════════════════════════════
def _aviso():
    return (
        '<div style="padding-top:6mm">'
        + L.caja(
            "Antes de preparar nada, lee esto",
            "<p>Este recetario es una guía de <b>cuidado casero de uso tradicional</b>. "
            "Es informativo. No sustituye el diagnóstico ni el tratamiento de tu médico.</p>"
            "<p><b>Nunca suspendas ni cambies tu medicina</b> por tomar algo de aquí. Y si "
            "ya tomas pastillas para dormir o para los nervios, <b>no las juntes con estos "
            "tés sin preguntarle a tu médico</b>: se suman, y amanecer atontada a los "
            "sesenta años termina en una caída.</p>"
            "<p>Dormir mal de vez en cuando le pasa a todo el mundo. Dormir mal "
            "<b>todas las noches durante meses</b> es otra cosa y tiene tratamiento: eso "
            "se consulta, no se aguanta.</p>", "alerta")
        + '</div>')


def _triaje():
    h = [L.capitulo("Lo primero", "Antes de buscar un té", token="triaje")]
    h.append(L.parrafo(
        "Hay tres cosas que se parecen a «dormir mal» y no lo son. Si te reconoces en "
        "alguna, este recetario no es lo que necesitas hoy — necesitas una consulta, y "
        "después seguimos aquí."))

    h.append(L.caja("Te levantas dos o tres veces a orinar",
        "<p>No es «vejiga de vieja» ni tomar agua en la noche. Con diabetes, "
        "levantarse seguido a orinar suele querer decir que <b>el azúcar anda alta</b>: "
        "el cuerpo la está sacando por ahí.</p>"
        "<p>En los hombres puede ser la próstata. En los dos casos se revisa. "
        "<b>Apunta cuántas veces te levantas por noche durante una semana</b> y llévalo "
        "a la consulta: es el dato que tu médico necesita.</p>", "alerta"))

    h.append(L.caja("Roncas y a veces parece que dejas de respirar",
        "<p>Si alguien de tu casa te ha dicho que roncas fuerte y que <b>haces pausas</b>, "
        "o si amaneces con dolor de cabeza y te duermes de día aunque hayas dormido ocho "
        "horas, eso puede ser apnea del sueño.</p>"
        "<p>La apnea descontrola el azúcar y la presión, y ningún té la toca. Se "
        "diagnostica con un estudio y se trata. Pídelo.</p>", "alerta"))

    h.append(L.caja("Despiertas a las cuatro con el pecho apretado, casi todos los días",
        "<p>Si además traes meses sin ganas de nada, o llorando sin motivo claro, o "
        "pensando que estorbas, eso no es insomnio: la tristeza que dura <b>tiene "
        "tratamiento</b> y no es cosa de carácter ni de fe.</p>"
        "<p>Díselo a tu médico con esas palabras. No te va a juzgar.</p>", "alerta"))

    h.append(L.seccion("Y una advertencia de madrugada", token="hipo"))
    h.append(L.caja("Si despiertas sudando, temblando o con hambre de golpe",
        "<p>Con insulina o glibenclamida, eso puede ser una <b>bajada de azúcar</b> de "
        "madrugada, no un mal sueño.</p>"
        "<p><b>Mídete antes que nada.</b> Si no tienes el aparato a la mano y te sientes "
        "así, toma azúcar de una vez: medio vaso de jugo o tres cucharaditas de azúcar "
        "en agua. Primero el azúcar, después las preguntas. Y cuéntaselo a tu médico, "
        "porque probablemente haya que ajustar algo.</p>", "alerta"))
    return "".join(h)


def _indice(paginas):
    entradas = [
        ("cap", "triaje", "Antes de buscar un té"),
        ("it", "hipo", "Si despiertas sudando o temblando"),
        ("grupo", "Los 18 remedios"),
    ]
    for c in CAPITULOS:
        entradas.append(("cap", c["token"], f'{c["num"]} — {c["titulo"]}'))
        for r in c["remedios"]:
            entradas.append(("it", f'r{r["n"]:02d}', f'{r["n"]:02d}. {r["nombre"]}'))
    return L.indice(entradas, paginas)


def _cuerpo_remedios():
    h = []
    for c in CAPITULOS:
        h.append(L.capitulo(c["num"], c["titulo"], sub=c["sub"],
                            cuantos=c["cuantos"], token=c["token"], nivel=0))
        for p in c["intro"]:
            h.append(L.parrafo(p))
        for r in c["remedios"]:
            h.append(L.remedio(r["n"], r["nombre"], r["tipo"], r["para"],
                               r["ingredientes"], r["preparacion"],
                               r["dosis"], r["hora"], r["advertencia"]))
    return "".join(h)


def _semana():
    h = [L.capitulo("Para ver si sirve", "Mis siete noches", token="semana")]
    h.append(L.parrafo(
        "Una noche buena no prueba nada y una mala tampoco. Apunta siete y mira el "
        "conjunto. Si al cabo de dos semanas no se mueve, llévale esta hoja a tu médico."))
    h.append(L.tabla(
        ["Noche", "Me acosté", "Me dormí como a", "Me desperté", "Qué hice distinto"],
        [[d, "", "", "", ""] for d in
         ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]]))
    return "".join(h)


def cuerpo(paginas):
    return "".join([_aviso(), _indice(paginas), _triaje(),
                    _cuerpo_remedios(), _semana()])


def final():
    return L.cierre(
        "El sueño no se persigue,<br>se le hace lugar",
        "<p>Escoge <strong>un té y un gesto</strong>. No los dieciocho. Dales una semana "
        "completa antes de decidir si sirven.</p>"
        "<p>Y acuérdate de lo que sostiene todo: <strong>la misma hora de levantarte</strong>, "
        "<strong>la última hora sin pantalla</strong>, y <strong>si llevas veinte minutos "
        "despierta, levántate</strong>.</p>"
        "<p>Si después de un mes sigues igual, eso ya no es costumbre. Eso se consulta.</p>"
        '<p class="firma">— Abuela Mei</p>')
