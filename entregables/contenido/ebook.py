# -*- coding: utf-8 -*-
"""
Ebook principal — Azúcar en Equilibrio.

Orden del libro:
  portada · aviso · carta · índice · las cuatro reglas ·
  capítulo de seguridad · la despensa y el modo de preparar ·
  los 55 remedios en 7 capítulos · índice por planta ·
  diario de 7 días · cierre

El capítulo de seguridad va ANTES de los remedios y no después, a
propósito: es lo que la página de ventas promete como "la parte más
importante", y es lo único del libro que puede evitar un accidente.
"""

import libro as L
from .remedios import CAPITULOS, todos

META = dict(
    slug="ebook",
    archivo="Azucar-en-Equilibrio.pdf",
    titulo_pdf="Azúcar en Equilibrio — 55 remedios naturales con dosis, hora y advertencia",
    autor="Abuela Mei",
    asunto="Guía de cuidado casero de uso tradicional para acompañar el "
           "tratamiento del azúcar. No sustituye la consulta médica.",
    claves="azúcar, glucosa, remedios naturales, tés, aguas, mistelas, "
           "cataplasmas, nopal, hoja de guayaba, canela, moringa, diabetes",
    pie="Azúcar en Equilibrio",
)


# ------------------------------------------------------------------
def portada():
    return L.portada(
        sello="Raíces de la Naturaleza",
        titulo_html="Azúcar<br>en <span>Equilibrio</span>",
        sub="55 remedios naturales — tés, aguas, mistelas y cataplasmas — "
            "ordenados por lo que sientes, cada uno con su dosis, su hora "
            "y su advertencia.",
        cuenta="55 REMEDIOS · 7 CAPÍTULOS",
        autor="de la Abuela Mei",
    )


# ------------------------------------------------------------------
def _aviso():
    return (
        '<div style="padding-top:6mm">'
        + L.caja(
            "Antes de preparar nada, lee esto",
            "<p>Este libro es una guía de <b>cuidado casero de uso tradicional</b>. "
            "Es informativo. No es un medicamento, no es una consulta y no sustituye "
            "el diagnóstico ni el tratamiento de tu médico.</p>"
            "<p><b>Nunca suspendas, cambies ni saltes tu medicina</b> para el azúcar, "
            "la presión o el corazón por tomar algo de este libro. Los remedios de "
            "aquí <b>acompañan</b> tu tratamiento; no lo reemplazan y no compiten con él.</p>"
            "<p>Varias de estas plantas <b>bajan el azúcar por su cuenta</b>. Eso suena "
            "bien, pero significa que se <b>suman</b> al efecto de la metformina, la "
            "glibenclamida y la insulina, y que juntas te pueden bajar el azúcar de más. "
            "Por eso cada ficha trae su advertencia, y por eso el capítulo de seguridad "
            "va antes que los remedios.</p>"
            "<p>Si tienes embarazo o lactancia, enfermedad del riñón o del hígado, "
            "cáncer, un trasplante o una cirugía programada, <b>consulta con tu médico "
            "antes de usar cualquier remedio de este libro</b>.</p>",
            "alerta")
        + L.caja(
            "Si en este momento te sientes mal",
            "<p>Si tienes <b>temblor, sudor frío, mareo, visión borrosa, confusión o "
            "el corazón acelerado</b>, deja el libro: puede ser azúcar baja y se "
            "atiende con azúcar de verdad, ahora mismo. Ve directo a la página de "
            "<b>Cuando el azúcar baja de más</b>, en el capítulo de seguridad.</p>"
            "<p>Si tienes <b>vómito que no para, aliento con olor dulce o a fruta, "
            "respiración rápida y profunda, dolor en el pecho o mucho sueño del que "
            "no puedes salir</b>, eso es urgencia médica. Llama al <b>911</b>.</p>",
            "")
        + "</div>"
    )


