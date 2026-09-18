# -*- coding: utf-8 -*-
"""
Bono 2 — Guía del Mercado de la Abuela Mei.

Qué comprar, cómo reconocerlo, cuánto debe costar y con qué sustituirlo.

Nota sobre los precios: son de orientación, en pesos mexicanos, y en el
texto se dice que varían por ciudad y temporada. Poner un precio exacto
sería mentirle a la lectora; no ponerlo la deja sin defensa en el puesto.
El rango es el punto medio honesto, y la guía enseña a comparar antes de
pagar.

La ficha de la canela es la más larga del bono a propósito: es donde
más le cambian el producto a la gente, y es la planta que más se usa
en el ebook.
"""

import libro as L

META = dict(
    slug="bono2",
    archivo="Bono-2-Guia-del-Mercado.pdf",
    titulo_pdf="Bono 2 — Guía del Mercado de la Abuela Mei",
    autor="Abuela Mei",
    asunto="Guía de compra de hierbas y frutas para los remedios de Azúcar "
           "en Equilibrio: cómo reconocerlas, precio justo y sustitutos.",
    claves="mercado, herbolaria, canela de Ceilán, cassia, nopal, hoja de "
           "guayaba, moringa, precios, tianguis",
    pie="Guía del Mercado",
)


def portada():
    return L.portada(
        sello="Bono 2 · Azúcar en Equilibrio",
        titulo_html="Guía del<br><span>Mercado</span>",
        sub="Dónde conseguir cada cosa, cómo distinguir la buena de la falsa, "
            "cuánto debe costarte y con qué sustituirla si no la encuentras.",
        cuenta="24 INGREDIENTES · PRECIO JUSTO",
        autor="de la Abuela Mei",
        hoja="&#10070;",
    )


# ------------------------------------------------------------------
def _entrada():
    h = [L.capitulo("Antes de ir al mercado", "Que no te vean la cara",
                    sub="Lo que cuesta un remedio no es la hierba: es lo que "
                        "pagas de más por no saber qué estás comprando.",
                    token="entrada", nivel=0)]
    h.append(L.entrada(
        "Me ha pasado de todo en cuarenta años de puesto en puesto. Que me "
        "vendan hoja de guayaba con la mitad de ramas. Que me den cassia por "
        "canela y me cobren como si fuera de Ceilán. Que me quieran vender "
        "una cápsula importada de doscientos pesos que adentro trae lo mismo "
        "que el nopal de veinte."))
    h.append(L.parrafo(
        "Así que aquí te dejo lo que yo miro antes de pagar. No necesitas ser "
        "experta: con tres sentidos — <b>ver, oler y tocar</b> — ya no te "
        "dan gato por liebre."))

    h.append(L.seccion("Las tres pruebas de la Abuela Mei", token="pruebas"))
    h.append(L.caja(
        "1 · El olor",
        "<p>Agarra un poquito y estrújalo entre los dedos. <b>Si no huele, ya "
        "no sirve.</b> La hierba seca buena suelta olor en cuanto la aprietas — "
        "la manzanilla huele a manzanilla, el romero pica la nariz. "
        "Si huele a polvo, a humedad o a nada, es vieja.</p>",
        "suave"))
    h.append(L.caja(
        "2 · El color",
        "<p>La hierba seca buena conserva color: la manzanilla amarilla, la "
        "hoja de guayaba verde grisáceo, la jamaica vino oscuro. <b>Lo que se "
        "ve café, apagado o descolorido llevó sol y tiempo</b>, y con el color "
        "se le fue la fuerza.</p>",
        "suave"))
    h.append(L.caja(
        "3 · Lo que traen de relleno",
        "<p>Mete la mano en la bolsa. Si sale mucho <b>palito, rama gruesa o "
        "polvo del fondo</b>, te están vendiendo peso que no vas a usar. "
        "Pide que te dejen ver antes de pesar. En un puesto honesto te dejan.</p>",
        "suave"))
    h.append(L.caja(
        "Y una prueba más, que es de seguridad",
        "<p>Si ves <b>telarañas finas, bolitas apelmazadas, puntitos que se "
        "mueven o manchas negras de moho</b>: no lo compres y no lo uses "
        "aunque te lo regalen. La hierba con moho no se lava ni se hierve — "
        "se tira.</p>",
        "alerta"))

    h.append(L.seccion("Dónde comprar cada cosa", token="donde"))
    h.append(L.tabla(
        ["Lugar", "Bueno para", "Ojo con"],
        [["<b>Mercado y tianguis</b>",
          "Lo fresco: nopal, xoconostle, hierbas de manojo, fruta, verdura",
          "Que te lo den del día. Pregunta cuándo surten."],
         ["<b>Herbolaria</b>",
          "Hierba seca a granel, cortezas, semillas, lo difícil de hallar",
          "El granel sin tapa junto a la puerta agarra polvo y humedad."],
         ["<b>Súper</b>",
          "Chía, linaza, vinagre de manzana, especias de frasco",
          "Los tés de cajita suelen traer poquísima hierba y mucho saborizante."],
         ["<b>En línea</b>",
          "Solo lo que no encuentres de ningún otro modo",
          "No puedes oler ni ver. Y es donde más venden cassia como Ceilán."]]))
    h.append(L.caja(
        "El mejor día para ir",
        "<p>Entre semana y temprano. El fin de semana el mercado surte para el "
        "gentío y sale lo que quedó; los lunes muchos puestos traen lo del "
        "sábado. Yo voy <b>martes o miércoles, antes de las diez</b>.</p>",
        ""))
    return "".join(h)


