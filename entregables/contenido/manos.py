# -*- coding: utf-8 -*-
"""
Manos y Rodillas — dolor de articulaciones.

Order bump de Azúcar en Equilibrio. Mismo público, misma hora del día:
la rodilla que avisa al bajar la escalera y la mano que amanece tiesa.

Criterios propios de este libro:
  · Una articulación ROJA, CALIENTE E HINCHADA de golpe no es artrosis:
    puede ser gota o infección. Va en el triaje, antes de cualquier
    receta, porque una infección articular se trata en horas.
  · El sauce blanco es aspirina de planta. Lleva las mismas prohibiciones
    que la aspirina, escritas completas.
  · El árnica NUNCA se toma. Solo por fuera y sobre piel entera. Es el
    error más común con esta planta.
  · Calor y frío no son intercambiables, y usarlos al revés empeora.
    Tiene su propio cuadro.
  · Con diabetes, cualquier calor se prueba con el codo: el pie dormido
    no avisa cuando se quema.
"""

import libro as L

META = dict(
    slug="manos",
    archivo="Manos-y-Rodillas.pdf",
    titulo_pdf="Manos y Rodillas — Para el dolor de articulaciones",
    autor="Abuela Mei",
    asunto="18 remedios de uso tradicional para acompañar el dolor de manos, "
           "rodillas y espalda. No sustituye tratamiento médico.",
    claves="artrosis, dolor de rodillas, manos tiesas, árnica, jengibre, "
           "cúrcuma, compresas, remedios caseros, México",
    pie="Manos y Rodillas",
)


def portada():
    return L.portada(
        sello="Recetario de la Abuela Mei",
        titulo_html="Manos<br><span>y Rodillas</span>",
        sub="Dieciocho remedios para la mano que amanece tiesa y la rodilla que "
            "avisa al bajar la escalera. Con su dosis, su hora y su advertencia.",
        cuenta="18 REMEDIOS · 3 CAPÍTULOS",
        autor="de la Abuela Mei",
        hoja="&#10051;",
    )