# ------------------------------------------------------------------
def _carta():
    return (
        L.capitulo("Unas palabras primero", "Lo que hacemos con las otras 23 horas",
                   token="carta", nivel=0)
        + L.entrada(
            "Casi todas llegan igual. Toman su pastilla, se miden el dedo, "
            "apuntan el número — y ahí se les acabó el día de cuidarse.")
        + L.parrafo(
            "Y yo les pregunto siempre lo mismo: ¿y las otras veintitrés horas?")
        + L.parrafo(
            "Porque el cuerpo no avisa solo cuando te mides. Avisa a media tarde, "
            "cuando la comida te tumba en el sillón. Avisa en la noche, cuando te "
            "levantas por tercera vez con la boca seca. Avisa a las cinco, cuando "
            "la mano se va sola al pan sin que tú se lo ordenes. Y avisa en los pies, "
            "que un día empiezan a sentirse como si los trajeras dormidos.", "capitular")
        + L.parrafo(
            "Esas horas son las que nadie te explica. Y son las que se pueden acompañar.")
        + L.parrafo(
            "Lo que tienes en las manos son 55 remedios que mi abuela me enseñó y que "
            "yo fui acomodando cuarenta años, con lo que da el mercado de aquí: el nopal, "
            "la hoja de guayaba, la canela, la moringa, el jengibre. Nada importado, "
            "nada de cápsula cara, nada que tengas que pedir por internet.")
        + L.parrafo(
            "Pero te voy a decir algo que a lo mejor no esperas de un libro de remedios, "
            "y prefiero decírtelo en la primera página que en la última:")
        + L.caja(
            "",
            "<p><b>Ningún té de este libro va a hacer el trabajo de tu medicina.</b> "
            "Si alguien te promete que sí, te está mintiendo y te está poniendo en "
            "riesgo. Tu pastilla no se toca. Tu insulina no se toca. Lo que hacemos "
            "aquí es acompañar — que es otra cosa, y no es poca cosa.</p>",
            "verde")
        + L.parrafo(
            "Y hay algo más, que es justo lo contrario de lo que se suele decir: "
            "varias de estas plantas <b>sí bajan el azúcar</b>. Por eso mismo hay que "
            "tenerles respeto. El nopal en ayunas, la canela a diario, el fenogreco, "
            "la tronadora — todas se suman a lo que tú ya tomas. Y dos cosas que bajan "
            "el azúcar al mismo tiempo pueden bajarla de más.")
        + L.parrafo(
            "Por eso cada uno de los 55 remedios de este libro trae tres cosas que "
            "casi ningún libro de hierbas trae: <b>cuánto</b>, <b>a qué hora</b> y "
            "<b>quién no debe tomarlo</b>. Ese último renglón es el que más me costó "
            "escribir, y es el que más importa.")
        + L.parrafo(
            "Empieza por el capítulo que sigue. Sé que dan ganas de irse directo a los "
            "tés — todas quieren — pero ese capítulo es el que hace que lo demás sea "
            "seguro. Son doce páginas. Con eso ya sabrás qué no mezclar con tu medicina, "
            "cómo se siente cuando el azúcar baja de más y qué señales son de médico "
            "y no de cocina.")
        + L.parrafo("Luego sí, ponemos el agua a hervir.")
        + '<p class="firma">— Abuela Mei</p>'
    )


# ------------------------------------------------------------------
def _indice(paginas):
    entradas = [
        ("cap", "carta", "Lo que hacemos con las otras 23 horas"),
        ("cap", "seguridad", "Lo primero, antes que cualquier té"),
        ("it", "reglas", "Las cuatro reglas de la Abuela Mei"),
        ("it", "baja", "Cuando el azúcar baja de más"),
        ("it", "alarma", "Las señales que piden médico, no té"),
        ("it", "medicinas", "Qué no mezclar con tu medicina"),
        ("it", "quien_no", "Quién no debe usar estos remedios"),
        ("it", "empezar", "Cómo empezar sin arriesgar"),
        ("cap", "despensa", "La despensa y el modo de preparar"),
        ("grupo", "Los 55 remedios"),
    ]
    for c in CAPITULOS:
        entradas.append(("cap", c["token"],
                         f'{c["num"]} — {c["titulo"]}'))
        for r in c["remedios"]:
            entradas.append(("it", f'r{r["n"]:02d}',
                             f'{r["n"]:02d}. {r["nombre"]}'))
    entradas += [
        ("grupo", "Para buscar rápido"),
        ("cap", "por_planta", "Índice por planta"),
        ("cap", "diario", "Mi diario de 7 días"),
    ]
    return (L.capitulo("Índice", "Lo que hay adentro", token="indice", nivel=0)
            + L.indice(entradas, paginas))


