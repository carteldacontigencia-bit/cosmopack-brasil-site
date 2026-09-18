# -*- coding: utf-8 -*-
"""
Los 55 remedios, en el orden en que salen en el libro.

Están agrupados por lo que siente la lectora, no por planta: así es como
ella los busca. Cada ficha tiene siempre los mismos seis campos, y el de
advertencia nunca va vacío — es el que sostiene todo lo demás.

Criterios que se siguieron al escribirlos:
  · Ingredientes de mercado, tianguis o herbolaria mexicana. Nada importado.
  · Dosis conservadoras y por tiempo limitado, no "tómalo siempre".
  · Toda planta con fama de bajar el azúcar lleva escrito que se suma al
    efecto de la medicina. Es el accidente más probable de este libro.
  · Nada de ruda, ajenjo, raíz de tejocote ni hierbas abortivas o de
    toxicidad conocida, por tradicional que sea su fama.
"""

CAPITULOS = [
    # ==========================================================
    dict(
        num="Capítulo 1",
        token="cap1",
        titulo="El sueño que te tumba después de comer",
        sub="Los tés de sobremesa. Se toman con la comida ya en la mesa o "
            "apenas terminando, que es cuando el cuerpo está trabajando de más.",
        cuantos="10 remedios",
        intro=[
            "Este es el capítulo que más me piden. No es flojera, mija, y no es la edad: "
            "es que después de una comida fuerte el cuerpo se queda batallando un buen rato, "
            "y ese sueño pesado de las tres de la tarde es el aviso.",
            "Todo lo de aquí se toma <b>alrededor de la comida</b> — unos antes, otros después. "
            "Fíjate bien en el renglón de la hora, porque en estos remedios la hora importa "
            "tanto como la planta.",
        ],
        remedios=[
            dict(
                n=1,
                nombre="Té de canela de Ceilán de sobremesa",
                tipo="Té · caliente",
                para="Para el sueño y la pesadez de después de la comida fuerte del día.",
                ingredientes=[
                    "1 raja chica de <b>canela de Ceilán</b> (de la que se deshace en capas, no la dura)",
                    "1 taza de agua (250 ml)",
                    "Opcional: 2 gotas de limón",
                ],
                preparacion=[
                    "Pon el agua a hervir con la raja de canela adentro.",
                    "En cuanto suelte el hervor, bájale al mínimo y déjala 5 minutos tapada.",
                    "Apaga y deja reposar otros 5 minutos. Cuela.",
                    "Tómala tibia, a sorbos, sin azúcar ni miel.",
                ],
                dosis="1 taza. Máximo 2 tazas al día, y con la misma raja no más de dos usos.",
                hora="Justo al terminar de comer, o hasta 20 minutos después.",
                advertencia="Que sea <b>canela de Ceilán</b> y no canela cassia (la china, "
                            "dura y de una sola pieza): la cassia trae cumarina y en cantidad "
                            "diaria le pesa al hígado. En el Bono 2 te enseño a distinguirlas en "
                            "el puesto. La canela <b>ayuda a bajar el azúcar</b>, así que si tomas "
                            "metformina, glibenclamida o insulina, se suma a tu medicina: empieza "
                            "con una taza al día y mídete más seguido esa primera semana. "
                            "No la uses en embarazo ni si tomas warfarina.",
            ),
            dict(
                n=2,
                nombre="Té de hoja de guayaba",
                tipo="Té · caliente",
                para="Para la pesadez después de comer y cuando el estómago anda suelto.",
                ingredientes=[
                    "5 hojas de guayaba frescas, o 3 secas",
                    "1 taza de agua (250 ml)",
                ],
                preparacion=[
                    "Lava bien las hojas y estrújalas un poco con la mano para que suelten.",
                    "Hierve el agua, apaga el fuego y echa las hojas.",
                    "Tapa y deja reposar 10 minutos. Cuela.",
                ],
                dosis="1 taza. Hasta 2 al día, por periodos de 15 días con una semana de descanso.",
                hora="Después de la comida principal, y la segunda después de la cena si hace falta.",
                advertencia="La hoja de guayaba <b>baja el azúcar</b> y también puede bajar la "
                            "presión. Si tomas medicina para cualquiera de las dos, se suman: "
                            "mídete y avísale a tu médico que la estás tomando. Si andas estreñida "
                            "te va a estreñir más. No la tomes en embarazo.",
            ),
            dict(
                n=3,
                nombre="Té de hoja de higo",
                tipo="Té · caliente",
                para="Para el bajón de la tarde después de comer, cuando ni las ganas de "
                     "levantarte del sillón te dan.",
                ingredientes=[
                    "2 hojas de higo secas, partidas en pedazos",
                    "2 tazas de agua (500 ml)",
                ],
                preparacion=[
                    "Pon las hojas en el agua fría y lleva a hervor.",
                    "Deja hervir suave 10 minutos.",
                    "Apaga, tapa y reposa 10 minutos más. Cuela.",
                ],
                dosis="½ taza. Máximo 1 taza al día, en periodos de 10 días.",
                hora="Media hora después de la comida del mediodía.",
                advertencia="De las que más <b>bajan el azúcar</b> de este capítulo, así que "
                            "media taza y no más, sobre todo si tomas glibenclamida o insulina. "
                            "La leche blanca del higo fresco <b>quema la piel si te da el sol</b>: "
                            "si cortas hojas del árbol, usa guantes y lávate las manos. "
                            "No en embarazo ni lactancia.",
            ),
            dict(
                n=4,
                nombre="Té de prodigiosa",
                tipo="Té · caliente · amargo",
                para="Para la digestión lenta y la sensación de que la comida se te quedó ahí.",
                ingredientes=[
                    "1 cucharadita de prodigiosa seca (hierba amarga)",
                    "1 taza de agua (250 ml)",
                ],
                preparacion=[
                    "Hierve el agua y apaga.",
                    "Echa la hierba, tapa y deja 7 minutos. No más, porque se pone intomable.",
                    "Cuela y tómala tibia. Es amarga de verdad; ese amargo es el que trabaja.",
                ],
                dosis="1 taza al día. Cursos de 10 días con 10 de descanso.",
                hora="20 minutos <b>antes</b> de la comida principal.",
                advertencia="Es de las hierbas amargas con fama de <b>bajar el azúcar</b>: si "
                            "tomas medicina, vigílate. No la tomes si tienes gastritis o úlcera "
                            "activa, porque el amargo pica. Nada de esto en embarazo.",
            ),
            dict(
                n=5,
                nombre="Agua de nopal con limón",
                tipo="Agua · fría",
                para="Para acompañar la comida fuerte y para el sueño que viene después.",
                ingredientes=[
                    "½ penca de nopal fresco, limpia y en cuadritos",
                    "1 vaso de agua (250 ml)",
                    "El jugo de ½ limón",
                    "Unas hojas de hierbabuena",
                ],
                preparacion=[
                    "Licúa el nopal con el agua unos 20 segundos, no más: entre más lo licúas, más baba suelta.",
                    "Cuela si no te gusta la textura. Yo no la cuelo: esa baba es la que sirve.",
                    "Agrega el limón y la hierbabuena. Sin azúcar y sin endulzante.",
                ],
                dosis="1 vaso de 250 ml.",
                hora="Con la comida, o 15 minutos antes de sentarte a la mesa.",
                advertencia="El nopal es fibra pura, y la fibra <b>retrasa la absorción de las "
                            "pastillas</b>: deja pasar al menos 1 hora entre tu medicina y este "
                            "vaso. También baja el azúcar por su cuenta, así que se suma a tu "
                            "tratamiento. Si te da cólico o gases los primeros días, empieza con "
                            "medio vaso.",
            ),
            dict(
                n=6,
                nombre="Té de jengibre y limón",
                tipo="Té · caliente",
                para="Para la comida grasosa que se queda pesada y para el frío de manos y pies.",
                ingredientes=[
                    "3 rodajas delgadas de jengibre fresco (como 2 cm en total)",
                    "1 taza de agua (250 ml)",
                    "El jugo de ½ limón, al final",
                ],
                preparacion=[
                    "Hierve el agua con el jengibre 7 minutos a fuego bajo.",
                    "Apaga, tapa y reposa 5 minutos.",
                    "Cuela, deja entibiar y <b>hasta entonces</b> exprime el limón.",
                ],
                dosis="1 taza. Máximo 2 al día.",
                hora="Después de comer, o a media tarde cuando hace frío.",
                advertencia="El jengibre <b>hace la sangre más delgada</b>: si tomas warfarina, "
                            "aspirina o clopidogrel, consulta antes. Si tienes gastritis, reflujo "
                            "o piedras en la vesícula, te puede caer mal. Suspéndelo <b>dos semanas "
                            "antes de cualquier cirugía</b> y dile al anestesiólogo.",
            ),
            dict(
                n=7,
                nombre="Té de tronadora",
                tipo="Té · caliente",
                para="El de toda la vida para acompañar el cuidado del azúcar, de los que "
                     "más se piden en la herbolaria.",
                ingredientes=[
                    "1 cucharadita de hoja y flor de tronadora seca",
                    "1 taza de agua (250 ml)",
                ],
                preparacion=[
                    "Hierve el agua y apaga.",
                    "Echa la tronadora, tapa y deja 10 minutos.",
                    "Cuela y tómala tibia.",
                ],
                dosis="1 taza al día. Cursos de 15 días con 15 de descanso, no todo el año.",
                hora="Después de la comida del mediodía.",
                advertencia="Esta es de las <b>fuertes</b> del libro: tiene fama de bajar el "
                            "azúcar de verdad y se estudia poco. Una taza al día es suficiente y "
                            "no se toma de por vida. Si usas glibenclamida, glimepirida o insulina, "
                            "<b>habla con tu médico antes</b> de empezarla y mídete más seguido las "
                            "primeras dos semanas. Nunca en embarazo ni lactancia.",
            ),
            dict(
                n=8,
                nombre="Vinagre de manzana antes de comer",
                tipo="Agua · fría",
                para="Para que la comida con harina o con pan no te pegue tan de golpe.",
                ingredientes=[
                    "1 cucharada sopera de vinagre de manzana (15 ml)",
                    "1 vaso grande de agua (300 ml)",
                    "Un popote, si tienes",
                ],
                preparacion=[
                    "Disuelve el vinagre en el agua. Nunca lo tomes puro.",
                    "Tómalo con popote si puedes, y enjuágate la boca con agua simple después.",
                ],
                dosis="1 cucharada en un vaso grande. Máximo 2 veces al día.",
                hora="De 10 a 15 minutos <b>antes</b> de la comida con más harina del día.",
                advertencia="Puro <b>daña el esmalte de los dientes</b> y quema la garganta: "
                            "siempre diluido y enjuagándote después. Si tienes reflujo, gastritis "
                            "o el estómago que se vacía lento (<b>gastroparesia</b>, común en "
                            "diabetes de muchos años), este remedio no es para ti: lo empeora. "
                            "Si tomas diurético o digoxina, consulta, porque puede bajarte el potasio.",
            ),
            dict(
                n=9,
                nombre="Té de hierbabuena con anís",
                tipo="Té · caliente",
                para="Para la panza inflada y los gases de después de comer, y para dormir "
                     "mejor cuando cenas tarde.",
                ingredientes=[
                    "1 ramita de hierbabuena fresca (o 1 cdta seca)",
                    "½ cucharadita de anís en grano",
                    "1 taza de agua (250 ml)",
                ],
                preparacion=[
                    "Hierve el agua con el anís 3 minutos.",
                    "Apaga, echa la hierbabuena, tapa y deja 5 minutos.",
                    "Cuela y tómala tibia.",
                ],
                dosis="1 taza. Puedes repetirla después de la cena.",
                hora="Al terminar de comer, y otra después de cenar si cenaste pesado.",
                advertencia="La hierbabuena <b>relaja la válvula del estómago</b>, así que si "
                            "tienes reflujo te puede dar más agruras: cámbiala por manzanilla. "
                            "Si compras anís estrella, que sean estrellas enteras y de lugar de "
                            "confianza — el molido se adultera con anís estrella japonés, que es "
                            "tóxico. Nunca se lo des a un bebé.",
            ),
            dict(
                n=10,
                nombre="Té de romero y laurel",
                tipo="Té · caliente",
                para="Para la comida grasosa y el bajón de la tarde con dolor de cabeza.",
                ingredientes=[
                    "1 ramita chica de romero (o ½ cdta seco)",
                    "1 hoja de laurel",
                    "1 taza de agua (250 ml)",
                ],
                preparacion=[
                    "Hierve el agua, apaga y echa el romero y el laurel.",
                    "Tapa y deja 8 minutos.",
                    "Cuela. Queda fuerte de sabor: es normal.",
                ],
                dosis="1 taza al día, no más.",
                hora="Media hora después de la comida del mediodía.",
                advertencia="En cantidad de té está bien; en cantidad de medicina <b>no</b>. "
                            "El romero no se usa en embarazo, ni si tienes epilepsia o "
                            "convulsiones, ni si tomas anticoagulante. Una taza al día es el tope.",
            ),
        ],
    ),

    # ==========================================================
    dict(
        num="Capítulo 2",
        token="cap2",
        titulo="La sed de noche y tanta ida al baño",
        sub="Las aguas del riñón. Acompañan, refrescan y ayudan a que el cuerpo "
            "trabaje con calma — no lo exprimen.",
        cuantos="9 remedios",
        intro=[
            "Levantarte dos y tres veces en la noche cansa más que el día entero. Y luego "
            "viene la sed, y luego otra vez el baño, y así hasta que amanece.",
            "Aquí hay que tener cuidado con una cosa que casi nadie dice: <b>una hierba que "
            "te hace orinar más no está curando nada</b>. Solo te está sacando agua. Por eso "
            "las de este capítulo van en dosis chicas, por tiempo corto, y varias no se pueden "
            "tomar si el riñón ya anda trabajado. Si tu médico te dijo que tienes algo del "
            "riñón, este capítulo lo lees <b>con él</b>, no sola.",
        ],
        remedios=[
            dict(
                n=11,
                nombre="Agua de cola de caballo",
                tipo="Agua · tibia",
                para="Para la hinchazón de piernas al final del día y la sensación de retener líquido.",
                ingredientes=[
                    "1 cucharadita de cola de caballo seca",
                    "1 taza de agua (250 ml)",
                ],
                preparacion=[
                    "Hierve el agua y apaga.",
                    "Echa la hierba, tapa y deja reposar 10 minutos.",
                    "Cuela bien, que no queden hebras.",
                ],
                dosis="1 taza al día. <b>Máximo 7 días seguidos</b>, luego descansa 3 semanas.",
                hora="A media mañana. Nunca de noche, o te levantas más veces.",
                advertencia="Esta tiene fecha de caducidad: usada por semanas <b>te gasta la "
                            "vitamina B1</b> y te descompensa las sales. No la tomes si tienes "
                            "enfermedad del riñón o del corazón, si tomas diurético (furosemida, "
                            "hidroclorotiazida) o litio, ni en embarazo. Si un día orinas menos "
                            "en vez de más, suspéndela y ve al médico.",
            ),
            dict(
                n=12,
                nombre="Agua de pepino, apio y limón",
                tipo="Agua · fría",
                para="Para la sed de todo el día, para dejar el refresco y para los tobillos "
                     "hinchados de la tarde.",
                ingredientes=[
                    "½ pepino con cáscara, en rodajas",
                    "1 tallo de apio picado",
                    "El jugo de 1 limón",
                    "1 litro de agua",
                    "Hielo o un rato de refrigerador",
                ],
                preparacion=[
                    "Echa todo en una jarra con el agua.",
                    "Déjala en el refrigerador al menos 2 horas. Toda la noche queda mejor.",
                    "Tómala a lo largo del día. Se hace fresca todos los días.",
                ],
                dosis="Hasta 1 litro repartido en el día.",
                hora="De la mañana hasta las 6 de la tarde. Después de esa hora, mejor no.",
                advertencia="El apio <b>puede bajar la presión</b>: si tomas medicina para la "
                            "presión, empieza con medio litro y fíjate cómo te sientes al "
                            "levantarte. También hace la piel más sensible al sol en algunas "
                            "personas. Si tu médico te limitó los líquidos por el riñón o el "
                            "corazón, <b>esta agua no</b>: pregúntale cuánto puedes tomar.",
            ),
            dict(
                n=13,
                nombre="Agua de chía con limón",
                tipo="Agua · fría",
                para="Para la sed que no se quita y para llegar a la cena sin tanta hambre.",
                ingredientes=[
                    "1 cucharada sopera de chía",
                    "1 vaso grande de agua (300 ml)",
                    "El jugo de 1 limón",
                ],
                preparacion=[
                    "Echa la chía en el agua y revuelve bien.",
                    "Déjala <b>al menos 20 minutos</b>, hasta que se ponga gelatinosa. Revuelve otra vez.",
                    "Agrega el limón. Sin azúcar.",
                ],
                dosis="1 vaso al día, con 1 cucharada de chía. No más de 2 cucharadas diarias.",
                hora="A media tarde, o 20 minutos antes de la cena.",
                advertencia="<b>Nunca te comas la chía seca a cucharadas</b> — se hincha en el "
                            "camino y hay quien se ha atorado. Siempre remojada y con harta agua. "
                            "La fibra <b>retrasa la absorción de las pastillas</b>: separa este "
                            "vaso al menos 1 hora de tu metformina y 4 horas de la levotiroxina. "
                            "Si tienes problemas para tragar o el estómago lento, consulta antes.",
            ),
            dict(
                n=14,
                nombre="Agua de jamaica sin azúcar",
                tipo="Agua · fría o caliente",
                para="Para el antojo de refresco y para la sed de la tarde.",
                ingredientes=[
                    "1 puño chico de flor de jamaica (unos 15 g)",
                    "1 litro de agua",
                    "Opcional: 3 rajas de canela de Ceilán o unas hojas de hierbabuena",
                ],
                preparacion=[
                    "Hierve el agua, apaga y echa la jamaica.",
                    "Tapa y deja reposar 15 minutos. Entre más tiempo, más amarga.",
                    "Cuela y enfría. <b>Sin azúcar</b>: si te cuesta, empieza con la canela, que engaña bonito.",
                ],
                dosis="Hasta 2 vasos al día (500 ml).",
                hora="Con la comida o a media tarde. No de noche.",
                advertencia="La jamaica <b>baja la presión</b>: si ya tomas medicina para la "
                            "presión, dos vasos es el tope y fíjate si te mareas al pararte. "
                            "Puede interferir con algunos medicamentos (hidroclorotiazida, "
                            "cloroquina) — si tomas algo fijo, pregúntale a tu médico. "
                            "No se toma en embarazo. Y ojo: la jamaica endulzada del puesto "
                            "es prácticamente un refresco.",
            ),
            dict(
                n=15,
                nombre="Té de diente de león",
                tipo="Té · caliente",
                para="Para la hinchazón, la panza llena de aire y la digestión de la grasa.",
                ingredientes=[
                    "1 cucharadita de hoja de diente de león seca",
                    "1 taza de agua (250 ml)",
                ],
                preparacion=[
                    "Hierve el agua y apaga.",
                    "Echa la hoja, tapa y deja 10 minutos.",
                    "Cuela y tómala tibia.",
                ],
                dosis="1 taza al día. Cursos de 2 semanas con 1 de descanso.",
                hora="A media mañana o 20 minutos antes de la comida.",
                advertencia="No la tomes si tienes <b>piedras en la vesícula o los conductos "
                            "tapados</b>, ni si eres alérgica a la manzanilla, el girasol o la "
                            "ambrosía (son de la misma familia). Hace orinar, así que se suma al "
                            "diurético si tomas uno, y puede subirte el potasio si usas espironolactona. "
                            "Con enfermedad del riñón, solo con permiso de tu médico.",
            ),
            dict(
                n=16,
                nombre="Agua de linaza de la noche",
                tipo="Agua · tibia",
                para="Para el estreñimiento que viene con el tratamiento y para la sed nocturna.",
                ingredientes=[
                    "1 cucharada sopera de linaza entera (no molida)",
                    "1 vaso de agua (250 ml)",
                ],
                preparacion=[
                    "Pon la linaza en el agua desde la tarde.",
                    "Déjala reposar de 6 a 8 horas. Va a soltar una baba transparente: esa es la que sirve.",
                    "Cuela y toma el agua. Las semillas se tiran.",
                ],
                dosis="1 vaso al día.",
                hora="Temprano en la noche, antes de las 8, y siempre con otro vaso de agua simple detrás.",
                advertencia="Sin <b>suficiente agua</b> la linaza estriñe en vez de ayudar: nunca "
                            "la tomes si no vas a tomar agua después. No la uses si tienes "
                            "obstrucción intestinal, estrechamiento del esófago o el estómago lento. "
                            "Separa 1 hora de tus pastillas y 4 horas de la levotiroxina. "
                            "No en embarazo.",
            ),
            dict(
                n=17,
                nombre="Té ligero de perejil",
                tipo="Té · tibio",
                para="Para los pies y los dedos hinchados de los días de mucho calor o mucha sal.",
                ingredientes=[
                    "1 ramita chica de perejil fresco (como 5 g)",
                    "1 taza de agua (250 ml)",
                ],
                preparacion=[
                    "Hierve el agua y apaga.",
                    "Echa el perejil, tapa y deja 8 minutos.",
                    "Cuela. Debe quedar un té claro, no un concentrado verde oscuro.",
                ],
                dosis="1 taza al día, <b>máximo 3 días seguidos</b>. No es de diario.",
                hora="A media mañana.",
                advertencia="En la sopa el perejil es un alimento; en té concentrado y diario es "
                            "otra cosa: <b>irrita el riñón</b> y en cantidad es abortivo. "
                            "Prohibido en embarazo. No lo tomes si tienes enfermedad renal, ni "
                            "junto con diuréticos o litio. Si un día te hinchas más en vez de "
                            "menos, eso es para el médico, no para otro té.",
            ),
            dict(
                n=18,
                nombre="Infusión de hoja de moringa",
                tipo="Té · caliente",
                para="Para el cansancio de la mañana y para acompañar el cuidado del azúcar.",
                ingredientes=[
                    "1 cucharadita de hoja de moringa seca (o 5 hojas frescas)",
                    "1 taza de agua (250 ml)",
                ],
                preparacion=[
                    "Hierve el agua y apaga. <b>No hiervas la hoja</b>: se amarga y pierde.",
                    "Echa la moringa, tapa y deja 7 minutos.",
                    "Cuela y tómala tibia.",
                ],
                dosis="1 taza al día. Cursos de 3 semanas con 1 de descanso.",
                hora="En la mañana, con el desayuno.",
                advertencia="Solo <b>hoja</b>. La raíz y la corteza de moringa <b>no se toman</b>: "
                            "son tóxicas y abortivas. La hoja baja el azúcar, así que se suma a tu "
                            "medicina — empieza con media taza. Si tomas levotiroxina, separa "
                            "4 horas. No en embarazo. Si te da diarrea los primeros días, bájale a "
                            "media taza.",
            ),
            dict(
                n=19,
                nombre="Té de manzanilla con toronjil",
                tipo="Té · caliente",
                para="Para la noche en que te acuestas y la cabeza no se apaga, y para "
                     "levantarte menos veces.",
                ingredientes=[
                    "1 cucharadita de manzanilla",
                    "1 cucharadita de toronjil",
                    "1 taza de agua (250 ml)",
                ],
                preparacion=[
                    "Hierve el agua y apaga.",
                    "Echa las dos hierbas, tapa y deja 7 minutos.",
                    "Cuela y tómala tibia, sin prisa, con la luz ya baja.",
                ],
                dosis="1 taza.",
                hora="Una hora antes de acostarte — no en la cama, que si no te levantas al baño.",
                advertencia="Si eres alérgica a la manzanilla, el girasol o la ambrosía, sáltala. "
                            "El toronjil <b>da sueño</b>: no lo mezcles con pastillas para dormir "
                            "ni con calmantes sin preguntarle a tu médico, y no manejes después. "
                            "Si tomas medicina para la tiroides, consulta: el toronjil puede "
                            "interferir.",
            ),
        ],
    ),

    # ==========================================================
    dict(
        num="Capítulo 3",
        token="cap3",
        titulo="Los pies dormidos y las piernas pesadas",
        sub="Lo de fuera y lo de dentro. Aquí van los baños de pies, las cataplasmas "
            "y los tés que acompañan la circulación.",
        cuantos="9 remedios",
        intro=[
            "Este capítulo lo escribí con más cuidado que ningún otro, y te voy a decir "
            "por qué antes de que prepares nada.",
            "Cuando el azúcar lleva años alto, los pies <b>sienten menos</b>. Y un pie que "
            "siente menos se quema con agua que a ti te parece tibia, se lastima con una "
            "piedrita y no avisa. Por eso aquí <b>no hay agua caliente</b>: todos los baños de "
            "pies de este libro van tibios, cortos, y con la temperatura probada con el codo "
            "o con el termómetro — nunca con el pie.",
            "Y la regla que no se negocia: <b>si tienes una herida, una ampolla, una grieta "
            "abierta, una uña enterrada o una mancha oscura en el pie, no le pongas nada "
            "encima. Eso es de médico el mismo día.</b>",
        ],
        remedios=[
            dict(
                n=20,
                nombre="Baño de pies templado de manzanilla y sal",
                tipo="Baño de pies · externo",
                para="Para el cansancio y el hormigueo del final del día.",
                ingredientes=[
                    "2 puños de manzanilla seca",
                    "2 litros de agua",
                    "1 cucharada sopera de sal de grano",
                    "Una toalla limpia y suave",
                ],
                preparacion=[
                    "Hierve la manzanilla en 1 litro de agua 5 minutos y cuela.",
                    "Mézclala con 1 litro de agua fría en una tina. Debe quedar <b>tibia, "
                    "no caliente</b>: pruébala con el codo o con termómetro — máximo 37 °C.",
                    "Disuelve la sal.",
                    "Mete los pies <b>10 minutos, ni un minuto más</b>.",
                    "Sécalos muy bien, sobre todo <b>entre los dedos</b>. Ahí es donde empieza el hongo.",
                ],
                dosis="10 minutos. Máximo 3 veces por semana.",
                hora="En la tarde-noche, con tiempo de secarte bien antes de acostarte.",
                advertencia="<b>Nada de agua caliente y nada de remojar de más.</b> El agua "
                            "caliente quema un pie que siente poco, y el remojo largo reblandece "
                            "la piel y abre la puerta a la infección. <b>No lo hagas</b> si tienes "
                            "cualquier herida, úlcera, grieta abierta o pie hinchado y rojo: eso "
                            "es urgencia médica, no baño. Si un pie está más caliente o más rojo "
                            "que el otro, ve hoy mismo.",
            ),
            dict(
                n=21,
                nombre="Aceite de romero para masaje de pies",
                tipo="Aceite · externo",
                para="Para el hormigueo de la noche y para revisarte los pies sin que se "
                     "sienta obligación.",
                ingredientes=[
                    "1 taza de aceite de oliva o de coco",
                    "2 ramas de romero fresco, bien secas (sin nada de agua)",
                    "Un frasco de vidrio limpio y seco",
                ],
                preparacion=[
                    "Mete el romero en el frasco y cúbrelo con el aceite.",
                    "Tápalo y déjalo <b>2 semanas</b> en un lugar oscuro. Muévelo cada tantos días.",
                    "Cuela y guarda el aceite. Dura unos 3 meses.",
                    "Para usarlo: una cucharadita en la mano, y masajea del tobillo hacia la rodilla, "
                    "y luego el pie con movimientos suaves.",
                ],
                dosis="1 cucharadita por pierna.",
                hora="En la noche, después de bañarte.",
                advertencia="<b>Solo por fuera, nunca se toma.</b> No lo pongas entre los dedos "
                            "— ahí la humedad es la que sobra. No lo uses sobre heridas, grietas "
                            "abiertas ni piel rota. Si la rama no está <b>completamente seca</b> "
                            "cuando la metes al aceite, el frasco se echa a perder y puede criar "
                            "bacterias: si huele raro o se ve turbio, se tira. "
                            "Prueba primero en un pedacito de brazo por si te irrita.",
            ),
            dict(
                n=22,
                nombre="Cataplasma de hoja de col para las piernas",
                tipo="Cataplasma · externo",
                para="Para la pesadez y la hinchazón de las piernas al final del día.",
                ingredientes=[
                    "3 o 4 hojas grandes de col (repollo), las de afuera",
                    "Un rodillo o una botella de vidrio",
                    "Una venda o una tela de algodón",
                ],
                preparacion=[
                    "Lava las hojas y sécalas. Quítales el tronquito duro del centro.",
                    "Aplástalas con el rodillo hasta que se vean húmedas y flexibles.",
                    "Póntelas <b>a temperatura ambiente</b> sobre la pantorrilla — ni calientes ni del refrigerador.",
                    "Sujétalas con la tela, sin apretar, y siéntate con las piernas en alto 30 minutos.",
                ],
                dosis="30 minutos. Hasta 4 veces por semana.",
                hora="En la tarde, cuando la pierna ya está pesada.",
                advertencia="<b>Sobre piel sana nada más.</b> Si hay várices con la piel rota, "
                            "úlcera, herida o una zona roja y caliente, no se pone nada encima: "
                            "es de médico. No amarres apretado — en una pierna con mala "
                            "circulación una venda apretada hace daño. Si <b>una sola pierna</b> "
                            "se hincha de repente, duele y está caliente, eso puede ser un coágulo: "
                            "urgencias hoy.",
            ),
            dict(
                n=23,
                nombre="Compresa fresca de hierbabuena",
                tipo="Compresa · externo",
                para="Para el ardor y el hormigueo de los pies en las noches de calor.",
                ingredientes=[
                    "2 puños de hierbabuena fresca",
                    "1 litro de agua",
                    "Una toalla chica de algodón",
                ],
                preparacion=[
                    "Hierve el agua con la hierbabuena 5 minutos. Apaga y deja enfriar <b>por completo</b>.",
                    "Guarda el agua en el refrigerador, pero sácala 15 minutos antes de usarla: "
                    "fresca, no helada.",
                    "Moja la toalla, exprímela y envuelve el pie 10 minutos.",
                    "Seca bien, sobre todo entre los dedos.",
                ],
                dosis="10 minutos por pie.",
                hora="En la noche, antes de acostarte.",
                advertencia="<b>Fresca, nunca helada ni con hielo directo.</b> El frío fuerte en "
                            "un pie que siente poco también lastima, igual que el calor. No la "
                            "uses sobre piel rota. Si el ardor es cada noche más fuerte, o ya no "
                            "te deja dormir, díselo a tu médico: hay tratamiento para eso y el "
                            "té no lo reemplaza.",
            ),
            dict(
                n=24,
                nombre="Té de jengibre con cúrcuma",
                tipo="Té · caliente",
                para="Para el frío en las manos y los pies, y para el cuerpo entumido de la mañana.",
                ingredientes=[
                    "3 rodajas de jengibre fresco",
                    "½ cucharadita de cúrcuma en polvo",
                    "1 pizca chica de pimienta negra",
                    "1 taza de agua (250 ml)",
                    "Unas gotas de limón",
                ],
                preparacion=[
                    "Hierve el agua con el jengibre 7 minutos.",
                    "Apaga, agrega la cúrcuma y la pimienta y revuelve.",
                    "Reposa 5 minutos, cuela y ponle el limón al final.",
                ],
                dosis="1 taza al día.",
                hora="En la mañana, con el desayuno.",
                advertencia="Jengibre y cúrcuma juntos <b>hacen la sangre más delgada</b>: si "
                            "tomas warfarina, aspirina, clopidogrel o cualquier anticoagulante, "
                            "<b>consulta antes</b>. No los uses si tienes piedras en la vesícula "
                            "ni si tienes cirugía programada (suspende 2 semanas antes). "
                            "La cúrcuma en polvo mancha todo: usa cuchara de metal.",
            ),
            dict(
                n=25,
                nombre="Gel de sábila para los pies resecos",
                tipo="Gel · externo",
                para="Para los talones partidos y la piel reseca y tirante de las piernas.",
                ingredientes=[
                    "1 penca de sábila",
                    "Un cuchillo y un vaso",
                ],
                preparacion=[
                    "Corta la penca y párala en un vaso <b>30 minutos</b>, para que escurra "
                    "el jugo amarillo. Ese jugo se tira: irrita.",
                    "Enjuaga la penca, ábrela y saca solo el <b>gel transparente</b>.",
                    "Úntalo en talones, empeines y piernas. Deja secar.",
                    "Lo que sobre, en el refrigerador, y se usa en 3 días.",
                ],
                dosis="Una capa delgada, 1 vez al día.",
                hora="En la noche, después del baño.",
                advertencia="<b>Entre los dedos no.</b> Ahí hay que secar, no humedecer. "
                            "No la pongas sobre heridas abiertas ni úlceras sin que un médico lo "
                            "indique. El <b>acíbar</b> (el jugo amarillo) irrita la piel y, tomado, "
                            "es un purgante fuerte que descompensa las sales — en este libro la "
                            "sábila es solo de uso externo. Prueba en un pedacito de brazo "
                            "primero: hay quien es alérgica.",
            ),
            dict(
                n=26,
                nombre="Baño de pies de hoja de guayaba",
                tipo="Baño de pies · externo",
                para="Para el pie sudado, el mal olor y la comezón entre los dedos.",
                ingredientes=[
                    "15 hojas de guayaba",
                    "2 litros de agua",
                ],
                preparacion=[
                    "Hierve las hojas en 1 litro de agua 10 minutos. Cuela.",
                    "Mezcla con 1 litro de agua fría hasta que quede <b>tibia</b> (pruébala con el codo).",
                    "Mete los pies <b>10 minutos</b>.",
                    "Seca a golpecitos, con muchísimo cuidado <b>entre cada dedo</b>. "
                    "Puedes usar la secadora de pelo en frío.",
                ],
                dosis="10 minutos. 3 veces por semana, máximo 2 semanas seguidas.",
                hora="En la tarde.",
                advertencia="Lo mismo que el baño de manzanilla: <b>tibia y corta</b>. "
                            "Si entre los dedos la piel está blanca, abierta o supurando, ya no "
                            "es cosa de baños — es hongo o infección y necesita tratamiento del "
                            "médico. En diabetes una infección de pie se complica rápido: "
                            "no la dejes pasar dos semanas a ver si se quita.",
            ),
            dict(
                n=27,
                nombre="Té de ortiga",
                tipo="Té · caliente",
                para="Para las piernas cansadas y la sensación de traer las venas trabajadas.",
                ingredientes=[
                    "1 cucharadita de hoja de ortiga seca",
                    "1 taza de agua (250 ml)",
                ],
                preparacion=[
                    "Hierve el agua y apaga.",
                    "Echa la ortiga, tapa y deja 10 minutos.",
                    "Cuela bien.",
                ],
                dosis="1 taza al día. Cursos de 2 semanas con 1 de descanso.",
                hora="A media mañana.",
                advertencia="La ortiga <b>hace orinar, baja la presión y puede bajar el azúcar</b>: "
                            "las tres se suman a lo que ya tomas. No la uses con diuréticos, con "
                            "medicina para la presión ni con anticoagulantes sin consultar. "
                            "No en embarazo. Si tienes enfermedad del riñón, pregúntale a tu "
                            "médico antes.",
            ),
            dict(
                n=28,
                nombre="La bomba de tobillos y las piernas en alto",
                tipo="Sin planta · movimiento",
                para="Para las piernas pesadas, los tobillos hinchados y el hormigueo de "
                     "estar mucho tiempo sentada.",
                ingredientes=[
                    "Nada. Una silla y una almohada.",
                ],
                preparacion=[
                    "Siéntate y estira una pierna.",
                    "Sube la punta del pie hacia ti y bájala, despacio, <b>20 veces</b>. "
                    "Luego la otra pierna.",
                    "Haz 10 círculos con cada tobillo, para un lado y para el otro.",
                    "Acuéstate 15 minutos con las piernas sobre dos almohadas, más arriba "
                    "que el corazón.",
                ],
                dosis="Las dos rondas, 2 veces al día.",
                hora="A media tarde y antes de dormir. Y cada hora si pasas el día sentada.",
                advertencia="Te pongo este entre los remedios a propósito: <b>no cuesta un peso "
                            "y es de los que más sirven</b> para la pierna pesada. Si te marea "
                            "subir las piernas, si te falta el aire acostada o si <b>una sola "
                            "pierna</b> se hinchó de repente y duele, para y llama al médico. "
                            "Con insuficiencia cardiaca, pregúntale primero a tu médico cuánto "
                            "puedes subir las piernas.",
            ),
        ],
    ),

    # ==========================================================
    dict(
        num="Capítulo 4",
        token="cap4",
        titulo="El antojo de dulce de las cinco de la tarde",
        sub="Lo que se toma cuando la mano va sola al pan. Todos sin azúcar, "
            "todos listos en menos de diez minutos.",
        cuantos="8 remedios",
        intro=[
            "A las cinco de la tarde no te falla la voluntad. Te falla el plan.",
            "Si a esa hora no hay nada preparado, lo que hay es pan. Por eso este capítulo "
            "se trata menos de plantas y más de <b>tener algo listo</b> — algo caliente, algo "
            "con sabor, algo que ocupe la boca y las manos los diez minutos que dura la ganas.",
            "Antes de entrar, una cosa que puede salvarte de un susto: <b>si además del "
            "antojo te tiemblan las manos, sudas frío, se te nubla la vista o te sientes "
            "rara, eso no es antojo — puede ser el azúcar bajo</b>. En ese caso no es té: "
            "es azúcar de verdad, y viene explicado en el Bono 3 y en el capítulo de "
            "seguridad. Léelo antes que este.",
        ],
        remedios=[
            dict(
                n=29,
                nombre="Agua de canela con clavo",
                tipo="Agua · caliente",
                para="Para el antojo de pan dulce de la tarde. Sabe a postre y no lleva azúcar.",
                ingredientes=[
                    "1 raja de canela de Ceilán",
                    "2 clavos de olor",
                    "2 tazas de agua (500 ml)",
                ],
                preparacion=[
                    "Hierve el agua con la canela y los clavos 5 minutos.",
                    "Apaga, tapa y deja reposar 10 minutos.",
                    "Cuela y tómala caliente, despacio, en una taza bonita. La taza importa más de lo que crees.",
                ],
                dosis="1 taza (250 ml). Puedes tomar hasta 2 al día.",
                hora="Entre las 4 y las 6 de la tarde, apenas empiece el antojo.",
                advertencia="Canela de Ceilán, no cassia (ver remedio 01). El clavo en cantidad "
                            "<b>afecta la coagulación</b>: dos clavos por taza es el tope si "
                            "tomas anticoagulante. Si te da agruras, quita el clavo y déjale "
                            "solo la canela.",
            ),
            dict(
                n=30,
                nombre="Té de fenogreco",
                tipo="Té · caliente",
                para="Para el antojo que viene del hambre de verdad, no del aburrimiento.",
                ingredientes=[
                    "1 cucharadita de semilla de fenogreco (alholva)",
                    "1 taza de agua (250 ml)",
                ],
                preparacion=[
                    "Remoja las semillas en el agua toda la noche.",
                    "En la mañana, hierve todo 5 minutos.",
                    "Cuela y tómalo tibio. Es amargo, y con nuez por detrás.",
                ],
                dosis="1 taza al día. Cursos de 2 semanas con 1 de descanso.",
                hora="A media tarde, o 30 minutos antes de la comida.",
                advertencia="El fenogreco <b>baja el azúcar de forma notoria</b>: es de los que "
                            "más se suman a la glibenclamida y a la insulina. Empieza con media "
                            "taza y mídete. <b>Prohibido en embarazo</b> — hace que el útero se "
                            "contraiga. Si eres alérgica al cacahuate o al garbanzo, puedes serlo "
                            "a esta. Te va a cambiar el olor del sudor a jarabe de maple: es "
                            "normal y se quita al dejarlo.",
            ),
            dict(
                n=31,
                nombre="Agua de jamaica con naranja",
                tipo="Agua · fría",
                para="Para el antojo de refresco y para la boca seca de la tarde.",
                ingredientes=[
                    "1 puño chico de jamaica",
                    "1 litro de agua",
                    "La cáscara de ½ naranja, sin lo blanco",
                    "Hierbabuena al gusto",
                ],
                preparacion=[
                    "Hierve el agua, apaga y echa la jamaica y la cáscara de naranja.",
                    "Tapa y reposa 15 minutos. Cuela.",
                    "Enfría y agrega la hierbabuena al servir. Nada de azúcar.",
                ],
                dosis="1 o 2 vasos al día (máximo 500 ml).",
                hora="A media tarde, bien fría.",
                advertencia="Mismas advertencias que el remedio 14: la jamaica <b>baja la presión</b> "
                            "y no se toma en embarazo. Usa la <b>cáscara</b>, no el jugo de naranja "
                            "— el jugo es azúcar líquida y te hace lo contrario de lo que buscas. "
                            "Si la cáscara no es de naranja lavada, tállala bien antes.",
            ),
            dict(
                n=32,
                nombre="Té verde con hierbabuena",
                tipo="Té · caliente",
                para="Para el bajón de las cinco con sueño y ganas de algo dulce.",
                ingredientes=[
                    "1 cucharadita de té verde (o 1 bolsita)",
                    "1 ramita de hierbabuena",
                    "1 taza de agua a 80 °C — hervida y reposada 3 minutos",
                ],
                preparacion=[
                    "Calienta el agua y déjala reposar 3 minutos fuera del fuego. "
                    "Con agua hirviendo el té verde se amarga.",
                    "Echa el té y la hierbabuena, tapa y deja <b>solo 3 minutos</b>.",
                    "Cuela en cuanto pase el tiempo.",
                ],
                dosis="1 taza. Máximo 2 al día.",
                hora="Entre las 4 y las 6. Después de las 6 te quita el sueño.",
                advertencia="Tiene <b>cafeína</b>: si tienes presión alta, arritmia, insomnio o "
                            "ansiedad, con una taza basta. <b>Estorba la absorción del hierro</b>, "
                            "así que no lo tomes con las comidas si tienes anemia, y sepáralo "
                            "2 horas de las pastillas de hierro. Si tomas anticoagulante, "
                            "consulta: el té verde trae vitamina K.",
            ),
            dict(
                n=33,
                nombre="Agua de tamarindo natural",
                tipo="Agua · fría",
                para="Para el antojo de algo agrio y dulce a la vez, y para el estreñimiento leve.",
                ingredientes=[
                    "3 vainas de tamarindo natural (no pulpa con azúcar)",
                    "1 litro de agua",
                    "Opcional: 1 raja de canela de Ceilán",
                ],
                preparacion=[
                    "Pela las vainas y remoja la pulpa en 2 tazas de agua caliente 20 minutos.",
                    "Deshaz la pulpa con la mano y cuela, apretando bien.",
                    "Completa con el resto del agua. <b>Sin azúcar</b> — si te sabe muy agrio, "
                    "rebájalo con más agua, no con dulce.",
                ],
                dosis="1 vaso (250 ml) al día.",
                hora="A media tarde.",
                advertencia="El tamarindo <b>tiene su propia azúcar</b>: un vaso al día es el "
                            "tope, y este es el remedio de este capítulo que más conviene medir "
                            "después. Nada de la pulpa endulzada del súper ni de los dulces de "
                            "tamarindo enchilado. Es laxante suave: si te suelta, bájale a medio "
                            "vaso. Puede aumentar el efecto de la aspirina y del ibuprofeno.",
            ),
            dict(
                n=34,
                nombre="Agua de pepino con menta y jengibre",
                tipo="Agua · fría",
                para="Para la boca aburrida — cuando no es hambre, son ganas de estar comiendo algo.",
                ingredientes=[
                    "½ pepino en rodajas, con cáscara",
                    "1 ramita de menta o hierbabuena",
                    "2 rodajas delgadas de jengibre",
                    "1 litro de agua",
                ],
                preparacion=[
                    "Echa todo a la jarra con el agua.",
                    "Refrigera al menos 1 hora.",
                    "Tómala fría, a lo largo de la tarde. Se hace nueva todos los días.",
                ],
                dosis="Hasta 1 litro en el día.",
                hora="De la comida hasta las 6 de la tarde.",
                advertencia="Es de los remedios más suaves del libro, pero el jengibre sigue "
                            "contando: si tomas anticoagulante, déjalo en dos rodajas por jarra. "
                            "Con reflujo, quítale la menta. Si tu médico te limitó los líquidos, "
                            "pregúntale cuánto puedes tomar.",
            ),
            dict(
                n=35,
                nombre="Té de cáscara de manzana con canela",
                tipo="Té · caliente",
                para="Para el antojo de pan y para las tardes de frío. Huele a casa.",
                ingredientes=[
                    "La cáscara de 1 manzana (lavada)",
                    "1 raja de canela de Ceilán",
                    "2 tazas de agua (500 ml)",
                ],
                preparacion=[
                    "Hierve las cáscaras con la canela 10 minutos a fuego bajo, tapado.",
                    "Apaga y reposa 5 minutos.",
                    "Cuela y tómalo caliente. La cáscara se tira.",
                ],
                dosis="1 taza (250 ml). Hasta 2 al día.",
                hora="A media tarde, cuando empieza el antojo.",
                advertencia="Es de los más inofensivos, con una condición: la <b>cáscara</b>, "
                            "no la manzana entera licuada ni el jugo. Lava bien la manzana antes "
                            "de pelarla, porque la cera y el pesticida se quedan en la cáscara. "
                            "Aplican las advertencias de la canela del remedio 01.",
            ),
            dict(
                n=36,
                nombre="Té de anís con hinojo",
                tipo="Té · caliente",
                para="Para el antojo de dulce que viene con la panza inflada después de la comida.",
                ingredientes=[
                    "½ cucharadita de anís en grano",
                    "½ cucharadita de semilla de hinojo",
                    "1 taza de agua (250 ml)",
                ],
                preparacion=[
                    "Machaca un poco las semillas con el mango del cuchillo, para que suelten.",
                    "Hierve el agua, apaga y échalas.",
                    "Tapa y deja 8 minutos. Cuela.",
                ],
                dosis="1 taza. Máximo 2 al día.",
                hora="Después de comer o a media tarde.",
                advertencia="El hinojo <b>no se usa en embarazo ni en lactancia</b> en dosis de "
                            "té, y no se recomienda para niñas. Si has tenido cáncer de mama o "
                            "de útero sensible a hormonas, consulta antes: el hinojo tiene efecto "
                            "parecido al estrógeno. Anís estrella, solo en estrellas enteras y de "
                            "lugar de confianza.",
            ),
        ],
    ),

    # ==========================================================
    dict(
        num="Capítulo 5",
        token="cap5",
        titulo="El hígado y la digestión pesada",
        sub="Para ese peso del lado derecho después de comer, y para la comida "
            "que se queda sentada horas.",
        cuantos="7 remedios",
        intro=[
            "Cuando el azúcar lleva tiempo alto, el hígado también trabaja de más. "
            "Muchas de ustedes me lo describen igual: un peso del lado derecho, debajo "
            "de las costillas, sobre todo después de comer carnitas o algo frito.",
            "Las hierbas de este capítulo son <b>de curso corto</b>. Ninguna se toma todo "
            "el año, y dos de ellas tienen fecha de suspensión estricta. Y si el peso "
            "viene con la piel o los ojos amarillos, con la orina muy oscura o con dolor "
            "fuerte que te dobla, <b>eso no es para un té</b>: es para el médico, hoy.",
        ],
        remedios=[
            dict(
                n=37,
                nombre="Té de boldo",
                tipo="Té · caliente · curso corto",
                para="Para la digestión pesada de la comida grasosa y el peso del lado derecho.",
                ingredientes=[
                    "3 hojas de boldo secas (o ½ cucharadita)",
                    "1 taza de agua (250 ml)",
                ],
                preparacion=[
                    "Hierve el agua y apaga.",
                    "Echa el boldo, tapa y deja <b>solo 5 minutos</b>. Más tiempo lo hace más fuerte, no mejor.",
                    "Cuela y tómalo tibio.",
                ],
                dosis="1 taza al día. <b>Máximo 10 días seguidos, dos veces al año.</b>",
                hora="Después de la comida más pesada del día.",
                advertencia="Esta es la hierba con la fecha más estricta del libro. El boldo "
                            "usado por semanas <b>puede dañar el hígado</b> — justo lo que quieres "
                            "cuidar. No lo tomes si ya tienes enfermedad del hígado, piedras en "
                            "la vesícula o los conductos tapados, ni si tomas anticoagulante. "
                            "<b>Prohibido en embarazo.</b> Diez días y se descansa: no lo "
                            "estires porque te cayó bien.",
            ),
            dict(
                n=38,
                nombre="Té de cuachalalate",
                tipo="Té · caliente",
                para="Para la gastritis, el ardor del estómago y la digestión que arde.",
                ingredientes=[
                    "1 pedazo chico de corteza de cuachalalate (unos 5 g)",
                    "2 tazas de agua (500 ml)",
                ],
                preparacion=[
                    "Pon la corteza en el agua fría y lleva a hervor.",
                    "Hierve suave 10 minutos, tapado.",
                    "Apaga y reposa 10 minutos. Cuela. Queda color madera.",
                ],
                dosis="1 taza al día. Cursos de 2 semanas con 1 de descanso.",
                hora="En ayunas, o 30 minutos antes del desayuno.",
                advertencia="No lo tomes en <b>embarazo ni lactancia</b>. Si tienes gastritis "
                            "diagnosticada, el cuachalalate acompaña pero <b>no reemplaza</b> el "
                            "omeprazol ni el tratamiento contra la bacteria <i>H. pylori</i>. "
                            "Si el ardor viene con vómito negro o con popó negra y pegajosa, "
                            "eso es sangrado: urgencias, hoy mismo.",
            ),
            dict(
                n=39,
                nombre="Té de hoja de alcachofa",
                tipo="Té · caliente · amargo",
                para="Para la digestión de la grasa y la sensación de lleno que no se va.",
                ingredientes=[
                    "1 cucharadita de hoja de alcachofa seca",
                    "1 taza de agua (250 ml)",
                ],
                preparacion=[
                    "Hierve el agua y apaga.",
                    "Echa la hoja, tapa y deja 10 minutos.",
                    "Cuela. Es amarga: se toma en dos o tres tandas si hace falta.",
                ],
                dosis="1 taza al día. Cursos de 3 semanas con 1 de descanso.",
                hora="20 minutos antes de la comida principal.",
                advertencia="No la tomes si tienes <b>piedras en la vesícula o los conductos "
                            "biliares tapados</b> — hace trabajar a la vesícula y puede provocar "
                            "un cólico. Si eres alérgica a la manzanilla, la ambrosía o el "
                            "girasol, evítala. No en embarazo.",
            ),
            dict(
                n=40,
                nombre="Té de manzanilla con anís después de cenar",
                tipo="Té · caliente",
                para="Para la cena que se queda sentada y no te deja dormir.",
                ingredientes=[
                    "1 cucharadita de manzanilla",
                    "½ cucharadita de anís en grano",
                    "1 taza de agua (250 ml)",
                ],
                preparacion=[
                    "Hierve el agua con el anís 3 minutos.",
                    "Apaga, echa la manzanilla, tapa y deja 6 minutos.",
                    "Cuela y tómalo tibio, sentada, sin la tele.",
                ],
                dosis="1 taza.",
                hora="30 minutos después de cenar.",
                advertencia="Si eres alérgica a la manzanilla, el girasol o la ambrosía, no la "
                            "tomes. En cantidad la manzanilla puede aumentar el efecto de los "
                            "<b>anticoagulantes y de los calmantes</b>: una taza al día está bien, "
                            "media jarra no. Si tomas ciclosporina o medicina para el trasplante, "
                            "consulta antes.",
            ),
            dict(
                n=41,
                nombre="Té de muicle",
                tipo="Té · caliente",
                para="Para el cansancio con digestión lenta y para la piel que se ve apagada.",
                ingredientes=[
                    "1 ramita de muicle con hojas (o 1 cdta seco)",
                    "1 taza de agua (250 ml)",
                ],
                preparacion=[
                    "Hierve el agua y apaga.",
                    "Echa el muicle, tapa y deja 10 minutos. El agua se pone azulosa: es normal.",
                    "Cuela y tómalo tibio.",
                ],
                dosis="1 taza al día. Cursos de 10 días con 10 de descanso.",
                hora="A media mañana.",
                advertencia="Es una planta muy usada en México y <b>poco estudiada</b>: por eso "
                            "va en cursos cortos y en una taza al día. No en embarazo ni lactancia. "
                            "Si tomas anticoagulante o medicina para la presión, consulta antes. "
                            "Si te sale sarpullido o comezón, suspéndelo.",
            ),
            dict(
                n=42,
                nombre="Agua tibia con limón en ayunas",
                tipo="Agua · tibia",
                para="Para arrancar el día sin el estómago pesado y para ir al baño con más orden.",
                ingredientes=[
                    "1 vaso de agua tibia (250 ml) — tibia, no caliente",
                    "El jugo de ½ limón",
                ],
                preparacion=[
                    "Exprime el limón en el agua tibia.",
                    "Tómalo despacio, recién levantada, antes de cualquier otra cosa.",
                    "Enjuágate la boca con agua simple después.",
                ],
                dosis="1 vaso.",
                hora="En ayunas, al levantarte. Espera 20 minutos antes de desayunar.",
                advertencia="El limón diario <b>desgasta el esmalte</b>: enjuágate la boca "
                            "después y no te laves los dientes en los siguientes 30 minutos "
                            "(ahí el esmalte está blando). Si tienes gastritis, úlcera o reflujo, "
                            "en ayunas te va a arder: tómalo después del desayuno o sáltatelo. "
                            "Si tomas metformina en ayunas, deja pasar 30 minutos entre una cosa y la otra.",
            ),
            dict(
                n=43,
                nombre="La caminata de los diez minutos",
                tipo="Sin planta · movimiento",
                para="Para el sueño de después de comer y para que la comida no te pegue tan de golpe.",
                ingredientes=[
                    "Zapato cerrado y cómodo. Nada más.",
                ],
                preparacion=[
                    "En cuanto termines de comer, no te sientes: ponte de pie.",
                    "Camina <b>10 minutos</b> a paso tranquilo — el patio, la cuadra, el pasillo "
                    "de la casa si llueve.",
                    "No es ejercicio ni es caminata rápida. Es caminar y ya.",
                    "Antes de salir, <b>revisa el zapato por dentro con la mano</b>: una piedrita "
                    "que no sientes puede hacerte una herida.",
                ],
                dosis="10 minutos después de cada comida fuerte. Con una vez al día ya se nota.",
                hora="Empezando a caminar dentro de los primeros 15 minutos después de comer.",
                advertencia="Te lo pongo como remedio porque lo es: de todo lo que hay en este "
                            "libro, <b>esto es de lo que más sirve</b> para lo que viene después "
                            "de comer, y es gratis. Usa siempre zapato cerrado — <b>nunca "
                            "descalza ni en chancla</b>. Revísate los pies al volver. "
                            "Si te da dolor en el pecho, falta de aire, mareo o un dolor en la "
                            "pantorrilla que te hace parar, siéntate y llama al médico.",
            ),
        ],
    ),

    # ==========================================================
    dict(
        num="Capítulo 6",
        token="cap6",
        titulo="Las mistelas de la Abuela Mei",
        sub="Macerados fríos, sin alcohol y sin azúcar. Se dejan reposar un día "
            "o dos y quedan listos para toda la semana.",
        cuantos="6 remedios",
        intro=[
            "La mistela de antes se hacía con aguardiente y con harta azúcar. Yo así ya "
            "no la hago, y te voy a decir por qué sin adornos.",
            "El <b>alcohol</b> con glibenclamida o con insulina puede bajarte el azúcar de "
            "noche, dormida, que es cuando menos te das cuenta. Y el <b>azúcar</b> de la "
            "receta vieja deshace justo lo que estamos cuidando. Así que la mistela de este "
            "libro es otra cosa: fruta, especia y raíz macerados en frío, en agua o en "
            "vinagre de manzana. Queda concentrada, dura toda la semana en el refrigerador "
            "y se toma en trago corto, rebajada.",
            "Regla de las seis: <b>se toman diluidas, nunca a tragos puros, y máximo "
            "60 ml al día.</b>",
        ],
        remedios=[
            dict(
                n=44,
                nombre="Mistela de canela y manzana",
                tipo="Mistela · sin alcohol",
                para="Para el antojo de dulce y para tener algo rico a la mano toda la semana.",
                ingredientes=[
                    "1 manzana en cuadritos, con cáscara",
                    "2 rajas de canela de Ceilán",
                    "500 ml de agua hervida y fría",
                    "1 frasco de vidrio con tapa, bien limpio",
                ],
                preparacion=[
                    "Echa la manzana y la canela en el frasco y cubre con el agua fría.",
                    "Tapa y déjalo <b>48 horas en el refrigerador</b>. No lo dejes fuera.",
                    "Cuela, guarda el líquido en el frasco limpio y tira la fruta.",
                    "Dura <b>5 días</b> en el refrigerador. Si huele agrio o burbujea, se tira.",
                ],
                dosis="<b>30 ml</b> (2 cucharadas soperas) rebajados en medio vaso de agua.",
                hora="A media tarde, una vez al día.",
                advertencia="Lleva la <b>azúcar propia de la manzana</b>: 30 ml es el tope y no "
                            "se toma a tragos. Aplican las advertencias de la canela (remedio 01): "
                            "que sea de Ceilán y que se sume a tu medicina. Si el frasco no está "
                            "bien limpio o lo dejas fuera del refrigerador, se fermenta — y un "
                            "macerado fermentado ya tiene alcohol.",
            ),
            dict(
                n=45,
                nombre="Mistela de jengibre y limón en vinagre",
                tipo="Mistela · en vinagre",
                para="Para antes de la comida con harina, y para el frío en las manos.",
                ingredientes=[
                    "1 trozo de jengibre (5 cm) en rodajas delgadas",
                    "La cáscara de 1 limón, sin lo blanco",
                    "300 ml de vinagre de manzana",
                    "1 frasco de vidrio con tapa (que la tapa no sea de metal, o ponle plástico debajo)",
                ],
                preparacion=[
                    "Mete el jengibre y la cáscara en el frasco y cubre con el vinagre.",
                    "Tapa y deja <b>7 días</b> en un lugar fresco y oscuro. Muévelo cada día.",
                    "Cuela y guarda en el refrigerador. Dura 2 meses.",
                ],
                dosis="<b>1 cucharada sopera (15 ml)</b> en un vaso grande de agua. Máximo 2 veces al día.",
                hora="De 10 a 15 minutos antes de la comida con más harina.",
                advertencia="Mismas advertencias del vinagre (remedio 08): <b>nunca puro</b>, "
                            "siempre en vaso grande de agua, enjuágate la boca después. "
                            "<b>No lo uses si tienes reflujo, gastritis o gastroparesia.</b> "
                            "El jengibre adelgaza la sangre: consulta si tomas anticoagulante. "
                            "Si tomas diurético o digoxina, pregunta por el potasio.",
            ),
            dict(
                n=46,
                nombre="Mistela de jamaica y naranja",
                tipo="Mistela · sin alcohol",
                para="Para sustituir el refresco de la comida y para el antojo de algo agrio.",
                ingredientes=[
                    "2 puños de flor de jamaica",
                    "La cáscara de 1 naranja, sin lo blanco",
                    "500 ml de agua hervida y fría",
                    "2 clavos de olor",
                ],
                preparacion=[
                    "Todo al frasco, cubierto con el agua fría.",
                    "Tapa y deja <b>24 horas en el refrigerador</b>. Queda color vino oscuro.",
                    "Cuela. Dura 5 días en el refrigerador.",
                ],
                dosis="<b>50 ml</b> en un vaso de agua fría, una vez al día.",
                hora="Con la comida.",
                advertencia="La jamaica <b>baja la presión</b> y concentrada la baja más: si "
                            "tomas medicina para la presión, empieza con 30 ml y fíjate si te "
                            "mareas al levantarte. <b>No en embarazo.</b> Si tomas "
                            "hidroclorotiazida o cloroquina, consulta.",
            ),
            dict(
                n=47,
                nombre="Mistela de nopal y xoconostle",
                tipo="Mistela · sin alcohol",
                para="Para acompañar la comida fuerte del día. Es la más mexicana de las seis.",
                ingredientes=[
                    "1 penca chica de nopal, limpia y en cuadritos",
                    "2 xoconostles pelados y sin semillas",
                    "500 ml de agua hervida y fría",
                    "El jugo de 1 limón",
                ],
                preparacion=[
                    "Todo al frasco con el agua. El limón también, desde el principio.",
                    "Tapa y deja <b>24 horas en el refrigerador</b>.",
                    "Licúa unos segundos, cuela con colador fino y guarda el líquido.",
                    "Dura <b>3 días</b> nada más, por el nopal. Si se pone babosa de más, se tira.",
                ],
                dosis="<b>60 ml</b> rebajados en medio vaso de agua, una vez al día.",
                hora="15 minutos antes de la comida principal.",
                advertencia="Nopal y xoconostle <b>bajan el azúcar</b> y aquí van concentrados: "
                            "es la mistela que más se suma a tu medicina. Empieza con 30 ml y "
                            "mídete la primera semana. La fibra retrasa las pastillas: "
                            "sepárala 1 hora de tu metformina. Es la que menos dura de las seis: "
                            "tres días y a la basura.",
            ),
            dict(
                n=48,
                nombre="Mistela de hoja de guayaba y menta",
                tipo="Mistela · sin alcohol",
                para="Para la pesadez de después de comer, cuando no te dan ganas ni de poner el agua a hervir.",
                ingredientes=[
                    "15 hojas de guayaba",
                    "1 manojo chico de menta o hierbabuena",
                    "500 ml de agua hervida y fría",
                ],
                preparacion=[
                    "Estruja las hojas con la mano y mételas al frasco.",
                    "Cubre con el agua fría, tapa y deja <b>24 horas en el refrigerador</b>.",
                    "Cuela. Dura 5 días en el refrigerador.",
                ],
                dosis="<b>50 ml</b> en medio vaso de agua, una vez al día.",
                hora="Después de la comida principal.",
                advertencia="Aplican las advertencias de la hoja de guayaba (remedio 02): "
                            "<b>baja el azúcar y la presión</b>, se suma a tu medicina, estriñe "
                            "y no se usa en embarazo. Concentrada en frío pega más que el té: "
                            "por eso son 50 ml y una vez al día.",
            ),
            dict(
                n=49,
                nombre="Mistela de tamarindo y clavo",
                tipo="Mistela · sin alcohol",
                para="Para el antojo fuerte de dulce de la tarde y para el estreñimiento leve.",
                ingredientes=[
                    "4 vainas de tamarindo natural, peladas",
                    "3 clavos de olor",
                    "1 raja de canela de Ceilán",
                    "500 ml de agua hervida y fría",
                ],
                preparacion=[
                    "Deshaz la pulpa del tamarindo con las manos y échala al frasco con las especias.",
                    "Cubre con el agua fría, tapa y deja <b>24 horas en el refrigerador</b>.",
                    "Cuela apretando bien. Dura 5 días en el refrigerador.",
                ],
                dosis="<b>30 ml</b> en un vaso de agua. Solo una vez al día.",
                hora="A media tarde, cuando aprieta el antojo.",
                advertencia="De las seis, esta es la que <b>más azúcar propia trae</b>: 30 ml es "
                            "el tope de verdad, y conviene medirte un par de veces las primeras "
                            "tardes que la tomes. Es laxante: si te suelta, bájale. El clavo en "
                            "cantidad afecta la coagulación y el tamarindo puede aumentar el "
                            "efecto de la aspirina y el ibuprofeno.",
            ),
        ],
    ),

    # ==========================================================
    dict(
        num="Capítulo 7",
        token="cap7",
        titulo="Cataplasmas y remedios de fuera",
        sub="Lo que se pone encima, no lo que se toma. Piel, piernas, ojos "
            "cansados y manos entumidas.",
        cuantos="6 remedios",
        intro=[
            "Estos no se toman. Se ponen. Y por eso tienen su propia regla, que es "
            "la misma para los seis:",
            "<b>Sobre piel sana y cerrada, siempre.</b> Nada de cataplasmas sobre heridas, "
            "úlceras, ampollas, grietas abiertas ni piel roja y caliente. Y nada caliente "
            "sobre los pies. Con el azúcar alto de muchos años la piel se repara más "
            "despacio y siente menos: lo que en otra persona sería una molestia, aquí "
            "puede terminar en una infección.",
            "Prueba cualquiera de estos <b>primero en un pedacito de brazo</b> y espera "
            "un día. Si sale ronchita o comezón, no es para ti.",
        ],
        remedios=[
            dict(
                n=50,
                nombre="Cataplasma tibia de linaza para el vientre",
                tipo="Cataplasma · externo",
                para="Para el vientre inflado y el cólico de la digestión pesada. "
                     "<b>Solo en el vientre, nunca en los pies.</b>",
                ingredientes=[
                    "4 cucharadas de linaza molida",
                    "Agua caliente, la necesaria",
                    "Una tela de algodón limpia",
                ],
                preparacion=[
                    "Mezcla la linaza con agua caliente hasta formar una pasta espesa.",
                    "Deja que se <b>entibie</b> — pruébala en el interior de tu muñeca. "
                    "Debe sentirse tibia y agradable, nunca caliente.",
                    "Extiéndela sobre la tela y ponla sobre el vientre 20 minutos.",
                    "Retira y limpia la piel con agua tibia.",
                ],
                dosis="20 minutos, hasta 3 veces por semana.",
                hora="En la noche, un rato después de cenar.",
                advertencia="<b>En el vientre sí; en los pies y las piernas no</b>, por el "
                            "riesgo de quemadura en piel que siente poco. No la uses si hay "
                            "dolor fuerte de vientre, fiebre, vómito o el vientre duro como "
                            "tabla: eso es urgencia, no cataplasma. Tampoco sobre la piel "
                            "irritada ni en embarazo.",
            ),
            dict(
                n=51,
                nombre="Cataplasma de sábila para piernas resecas",
                tipo="Cataplasma · externo",
                para="Para la piel de las piernas reseca, tirante y con comezón.",
                ingredientes=[
                    "Gel de 1 penca de sábila (ver remedio 25 para limpiarla)",
                    "1 cucharadita de aceite de oliva",
                    "Una tela de algodón",
                ],
                preparacion=[
                    "Escurre la penca 30 minutos para que suelte el acíbar amarillo y tíralo.",
                    "Saca el gel transparente y mézclalo con el aceite.",
                    "Extiende sobre la pierna, cubre con la tela y deja 20 minutos.",
                    "Enjuaga con agua tibia y seca con toquecitos.",
                ],
                dosis="20 minutos, 2 o 3 veces por semana.",
                hora="En la noche.",
                advertencia="El <b>acíbar</b> (jugo amarillo) irrita: escúrrelo bien. "
                            "Nada sobre heridas ni úlceras. Si la comezón de las piernas es "
                            "constante y no cede, díselo a tu médico — la comezón que no se "
                            "quita puede ser señal de azúcar descontrolada o de algo del riñón, "
                            "y no se arregla con crema.",
            ),
            dict(
                n=52,
                nombre="Compresa de manzanilla para los ojos cansados",
                tipo="Compresa · externo",
                para="Para los ojos cansados y los párpados hinchados de la mañana.",
                ingredientes=[
                    "2 bolsitas de manzanilla (o 2 cdtas en un colador)",
                    "1 taza de agua",
                ],
                preparacion=[
                    "Prepara el té y déjalo enfriar <b>por completo</b>.",
                    "Empapa dos algodones limpios y exprímelos.",
                    "Acuéstate y póntelos sobre los párpados <b>cerrados</b> 10 minutos.",
                    "Un algodón para cada ojo, y se tiran después. No se reusan.",
                ],
                dosis="10 minutos, una vez al día.",
                hora="En la mañana o al llegar de la calle.",
                advertencia="<b>Nada de esto entra al ojo</b>: va sobre el párpado cerrado. "
                            "Si eres alérgica a la manzanilla, no. Y lo importante: "
                            "si ves <b>borroso de repente, si ves manchitas flotando, "
                            "destellos o se te oscurece una parte de la vista</b>, eso no es "
                            "cansancio — es urgencia del oftalmólogo el mismo día. La vista es "
                            "de lo primero que avisa cuando el azúcar lleva tiempo alta.",
            ),
            dict(
                n=53,
                nombre="Cataplasma de nopal para el golpe o la inflamación",
                tipo="Cataplasma · externo",
                para="Para el golpe reciente, el moretón y la articulación inflamada.",
                ingredientes=[
                    "1 penca de nopal limpia, sin espinas",
                    "Una tela de algodón",
                ],
                preparacion=[
                    "Asa la penca unos minutos y déjala <b>entibiar</b> hasta que la aguantes "
                    "cómodamente en la muñeca. O úsala cruda, a temperatura ambiente.",
                    "Ábrela a lo largo y pon la parte babosa sobre la zona.",
                    "Sujeta con la tela sin apretar y deja 20 minutos.",
                ],
                dosis="20 minutos, hasta 2 veces al día los primeros 2 días del golpe.",
                hora="Cuando haga falta.",
                advertencia="Revisa <b>tres veces</b> que no queden espinitas: las chiquitas "
                            "casi no se ven y en un pie que siente poco pasan desapercibidas "
                            "hasta que se infectan. Nunca sobre piel rota. Si el golpe fue "
                            "fuerte, si no puedes apoyar, si se deforma o si el moretón crece "
                            "solo, eso es de radiografía. Y si tomas anticoagulante, "
                            "cualquier moretón grande se le avisa al médico.",
            ),
            dict(
                n=54,
                nombre="Ungüento de coco y romero para talones partidos",
                tipo="Ungüento · externo",
                para="Para los talones partidos y la piel gruesa de los pies.",
                ingredientes=[
                    "3 cucharadas de aceite de coco",
                    "1 cucharadita de romero seco bien molido",
                    "Calcetines de algodón limpios",
                ],
                preparacion=[
                    "Derrite el aceite de coco a fuego muy bajo, sin que humee.",
                    "Agrega el romero, apaga y deja enfriar 20 minutos.",
                    "Cuela y guarda en un frasquito. Se pone firme al enfriar.",
                    "En la noche, una capa delgada en el talón, <b>sin meterlo entre los dedos</b>, "
                    "y ponte los calcetines.",
                ],
                dosis="Una capa delgada, de noche.",
                hora="Antes de dormir, con el pie recién lavado y bien seco.",
                advertencia="<b>Entre los dedos no va nada</b>: ahí se seca, no se humecta. "
                            "Si el talón tiene una <b>grieta abierta que sangra</b>, eso ya no es "
                            "para un ungüento casero: es del médico, porque por ahí entra la "
                            "infección. Nunca te cortes los callos con navaja ni uses parches "
                            "de ácido para callos — con diabetes eso termina en úlcera. "
                            "El piso queda resbaloso con el coco: ponte los calcetines ahí mismo.",
            ),
            dict(
                n=55,
                nombre="Compresa de árnica para piernas cansadas",
                tipo="Compresa · externo · nunca se toma",
                para="Para las piernas cansadas y los moretones que salen solos.",
                ingredientes=[
                    "1 cucharada de flor de árnica seca",
                    "1 taza de agua",
                    "Una tela de algodón",
                ],
                preparacion=[
                    "Hierve el agua, apaga y echa el árnica. Tapa 15 minutos.",
                    "Cuela y deja enfriar <b>por completo</b>.",
                    "Moja la tela, exprime y pon sobre la pierna 15 minutos.",
                ],
                dosis="15 minutos, hasta 3 veces por semana, máximo 2 semanas seguidas.",
                hora="En la tarde-noche.",
                advertencia="<b>El árnica no se toma. Nunca. Por ningún motivo.</b> Tomada es "
                            "tóxica para el corazón. Es de uso externo y sobre <b>piel cerrada</b>: "
                            "nada sobre heridas, raspones ni piel rota, porque se absorbe. "
                            "No la uses más de dos semanas seguidas ni si eres alérgica a la "
                            "manzanilla o al girasol. Si sale sarpullido, suspende. "
                            "Guárdala donde no la alcancen los niños.",
            ),
        ],
    ),
]


def todos():
    """Los 55, en orden, sin agrupar."""
    return [r for c in CAPITULOS for r in c["remedios"]]