# ══════════════════════════════════════════════════════════════════
CAPITULOS = [
    dict(
        num="Capítulo 1", token="c1",
        titulo="Para las manos que amanecen tiesas",
        sub="Lo de la mañana. Se hace antes de levantarse de la cama, o mientras "
            "se calienta el café.",
        cuantos="6 remedios",
        intro=[
            "La mano tiesa de la mañana es la queja que más me llega. Se afloja en media "
            "hora, pero esa media hora es justo cuando hay que hacer el desayuno.",
            "Lo de aquí es de <b>calor</b>, porque la tiesura de la mañana afloja con calor. "
            "Si la mano está hinchada y caliente, eso es otra cosa y va en el triaje de "
            "la página siguiente.",
        ],
        remedios=[
            dict(n=1, nombre="Baño de manos en agua tibia con sal",
                 tipo="Externo · mañana",
                 para="Para aflojar los dedos antes de empezar el día.",
                 ingredientes=["Un recipiente hondo", "Agua tibia",
                               "2 cucharadas de <b>sal de grano</b>"],
                 preparacion=["Llena el recipiente con agua tibia y disuelve la sal.",
                              "Mete las manos 10 minutos.",
                              "Dentro del agua, abre y cierra los dedos despacio, 20 veces.",
                              "Seca bien y ponte algo de crema."],
                 dosis="10 minutos. Todas las mañanas si quieres.",
                 hora="Al levantarte.",
                 advertencia="<b>Tibia, nunca caliente.</b> Con diabetes, prueba el agua con "
                             "el codo y revisa que no haya heridas ni piel abierta. Si la "
                             "mano está <b>roja e hinchada</b>, no le pongas calor: ve al "
                             "triaje de la página siguiente."),
            dict(n=2, nombre="Compresa de jengibre",
                 tipo="Externo · compresa",
                 para="Para los nudillos que no quieren doblarse.",
                 ingredientes=["Un trozo de <b>jengibre</b> fresco, rallado",
                               "2 tazas de agua", "Un lienzo"],
                 preparacion=["Hierve el jengibre en el agua 10 minutos.",
                              "Cuela y deja enfriar hasta que aguantes la mano.",
                              "Empapa el lienzo, escúrrelo y envuelve la mano.",
                              "Déjalo 15 minutos. Repite si se enfría."],
                 dosis="15 minutos. Hasta 2 veces al día.",
                 hora="En la mañana y en la noche.",
                 advertencia="Solo por fuera. El jengibre irrita en piel delicada: prueba "
                             "primero en el antebrazo y espera un día. No sobre piel rota ni "
                             "sobre articulación caliente. Tibia, no caliente, sobre todo "
                             "con diabetes."),
            dict(n=3, nombre="Aceite de árnica para masaje",
                 tipo="Externo · masaje",
                 para="Para el dolor sordo de los dedos al final del día.",
                 ingredientes=["Un puño de <b>flores de árnica</b> secas",
                               "1 taza de aceite de almendras o de oliva"],
                 preparacion=["Pon el árnica en un frasco y cúbrela con el aceite.",
                              "Déjala 20 días en lugar oscuro, agitando cada tercer día.",
                              "Cuela y guarda en frasco de vidrio, tapado y oscuro.",
                              "Unas gotas por mano, masaje suave dedo por dedo."],
                 dosis="Unas gotas. Hasta 3 veces al día.",
                 hora="Cuando duela.",
                 advertencia="<b>El árnica NUNCA se toma</b>, en ningún preparado, por más "
                             "que te lo digan: por dentro es tóxica. Solo por fuera y solo "
                             "sobre <b>piel entera</b>: nada de heridas, raspones ni piel "
                             "abierta. Si te sale ronchita o comezón, suspéndela. No en "
                             "embarazo. No si eres alérgica al girasol o a la manzanilla."),
            dict(n=4, nombre="Té de cúrcuma con pimienta",
                 tipo="Té · caliente",
                 para="Para acompañar por dentro, de diario y por semanas.",
                 ingredientes=["½ cucharadita de <b>cúrcuma</b> en polvo",
                               "Una <b>pizca de pimienta negra</b> (sin ella no sirve de nada)",
                               "1 taza de agua", "Una rodajita de jengibre"],
                 preparacion=["Hierve el agua con el jengibre 5 minutos.",
                              "Apaga, echa la cúrcuma y la pimienta y revuelve bien.",
                              "Deja reposar 5 minutos. No lo cueles: revuelve y tómalo."],
                 dosis="1 taza al día. Cursos de 3 semanas con 1 de descanso.",
                 hora="Después de la comida.",
                 advertencia="La cúrcuma en cantidad <b>adelgaza la sangre</b>: nada de esto "
                             "con warfarina o clopidogrel, y suspéndela una semana antes de "
                             "cirugía o extracción de muela. No con piedras en la vesícula. "
                             "No en embarazo. Si tomas medicina del azúcar, la cúrcuma puede "
                             "bajarla tantito: mídete la primera semana."),
            dict(n=5, nombre="Los ejercicios de la mano",
                 tipo="Gesto · sin ingredientes",
                 para="Para que la mano no se vaya cerrando con los años.",
                 ingredientes=["Una toalla enrollada", "Diez minutos"],
                 preparacion=["Abre la mano todo lo que puedas y ciérrala despacio. 20 veces.",
                              "Junta la yema del pulgar con cada dedo, uno por uno. 3 vueltas.",
                              "Aprieta la toalla enrollada 5 segundos y suelta. 10 veces.",
                              "Sube y baja la muñeca, sin forzar. 20 veces."],
                 dosis="10 minutos, dos veces al día.",
                 hora="En la mañana y en la tarde.",
                 advertencia="Nunca hasta el dolor. Molestia leve sí, dolor no. Si una "
                             "articulación está <b>caliente e hinchada</b>, ese día no la "
                             "muevas: descánsala y ve el triaje. Si un dedo se te queda "
                             "trabado y truena al abrirlo, eso tiene nombre y tratamiento: "
                             "díselo a tu médico."),
            dict(n=6, nombre="Guantes de dormir",
                 tipo="Gesto · noche",
                 para="Para amanecer con la mano menos tiesa.",
                 ingredientes=["Un par de guantes de algodón, de los delgados",
                               "Crema o el aceite de árnica"],
                 preparacion=["Antes de acostarte, ponte crema o unas gotas de aceite y masajea.",
                              "Ponte los guantes de algodón.",
                              "Duerme con ellos. El calor parejo toda la noche es lo que hace el trabajo."],
                 dosis="Toda la noche.",
                 hora="Al acostarte.",
                 advertencia="Que no aprieten en la muñeca: si te dejan marca o se te "
                             "duermen las manos, quedan flojos o no se usan. Si amaneces con "
                             "los dedos dormidos y hormigueando casi todas las noches, eso "
                             "puede ser el túnel del carpo o el azúcar: se revisa."),
        ]),
    dict(
        num="Capítulo 2", token="c2",
        titulo="Para las rodillas que avisan en la escalera",
        sub="Lo de las piernas. Aquí el peso y el músculo mandan más que "
            "cualquier planta — y eso hay que decirlo.",
        cuantos="6 remedios",
        intro=[
            "La rodilla avisa al bajar, no al subir. Y avisa más en la tarde que en la mañana, "
            "al revés que las manos.",
            "Te lo digo con franqueza, mija: en la rodilla, lo que más sirve es <b>el músculo "
            "del muslo</b>. Ningún emplasto compite con eso. Los remedios de aquí acompañan "
            "mientras haces lo otro.",
        ],
        remedios=[
            dict(n=7, nombre="Compresa de hojas de col",
                 tipo="Externo · emplasto",
                 para="Para la rodilla hinchada y pesada al final del día.",
                 ingredientes=["3 o 4 <b>hojas de col</b> (repollo)", "Una venda o tela de algodón"],
                 preparacion=["Lava las hojas y sécalas. Quítales el tronquito duro del centro.",
                              "Aplástalas con el rodillo hasta que se vean húmedas y flexibles.",
                              "Póntelas a <b>temperatura ambiente</b> sobre la rodilla — ni calientes ni del refrigerador.",
                              "Sujétalas con la tela, sin apretar, y siéntate con la pierna en alto 30 minutos."],
                 dosis="30 minutos. Hasta 4 veces por semana.",
                 hora="En la tarde, cuando la pierna ya está pesada.",
                 advertencia="Solo sobre piel entera. Si la rodilla está <b>roja y caliente</b> "
                             "y te duele al mínimo movimiento, no le pongas nada encima: ve "
                             "el triaje. Si la hinchazón es de las dos piernas y sube hacia "
                             "arriba, eso no es rodilla: se consulta."),
            dict(n=8, nombre="Baño de asiento tibio con romero",
                 tipo="Externo · tarde",
                 para="Para la rodilla y la cadera de los días largos de estar parada.",
                 ingredientes=["Un puño de <b>romero</b>", "3 litros de agua",
                               "Una tina o cubeta grande"],
                 preparacion=["Hierve el romero en los 3 litros, 5 minutos. Tapa y deja 10.",
                              "Vacíalo en la tina y agrega agua tibia hasta que cubra.",
                              "Siéntate con las rodillas dentro 15 minutos.",
                              "Sécate bien y no salgas al frío enseguida."],
                 dosis="15 minutos. Hasta 3 veces por semana.",
                 hora="En la tarde-noche.",
                 advertencia="Tibia, no caliente, y probada con el codo si tienes diabetes. "
                             "Si tienes <b>presión alta sin control</b>, el agua caliente te "
                             "la puede mover: que sea tibia y no más de 15 minutos. No "
                             "sobre várices muy abultadas ni piel abierta."),
            dict(n=9, nombre="Hielo envuelto, de los veinte minutos",
                 tipo="Externo · frío",
                 para="Para después de caminar de más, o del día que te pasaste.",
                 ingredientes=["Hielo o una bolsa de chícharos congelados", "Una toalla delgada"],
                 preparacion=["<b>Envuelve el hielo en la toalla.</b> Nunca directo a la piel.",
                              "Ponlo sobre la rodilla 20 minutos.",
                              "Quítalo al menos una hora antes de volver a ponerlo."],
                 dosis="20 minutos. Hasta 3 veces al día.",
                 hora="Después del esfuerzo, o en la noche si quedó caliente.",
                 advertencia="<b>Veinte minutos y ya.</b> Más tiempo quema la piel igual que "
                             "el calor. Nunca directo. <b>Con diabetes o con el pie dormido, "
                             "no uses hielo sin preguntarle a tu médico</b>: si no sientes, "
                             "no sabes cuándo parar. Tampoco si tienes mala circulación en "
                             "esa pierna."),
            dict(n=10, nombre="Té de harpagofito",
                 tipo="Té · caliente · muy amargo",
                 para="Para las temporadas malas, cuando el dolor no da tregua en días.",
                 ingredientes=["1 cucharadita de <b>harpagofito</b> (garra del diablo)",
                               "1 taza de agua"],
                 preparacion=["Hierve el agua, apaga y echa la raíz.",
                              "Tapa 10 minutos. Cuela.",
                              "Tómalo tibio. Es muy amargo y así se queda."],
                 dosis="1 taza al día. <b>Máximo 3 semanas</b>, luego descansa dos.",
                 hora="Después de la comida, nunca en ayunas.",
                 advertencia="<b>No lo tomes si tienes o tuviste úlcera o gastritis fuerte</b>: "
                             "sube el ácido del estómago. No con warfarina ni clopidogrel. "
                             "No con piedras en la vesícula. No en embarazo. Puede bajar "
                             "tantito el azúcar: si tomas medicina para eso, mídete la "
                             "primera semana. Si tomas medicina del corazón, consulta antes."),
            dict(n=11, nombre="El muslo fuerte: la silla",
                 tipo="Gesto · sin ingredientes",
                 para="Para lo único que de verdad le quita carga a la rodilla.",
                 ingredientes=["Una silla firme, sin ruedas"],
                 preparacion=["Siéntate en la orilla, con los pies bien apoyados.",
                              "Estira una pierna hasta dejarla derecha. Aguanta 5 segundos.",
                              "Bájala despacio, contando tres. Ahí está el trabajo, en la bajada.",
                              "10 veces cada pierna. Descansa y repite otra serie."],
                 dosis="2 series de 10, cada pierna. Cinco días a la semana.",
                 hora="En la mañana o en la tarde, cuando estés fresca.",
                 advertencia="Nunca hasta el dolor. Si la rodilla truena sin doler, está "
                             "bien; si truena <b>y duele</b>, para. Si tienes la rodilla "
                             "hinchada hoy, ese día no toca. Si te operaron o te pusieron "
                             "prótesis, haz lo que te dijo tu rehabilitador, no esto."),
            dict(n=12, nombre="Agua de limón con colágeno de la olla",
                 tipo="Caldo · caliente",
                 para="Para acompañar de adentro, con lo que ya se cocina en casa.",
                 ingredientes=["Huesos con cartílago (espinazo, patita, rodilla de res)",
                               "2 litros de agua", "Un chorrito de vinagre o limón",
                               "Ajo, cebolla y hierbas al gusto", "<b>Poca sal</b>"],
                 preparacion=["Pon los huesos con el agua y el chorrito de vinagre — ayuda a sacar lo bueno.",
                              "Hierve a fuego muy bajo 4 horas, tapado.",
                              "Cuela, deja enfriar y quita la grasa que se junta arriba.",
                              "Guárdalo en el refrigerador. Se usa como base de sopas."],
                 dosis="1 taza al día, o como base de la sopa.",
                 hora="En la comida.",
                 advertencia="<b>Quítale la grasa</b> si cuidas el colesterol: se junta arriba "
                             "cuando se enfría y se retira con la cuchara. Poca sal, sobre "
                             "todo con presión alta. Si tienes problema del riñón, "
                             "pregúntale a tu médico: los caldos largos llevan bastante "
                             "fósforo y potasio."),
        ]),
    dict(
        num="Capítulo 3", token="c3",
        titulo="Calor, frío y lo de todos los días",
        sub="Cuál va cuándo, y los tres gestos que sostienen todo lo demás.",
        cuantos="6 remedios",
        intro=[
            "Esta es la parte que casi todo el mundo hace al revés: calor cuando tocaba frío, "
            "y frío cuando tocaba calor. Y eso no es que no sirva — <b>empeora</b>.",
            "La regla corta: <b>tieso, calor. Hinchado y caliente, frío.</b> Y si tienes dudas, "
            "no le pongas nada y consulta.",
        ],
        remedios=[
            dict(n=13, nombre="Saquito de semillas para el calor seco",
                 tipo="Externo · calor",
                 para="Para la tiesura de la mañana y el dolor sordo sin hinchazón.",
                 ingredientes=["Una funda de tela de algodón, cosida",
                               "2 tazas de arroz o de semillas de linaza",
                               "Opcional: un puño de lavanda seca"],
                 preparacion=["Llena la funda hasta dos terceras partes y cósela cerrada.",
                              "Caliéntala en el microondas <b>1 minuto</b>, no más.",
                              "Pruébala en el antebrazo antes de ponértela.",
                              "Déjala 15 minutos sobre la articulación."],
                 dosis="15 minutos. Hasta 3 veces al día.",
                 hora="En la mañana y cuando duela.",
                 advertencia="<b>Un minuto de microondas, no dos.</b> Pruébala siempre en el "
                             "antebrazo. Con diabetes o con la piel dormida, tibia y con "
                             "una tela en medio: la quemadura de saquito es de las más "
                             "comunes y no se siente hasta después. Nunca te duermas con él "
                             "puesto."),
            dict(n=14, nombre="Cuándo calor y cuándo frío",
                 tipo="Regla · sin ingredientes",
                 para="Para no empeorar lo que quieres aliviar.",
                 ingredientes=["Nada. Solo saber cuál toca"],
                 preparacion=["<b>Tiesa en la mañana, dolor sordo, sin hinchazón</b> → calor tibio, 15 minutos.",
                              "<b>Hinchada, caliente al tacto, después de esfuerzo</b> → frío envuelto, 20 minutos.",
                              "<b>Roja, muy caliente, dolor fuerte de golpe</b> → ni calor ni frío: médico hoy.",
                              "Si no sabes cuál es, empieza por frío: hace menos daño si te equivocas."],
                 dosis="Según el caso.",
                 hora="Cuando haga falta.",
                 advertencia="El error que más veo: ponerle calor a una articulación "
                             "hinchada y caliente. El calor le mete más sangre y la hincha "
                             "más. Si dudas, frío."),
            dict(n=15, nombre="Emplasto de linaza tibia",
                 tipo="Externo · emplasto",
                 para="Para la espalda baja y el hombro agarrotado.",
                 ingredientes=["3 cucharadas de <b>linaza</b> molida", "Agua caliente",
                               "Un lienzo de algodón"],
                 preparacion=["Mezcla la linaza con agua caliente hasta que quede como atole espeso.",
                              "Extiéndela sobre el lienzo, en una capa de un dedo de grueso.",
                              "Deja que se entibie y póntela con el lienzo entre la pasta y la piel.",
                              "Déjala 20 minutos y enjuaga."],
                 dosis="20 minutos. Hasta 3 veces por semana.",
                 hora="En la noche.",
                 advertencia="Tibia, y siempre con la tela entre la pasta y la piel. Nunca "
                             "sobre piel rota. Con diabetes, pruébala con el codo. Si el "
                             "dolor de espalda baja <b>por la pierna</b> hasta el pie, o si "
                             "te cuesta controlar el pipí, eso es urgencia, no emplasto."),
            dict(n=16, nombre="La caminata corta, dos veces al día",
                 tipo="Gesto · sin ingredientes",
                 para="Para la articulación que se oxida de estar quieta.",
                 ingredientes=["Zapato cerrado con suela buena"],
                 preparacion=["Diez minutos en la mañana y diez en la tarde.",
                              "Terreno plano. Nada de cerros ni de escaleras al principio.",
                              "Si duele durante, acorta. Si duele <b>al día siguiente</b>, fue mucho.",
                              "Sube de a dos minutos por semana, no más."],
                 dosis="10 minutos, dos veces al día.",
                 hora="Mañana y tarde.",
                 advertencia="Zapato cerrado y que no talle. <b>Con diabetes, revisa tus "
                             "pies antes y después</b>: una ampolla que no sientes se "
                             "convierte en úlcera. Nunca camines con una rodilla hinchada y "
                             "caliente."),
            dict(n=17, nombre="Los cinco kilos",
                 tipo="Gesto · a largo plazo",
                 para="Para lo que más le quita carga a la rodilla, aunque no sea un té.",
                 ingredientes=["Paciencia"],
                 preparacion=["Cada kilo de menos le quita a la rodilla varias veces ese peso al caminar.",
                              "No es dieta ni es de golpe: es el refresco que se cambia por agua de jamaica.",
                              "Es la caminata de arriba, sostenida.",
                              "Cinco kilos en seis meses es un cambio enorme para una rodilla."],
                 dosis="Sin prisa.",
                 hora="Todos los días, un poquito.",
                 advertencia="Si tomas medicina del azúcar y empiezas a bajar de peso, "
                             "<b>puede que tu dosis te quede grande</b> y te baje el azúcar "
                             "de más: díselo a tu médico para que la ajuste. Nada de dietas "
                             "de moda ni de pastillas para adelgazar."),
            dict(n=18, nombre="Anotar los días malos",
                 tipo="Gesto · cuaderno",
                 para="Para que la consulta sirva de algo.",
                 ingredientes=["Un cuaderno"],
                 preparacion=["Apunta los días que dolió y del 1 al 10 cuánto.",
                              "Apunta qué hiciste ese día y el anterior.",
                              "Apunta qué usaste y si ayudó.",
                              "Llévalo a la consulta. Un mes de apuntes vale más que «me duele seguido»."],
                 dosis="Un renglón al día.",
                 hora="En la noche.",
                 advertencia="Si el dolor va subiendo semana tras semana, si despierta de "
                             "noche, o si viene con fiebre, pérdida de peso o cansancio "
                             "raro, no esperes a la cita de rutina: adelántala."),
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
            "<p><b>Nunca suspendas ni cambies tu medicina</b> por usar algo de aquí.</p>"
            "<p>Dos cosas que en este recetario importan más que en los otros: el "
            "<b>árnica nunca se toma</b> —solo por fuera y sobre piel entera— y una "
            "articulación <b>roja, caliente e hinchada de golpe</b> no es para la cocina. "
            "Las dos tienen su página antes de las recetas.</p>", "alerta")
        + '</div>')


def _triaje():
    h = [L.capitulo("Lo primero", "Cuándo no es para la cocina", token="triaje")]
    h.append(L.parrafo(
        "Casi todo el dolor de articulaciones de nuestra edad es desgaste, y con eso se "
        "vive bien. Pero hay cuadros que se parecen y no lo son."))

    h.append(L.caja("Vete hoy con un médico si",
        L.lista_no([
            "Una articulación se puso <b>roja, caliente e hinchada de golpe</b>, y duele "
            "al mínimo movimiento",
            "Tienes fiebre junto con el dolor de la articulación",
            "El dedo gordo del pie amaneció rojo y no aguanta ni la sábana",
            "Se te hinchó una rodilla sola, sin golpe y en pocas horas",
            "El dolor de espalda baja te corre por la pierna hasta el pie",
            "Te cuesta controlar el pipí o sientes dormida la entrepierna",
            "Perdiste peso sin quererlo, junto con el dolor",
        ]), "alerta"))
    h.append(L.parrafo(
        "Los tres primeros pueden ser gota o una infección dentro de la articulación. "
        "Una infección articular se trata <b>en horas</b>, no en días: ahí no hay compresa "
        "que valga."))

    h.append(L.seccion("El árnica, con todas sus letras", token="arnica"))
    h.append(L.caja("Nunca por dentro",
        "<p>El árnica es de las mejores plantas que hay para el golpe y el dolor "
        "<b>por fuera</b>. Y es tóxica <b>por dentro</b>. No hay té de árnica que valga "
        "la pena, ni en gotas, ni «poquito».</p>"
        "<p>Por fuera: solo sobre <b>piel entera</b>. Nada de heridas, raspones ni piel "
        "abierta. Si te sale comezón o ronchita, suspéndela.</p>", "alerta"))

    h.append(L.seccion("Qué no mezclar con tu medicina", token="medicinas"))
    h.append(L.tabla(
        ["Si tomas", "Cuidado con", "Qué hacer"],
        [["<b>Warfarina, clopidogrel<br>o aspirina diaria</b>",
          "Cúrcuma, jengibre, harpagofito, sauce",
          "Todos adelgazan la sangre y se suman. Consulta antes, y suspéndelos "
          "<b>una semana antes</b> de cirugía o extracción de muela."],
         ["<b>Medicina del azúcar</b>",
          "Cúrcuma, harpagofito",
          "Bajan tantito el azúcar y se suman. Mídete más seguido la primera semana."],
         ["<b>Medicina del corazón<br>o de la presión</b>",
          "Harpagofito",
          "Puede interferir. No lo tomes sin preguntar."],
         ["<b>Antiinflamatorios</b><br>(ibuprofeno, naproxeno)",
          "Harpagofito, sauce blanco",
          "Se suman en el estómago. Juntos suben el riesgo de úlcera y de sangrado."],
        ]))

    h.append(L.seccion("Quién no debe usar estos remedios", token="quien_no"))
    h.append(L.lista_no([
        "Embarazo y lactancia",
        "Úlcera o gastritis fuerte, para los remedios que se toman",
        "Enfermedad del riñón o del hígado, sin consultar",
        "Cirugía programada en los próximos 15 días",
        "Piel abierta o infectada, para todo lo de por fuera",
        "Prótesis de rodilla o cadera reciente: haz lo de tu rehabilitador, no esto",
    ]))
    return "".join(h)


def _indice(paginas):
    entradas = [
        ("cap", "triaje", "Cuándo no es para la cocina"),
        ("it", "arnica", "El árnica, con todas sus letras"),
        ("it", "medicinas", "Qué no mezclar con tu medicina"),
        ("it", "quien_no", "Quién no debe usar estos remedios"),
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


def cuerpo(paginas):
    return "".join([_aviso(), _indice(paginas), _triaje(), _cuerpo_remedios()])


def final():
    return L.cierre(
        "La articulación que se mueve<br>es la que menos duele",
        "<p>De todo lo que hay en estas páginas, lo que más te va a servir no es un "
        "emplasto: es <strong>el muslo fuerte</strong> y <strong>la caminata corta de "
        "dos veces al día</strong>. Los remedios acompañan mientras haces eso.</p>"
        "<p>Y la regla corta, para no equivocarte: <strong>tiesa, calor. Hinchada y "
        "caliente, frío. Roja y de golpe, médico hoy.</strong></p>"
        '<p class="firma">— Abuela Mei</p>')