# ------------------------------------------------------------------
def _seguridad():
    h = [L.capitulo(
        "Capítulo de seguridad",
        "Lo primero, antes que cualquier té",
        sub="Este es el capítulo que sostiene a los otros siete. Si solo vas a "
            "leer una parte del libro, que sea esta.",
        token="seguridad", nivel=0)]

    # --- las cuatro reglas ---
    h.append(L.seccion("Las cuatro reglas de la Abuela Mei", token="reglas"))
    h.append(L.parrafo(
        "Cuarenta años me llevó resumirlo en cuatro. Si te aprendes estas cuatro, "
        "el resto del libro se vuelve seguro casi solo."))
    h.append(L.caja(
        "1 · La pastilla no se toca",
        "<p>Tu metformina, tu glibenclamida, tu insulina y tu medicina de la presión "
        "se siguen tomando <b>igual, a la misma hora y en la misma cantidad</b>. "
        "Ningún remedio de este libro es motivo para bajarle, saltártela o dejarla. "
        "Eso lo decide tu médico con estudios en la mano, nunca un té y nunca yo.</p>",
        "verde"))
    h.append(L.caja(
        "2 · Un remedio nuevo a la vez, y de día",
        "<p>Cuando estrenes algo de este libro, que sea <b>uno solo</b> y por la "
        "mañana o a mediodía — nunca dos cosas nuevas el mismo día, y nunca algo "
        "nuevo antes de dormir. Si te va a caer mal o te va a bajar el azúcar, "
        "quieres estar despierta y acompañada cuando pase, no dormida. "
        "Dale <b>tres días</b> a cada remedio nuevo antes de sumar otro.</p>",
        "verde"))
    h.append(L.caja(
        "3 · Si te sientes mal: azúcar primero, preguntas después",
        "<p>Temblor, sudor frío, mareo, hambre de repente, corazón acelerado, "
        "visión borrosa. Eso <b>no se aguanta</b> ni se pasa con un té. "
        "Se atiende con azúcar de verdad, en ese momento, y viene explicado "
        "en la página siguiente. Primero te compones; después averiguas por qué pasó.</p>",
        "verde"))
    h.append(L.caja(
        "4 · Lo que tomas todos los días, se le dice al médico",
        "<p>Llévale este libro a tu próxima consulta, o una lista de lo que estás "
        "tomando. No es para pedirle permiso: es para que tenga el cuadro completo "
        "cuando lea tus estudios. Un médico que sabe que tomas canela y nopal a "
        "diario puede ajustarte la medicina bien. Uno que no lo sabe, no.</p>",
        "verde"))

    # --- hipoglucemia ---
    h.append(L.seccion("Cuando el azúcar baja de más", token="baja"))
    h.append(L.parrafo(
        "A esto se le llama <b>hipoglucemia</b>, y es lo único de este libro que "
        "de verdad puede ponerte en riesgo en cuestión de minutos. No pasa seguido, "
        "pero cuando pasa hay que saber qué hacer sin ir a buscarlo."))
    h.append(L.parrafo(
        "Es más probable si usas <b>glibenclamida, glimepirida o insulina</b>, "
        "si te saltaste una comida, si tomaste alcohol, si caminaste más de lo "
        "normal — o si estrenaste una planta de las que bajan el azúcar sin avisarle "
        "a nadie."))
    h.append(L.sub("Así se siente"))
    h.append(L.lista_pt([
        "Temblor en las manos, sobre todo si no hacía frío",
        "Sudor frío, de repente y sin razón",
        "Hambre que aparece de golpe, con ansiedad",
        "El corazón acelerado o golpeando",
        "Mareo, debilidad en las piernas, ganas de sentarte",
        "Visión borrosa o doble",
        "Irritabilidad o ganas de llorar sin motivo",
        "Hormigueo alrededor de la boca",
        "Dificultad para encontrar las palabras, o sentirte 'rara' sin saber explicar",
    ]))
    h.append(L.caja(
        "La regla del 15 y 15",
        "<p><b>1.</b> Si puedes medirte, mídete. Menos de <b>70 mg/dL</b> es azúcar baja. "
        "Si no tienes con qué medirte y te sientes así, <b>trátalo igual</b>: es peor "
        "esperar.</p>"
        "<p><b>2.</b> Toma <b>15 gramos de azúcar rápida</b>. Eso es una de estas, "
        "una sola:</p>"
        "<ul class='lista lista-pt'>"
        "<li>1 cucharada sopera de azúcar en medio vaso de agua</li>"
        "<li>½ vaso (120 ml) de refresco normal — <b>no de dieta</b></li>"
        "<li>½ vaso (120 ml) de jugo de naranja o de manzana</li>"
        "<li>1 cucharada sopera de miel</li>"
        "<li>3 o 4 tabletas de glucosa de farmacia</li>"
        "</ul>"
        "<p><b>3.</b> Espera <b>15 minutos</b> sentada. No camines, no te pongas a "
        "hacer cosas.</p>"
        "<p><b>4.</b> Vuelve a medirte. Si sigue abajo de 70, <b>repite</b> los 15 gramos.</p>"
        "<p><b>5.</b> Cuando ya subió, come algo de verdad: una torta chica, un "
        "sándwich, unas galletas con queso. Si tu siguiente comida es en más de una "
        "hora, este paso no te lo saltes.</p>",
        "alerta"))
    h.append(L.caja(
        "Lo que no se hace",
        "<p><b>No</b> te cures una baja con chocolate, pan dulce, helado o galletas "
        "con crema: la grasa hace que el azúcar tarde en llegar, justo cuando "
        "necesitas que llegue rápido.</p>"
        "<p><b>No</b> uses refresco de dieta, ni endulzante, ni fruta sola: no traen "
        "el azúcar que hace falta en ese momento.</p>"
        "<p><b>Si la persona está inconsciente o no puede tragar, no le metas nada "
        "a la boca.</b> Ponla de lado, en el piso, y llama al <b>911</b>. Si tienes "
        "glucagón en casa y te enseñaron a usarlo, es el momento.</p>",
        "alerta"))
    h.append(L.caja(
        "Después de una baja",
        "<p>Apúntala: la hora, qué habías comido, qué medicina te tocaba, qué "
        "remedio nuevo habías empezado. Y avísale a tu médico <b>aunque ya se te "
        "haya pasado</b>. Dos bajas en una misma semana significan que hay que "
        "ajustar algo — casi siempre la medicina, a veces el remedio. Y mientras "
        "tanto, <b>suspende el remedio nuevo</b> hasta que hables con él.</p>",
        "suave"))

    # --- señales de alarma ---
    h.append(L.seccion("Las señales que piden médico, no té", token="alarma"))
    h.append(L.parrafo(
        "Esta es la página que más me costó escribir, porque es la que dice dónde "
        "termina lo que yo puedo hacer por ti. Si tienes cualquiera de estas, "
        "cierra el libro y busca atención. Un remedio casero aquí no ayuda: "
        "<b>retrasa</b>, y el retraso es lo que hace el daño."))
    h.append(L.caja(
        "Al 911 o a urgencias, ahora",
        "<ul class='lista lista-no'>"
        "<li>Vómito que no para y no puedes retener ni agua</li>"
        "<li>Aliento con olor dulce o a fruta, respiración rápida y profunda</li>"
        "<li>Confusión, no poder despertar bien, desmayo</li>"
        "<li>Dolor en el pecho, falta de aire, o dolor que baja por el brazo o la mandíbula</li>"
        "<li>Azúcar arriba de 300 mg/dL que no baja, con vómito o mucho sueño</li>"
        "<li>Un pie hinchado, rojo, caliente, con mal olor o con una zona negra</li>"
        "<li>Fiebre alta con escalofríos y no poder tomar líquidos</li>"
        "<li>Debilidad de un lado del cuerpo, boca torcida, no poder hablar bien</li>"
        "</ul>",
        "alerta"))
    h.append(L.caja(
        "Al médico esta semana, sin dejarlo pasar",
        "<ul class='lista lista-no'>"
        "<li>Una herida en el pie o la pierna que lleva más de una semana sin cerrar</li>"
        "<li>Sed que no se quita por más agua que tomes, y orinar muchísimo</li>"
        "<li>Bajar de peso sin estar haciendo nada para bajar</li>"
        "<li>Visión borrosa nueva, manchitas flotando o destellos de luz</li>"
        "<li>Hormigueo o adormecimiento que avanza, o que ya no sientes nada en los pies</li>"
        "<li>Infecciones que se repiten: en la orina, en la piel, en la boca</li>"
        "<li>Dos episodios de azúcar baja en la misma semana</li>"
        "<li>Números en ayunas arriba de 200 mg/dL varios días seguidos</li>"
        "<li>Piel u ojos amarillos, orina muy oscura, dolor fuerte del lado derecho</li>"
        "</ul>",
        ""))
    h.append(L.caja(
        "El pie se revisa todos los días",
        "<p>Un minuto, con luz, todas las noches. Planta, talón, entre cada dedo y "
        "las uñas. Si no alcanzas a verte la planta, usa un espejo en el piso o "
        "pide que te revisen.</p>"
        "<p>Buscas: cortadas, ampollas, piel blanca entre los dedos, manchas "
        "moradas o negras, uñas enterradas, zonas calientes. <b>Un pie que siente "
        "menos no te va a avisar con dolor.</b> Tienes que verlo tú.</p>",
        "suave"))

    # --- interacciones ---
    h.append(L.seccion("Qué no mezclar con tu medicina", token="medicinas"))
    h.append(L.parrafo(
        "Busca aquí lo que tú tomas. Esto no es para asustarte: es para que sepas "
        "con qué estar pendiente y qué preguntarle a tu médico en la consulta."))
    h.append(L.tabla(
        ["Si tomas", "Cuidado con", "Qué hacer"],
        [
            ["<b>Metformina</b>",
             "Plantas que bajan el azúcar: canela, nopal, hoja de guayaba, hoja de higo, "
             "tronadora, fenogreco, moringa, vinagre",
             "Se suman. Empieza con la mitad de la dosis del remedio y mídete más "
             "seguido la primera semana. Separa 1 hora de la fibra (chía, linaza, nopal)."],
            ["<b>Glibenclamida, glimepirida</b> (sulfonilureas)",
             "Las mismas de arriba, y el alcohol",
             "Es el grupo con <b>más riesgo de azúcar baja</b>. No te saltes comidas, "
             "trae siempre azúcar a la mano y avísale a tu médico antes de empezar "
             "cualquier remedio de los fuertes (7, 30, 47)."],
            ["<b>Insulina</b>",
             "Las mismas, más el ejercicio y el ayuno",
             "Mídete antes y 2 horas después de estrenar un remedio. "
             "Nunca ajustes tus unidades por tu cuenta por estar tomando un té."],
            ["<b>Warfarina, aspirina, clopidogrel</b>",
             "Jengibre, cúrcuma, ajo, clavo, canela cassia, té verde, manzanilla en exceso",
             "Consulta antes. Si te salen moretones fácil, si te sangran las encías "
             "o la nariz, suspende el remedio y avisa."],
            ["<b>Medicina para la presión</b>",
             "Jamaica, apio, hoja de guayaba, ortiga, cola de caballo",
             "Pueden bajarte la presión de más. Si te mareas al levantarte, "
             "siéntate, y bájale al remedio."],
            ["<b>Diuréticos</b> (furosemida, hidroclorotiazida)",
             "Cola de caballo, diente de león, perejil, ortiga, jamaica",
             "Se suman y te sacan sales. <b>No los combines</b> sin que tu médico lo sepa."],
            ["<b>Levotiroxina</b> (tiroides)",
             "Moringa, chía, linaza, toronjil, té verde",
             "Separa <b>4 horas</b> entre tu pastilla y estos remedios."],
            ["<b>Cualquier pastilla</b>",
             "La fibra: nopal, chía, linaza",
             "Retrasan la absorción. Deja <b>1 hora</b> entre tu medicina y el remedio."],
            ["<b>Cirugía programada</b>",
             "Todo lo que baje el azúcar o adelgace la sangre",
             "<b>Suspende 2 semanas antes</b> y dile al anestesiólogo todo lo que tomas."],
        ]))

    # --- quién no ---
    h.append(L.seccion("Quién no debe usar estos remedios", token="quien_no"))
    h.append(L.lista_no([
        "<b>Embarazo y lactancia.</b> La mayoría de las plantas de este libro no "
        "están estudiadas en embarazo y varias son abortivas. Si estás embarazada, "
        "buscando embarazo o amamantando, este libro no es para ti ahorita.",
        "<b>Niñas y niños.</b> Las dosis de aquí son de adulto. Nada de esto se le "
        "da a un menor sin pediatra.",
        "<b>Enfermedad del riñón.</b> Todo el capítulo 2 y varias hierbas diuréticas "
        "quedan fuera salvo que tu nefrólogo diga otra cosa.",
        "<b>Enfermedad del hígado.</b> Fuera el boldo, la canela cassia y la cúrcuma "
        "en cantidad.",
        "<b>Diabetes tipo 1.</b> Estos remedios pueden acompañar, pero la insulina "
        "es insustituible, siempre y sin excepción.",
        "<b>Trasplante o medicina inmunosupresora.</b> Muchas plantas interfieren. "
        "Consulta cada una, sin excepción.",
        "<b>Gastroparesia</b> (el estómago se vacía lento). Fuera el vinagre y "
        "cuidado con la fibra.",
    ]))

    # --- cómo empezar ---
    h.append(L.seccion("Cómo empezar sin arriesgar", token="empezar"))
    h.append(L.numerada([
        "Elige <b>un solo</b> remedio, del capítulo de lo que más te molesta hoy.",
        "Prepáralo con <b>la mitad</b> de la dosis los primeros tres días.",
        "Tómalo <b>de día</b>, nunca estrenando de noche.",
        "Mídete como siempre, y además <b>2 horas después</b> del remedio esos primeros días.",
        "Apúntalo en el diario de la página final: qué tomaste, a qué hora, qué número saliste.",
        "Si a los tres días vas bien, sube a la dosis completa o suma un segundo remedio.",
        "Si te sientes rara, <b>suspéndelo</b> y anótalo. No lo aguantes a ver si se pasa.",
    ]))
    h.append(L.caja(
        "Si prefieres que yo te lo ordene",
        "<p>El <b>Bono 1 — Reto de 30 Días</b> ya trae este primer mes armado, "
        "día por día, con las dosis subiendo despacio y en el orden correcto. "
        "Si te abruma escoger, empieza por ahí y este libro lo usas de consulta.</p>",
        "suave"))
    return "".join(h)