# ------------------------------------------------------------------
def _canela():
    h = [L.capitulo("La más importante", "La canela: Ceilán o cassia",
                    sub="Si solo aprendes a distinguir una cosa de toda esta "
                        "guía, que sea esta.",
                    token="canela", nivel=0)]
    h.append(L.entrada(
        "En México, casi toda la canela que se vende molida y buena parte de "
        "la que se vende en raja <b>no es canela de Ceilán: es cassia</b>. "
        "Y no da lo mismo."))
    h.append(L.parrafo(
        "La cassia trae <b>cumarina</b>, una sustancia que al hígado le pesa "
        "si la tomas todos los días. Para un arroz con leche de vez en cuando "
        "no importa. Para tomarte un té de canela a diario durante meses, "
        "como te propone este libro, <b>sí importa</b>."))
    h.append(L.parrafo(
        "La buena noticia es que se distinguen a simple vista, y en cuanto se "
        "las ves una vez ya no se te olvida."))

    h.append(L.tabla(
        ["", "Canela de Ceilán <span style='color:#DDE5DC'>(la que quieres)</span>",
         "Cassia <span style='color:#DDE5DC'>(la común)</span>"],
        [["<b>La raja</b>",
          "Muchas capas finas enrolladas juntas, como un puro o un cigarro de hojas",
          "Una sola capa gruesa, enrollada sobre sí misma como un tubo"],
         ["<b>Se rompe</b>",
          "Fácil, con los dedos. Se desmorona en hojitas",
          "Dura. Necesitas fuerza o un molino"],
         ["<b>Color</b>", "Café claro, como canela con leche", "Café rojizo oscuro"],
         ["<b>Olor y sabor</b>", "Suave, dulce, fino", "Fuerte, picante, más agresivo"],
         ["<b>Cumarina</b>", "Casi nada", "Alta — por eso no es de diario"],
         ["<b>Precio</b>", "$60 a $120 los 100 g", "$25 a $40 los 100 g"],
         ["<b>De dónde viene</b>", "Sri Lanka", "China, Indonesia, Vietnam"]]))

    h.append(L.caja(
        "La prueba de los dedos",
        "<p>Pide que te dejen agarrar una raja y <b>trata de romperla con la "
        "mano</b>. Si cede y se deshace en capas delgaditas, es Ceilán. "
        "Si está dura como un palo y no cede, es cassia.</p>"
        "<p>Ese es el truco entero. No hace falta nada más.</p>",
        "verde"))
    h.append(L.caja(
        "Cuidado con estos nombres",
        "<p>La cassia se vende como <b>canela china</b>, <b>canela de Saigón</b>, "
        "<b>canela indonesia</b> o simplemente <b>canela</b>. La que quieres se "
        "llama <b>canela de Ceilán</b>, <b>canela verdadera</b> o "
        "<b><i>Cinnamomum verum</i></b> — si la etiqueta trae ese nombre en latín, "
        "vas bien.</p>"
        "<p>Y una regla dura: <b>la canela molida barata, dala por cassia</b>. "
        "Molida no hay forma de distinguirla, y la de Ceilán molida cuesta el "
        "triple. Si te la ofrecen molida y barata como Ceilán, te están viendo "
        "la cara.</p>",
        "alerta"))
    h.append(L.caja(
        "Si de plano no consigues Ceilán",
        "<p>No pasa nada: <b>usa cassia pero no de diario</b>. Máximo tres "
        "veces por semana, una taza, y descansa. O cámbiala por los remedios "
        "que no llevan canela — en el capítulo 1 del ebook tienes nueve más.</p>"
        "<p>Lo que <b>no</b> se hace es tomar cassia todos los días durante "
        "meses porque no se consiguió la otra.</p>",
        "suave"))
    return "".join(h)


