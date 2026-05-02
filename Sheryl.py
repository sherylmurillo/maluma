import tkinter as tk
from tkinter import messagebox
import nltk
from nltk import CFG
from nltk.parse import ChartParser

nltk.download('punkt')

def simplificar_ast(tree):
    if isinstance(tree, str):
        return tree

    hijos = [simplificar_ast(t) for t in tree]

    if tree.label() in ['Det']:
        return hijos[0]

    return f"{tree.label()}({', '.join(hijos)})"

def generar_derivacion(tree, modo="izquierda"):
    pasos = []

    actual = ["S"]
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

        for i in range(len(actual)):
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

    return "\n".join([f"{i+1}. {p}" for i, p in enumerate(pasos)])

def procesar():
    try:
        gramatica_texto = txt_gramatica.get("1.0", tk.END)
        expresion = entry_expresion.get().split()
        modo = opcion.get()

        grammar = CFG.fromstring(gramatica_texto)
        parser = ChartParser(grammar)

        trees = list(parser.parse(expresion))

        if not trees:
            resultado.delete("1.0", tk.END)
            resultado.insert(tk.END, "❌ No se pudo generar la derivación.")
            return

        tree = trees[0]

        resultado.delete("1.0", tk.END)

        resultado.insert(tk.END, f"📌 Derivación ({modo}):\n")
        resultado.insert(tk.END, generar_derivacion(tree, modo) + "\n\n")

        resultado.insert(tk.END, "🌳 Árbol de derivación generado (ver ventana emergente)\n\n")

        resultado.insert(tk.END, "🧠 AST:\n")
        resultado.insert(tk.END, simplificar_ast(tree) + "\n")

        tree.draw()

    except Exception as e:
        messagebox.showerror("Error", str(e))

ventana = tk.Tk()
ventana.title("Generador CFG PRO 🔥")
ventana.geometry("650x650")

tk.Label(ventana, text="Gramática (CFG):").pack()

txt_gramatica = tk.Text(ventana, height=10, width=70)
txt_gramatica.pack()

# Ejemplo por defecto
txt_gramatica.insert(tk.END, """S -> NP VP
NP -> Det N
VP -> V NP
Det -> 'the'
N -> 'dog' | 'cat'
V -> 'sees'""")

tk.Label(ventana, text="Expresión:").pack()

entry_expresion = tk.Entry(ventana, width=50)
entry_expresion.pack()
entry_expresion.insert(0, "the dog sees the cat")

opcion = tk.StringVar(value="izquierda")

frame = tk.Frame(ventana)
frame.pack()

tk.Radiobutton(frame, text="Izquierda", variable=opcion, value="izquierda").pack(side=tk.LEFT)
tk.Radiobutton(frame, text="Derecha", variable=opcion, value="derecha").pack(side=tk.LEFT)

tk.Button(ventana, text="Procesar", command=procesar, bg="lightblue").pack(pady=10)

resultado = tk.Text(ventana, height=18, width=70)
resultado.pack()

ventana.mainloop()