# ------------------------------------------------------------------
def _despensa():
    h = [L.capitulo(
        "Antes de los remedios",
        "La despensa y el modo de preparar",
        sub="Cuatro maneras de preparar, seis medidas y tres reglas de higiene. "
            "Con esto entiendes las 55 fichas que siguen.",
        token="despensa", nivel=0)]

    h.append(L.seccion("Las cuatro formas que vas a ver"))
    h.append(L.tabla(
        ["Forma", "Qué es", "Para qué sirve"],
        [
            ["<b>Té (infusión)</b>",
             "Se hierve el agua, se <b>apaga</b> y se echa la hierba tapada 5 a 10 minutos.",
             "Hoja y flor, que son delicadas: manzanilla, hierbabuena, moringa, guayaba."],
            ["<b>Cocimiento</b>",
             "La planta se pone desde el agua fría y se <b>hierve</b> 10 minutos.",
             "Raíz, corteza y semilla, que son duras: canela, cuachalalate, jengibre, hoja de higo."],
            ["<b>Agua</b>",
             "En frío, reposando en el refrigerador. No lleva fuego.",
             "Fruta, verdura y semilla: pepino, chía, linaza, nopal."],
            ["<b>Mistela</b>",
             "Macerado en frío, 24 a 48 horas, en agua o vinagre. <b>Sin alcohol y sin azúcar.</b>",
             "Concentrados que duran la semana. Se toman diluidos y en dosis chicas."],
            ["<b>Cataplasma y compresa</b>",
             "Se pone <b>encima</b>, nunca se toma.",
             "Piernas, vientre, talones, ojos cansados."],
        ]))
    h.append(L.caja(
        "Por qué importa la diferencia",
        "<p>Si hierves una hoja delicada, la echas a perder y te sabe a pasto. "
        "Si solo remojas una corteza, no suelta nada y te tomas agua de color. "
        "Cada ficha te dice cuál usar; ya no tienes que acordarte.</p>",
        "suave"))

    h.append(L.seccion("Las medidas de este libro"))
    h.append(L.tabla(
        ["Cuando digo", "Quiere decir"],
        [
            ["1 taza", "250 ml — una taza de café normal, no un tarro"],
            ["1 vaso", "250 ml. Cuando digo <i>vaso grande</i>, son 300 ml"],
            ["1 cucharada sopera", "15 ml — la grande de la sopa"],
            ["1 cucharadita", "5 ml — la del café"],
            ["1 puño chico", "Lo que cabe en tu mano cerrada, como 15 g de hierba seca"],
            ["1 raja de canela", "Un tramo de 5 cm, del grueso de un dedo"],
        ]))

    h.append(L.seccion("Tres reglas de higiene que no me salto"))
    h.append(L.numerada([
        "<b>Frasco de vidrio, limpio y seco.</b> Para las mistelas, lávalo con agua "
        "caliente y jabón y déjalo secar boca abajo. Una gota de agua sucia echa a "
        "perder el frasco entero.",
        "<b>Todo lo fresco se lava antes</b>, aunque venga del mercado y se vea limpio. "
        "La hoja de guayaba y la hierbabuena se enjuagan hoja por hoja.",
        "<b>Lo que huela agrio, burbujee o se vea turbio, se tira.</b> Sin duelo y "
        "sin probarlo. Un macerado fermentado ya tiene alcohol, y el alcohol aquí "
        "no lo queremos.",
    ]))

    h.append(L.seccion("Cuánto dura cada cosa"))
    h.append(L.tabla(
        ["Preparado", "Dura", "Dónde"],
        [
            ["Té recién hecho", "El mismo día", "Fuera, tapado"],
            ["Agua de fruta o verdura", "24 horas", "Refrigerador"],
            ["Mistela de agua", "5 días", "Refrigerador, en su frasco"],
            ["Mistela de nopal", "<b>3 días</b>", "Refrigerador"],
            ["Mistela en vinagre", "2 meses", "Refrigerador"],
            ["Aceite de romero", "3 meses", "Frasco oscuro, lugar fresco"],
            ["Hierba seca", "1 año", "Frasco cerrado, lejos de la luz y del vapor"],
        ]))
    h.append(L.caja(
        "La hierba seca también se echa a perder",
        "<p>Si ya no huele a nada, ya no sirve. Guárdala en frasco, no en la bolsita "
        "del mercado, y lejos de la estufa: el vapor la arruina en un mes. "
        "En el <b>Bono 2 — Guía del Mercado</b> te digo cuánto debe costar cada cosa "
        "y cómo saber si te están dando gato por liebre.</p>",
        "suave"))
    return "".join(h)