# ------------------------------------------------------------------
FICHAS = [
    ("Nopal fresco", "Penca, verdura de nopal", "nopal", [
        ("Lo bueno", "Penca <b>tiesa y de verde parejo</b>, que no se doble sola. "
                     "Las chicas y medianas son más tiernas que las grandes."),
        ("Lo malo", "Flácida, con manchas cafés o naranjas, con la orilla seca, "
                    "o babeando antes de cortarla."),
        ("Precio justo", "<span class='precio'>$10 a $20 el kilo</span> con espinas · "
                         "<span class='precio'>$25 a $35</span> ya limpio"),
        ("Dónde", "Mercado y tianguis. En el súper sale al doble y menos fresco."),
        ("Cómo guardar", "En el refrigerador, envuelto en papel de estraza o "
                         "en bolsa de tela. <b>Una semana entero, 2 días ya picado.</b>"),
        ("Sustituto", "Xoconostle, o nopal en salmuera <b>bien enjuagado</b> "
                      "(trae mucha sal; solo si de plano no hay fresco)."),
    ], "<b>No pagues de más por el limpiado.</b> Quitarle las espinas con un "
       "cuchillo y raspando toma tres minutos. Si te lo venden limpio, que no "
       "te cueste más del doble."),

    ("Canela de Ceilán", "Canela verdadera, Cinnamomum verum", "canela_f", [
        ("Lo bueno", "Raja de <b>muchas capas finas</b>, café claro, que se "
                     "rompe con los dedos."),
        ("Lo malo", "Tubo grueso de una sola capa, rojizo y duro: es cassia."),
        ("Precio justo", "<span class='precio'>$60 a $120 los 100 g</span>"),
        ("Dónde", "Herbolaria y tiendas de especias. Pide verla antes."),
        ("Cómo guardar", "En frasco de vidrio cerrado, lejos de la estufa. "
                         "<b>Un año en raja</b>, mucho menos molida."),
        ("Sustituto", "Cassia, pero no de diario — ver la página anterior."),
    ], "Una raja de 5 cm rinde <b>dos tés</b>: se puede volver a hervir una "
       "segunda vez. A la tercera ya no suelta nada."),

    ("Hoja de guayaba", "Hoja de guayabo", "guayaba", [
        ("Lo bueno", "Seca, <b>verde grisáceo</b>, entera, que truene al "
                     "apretarla y huela a guayaba."),
        ("Lo malo", "Café, hecha polvo en el fondo de la bolsa, o con más "
                    "ramita que hoja."),
        ("Precio justo", "<span class='precio'>$20 a $40 los 50 g</span>"),
        ("Dónde", "Herbolaria. Y si alguien de tu familia tiene guayabo en el "
                  "patio, es gratis y mejor."),
        ("Cómo guardar", "Frasco de vidrio, oscuro y seco. Un año."),
        ("Sustituto", "Hoja de higo (capítulo 1, remedio 03), pero es más fuerte: "
                      "media taza y no una."),
    ], "Si las cortas del árbol, agarra las <b>hojas de en medio</b> — ni los "
       "brotes tiernos ni las viejas de abajo. Lávalas y sécalas a la sombra "
       "tres días, nunca al sol directo."),

    ("Moringa", "Hoja de moringa, árbol milagro", "moringa", [
        ("Lo bueno", "Hoja seca <b>verde intenso</b>, casi entera, con olor a "
                     "té verde."),
        ("Lo malo", "Verde apagado o amarillento, o polvo muy fino. "
                    "<b>Y cualquier cosa que diga raíz o corteza.</b>"),
        ("Precio justo", "<span class='precio'>$40 a $70 los 100 g</span> en hoja"),
        ("Dónde", "Herbolaria. Cada vez más en mercados del centro y del sur."),
        ("Cómo guardar", "Frasco oscuro y cerrado. Seis meses, no más: "
                         "pierde color y con el color se va la fuerza."),
        ("Sustituto", "Té verde suave, aunque no es lo mismo."),
    ], "<b>Solo hoja.</b> La raíz y la corteza de moringa son tóxicas y "
       "abortivas. Si en el puesto te ofrecen 'raíz de moringa para el azúcar', "
       "no la compres y no vuelvas a ese puesto."),

    ("Jengibre", "Kion", "jengibre", [
        ("Lo bueno", "Rizoma <b>firme, pesado para su tamaño</b>, con la piel "
                     "lisa y tirante. Al rasparlo con la uña huele fuerte."),
        ("Lo malo", "Arrugado, blando, con moho en los nudos, o ya con brotes verdes."),
        ("Precio justo", "<span class='precio'>$60 a $90 el kilo</span> · "
                         "un trozo de 100 g te dura la semana"),
        ("Dónde", "Mercado y súper. En el mercado sale más barato y más fresco."),
        ("Cómo guardar", "En el refrigerador, en bolsa de papel: <b>3 semanas</b>. "
                         "Pelado y en el congelador: 3 meses, y se ralla congelado."),
        ("Sustituto", "No tiene bueno. Si no hay, sáltate el remedio."),
    ], "<b>No lo peles con pelapapas</b>: raspa la piel con el borde de una "
       "cuchara. Se va la piel y se queda lo bueno, que está justo debajo."),

    ("Flor de jamaica", "Hibisco", "jamaica", [
        ("Lo bueno", "Flor <b>entera, vino tinto oscuro</b>, que se sienta "
                     "seca pero flexible."),
        ("Lo malo", "Muy quebrada, café o rojiza pálida, o con polvo blanco encima."),
        ("Precio justo", "<span class='precio'>$90 a $140 el kilo</span> · "
                         "con 100 g haces cuatro jarras"),
        ("Dónde", "Mercado a granel. Mucho más barata que en bolsita."),
        ("Cómo guardar", "Frasco cerrado, lugar seco. Un año."),
        ("Sustituto", "Tamarindo natural, cuidando la porción por su azúcar."),
    ], "<b>La jamaica se puede usar dos veces.</b> Después de colar la primera "
       "jarra, vuelve a hervir la flor: sale una segunda más clarita, "
       "buena para la tarde."),

    ("Sábila", "Aloe vera, penca de sábila", "sabila", [
        ("Lo bueno", "Penca <b>gruesa, pesada y firme</b>, de las de abajo de "
                     "la planta, que son las más llenas."),
        ("Lo malo", "Delgada, doblada, con las puntas secas o con la base negra."),
        ("Precio justo", "<span class='precio'>$10 a $25 la pieza</span>, "
                         "según el tamaño"),
        ("Dónde", "Mercado y vivero. O una maceta en tu casa: aguanta todo."),
        ("Cómo guardar", "Entera en el refrigerador, 2 semanas. "
                         "El gel ya sacado, <b>3 días</b> y en frasco tapado."),
        ("Sustituto", "Aceite de coco para la piel reseca."),
    ], "El <b>jugo amarillo</b> que escurre al cortarla (el acíbar) irrita la "
       "piel y tomado es un purgante fuerte: para la penca en un vaso "
       "<b>30 minutos</b> y tira ese jugo antes de sacar el gel."),

    ("Chía y linaza", "Semillas", "semillas", [
        ("Lo bueno", "Semilla <b>brillante, suelta, sin olor raro</b>. La linaza "
                     "café o dorada da igual."),
        ("Lo malo", "Apelmazada, con olor a rancio o a pintura — eso es grasa "
                    "echada a perder."),
        ("Precio justo", "Chía <span class='precio'>$60 a $100 el kilo</span> · "
                         "Linaza <span class='precio'>$30 a $50 el kilo</span>"),
        ("Dónde", "Mercado a granel o súper. Medio kilo te dura meses."),
        ("Cómo guardar", "Frasco cerrado y fresco. <b>Entera aguanta un año; "
                         "molida se echa a perder en semanas</b> — por eso los "
                         "remedios de este libro la usan entera."),
        ("Sustituto", "Una por la otra, en la misma cantidad."),
    ], "Huélelas antes de comprar. La semilla rancia sabe a pintura y no se "
       "compone con nada."),

    ("Cola de caballo", "Equiseto", "colacaballo", [
        ("Lo bueno", "Tallos <b>verdes, huecos y con nudos</b>, que se quiebran "
                     "al doblarlos."),
        ("Lo malo", "Amarillenta, muy molida, o mezclada con otras hierbas que "
                    "no reconoces."),
        ("Precio justo", "<span class='precio'>$20 a $35 los 50 g</span>"),
        ("Dónde", "Herbolaria."),
        ("Cómo guardar", "Frasco cerrado. Un año."),
        ("Sustituto", "Té ligero de perejil, también por pocos días."),
    ], "Compra <b>poquita</b>. Esta hierba es de las que se usan una semana y "
       "se descansan tres: 50 g te duran medio año."),

    ("Tronadora y prodigiosa", "Las amargas del puesto", "amargas", [
        ("Lo bueno", "Tronadora con <b>flor amarilla</b> visible entre la hoja. "
                     "Prodigiosa gris verdosa y de olor fuerte."),
        ("Lo malo", "Bolsas sin etiqueta donde no distingues qué es qué."),
        ("Precio justo", "<span class='precio'>$20 a $45 los 50 g</span> cada una"),
        ("Dónde", "Herbolaria, con quien te sepa decir el nombre completo."),
        ("Cómo guardar", "Frasco cerrado y oscuro. Un año."),
        ("Sustituto", "Hoja de guayaba, que es más suave y más fácil de hallar."),
    ], "Estas dos son de las <b>fuertes</b>: se usan en cursos de 10 a 15 días "
       "y se descansan. Compra 50 g y ya. Si te ofrecen el kilo 'porque sale "
       "más barato', no lo necesitas."),

    ("Vinagre de manzana", "Vinagre de sidra", "vinagre", [
        ("Lo bueno", "Que diga <b>'de manzana' sin más</b>, turbio, y de "
                     "preferencia <b>con la madre</b> (esa telita del fondo)."),
        ("Lo malo", "'Vinagre blanco saborizado a manzana', o los que traen "
                    "azúcar o caramelo en la etiqueta. Lee la letra chica."),
        ("Precio justo", "<span class='precio'>$35 a $70 los 500 ml</span>"),
        ("Dónde", "Súper. Compara la etiqueta de dos marcas antes de escoger."),
        ("Cómo guardar", "En la alacena, cerrado. Dura años; lo turbio es normal."),
        ("Sustituto", "Jugo de limón, aunque no hace exactamente lo mismo."),
    ], "El vinagre no cura nada por sí solo, y <b>nunca se toma puro</b>: "
       "una cucharada en un vaso grande de agua. Puro te lastima el esmalte "
       "y la garganta."),

    ("Manzanilla, toronjil y hierbabuena", "Las de la noche", "noche", [
        ("Lo bueno", "Manzanilla con <b>flor amarilla entera</b>, no puro palo. "
                     "Hierbabuena de manojo, tiesa y de olor fuerte."),
        ("Lo malo", "Manzanilla café que ya no huele. Hierbabuena aguada o negra "
                    "en las puntas."),
        ("Precio justo", "Seca <span class='precio'>$15 a $35 los 50 g</span> · "
                         "manojo fresco <span class='precio'>$5 a $10</span>"),
        ("Dónde", "Lo seco en herbolaria; lo fresco en el mercado, de manojo."),
        ("Cómo guardar", "Lo fresco en el refrigerador, en un vaso con agua "
                         "como si fuera flor, 1 semana. Lo seco en frasco, un año."),
        ("Sustituto", "Tila o pasiflora para la noche, si no hay toronjil."),
    ], "La manzanilla de bolsita del súper casi siempre trae más polvo que flor. "
       "A granel cuesta menos y rinde el doble."),
]


