# -*- coding: utf-8 -*-
"""
Recetario del Corazón — presión y colesterol.

Order bump de Azúcar en Equilibrio. Mismo público, misma casa: la mujer
que compra el libro del azúcar casi siempre tiene también la presión
vigilada, o vive con quien la tiene.

Criterios, más estrictos que en el libro del azúcar:
  · La presión alta NO SE SIENTE. Por eso el capítulo de seguridad abre
    con medir, no con tomar. Un té que "cae bien" no dice nada.
  · Fuera el orozuz (regaliz), por tradicional que sea: sube la presión
    y tira el potasio. Es la planta que más daño podría hacer aquí.
  · Fuera la toronja de las recetas, y con aviso propio: choca con las
    estatinas y con el amlodipino, que es justo lo que toma este público.
  · Toda planta que baja la presión por su cuenta lleva escrito que se
    suma a la medicina. Es el accidente más probable de este libro.
  · Fuera efedra, naranja amarga y cualquier cosa que acelere el corazón.
"""

import libro as L

META = dict(
    slug="corazon",
    archivo="Recetario-del-Corazon.pdf",
    titulo_pdf="Recetario del Corazón — Presión y Colesterol",
    autor="Abuela Mei",
    asunto="24 remedios caseros de uso tradicional para acompañar el cuidado "
           "de la presión y de la grasa en la sangre. No sustituye tratamiento médico.",
    claves="presión alta, hipertensión, colesterol, triglicéridos, jamaica, "
           "ajo, avena, nopal, remedios caseros, México",
    pie="Recetario del Corazón",
)


def portada():
    return L.portada(
        sello="Recetario de la Abuela Mei",
        titulo_html="Recetario<br><span>del Corazón</span>",
        sub="Presión y grasa en la sangre. Veinticuatro remedios de los de "
            "antes, con su dosis, su hora y a quién no le tocan.",
        cuenta="24 REMEDIOS · 4 CAPÍTULOS",
        autor="de la Abuela Mei",
        hoja="&#10084;",
    )