# ------------------------------------------------------------------
def _cuerpo_remedios():
    h = []
    for c in CAPITULOS:
        h.append(L.capitulo(c["num"], c["titulo"], sub=c["sub"],
                            cuantos=c["cuantos"], token=c["token"], nivel=0))
        for p in c["intro"]:
            h.append(L.parrafo(p))
        for r in c["remedios"]:
            h.append(L.remedio(
                r["n"], r["nombre"], r["tipo"], r["para"],
                r["ingredientes"], r["preparacion"],
                r["dosis"], r["hora"], r["advertencia"]))
    return "".join(h)


# ------------------------------------------------------------------
PLANTAS = {
    "Anís": ["anís"], "Alcachofa": ["alcachofa"], "Apio": ["apio"],
    "Árnica": ["árnica"], "Canela de Ceilán": ["canela"],
    "Cáscara de manzana": ["manzana"], "Chía": ["chía"],
    "Clavo de olor": ["clavo"], "Col (repollo)": ["col (repollo)", "hojas grandes de col"],
    "Cola de caballo": ["cola de caballo"], "Cuachalalate": ["cuachalalate"],
    "Cúrcuma": ["cúrcuma"], "Diente de león": ["diente de león"],
    "Fenogreco (alholva)": ["fenogreco"], "Hierbabuena / menta": ["hierbabuena", "menta"],
    "Hinojo": ["hinojo"], "Hoja de guayaba": ["guayaba"],
    "Hoja de higo": ["hoja de higo", "hojas de higo"], "Jamaica": ["jamaica"],
    "Jengibre": ["jengibre"], "Laurel": ["laurel"], "Limón": ["limón"],
    "Linaza": ["linaza"], "Manzanilla": ["manzanilla"], "Moringa": ["moringa"],
    "Muicle": ["muicle"], "Nopal": ["nopal"], "Ortiga": ["ortiga"],
    "Pepino": ["pepino"], "Perejil": ["perejil"], "Prodigiosa": ["prodigiosa"],
    "Romero": ["romero"], "Sábila": ["sábila", "penca de sábila"],
    "Tamarindo": ["tamarindo"], "Té verde": ["té verde"],
    "Toronjil": ["toronjil"], "Tronadora": ["tronadora"],
    "Vinagre de manzana": ["vinagre de manzana"], "Xoconostle": ["xoconostle"],
}