def _fichas():
    h = [L.capitulo("Una por una", "Las doce que más vas a comprar",
                    sub="Cómo se ve la buena, cómo detectar la mala, cuánto "
                        "debe costarte y con qué la cambias.",
                    token="fichas", nivel=0)]
    for nombre, otros, token, filas, ojo in FICHAS:
        h.append(L.ingrediente(nombre, otros, filas,
                               ojo=f"<b>El consejo de la abuela:</b> {ojo}",
                               token=token))
    return "".join(h)


# ------------------------------------------------------------------
def _precios():
    h = [L.capitulo("De un vistazo", "La tabla de precios justos",
                    sub="Precios de orientación en pesos mexicanos. Varían por "
                        "ciudad, por temporada y por puesto — llévalos como "
                        "referencia, no como ley.",
                    token="precios", nivel=0)]
    h.append(L.caja(
        "Cómo usar esta tabla",
        "<p>Si te piden <b>mucho más</b> que el rango de aquí, pregunta en otro "
        "puesto antes de pagar. Si te piden <b>mucho menos</b>, revisa el olor "
        "y el color: casi siempre es hierba vieja o con relleno.</p>"
        "<p>Y no compres de a kilo lo que usas de a cucharadita.</p>",
        "suave"))
    h.append(L.tabla(
        ["Ingrediente", "Cantidad", "Precio justo"],
        [["Canela de Ceilán en raja", "100 g", "$60 – $120"],
         ["Canela cassia en raja", "100 g", "$25 – $40"],
         ["Hoja de guayaba seca", "50 g", "$20 – $40"],
         ["Hoja de higo seca", "50 g", "$25 – $45"],
         ["Moringa en hoja", "100 g", "$40 – $70"],
         ["Tronadora", "50 g", "$25 – $45"],
         ["Prodigiosa", "50 g", "$20 – $35"],
         ["Cola de caballo", "50 g", "$20 – $35"],
         ["Diente de león", "50 g", "$25 – $40"],
         ["Ortiga", "50 g", "$20 – $35"],
         ["Muicle", "50 g", "$20 – $35"],
         ["Boldo", "50 g", "$20 – $35"],
         ["Cuachalalate (corteza)", "50 g", "$25 – $45"],
         ["Hoja de alcachofa", "50 g", "$25 – $45"],
         ["Manzanilla", "50 g", "$15 – $30"],
         ["Toronjil", "50 g", "$20 – $35"],
         ["Árnica (uso externo)", "50 g", "$20 – $35"],
         ["Fenogreco en semilla", "100 g", "$30 – $50"],
         ["Anís en grano", "50 g", "$15 – $25"],
         ["Hinojo en semilla", "50 g", "$15 – $30"],
         ["Clavo de olor", "50 g", "$25 – $45"],
         ["Laurel", "50 g", "$10 – $20"],
         ["Cúrcuma en polvo", "100 g", "$30 – $60"],
         ["Té verde a granel", "100 g", "$40 – $80"],
         ["Flor de jamaica", "1 kg", "$90 – $140"],
         ["Chía", "1 kg", "$60 – $100"],
         ["Linaza", "1 kg", "$30 – $50"],
         ["Nopal fresco", "1 kg", "$10 – $20"],
         ["Xoconostle", "1 kg", "$30 – $50"],
         ["Jengibre fresco", "1 kg", "$60 – $90"],
         ["Tamarindo con vaina", "1 kg", "$50 – $80"],
         ["Sábila", "1 penca", "$10 – $25"],
         ["Hierbabuena, romero, perejil", "1 manojo", "$5 – $10"],
         ["Vinagre de manzana", "500 ml", "$35 – $70"],
         ["Aceite de oliva", "500 ml", "$60 – $120"],
         ["Aceite de coco", "250 ml", "$60 – $120"],
         ["Sal de grano", "1 kg", "$15 – $25"]]))
    h.append(L.caja(
        "Lo que cuesta empezar",
        "<p>Para arrancar el <b>Reto de 30 Días</b> completo, contando todo "
        "— hierbas, fruta, verdura, aceite y frascos — andas entre "
        "<b>$350 y $600 pesos</b> repartidos en cuatro semanas.</p>"
        "<p>Y de esos, la mitad te va a durar <b>meses</b>: la canela, la "
        "jamaica, la chía y la manzanilla no se acaban en un mes.</p>",
        "verde"))
    return "".join(h)