# ══════════════════════════════════════════════════════════════════
CAPITULOS = [
    dict(
        num="Capítulo 1", token="c1",
        titulo="Cuando la presión anda alta",
        sub="Aguas y tés de todos los días. Ninguno baja la presión de golpe — "
            "eso no existe en la cocina — pero acompañan al que sí lo hace.",
        cuantos="7 remedios",
        intro=[
            "La presión alta no duele, mija, y ese es todo el problema. Uno se siente "
            "igual de bien con 120 que con 160, y por eso hay quien deja la pastilla "
            "cuando se siente bien. No lo hagas.",
            "Lo de este capítulo es de <b>diario y sin prisa</b>. Se toma semanas, no tardes. "
            "Y todo lo de aquí <b>se suma</b> a tu medicina: si tomas losartán, enalapril, "
            "amlodipino o algún diurético, mídete más seguido la primera semana.",
        ],
        remedios=[
            dict(n=1, nombre="Agua de jamaica de todos los días",
                 tipo="Agua · fría o al tiempo",
                 para="Para acompañar el cuidado de la presión, en lugar del refresco de la comida.",
                 ingredientes=["Un puño chico de <b>flor de jamaica</b> seca (unos 10 g)",
                               "1 litro de agua",
                               "Nada de azúcar. Ni piloncillo, ni miel."],
                 preparacion=["Hierve el litro de agua y apágalo.",
                              "Echa la jamaica, tapa y déjala 10 minutos.",
                              "Cuela y déjala enfriar. Se guarda 2 días en el refrigerador.",
                              "Si te sabe muy ácida, alárgala con más agua, no con dulce."],
                 dosis="2 vasos al día (500 ml). Cursos de 3 semanas con 1 de descanso.",
                 hora="Uno con la comida y otro a media tarde.",
                 advertencia="La jamaica <b>baja la presión de verdad</b>, y por eso hay que "
                             "tratarla con respeto: se suma a tu medicina. Si tomas "
                             "hidroclorotiazida, losartán o enalapril, empieza con un vaso al "
                             "día y mídete. No la tomes si andas con la presión baja, si estás "
                             "embarazada o dando pecho. Endulzada pierde el chiste y te sube "
                             "el azúcar: en esta casa la jamaica va sin azúcar."),
            dict(n=2, nombre="Té de hoja de olivo",
                 tipo="Té · caliente",
                 para="Para los días en que la presión anda por arriba de tu número de siempre.",
                 ingredientes=["1 cucharadita de <b>hoja de olivo</b> seca",
                               "1 taza de agua (250 ml)"],
                 preparacion=["Calienta el agua hasta que empiece a soltar burbujas y apágala.",
                              "Echa la hoja, tapa y deja 8 minutos.",
                              "Cuela y tómala tibia."],
                 dosis="1 taza al día. Máximo 3 semanas seguidas.",
                 hora="A media mañana, lejos de la pastilla — una hora antes o dos después.",
                 advertencia="Se suma a la medicina de la presión y también le baja tantito al "
                             "azúcar: si tomas las dos cosas, vigila los dos números. No en "
                             "embarazo. Si te sientes mareada al levantarte, suspéndelo y "
                             "avísale a tu médico: puede ser la presión demasiado baja."),
            dict(n=3, nombre="Agua de apio, pepino y perejil",
                 tipo="Agua · fría",
                 para="Para el día siguiente de la carne asada, cuando amaneces hinchada.",
                 ingredientes=["2 tallos de <b>apio</b> con sus hojas",
                               "½ <b>pepino</b> con cáscara",
                               "Una ramita de <b>perejil</b>",
                               "1 litro de agua", "Jugo de ½ limón"],
                 preparacion=["Lava todo bien y pícalo grueso.",
                              "Licúalo con la mitad del agua.",
                              "Cuela, agrégale el resto del agua y el limón.",
                              "Tómala el mismo día."],
                 dosis="1 litro repartido en el día. No más de 3 días seguidos.",
                 hora="Desde la mañana hasta media tarde. De noche no, o te levanta al baño.",
                 advertencia="El apio y el perejil te hacen orinar más y llevan potasio. Si "
                             "tomas <b>espironolactona, losartán o enalapril</b>, el potasio se "
                             "te puede juntar de más: no hagas esta agua sin preguntarle a tu "
                             "médico. Nada de esto si tienes <b>problema del riñón</b>. El "
                             "perejil en cantidad no va en embarazo."),
            dict(n=4, nombre="Té de tila y azahar de la noche",
                 tipo="Té · caliente",
                 para="Para los días de coraje o de susto, cuando sientes el corazón golpeando.",
                 ingredientes=["1 cucharadita de <b>flor de tila</b>",
                               "½ cucharadita de <b>flor de azahar</b>",
                               "1 taza de agua"],
                 preparacion=["Hierve el agua y apágala.",
                              "Echa las flores, tapa y deja 7 minutos.",
                              "Cuela. Tómalo sin azúcar."],
                 dosis="1 taza. Hasta 2 al día en días difíciles.",
                 hora="Una hora antes de acostarte, o en el momento del disgusto.",
                 advertencia="Da sueño. No lo tomes si vas a manejar. Si usas pastillas para "
                             "dormir, para los nervios o clonazepam, se suman y te dejan "
                             "atontada al día siguiente: no los junten. El corazón acelerado "
                             "con dolor de pecho o falta de aire <b>no es para un té</b>: es "
                             "urgencia, llama al 911."),
            dict(n=5, nombre="Ajo macerado en limón",
                 tipo="Preparado · en frío",
                 para="Para acompañar el cuidado de la presión y de la grasa, a diario.",
                 ingredientes=["1 <b>diente de ajo</b> chico, crudo",
                               "Jugo de 1 limón", "1 cucharada de agua"],
                 preparacion=["Machaca el ajo y déjalo reposar 10 minutos al aire: ahí se forma lo bueno.",
                              "Mézclalo con el jugo de limón y el agua.",
                              "Tómatelo de un trago y come algo enseguida."],
                 dosis="1 diente al día. Nunca más de dos.",
                 hora="Después del desayuno, con el estómago ya con algo.",
                 advertencia="El ajo crudo <b>adelgaza la sangre</b>. Si tomas warfarina, "
                             "clopidogrel o aspirina diaria, no lo hagas sin avisarle a tu "
                             "médico. <b>Suspéndelo 7 días antes de cualquier cirugía o "
                             "extracción de muela.</b> En ayunas irrita; por eso va después "
                             "de comer algo."),
            dict(n=6, nombre="Té de flor de espino blanco",
                 tipo="Té · caliente",
                 para="Para acompañar al corazón cansado, cuando el médico ya te lo revisó.",
                 ingredientes=["1 cucharadita de <b>flor y hoja de espino blanco</b>",
                               "1 taza de agua"],
                 preparacion=["Hierve el agua, apágala y echa la planta.",
                              "Tapa 10 minutos. Cuela.",
                              "Tómalo tibio, despacio."],
                 dosis="1 taza al día. Cursos de 3 semanas con 1 de descanso.",
                 hora="A media tarde.",
                 advertencia="Este no es un té para andar probando. Si tomas <b>digoxina</b>, "
                             "no lo tomes: se potencian y eso es peligroso de verdad. Se suma "
                             "también a la medicina de la presión. Si te falta el aire al "
                             "caminar o se te hinchan los pies, eso es consulta, no cocina."),
            dict(n=7, nombre="Agua de chía con limón",
                 tipo="Agua · fría",
                 para="Para sustituir el refresco sin extrañarlo, todos los días.",
                 ingredientes=["1 cucharada de <b>chía</b>", "1 litro de agua",
                               "Jugo de 1 limón"],
                 preparacion=["Pon la chía en el agua y déjala 20 minutos hasta que se hinche.",
                              "Agrega el limón y revuelve.",
                              "Tómala a lo largo del día."],
                 dosis="1 litro al día.",
                 hora="Cuando te dé sed. Es la del diario.",
                 advertencia="Tómala con agua suficiente o se te atora: la chía crece. Si "
                             "tomas medicina, deja una hora de distancia — la fibra se lleva "
                             "parte de lo que tragas. No si tienes problema para pasar los "
                             "alimentos."),
        ]),
    dict(
        num="Capítulo 2", token="c2",
        titulo="Para la grasa en la sangre",
        sub="Colesterol y triglicéridos. Aquí la fibra y la paciencia hacen más "
            "que cualquier planta de fama.",
        cuantos="6 remedios",
        intro=[
            "De esto te enteras por un papel, no por cómo te sientes. Y como no duele, "
            "se deja. Luego pasan diez años.",
            "Lo de este capítulo es lento y aburrido, y así funciona: lo que hace bajar la "
            "grasa no es un té milagroso, es <b>fibra todos los días</b> y menos fritura. "
            "Los remedios ayudan; el plato manda.",
        ],
        remedios=[
            dict(n=8, nombre="Agua de avena con canela en ayunas",
                 tipo="Agua · al tiempo",
                 para="Para el colesterol, de diario y por meses. Es el más importante del capítulo.",
                 ingredientes=["3 cucharadas de <b>avena entera</b> (la de hojuela, no la instantánea)",
                               "1 raja chica de <b>canela de Ceilán</b>",
                               "1 litro de agua"],
                 preparacion=["Remoja la avena con la canela en el litro de agua toda la noche.",
                              "En la mañana licúa todo y cuela, o tómala sin colar si la aguantas.",
                              "No le pongas azúcar. Si acaso, una pizca de vainilla."],
                 dosis="1 vaso (250 ml) en ayunas, todos los días. El resto, en el día.",
                 hora="En ayunas, antes del desayuno.",
                 advertencia="Este es de los que sí se toman siempre, sin descanso. La fibra "
                             "se lleva parte de la medicina que tomes a la misma hora: deja "
                             "<b>una hora</b> entre esta agua y tus pastillas. La canela de "
                             "Ceilán baja tantito el azúcar, así que se suma a tu medicina "
                             "del azúcar. Que sea de Ceilán, no cassia."),
            dict(n=9, nombre="Té de alcachofa",
                 tipo="Té · caliente · amargo",
                 para="Para las comidas pesadas y para acompañar el cuidado de la grasa.",
                 ingredientes=["1 cucharadita de <b>hoja de alcachofa</b> seca",
                               "1 taza de agua"],
                 preparacion=["Hierve el agua y apágala.",
                              "Echa la hoja, tapa y deja 10 minutos.",
                              "Cuela. Es amargo de verdad: no lo endulces, acostúmbrate."],
                 dosis="1 taza al día. Cursos de 3 semanas con 1 de descanso.",
                 hora="20 minutos antes de la comida fuerte.",
                 advertencia="No lo tomes si tienes <b>piedras en la vesícula</b> o el "
                             "conducto tapado: mueve la bilis y te puede provocar un cólico. "
                             "Tampoco si eres alérgica a la manzanilla o al girasol — son de "
                             "la misma familia."),
            dict(n=10, nombre="Nopal en ayunas, licuado",
                 tipo="Licuado · sin colar",
                 para="Para la grasa y el azúcar a la vez. El de siempre, bien hecho.",
                 ingredientes=["1 <b>nopal</b> chico, crudo, sin espinas",
                               "1 vaso de agua", "Jugo de ½ limón",
                               "Opcional: una ramita de perejil"],
                 preparacion=["Lava el nopal y córtalo en cuadros.",
                              "Licúalo con el agua y el limón.",
                              "<b>No lo cueles</b>: lo que sirve es la baba y la fibra.",
                              "Tómatelo luego luego, antes de que se ponga espeso."],
                 dosis="1 vaso en ayunas. Todos los días si quieres.",
                 hora="En ayunas, 20 minutos antes del desayuno.",
                 advertencia="El nopal <b>baja el azúcar</b>: si tomas metformina, "
                             "glibenclamida o insulina, se suma. La primera semana mídete "
                             "antes del desayuno y a media mañana. Deja una hora entre el "
                             "nopal y tus pastillas, que la fibra se las lleva. Si te da "
                             "flojera del estómago, empieza con medio vaso."),
            dict(n=11, nombre="Linaza molida del diario",
                 tipo="Preparado · frío",
                 para="Para el colesterol y para el estreñimiento, que suelen andar juntos.",
                 ingredientes=["1 cucharada de <b>linaza</b>, molida en el momento",
                               "1 vaso grande de agua (300 ml)"],
                 preparacion=["Muele la linaza en el molinillo del café o en la licuadora seca.",
                              "Échala al vaso de agua y revuelve.",
                              "Tómatela enseguida, antes de que se ponga gelatina.",
                              "Después, otro vaso de agua sola."],
                 dosis="1 cucharada al día. Puedes subir a 2 después del primer mes.",
                 hora="Con el desayuno.",
                 advertencia="<b>Molida y del día</b>: entera pasa de largo y guardada se "
                             "enrancia. Siempre con agua de sobra — sin agua suficiente "
                             "estriñe en vez de ayudar. Deja una hora de distancia con "
                             "cualquier medicina. Nada de linaza si tienes obstrucción "
                             "intestinal o problema para pasar alimentos."),
            dict(n=12, nombre="Té de diente de león",
                 tipo="Té · caliente · amargo",
                 para="Para los días de comida grasosa y para la digestión pesada.",
                 ingredientes=["1 cucharadita de <b>hoja y raíz de diente de león</b>",
                               "1 taza de agua"],
                 preparacion=["Hierve el agua y apágala.",
                              "Echa la planta, tapa y deja 10 minutos.",
                              "Cuela y tómalo tibio."],
                 dosis="1 taza al día. Cursos de 2 semanas con 1 de descanso.",
                 hora="Media hora después de la comida del mediodía.",
                 advertencia="Te hace orinar más y lleva potasio: si tomas diurético, "
                             "losartán, enalapril o espironolactona, pregúntale a tu médico "
                             "antes. No con piedras en la vesícula. No si eres alérgica a la "
                             "manzanilla o al girasol."),
            dict(n=13, nombre="Leche dorada de cúrcuma",
                 tipo="Bebida · caliente",
                 para="Para las noches de cuerpo pesado, después de semanas de comer mal.",
                 ingredientes=["1 taza de leche o bebida vegetal sin azúcar",
                               "½ cucharadita de <b>cúrcuma</b> en polvo",
                               "Una <b>pizca de pimienta negra</b> (sin ella no sirve)",
                               "Una rodajita de jengibre"],
                 preparacion=["Calienta la leche con la cúrcuma, la pimienta y el jengibre.",
                              "No la dejes hervir: apenas que suelte vapor.",
                              "Revuelve bien y tómala tibia."],
                 dosis="1 taza al día. Máximo 4 veces por semana.",
                 hora="Después de cenar.",
                 advertencia="La cúrcuma en cantidad <b>adelgaza la sangre</b>: nada de esto "
                             "si tomas warfarina o clopidogrel, y suspéndela una semana antes "
                             "de una cirugía. No con piedras en la vesícula. En esta cantidad "
                             "de cocina es segura; las cápsulas concentradas son otra cosa y "
                             "esas no las recomiendo."),
        ]),
    dict(
        num="Capítulo 3", token="c3",
        titulo="Para las piernas y la circulación",
        sub="Lo de afuera: baños, compresas y masajes. Se sienten el mismo día, "
            "y por eso son los que más se repiten.",
        cuantos="5 remedios",
        intro=[
            "Cuando la sangre no corre bien, las piernas avisan primero: pesadas a las "
            "seis de la tarde, la marca del calcetín marcada, el hormigueo.",
            "Casi todo lo de este capítulo va <b>por fuera</b>. Eso lo hace más seguro "
            "—no se mezcla con tus pastillas— pero también significa que si hay una llaga, "
            "una herida que no cierra o una pierna caliente y roja, <b>eso es médico hoy</b>, "
            "no compresa.",
        ],
        remedios=[
            dict(n=14, nombre="Baño de pies con romero y sal",
                 tipo="Externo · noche",
                 para="Para las piernas pesadas del final del día.",
                 ingredientes=["Un puño de <b>romero</b> fresco o seco",
                               "2 litros de agua", "2 cucharadas de sal de grano"],
                 preparacion=["Hierve el romero en los 2 litros, 5 minutos. Apaga y tapa 10.",
                              "Vacíalo en una cubeta y agrégale la sal.",
                              "Deja que se entibie hasta que aguantes la mano.",
                              "Mete los pies 15 minutos. Sécalos bien, sobre todo entre los dedos."],
                 dosis="15 minutos. Hasta 4 veces por semana.",
                 hora="En la tarde-noche, con las piernas ya cansadas.",
                 advertencia="<b>Si tienes diabetes, el agua va tibia, nunca caliente</b>, y "
                             "la pruebas con el codo, no con el pie: si tienes el pie dormido "
                             "no vas a sentir que te quema. Revisa que no haya heridas antes "
                             "de meterlos. Si hay llaga, uña encarnada o piel abierta, no "
                             "metas el pie: ve a que te lo vean."),
            dict(n=15, nombre="Compresa fría de hamamelis",
                 tipo="Externo · compresa",
                 para="Para las várices que arden y las piernas hinchadas de estar parada.",
                 ingredientes=["1 cucharada de <b>hamamelis</b> (hoja seca)",
                               "1 taza de agua", "Un lienzo de algodón"],
                 preparacion=["Hierve el agua, apaga y echa el hamamelis. Tapa 15 minutos.",
                              "Cuela y mete la taza al refrigerador hasta que esté bien fría.",
                              "Empapa el lienzo y póntelo sobre la pierna, de abajo hacia arriba.",
                              "Déjalo 15 minutos, con la pierna en alto."],
                 dosis="15 minutos. Hasta 4 veces por semana.",
                 hora="En la tarde, cuando más pesan.",
                 advertencia="Solo por fuera y solo sobre piel sana. Si la pierna está "
                             "<b>roja, caliente y dura</b>, o si te duele una sola pantorrilla "
                             "de repente, eso no es várice cansada: puede ser un coágulo. "
                             "<b>Urgencia médica el mismo día.</b>"),
            dict(n=16, nombre="Té de jengibre con limón",
                 tipo="Té · caliente",
                 para="Para los días fríos y las manos heladas.",
                 ingredientes=["3 rodajitas de <b>jengibre</b> fresco",
                               "1 taza de agua", "Jugo de ½ limón"],
                 preparacion=["Hierve el agua con el jengibre 5 minutos, a fuego bajo.",
                              "Apaga y deja reposar 5 minutos.",
                              "Cuela y échale el limón ya servido."],
                 dosis="1 taza al día. Máximo 2 en días fríos.",
                 hora="A media mañana o a media tarde.",
                 advertencia="El jengibre <b>adelgaza la sangre</b>: con warfarina, "
                             "clopidogrel o aspirina diaria, pregúntale a tu médico. "
                             "Suspéndelo una semana antes de cirugía. En cantidad puede "
                             "subir tantito la presión en algunas personas: si la traes "
                             "descontrolada, déjalo para después."),
            dict(n=17, nombre="Aceite de romero para las piernas",
                 tipo="Externo · masaje",
                 para="Para dar movimiento a la pierna cansada, de abajo hacia arriba.",
                 ingredientes=["Un puño de <b>romero</b> seco",
                               "1 taza de aceite de oliva o de almendras"],
                 preparacion=["Pon el romero en un frasco y cúbrelo con el aceite.",
                              "Déjalo 15 días en un lugar oscuro, agitándolo cada tercer día.",
                              "Cuela y guárdalo en frasco de vidrio, tapado.",
                              "Para usarlo: una cucharadita, y masajea siempre <b>del pie hacia la rodilla</b>."],
                 dosis="Una cucharadita por pierna. Diario si quieres.",
                 hora="En la noche, antes de acostarte.",
                 advertencia="Solo por fuera, nunca se toma. Prueba primero en el antebrazo "
                             "y espera un día, por si te irrita. No lo pongas sobre várices "
                             "muy abultadas, heridas ni piel rota. En embarazo, mejor no."),
            dict(n=18, nombre="Las piernas en la pared",
                 tipo="Gesto · sin ingredientes",
                 para="Para deshinchar al final del día. No cuesta nada y es el que más sirve.",
                 ingredientes=["Una pared", "Un cojín para la cadera"],
                 preparacion=["Acuéstate de lado junto a la pared, con la cadera pegada.",
                              "Gírate y sube las piernas por la pared, rectas.",
                              "Pon el cojín bajo la cadera. Los brazos a los lados.",
                              "Respira despacio. Para bajar, dóblalas y rueda de lado."],
                 dosis="10 a 15 minutos.",
                 hora="En la noche, antes de dormir.",
                 advertencia="Si te mareas al subir las piernas, bájalas despacio. No lo "
                             "hagas si tienes glaucoma, presión muy alta sin control, o si "
                             "el médico te dijo que no bajes la cabeza. Si te falta el aire "
                             "acostada, eso se consulta."),
        ]),
    dict(
        num="Capítulo 4", token="c4",
        titulo="Después de la sal y de la fiesta",
        sub="Lo que se hace al día siguiente de la carne asada, del bautizo o de "
            "la posada. No repara — acompaña mientras el cuerpo se acomoda.",
        cuantos="6 remedios",
        intro=[
            "Nadie come bien los 365 días, y el que te diga que sí, miente. Hay bautizo, "
            "hay posada, hay el domingo de carne asada.",
            "Esto no es castigo ni reparación milagrosa. Es lo que hago yo el lunes: "
            "<b>agua, verde y descanso de sal</b>. Y me vuelvo a medir el martes, no el mismo "
            "lunes, porque el día después siempre sale peor y una se asusta de más.",
        ],
        remedios=[
            dict(n=19, nombre="Agua de pepino con menta del día después",
                 tipo="Agua · fría",
                 para="Para el lunes de la carne asada, cuando amaneciste hinchada y con sed.",
                 ingredientes=["1 <b>pepino</b> con cáscara", "Unas hojas de <b>hierbabuena</b>",
                               "1.5 litros de agua", "Jugo de 1 limón"],
                 preparacion=["Rebana el pepino y échalo al agua con la hierbabuena.",
                              "Déjalo 2 horas en el refrigerador.",
                              "Agrega el limón antes de tomarla."],
                 dosis="1.5 litros en el día.",
                 hora="Desde que te levantas hasta las seis de la tarde.",
                 advertencia="Si tienes <b>problema del riñón</b> o el médico te limitó los "
                             "líquidos, no tomes tanta agua: pregúntale primero. Nada de esto "
                             "arregla el exceso de sal de ayer; solo acompaña."),
            dict(n=20, nombre="Caldo de verduras sin sal",
                 tipo="Caldo · caliente",
                 para="Para la cena del día siguiente, cuando el cuerpo pide algo tibio.",
                 ingredientes=["Calabacita, zanahoria, apio, cebolla y ajo",
                               "1.5 litros de agua", "Hierbabuena o perejil al servir",
                               "<b>Sin sal.</b> El sabor va del ajo y del apio"],
                 preparacion=["Pica todo grueso y ponlo a hervir 25 minutos.",
                              "Apaga y deja reposar tapado 10 minutos.",
                              "Sirve con la hierba fresca encima y unas gotas de limón."],
                 dosis="1 plato hondo.",
                 hora="En la cena.",
                 advertencia="Si tomas diurético o tienes el riñón delicado, no le pongas "
                             "sustituto de sal: casi todos son de <b>potasio</b>, y eso sí te "
                             "puede hacer daño con losartán, enalapril o espironolactona. "
                             "Sin sal quiere decir sin sal."),
            dict(n=21, nombre="Té de cola de caballo",
                 tipo="Té · caliente",
                 para="Para los días de retención, cuando el anillo no entra.",
                 ingredientes=["1 cucharadita de <b>cola de caballo</b>", "1 taza de agua"],
                 preparacion=["Hierve el agua, apaga y echa la planta.",
                              "Tapa 10 minutos y cuela."],
                 dosis="1 taza al día. <b>Máximo 5 días seguidos</b>, y luego descansa dos semanas.",
                 hora="En la mañana. Nunca de noche.",
                 advertencia="Este tiene tiempo límite y por eso lo escribí en negritas: usado "
                             "a diario te tira el <b>potasio</b> y la vitamina B1. No lo tomes "
                             "si tienes problema del riñón o del corazón, si tomas diurético, "
                             "en embarazo o lactancia. Si estás hinchada varios días seguidos, "
                             "eso no es para un té: es consulta."),
            dict(n=22, nombre="Agua de limón con bicarbonato",
                 tipo="Agua · al tiempo",
                 para="Para la acidez del día después de la comilona.",
                 ingredientes=["Jugo de ½ limón", "1 vaso de agua",
                               "Una <b>pizca</b> de bicarbonato (la punta de la cuchara)"],
                 preparacion=["Mezcla el limón con el agua.",
                              "Agrega la pizca de bicarbonato y tómatelo mientras hace espuma."],
                 dosis="1 vaso. <b>Una sola vez</b>, no todos los días.",
                 hora="Cuando llega la acidez.",
                 advertencia="El bicarbonato es <b>puro sodio</b>: exactamente lo que no le "
                             "conviene a la presión alta. Por eso va una vez y no se hace "
                             "costumbre. Si tomas medicina para la presión o para el corazón, "
                             "mejor ni eso: pídele a tu médico algo para la acidez. Si te da "
                             "acidez casi diario, eso se revisa."),
            dict(n=23, nombre="Té de manzanilla con anís",
                 tipo="Té · caliente",
                 para="Para el estómago apretado después de comer de más.",
                 ingredientes=["1 cucharadita de <b>manzanilla</b>",
                               "½ cucharadita de <b>anís</b>", "1 taza de agua"],
                 preparacion=["Hierve el agua y apágala.",
                              "Echa las dos plantas, tapa 8 minutos.",
                              "Cuela y tómalo tibio, a sorbos."],
                 dosis="1 taza. Hasta 2 al día.",
                 hora="Media hora después de comer.",
                 advertencia="No si eres alérgica a la manzanilla, al girasol o a la "
                             "ambrosía. El anís en cantidad no va en embarazo. Si el dolor "
                             "de estómago es fuerte, con vómito o no te deja enderezarte, "
                             "eso es médico."),
            dict(n=24, nombre="La caminata de veinte minutos",
                 tipo="Gesto · sin ingredientes",
                 para="Para después de la comida grande. El remedio más subestimado del libro.",
                 ingredientes=["Zapato cómodo", "Veinte minutos"],
                 preparacion=["Sal a caminar entre 15 y 30 minutos después de terminar de comer.",
                              "Paso tranquilo, como si fueras a la tienda. No es ejercicio.",
                              "Si no puedes salir, camina dentro de la casa o ponte de pie a lavar trastes."],
                 dosis="20 minutos. Todos los días que puedas.",
                 hora="Justo después de la comida fuerte.",
                 advertencia="Si te da <b>dolor de pecho, falta de aire o mareo</b> al "
                             "caminar, párate y avísale a tu médico: eso hay que revisarlo "
                             "antes de seguir. Con diabetes, revisa tus pies antes y después, "
                             "y no camines con ampollas ni zapato que talle."),
        ]),
]


