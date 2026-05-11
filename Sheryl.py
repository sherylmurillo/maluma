import tkinter as tk
from tkinter import messagebox
import nltk
from nltk import CFG
from nltk.parse import ChartParser

# Descargar recursos necesarios
nltk.download('punkt')

# ---------------- AST ---------------- #
def simplificar_ast(tree):
    # Si es una palabra (terminal), devolverla
    if isinstance(tree, str):
        return tree

    hijos = [simplificar_ast(t) for t in tree]

    return f"{tree.label()}({', '.join(hijos)})"

# ---------------- DERIVACIÓN ---------------- #
def generar_derivacion(tree, modo="izquierda"):
    pasos = []

    actual = ["E"]
    pasos.append(" ".join(actual))

    def recorrer(t, actual):
        # Si es terminal, no hacer nada
        if isinstance(t, str):
            return actual

        label = t.label()

        hijos = []

        # Obtener hijos
        for h in t:
            if isinstance(h, str):
                hijos.append(h)
            else:
                hijos.append(h.label())

        # Buscar el símbolo a reemplazar
        for i in range(len(actual)):
            if actual[i] == label:

                # Reemplazar símbolo por hijos
                nueva = actual[:i] + hijos + actual[i+1:]

                pasos.append(" ".join(nueva))

                # Derivación izquierda
                if modo == "izquierda":
                    for h in t:
                        nueva = recorrer(h, nueva)

                # Derivación derecha
                else:
                    for h in reversed(t):
                        nueva = recorrer(h, nueva)

                return nueva

        return actual

    recorrer(tree, actual)

    return "\n".join([f"{i+1}. {p}" for i, p in enumerate(pasos)])

# ---------------- FUNCIÓN PRINCIPAL ---------------- #
def procesar():
    try:
        # Obtener gramática escrita por el usuario
        gramatica_texto = txt_gramatica.get("1.0", tk.END)

        # Obtener expresión
        expresion = entry_expresion.get().split()

        # Obtener modo
        modo = opcion.get()

        # Crear CFG
        grammar = CFG.fromstring(gramatica_texto)

        # Crear parser
        parser = ChartParser(grammar)

        # Generar árboles
        trees = list(parser.parse(expresion))

        # Si no encuentra derivación
        if not trees:
            resultado.delete("1.0", tk.END)
            resultado.insert(tk.END, "❌ No se pudo generar la derivación.")
            return

        # Tomar primer árbol
        tree = trees[0]

        # Limpiar resultados
        resultado.delete("1.0", tk.END)

        # Mostrar derivación
        resultado.insert(tk.END, f"📌 Derivación ({modo}):\n\n")
        resultado.insert(tk.END, generar_derivacion(tree, modo))
        resultado.insert(tk.END, "\n\n")

        # Mostrar AST
        resultado.insert(tk.END, "🧠 AST:\n\n")
        resultado.insert(tk.END, simplificar_ast(tree))

        # Dibujar árbol
        tree.draw()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------------- INTERFAZ ---------------- #
ventana = tk.Tk()
ventana.title("Generador CFG - Expresiones Aritméticas")
ventana.geometry("750x700")

# Título gramática
tk.Label(ventana, text="Gramática CFG:").pack()

# Caja gramática
txt_gramatica = tk.Text(ventana, height=12, width=90)
txt_gramatica.pack()

# Gramática por defecto
txt_gramatica.insert(tk.END, """E -> E '+' T | E '-' T | T
T -> T '*' F | T '/' F | F
F -> '(' E ')' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z'""")

# Expresión
tk.Label(ventana, text="Expresión:").pack()

entry_expresion = tk.Entry(ventana, width=60)
entry_expresion.pack()

# Expresión ejemplo
entry_expresion.insert(0, "a + b * c")

# Opciones derivación
opcion = tk.StringVar(value="izquierda")

frame = tk.Frame(ventana)
frame.pack(pady=5)

tk.Radiobutton(frame, text="Izquierda", variable=opcion, value="izquierda").pack(side=tk.LEFT)

tk.Radiobutton(frame, text="Derecha", variable=opcion, value="derecha").pack(side=tk.LEFT)

# Botón procesar
tk.Button(
    ventana,
    text="Procesar",
    command=procesar,
    bg="lightblue",
    width=20
).pack(pady=10)

# Resultados
resultado = tk.Text(ventana, height=25, width=90)
resultado.pack()

# Ejecutar ventana
ventana.mainloop()