# ------------------------------------------------------------------
def _no_comprar():
    h = [L.capitulo("Guarda tu dinero", "Lo que NO hay que comprar",
                    sub="Aquí es donde más se le saca el dinero a la gente "
                        "que quiere cuidarse el azúcar.",
                    token="no_comprar", nivel=0)]
    h.append(L.entrada(
        "Todo lo que necesitas para este libro se consigue en el mercado y "
        "cuesta poco. Lo caro casi siempre es lo que menos sirve — y a veces "
        "es lo que hace daño."))
    h.append(L.caja(
        "No lo compres, por caro que se vea",
        "<ul class='lista lista-no'>"
        "<li><b>Cápsulas importadas</b> de nopal, canela o moringa a $300 o "
        "$500. Adentro traen la misma planta que compras en $30, molida y en "
        "cantidad que nadie te garantiza.</li>"
        "<li><b>Raíz de tejocote</b> para bajar de peso. Se ha vendido "
        "adulterada y ha mandado gente al hospital por problemas del corazón. "
        "No la toques.</li>"
        "<li>Cualquier <b>té o producto 'para la diabetes'</b> que venga en "
        "cajita bonita sin decir qué plantas trae ni en qué cantidad.</li>"
        "<li><b>Productos milagro</b> sin registro sanitario, sobre todo los "
        "que se venden por mensaje o en la calle. Varios han salido con "
        "medicamento escondido adentro — y eso, con tu tratamiento, es "
        "peligroso de verdad.</li>"
        "<li><b>Anís estrella molido</b> de origen desconocido: se adultera "
        "con anís estrella japonés, que es tóxico. Cómpralo en estrellas "
        "enteras.</li>"
        "<li><b>Hierbas 'para la diabetes' que nadie te sabe nombrar.</b> "
        "Si en el puesto no te dicen cómo se llama la planta, no te la lleves.</li>"
        "</ul>",
        "alerta"))
    h.append(L.seccion("Las frases que te deben poner alerta", token="frases"))
    h.append(L.parrafo(
        "Si en un puesto, en un video o en un mensaje te dicen alguna de estas, "
        "cierra la cartera:"))
    h.append(L.lista_no([
        "«<b>Esto cura la diabetes</b>.» — Nada la cura. Nada.",
        "«<b>Con esto ya no vas a necesitar la pastilla</b>.» — Esa frase es "
        "la más peligrosa de todas.",
        "«<b>Es natural, no tiene contraindicaciones</b>.» — Todo lo que hace "
        "algo tiene contraindicaciones. Este libro entero trata de eso.",
        "«<b>Los médicos no quieren que se sepa</b>.»",
        "«<b>Fórmula secreta</b>» o «receta que no puedo decirte».",
        "«<b>Es la última pieza, llévatela hoy</b>.»",
    ]))
    h.append(L.caja(
        "La regla de oro",
        "<p>Si un remedio te pide <b>dejar tu medicina</b>, no es un remedio: "
        "es un riesgo. Lo de este libro acompaña. Nunca reemplaza.</p>",
        "verde"))
    return "".join(h)