# ══════════════════════════════════════════════════════════════════
def _aviso():
    return (
        '<div style="padding-top:6mm">'
        + L.caja(
            "Antes de preparar nada, lee esto",
            "<p>Este recetario es una guía de <b>cuidado casero de uso tradicional</b>. "
            "Es informativo. No es un medicamento, no es una consulta y no sustituye "
            "el diagnóstico ni el tratamiento de tu médico.</p>"
            "<p><b>Nunca suspendas, cambies ni saltes tu medicina</b> de la presión, del "
            "corazón o del colesterol por tomar algo de aquí. Estos remedios "
            "<b>acompañan</b>; no reemplazan y no compiten.</p>"
            "<p>Y hay algo que en este libro pesa más que en el del azúcar: <b>la presión "
            "alta no se siente</b>. Uno anda igual de bien con 120 que con 160. Por eso "
            "aquí no se mide por cómo te sientes — se mide con el aparato.</p>"
            "<p>Si tienes embarazo o lactancia, enfermedad del riñón, del hígado o del "
            "corazón, un trasplante, o una cirugía programada, <b>consulta con tu médico "
            "antes de usar cualquier remedio de este recetario</b>.</p>",
            "alerta")
        + '</div>')


def _carta():
    return (
        L.capitulo("Unas palabras primero", "Lo que sí está en tus manos", token="carta")
        + L.entrada(
            "A mí me lo dijeron a los cincuenta y ocho: la presión alta. Y lo primero que "
            "pensé fue lo que piensa todo el mundo — pero si yo me siento bien.")
        + L.parrafo(
            "Ese es el engaño, mija. La presión no duele. No avisa. Se siente igual de bien "
            "arriba que abajo, y por eso hay tanta gente que deja la pastilla cuando se "
            "siente bien y se entera diez años después, de golpe.")
        + L.parrafo(
            "Así que te lo digo de una vez, antes de que pases a las recetas: <b>la pastilla "
            "no se toca</b>. Nada de este recetario la sustituye. Lo que hay aquí es lo que "
            "hago yo <b>además</b> — el agua de jamaica en lugar del refresco, la avena en "
            "ayunas, la caminata después de comer, el baño de pies cuando las piernas ya "
            "no quieren.")
        + L.parrafo(
            "Son veinticuatro. Ninguno es milagroso y todos son de los de antes. Cada uno "
            "trae su dosis, su hora y <b>a quién no le toca</b> — ese último renglón es el "
            "que más trabajo me costó y el que más te va a servir.")
        + L.parrafo(
            "Escoge uno. Nada más uno para empezar. Y mídete la presión igual que siempre, "
            "que el aparato no miente y una se engaña sola.")
        + L.parrafo('<span class="firma">— Abuela Mei</span>'))