def _por_planta():
    h = [L.capitulo("Para buscar rápido", "Índice por planta",
                    sub="Si ya tienes la hierba en la mano y quieres ver en qué "
                        "remedios entra, búscala aquí.",
                    token="por_planta", nivel=0)]
    filas = []
    for planta, claves in sorted(PLANTAS.items()):
        nums = []
        for r in todos():
            texto = (" ".join(r["ingredientes"]) + " " + r["nombre"]).lower()
            if any(k in texto for k in claves):
                nums.append(f'{r["n"]:02d}')
        if nums:
            filas.append([f"<b>{planta}</b>", ", ".join(nums)])
    h.append(L.tabla(["Planta o ingrediente", "Remedios"], filas))
    h.append(L.caja(
        "Ojo con esto",
        "<p>Que una planta salga en varios remedios <b>no significa que puedas "
        "tomarlos todos el mismo día</b>. Se acumula. Si ya estás tomando canela "
        "en el remedio 01, no le sumes el 29, el 35 y la mistela 44 la misma tarde: "
        "escoge uno.</p>",
        "alerta"))
    return "".join(h)


# ------------------------------------------------------------------
def _diario():
    filas = "".join(
        "<tr><td></td><td></td><td></td><td></td><td></td></tr>" for _ in range(9))
    tabla = (
        '<table class="registro"><thead><tr>'
        '<th>Día</th><th>Remedio y hora</th><th>Azúcar en ayunas</th>'
        '<th>2 h después</th><th>Cómo me sentí</th>'
        "</tr></thead><tbody>" + filas + "</tbody></table>")
    return (
        L.capitulo("La última página", "Mi diario de 7 días",
                   sub="Imprímela o cópiala en un cuaderno. Es lo que le vas a "
                       "enseñar a tu médico en la próxima consulta.",
                   token="diario", nivel=0)
        + L.parrafo(
            "Una semana de apuntes vale más que un año de acordarse. Con esta hoja "
            "tu médico puede ver <b>qué remedio coincidió con qué número</b> — y eso "
            "es lo que le permite ajustarte bien la medicina.")
        + tabla
        + L.caja(
            "Cómo llenarla",
            "<p><b>Remedio y hora:</b> solo el número y la hora. \"R-07, 2 pm\" basta.</p>"
            "<p><b>Cómo me sentí:</b> en tres palabras. \"Menos sueño\", \"igual\", "
            "\"me dio cólico\". No escribas bonito, escribe rápido.</p>"
            "<p>Y si un día tuviste <b>azúcar baja</b>, márcalo con una cruz grande. "
            "Eso es lo primero que tu médico va a querer ver.</p>",
            "suave"))


# ------------------------------------------------------------------
def cuerpo(paginas):
    return "".join([
        _aviso(),
        _carta(),
        _indice(paginas),
        _seguridad(),
        _despensa(),
        _cuerpo_remedios(),
        _por_planta(),
        _diario(),
    ])


# ------------------------------------------------------------------
def final():
    return L.cierre(
        "Cuídate todos los días,<br>no solo cuando te mides",
        "<p>Ya tienes los 55. No los uses todos — no se trata de eso. "
        "Escoge el que va con lo que hoy te molesta, dale sus tres días y "
        "fíjate en cómo te sientes.</p>"
        "<p>Y acuérdate de las cuatro reglas, que son las que sostienen todo lo demás: "
        "<strong>la pastilla no se toca</strong>; <strong>un remedio nuevo a la vez y "
        "de día</strong>; <strong>si te sientes mal, azúcar primero</strong>; "
        "<strong>lo que tomas todos los días, se le dice al médico</strong>.</p>"
        "<p>Empieza mañana por la mañana. Con uno.</p>"
        '<p class="firma">— Abuela Mei</p>')