# ------------------------------------------------------------------
def _lista():
    filas = "".join("<tr><td></td><td></td><td></td></tr>" for _ in range(14))
    tabla = ('<table class="registro"><thead><tr>'
             '<th>Qué</th><th>Cuánto</th><th>Precio que pagué</th>'
             "</tr></thead><tbody>" + filas + "</tbody></table>")
    return (
        L.capitulo("Para llevar al mercado", "Mi lista y mis precios",
                   sub="Imprímela o cópiala. Anota lo que pagas: en tres "
                       "compras ya sabes cuál puesto te conviene.",
                   token="lista", nivel=0)
        + L.parrafo(
            "Lleva esta hoja y una pluma. Apuntar el precio que pagaste es lo "
            "que hace que a la tercera vez ya nadie te vea la cara.")
        + tabla
        + L.caja(
            "Antes de salir de casa",
            "<ul class='lista lista-pt'>"
            "<li>Bolsa de tela y bolsitas de papel para lo seco</li>"
            "<li>Esta hoja y una pluma</li>"
            "<li>Efectivo en <b>cambio chico</b>: en el mercado sale mejor precio</li>"
            "<li>Zapato cerrado y cómodo — vas a caminar más de lo que crees</li>"
            "</ul>",
            "suave"))


def cuerpo(paginas):
    return (_entrada() + _canela() + _fichas() + _precios()
            + _no_comprar() + _lista())


def final():
    return L.cierre(
        "Ya sabes comprar.<br>Eso no te lo quita nadie",
        "<p>La canela se distingue con los dedos. La hierba buena huele. "
        "Lo que no te saben nombrar, no se lleva. Y lo que promete curar, "
        "miente.</p>"
        "<p>Con eso ya compras mejor que la mayoría — y te ahorras cada mes "
        "más de lo que costó este libro.</p>"
        "<p>Nos vemos en el mercado, <strong>martes o miércoles, temprano</strong>.</p>"
        '<p class="firma">— Abuela Mei</p>',
        legal="<b>Sobre los precios.</b> Las cantidades en pesos de esta guía "
              "son de orientación y corresponden a precios de mercado "
              "observados en México; varían por ciudad, temporada y punto de "
              "venta, y cambian con el tiempo. Úsalas para comparar, no como "
              "precio oficial. Esta guía no recomienda marcas ni establecimientos "
              "y no recibe pago de ninguno.")