def _seguridad():
    h = [L.capitulo("Lo primero", "Antes que cualquier té", token="seguridad")]

    h.append(L.seccion("Las cuatro reglas de este recetario", token="reglas"))
    h.append(L.numerada([
        "<b>La pastilla no se toca.</b> Ni se salta, ni se baja, ni se cambia de hora "
        "porque hoy tomaste un té.",
        "<b>Un remedio nuevo a la vez</b>, y de día. Si algo te cae mal, así sabes cuál fue.",
        "<b>Mídete con el aparato</b>, no con cómo te sientes. Antes de empezar, y a la "
        "semana. Apunta los números.",
        "<b>Lo que tomas todos los días, se le dice al médico.</b> Aunque sea un té. "
        "Aunque sea natural. Sobre todo si es todos los días.",
    ]))

    h.append(L.seccion("Las señales que piden médico, no té", token="alarma"))
    h.append(L.parrafo(
        "Si aparece cualquiera de estas, esto no es para la cocina. Es urgencia:"))
    h.append(L.caja("Llama al 911 o vete a urgencias",
        L.lista_no([
            "Dolor u opresión en el pecho, aunque se quite",
            "Falta de aire de repente, o al acostarte",
            "Debilidad o entumecimiento de <b>un solo lado</b> del cuerpo",
            "Boca torcida, o que de pronto no te salgan las palabras",
            "Dolor de cabeza muy fuerte y distinto a los de siempre",
            "Ver borroso de golpe, o ver doble",
            "Una pantorrilla roja, caliente y dolorosa",
        ]), "alerta"))

    h.append(L.seccion("Qué no mezclar con tu medicina", token="medicinas"))
    h.append(L.tabla(
        ["Si tomas", "Cuidado con", "Qué hacer"],
        [["<b>Estatinas</b><br>(atorvastatina, simvastatina)",
          "<b>Toronja y su jugo</b>",
          "Ni un vaso. La toronja hace que la estatina se te acumule y puede dañarte el "
          "músculo. Es la mezcla más peligrosa de este recetario y por eso la toronja "
          "no aparece en ninguna receta."],
         ["<b>Amlodipino, nifedipino</b>",
          "<b>Toronja</b>",
          "Lo mismo: te baja la presión de más."],
         ["<b>Warfarina, clopidogrel<br>o aspirina diaria</b>",
          "Ajo crudo, jengibre, cúrcuma en cantidad",
          "Pregúntale a tu médico antes. Y suspéndelos <b>una semana antes</b> de "
          "cualquier cirugía o extracción de muela."],
         ["<b>Losartán, enalapril,<br>espironolactona</b>",
          "Perejil, apio, diente de león, sustituto de sal",
          "Todos llevan <b>potasio</b> y esas medicinas ya te lo retienen. Juntos, el "
          "potasio alto es peligroso para el corazón. Consulta antes."],
         ["<b>Cualquier medicina<br>de la presión</b>",
          "Jamaica, hoja de olivo, espino blanco, ajo",
          "Se <b>suman</b>. Empieza con la mitad y mídete más seguido la primera semana."],
         ["<b>Digoxina</b>", "Espino blanco, cola de caballo",
          "No los tomes. Aquí sí es un no rotundo."],
         ["<b>Diuréticos</b><br>(furosemida, hidroclorotiazida)",
          "Cola de caballo, diente de león",
          "Se suman y te tiran el potasio. No los juntes."],
        ]))

    h.append(L.seccion("La planta que dejé fuera a propósito", token="fuera"))
    h.append(L.caja("Orozuz (regaliz)",
        "<p>Es de las más tradicionales para la garganta y el estómago, y por eso te lo "
        "aclaro: <b>el orozuz sube la presión y te tira el potasio</b>. Tomado seguido "
        "puede subirla bastante, y a veces no se nota hasta que ya subió.</p>"
        "<p>Por eso no hay ni una receta con orozuz en este recetario, y por eso vale la "
        "pena que revises las etiquetas de los tés de bolsita: viene en muchas mezclas "
        "«digestivas» sin que nadie lo diga fuerte.</p>", "alerta"))

    h.append(L.seccion("Quién no debe usar estos remedios", token="quien_no"))
    h.append(L.lista_no([
        "Embarazo y lactancia — casi ninguno está estudiado ahí",
        "Enfermedad del riñón, aunque sea leve: las aguas con potasio y los diuréticos "
        "de planta son justo lo que no te conviene",
        "Insuficiencia cardiaca en tratamiento, sin hablarlo antes con tu médico",
        "Trasplante de cualquier órgano",
        "Cirugía programada en los próximos 15 días",
        "Niños",
    ]))

    h.append(L.seccion("Cómo empezar sin arriesgar", token="empezar"))
    h.append(L.numerada([
        "Apunta tu presión de hoy, en reposo, sentada y con el brazo apoyado. Ese es tu punto de partida.",
        "Escoge <b>un</b> remedio. El del capítulo que va con lo que hoy te molesta.",
        "Tómalo <b>una semana</b> a la dosis más baja que dice la ficha.",
        "Mídete a los siete días, a la misma hora del primer día.",
        "Si bajó de más, o te mareas al levantarte, suspéndelo y avísale a tu médico.",
        "Solo entonces, si quieres, agrega el segundo.",
    ]))
    return "".join(h)


