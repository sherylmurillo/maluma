import tkinter as tk
from tkinter import ttk, messagebox
import nltk
from nltk import CFG
from nltk.parse import EarleyChartParser
from nltk.tokenize import wordpunct_tokenize

# Descargar recursos
nltk.download('punkt')

# Variable global
ultimo_tree = None

# ---------------- AST TEXTO ---------------- #
def simplificar_ast(tree):

    if isinstance(tree, str):
        return tree

    hijos = [simplificar_ast(h) for h in tree]

    return f"{tree.label()}({', '.join(hijos)})"

# ---------------- CONVERTIR AST A ÁRBOL ---------------- #
def convertir_ast(tree):

    if isinstance(tree, str):
        return tree

    hijos = []

    for h in tree:

        if isinstance(h, str):

            # Ignorar paréntesis
            if h not in ["(", ")"]:
                hijos.append(h)

        else:

            hijos.append(
                convertir_ast(h)
            )

    return nltk.Tree(
        tree.label(),
        hijos
    )

# ---------------- DERIVACIÓN ---------------- #
def generar_derivacion(tree, modo="izquierda"):

    pasos = []

    actual = ["E"]

    pasos.append(" ".join(actual))

    def recorrer(t, actual):

        if isinstance(t, str):
            return actual

        label = t.label()

        hijos = []

        for h in t:

            if isinstance(h, str):
                hijos.append(h)

            else:
                hijos.append(h.label())

        indices = range(len(actual))

        if modo == "derecha":
            indices = reversed(range(len(actual)))

        for i in indices:

            if actual[i] == label:

                nueva = actual[:i] + hijos + actual[i+1:]

                pasos.append(" ".join(nueva))

                if modo == "izquierda":

                    for h in t:
                        nueva = recorrer(h, nueva)

                else:

                    for h in reversed(t):
                        nueva = recorrer(h, nueva)

                return nueva

        return actual

    recorrer(tree, actual)

    return "\n".join(
        [f"{i+1}. {p}" for i, p in enumerate(pasos)]
    )

# ---------------- MOSTRAR ÁRBOL ---------------- #
def mostrar_arbol():

    global ultimo_tree

    if ultimo_tree:

        ultimo_tree.draw()

    else:

        messagebox.showinfo(
            "Información",
            "Primero procesa una expresión."
        )

# ---------------- MOSTRAR AST ---------------- #
def mostrar_ast():

    global ultimo_tree

    if ultimo_tree:

        ast = convertir_ast(ultimo_tree)

        ast.draw()

    else:

        messagebox.showinfo(
            "Información",
            "Primero procesa una expresión."
        )

# ---------------- PROCESAR ---------------- #
def procesar():

    global ultimo_tree

    try:

        resultado.delete("1.0", tk.END)

        # Tokenizar expresión
        expresion = wordpunct_tokenize(
            entry_expresion.get()
        )

        # Gramática
        grammar = CFG.fromstring("""

        E -> E '+' T
        E -> E '-' T
        E -> T

        T -> T '*' F
        T -> T '/' F
        T -> F

        F -> '(' E ')'

        F -> '0'
        F -> '1'
        F -> '2'
        F -> '3'
        F -> '4'
        F -> '5'
        F -> '6'
        F -> '7'
        F -> '8'
        F -> '9'

        F -> 'a'
        F -> 'b'
        F -> 'c'
        F -> 'd'
        F -> 'e'
        F -> 'f'
        F -> 'g'
        F -> 'h'
        F -> 'i'
        F -> 'j'
        F -> 'k'
        F -> 'l'
        F -> 'm'
        F -> 'n'
        F -> 'o'
        F -> 'p'
        F -> 'q'
        F -> 'r'
        F -> 's'
        F -> 't'
        F -> 'u'
        F -> 'v'
        F -> 'w'
        F -> 'x'
        F -> 'y'
        F -> 'z'

        """)

        # Parser
        parser = EarleyChartParser(grammar)

        # Generar árboles
        trees = list(
            parser.parse(expresion)
        )

        # Validar
        if not trees:

            resultado.insert(
                tk.END,
                "❌ Expresión inválida"
            )

            return

        # Primer árbol
        tree = trees[0]

        # Guardar árbol
        ultimo_tree = tree

        # Tipo derivación
        modo = opcion.get()

        # ---------------- DERIVACIÓN ---------------- #

        resultado.insert(
            tk.END,
            f"📌 DERIVACIÓN ({modo.upper()})\n\n"
        )

        resultado.insert(
            tk.END,
            generar_derivacion(
                tree,
                modo
            )
        )

        resultado.insert(
            tk.END,
            "\n\n"
        )

        # ---------------- AST TEXTO ---------------- #

        resultado.insert(
            tk.END,
            "🧠 AST\n\n"
        )

        resultado.insert(
            tk.END,
            simplificar_ast(tree)
        )

        resultado.insert(
            tk.END,
            "\n\n✅ Expresión válida"
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )

# ---------------- INTERFAZ ---------------- #

ventana = tk.Tk()

ventana.title(
    "Generador CFG PRO"
)

ventana.geometry("800x550")

ventana.configure(
    bg="#1e1e2f"
)

# ---------------- ESTILO ---------------- #

style = ttk.Style()

style.theme_use("clam")

# ---------------- TÍTULO ---------------- #

titulo = tk.Label(
    ventana,
    text="🧠 GENERADOR CFG Y AST",
    font=("Segoe UI", 26, "bold"),
    bg="#1e1e2f",
    fg="white"
)

titulo.pack(pady=20)

# ---------------- FRAME PRINCIPAL ---------------- #

frame_principal = tk.Frame(
    ventana,
    bg="#1e1e2f"
)

frame_principal.pack(
    fill="both",
    expand=True
)

# ---------------- EXPRESIÓN ---------------- #

frame_expr = tk.Frame(
    frame_principal,
    bg="#2b2b40"
)

frame_expr.pack(
    padx=20,
    pady=20,
    fill="x"
)

label_expr = tk.Label(
    frame_expr,
    text="✏️ Expresión",
    font=("Segoe UI", 15, "bold"),
    bg="#2b2b40",
    fg="white"
)

label_expr.pack(
    anchor="w",
    padx=10,
    pady=10
)

entry_expresion = tk.Entry(
    frame_expr,
    font=("Consolas", 15),
    bg="#121220",
    fg="white",
    insertbackground="white",
    bd=0,
    width=60
)

entry_expresion.pack(
    padx=10,
    pady=10,
    ipady=8
)

entry_expresion.insert(
    0,
    "x+y*(5*x)"
)

# ---------------- OPCIONES ---------------- #

frame_opciones = tk.Frame(
    frame_principal,
    bg="#1e1e2f"
)

frame_opciones.pack(
    pady=10
)

opcion = tk.StringVar(
    value="izquierda"
)

radio1 = tk.Radiobutton(
    frame_opciones,
    text="Izquierda",
    variable=opcion,
    value="izquierda",
    font=("Segoe UI", 12),
    bg="#1e1e2f",
    fg="white",
    selectcolor="#2b2b40"
)

radio1.pack(
    side=tk.LEFT,
    padx=20
)

radio2 = tk.Radiobutton(
    frame_opciones,
    text="Derecha",
    variable=opcion,
    value="derecha",
    font=("Segoe UI", 12),
    bg="#1e1e2f",
    fg="white",
    selectcolor="#2b2b40"
)

radio2.pack(
    side=tk.LEFT,
    padx=20
)

# ---------------- BOTÓN PROCESAR ---------------- #

btn = tk.Button(
    frame_principal,
    text="🚀 Procesar",
    command=procesar,
    font=("Segoe UI", 14, "bold"),
    bg="#6c63ff",
    fg="white",
    activebackground="#5a52e0",
    activeforeground="white",
    bd=0,
    padx=20,
    pady=12,
    cursor="hand2"
)

btn.pack(
    pady=15
)

# ---------------- BOTONES EXTRA ---------------- #

frame_botones = tk.Frame(
    frame_principal,
    bg="#1e1e2f"
)

frame_botones.pack(
    pady=10
)

# Botón árbol sintáctico
btn_arbol = tk.Button(
    frame_botones,
    text="🌳 Ver Árbol",
    command=mostrar_arbol,
    font=("Segoe UI", 12, "bold"),
    bg="#00b894",
    fg="white",
    activebackground="#009e7f",
    activeforeground="white",
    bd=0,
    padx=20,
    pady=10,
    cursor="hand2"
)

btn_arbol.pack(
    side=tk.LEFT,
    padx=15
)

# Botón AST
btn_ast = tk.Button(
    frame_botones,
    text="🧠 Ver AST",
    command=mostrar_ast,
    font=("Segoe UI", 12, "bold"),
    bg="#fd79a8",
    fg="white",
    activebackground="#e66797",
    activeforeground="white",
    bd=0,
    padx=20,
    pady=10,
    cursor="hand2"
)

btn_ast.pack(
    side=tk.LEFT,
    padx=15
)

# ---------------- RESULTADOS ---------------- #

frame_resultado = tk.Frame(
    frame_principal,
    bg="#2b2b40"
)

frame_resultado.pack(
    padx=20,
    pady=20,
    fill="both",
    expand=True
)

label_resultado = tk.Label(
    frame_resultado,
    text="📄 Resultados",
    font=("Segoe UI", 15, "bold"),
    bg="#2b2b40",
    fg="white"
)

label_resultado.pack(
    anchor="w",
    padx=10,
    pady=10
)

resultado = tk.Text(
    frame_resultado,
    font=("Consolas", 12),
    bg="#121220",
    fg="white",
    insertbackground="white",
    bd=0
)

resultado.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

# ---------------- EJECUTAR ---------------- #

ventana.mainloop()