def _indice(paginas):
    entradas = [
        ("cap", "carta", "Lo que sí está en tus manos"),
        ("cap", "seguridad", "Antes que cualquier té"),
        ("it", "reglas", "Las cuatro reglas de este recetario"),
        ("it", "alarma", "Las señales que piden médico, no té"),
        ("it", "medicinas", "Qué no mezclar con tu medicina"),
        ("it", "fuera", "La planta que dejé fuera a propósito"),
        ("it", "quien_no", "Quién no debe usar estos remedios"),
        ("it", "empezar", "Cómo empezar sin arriesgar"),
        ("grupo", "Los 24 remedios"),
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


def _diario():
    h = [L.capitulo("Para no engañarte sola", "Mi cuaderno de la presión", token="diario")]
    h.append(L.parrafo(
        "Esta es la parte que nadie hace y la que más sirve. Fotocopia esta hoja o cópiala "
        "en un cuaderno. Llévala a la consulta: tu médico va a poder hacer mucho más con "
        "cuatro semanas de números que con un «me siento bien»."))
    h.append(L.tabla(
        ["Fecha", "Hora", "Presión", "Qué tomé hoy", "Cómo me sentí"],
        [["", "", "___ / ___", "", ""] for _ in range(14)]))
    h.append(L.caja("Cómo medirte bien",
        L.numerada([
            "Sentada, cinco minutos quieta antes de medir.",
            "El brazo apoyado, a la altura del corazón. La espalda recargada.",
            "Sin café, sin fumar y sin haber caminado en la última media hora.",
            "Dos veces, con un minuto entre una y otra. Apunta la segunda.",
            "A la misma hora siempre. La de la mañana es la que más dice.",
        ]), "verde"))
    return "".join(h)


def cuerpo(paginas):
    return "".join([_aviso(), _carta(), _indice(paginas), _seguridad(),
                    _cuerpo_remedios(), _diario()])


def final():
    return L.cierre(
        "La presión se cuida<br>los días que te sientes bien",
        "<p>Ya tienes los veinticuatro. No los uses todos — escoge el que va con lo que "
        "hoy te molesta y dale su semana.</p>"
        "<p>Y acuérdate de las cuatro: <strong>la pastilla no se toca</strong>; "
        "<strong>uno nuevo a la vez</strong>; <strong>mídete con el aparato, no con cómo "
        "te sientes</strong>; <strong>lo de todos los días se le dice al médico</strong>.</p>"
        "<p>Empieza mañana. Con uno, y con el aparato a un lado.</p>"
        '<p class="firma">— Abuela Mei</p>')
