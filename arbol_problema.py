# Creating a graphical representation of the problem tree using matplotlib

# Initialize the figure
fig, ax = plt.subplots(figsize=(10, 8))
ax.axis("off")  # Turn off the axes

# Main problem (trunk of the tree)
ax.text(0.5, 0.5, "Ineficiencias en el Proceso de Evaluación Psicológica", fontsize=12,
        bbox=dict(boxstyle="round,pad=0.5", edgecolor="black", facecolor="lightcoral"), ha="center", va="center")

# Define causes (roots)
causes = {
    "Falta de Digitalización": (0.3, 0.3),
    "Capacitación Insuficiente": (0.7, 0.3),
    "Altos Costos Operativos": (0.5, 0.2)
}

# Define consequences (branches)
consequences = {
    "Tiempos Prolongados de Evaluación": (0.3, 0.7),
    "Errores en Transcripción de Datos": (0.5, 0.8),
    "Baja Calidad en la Selección de Conductores": (0.7, 0.7)
}

# Add causes (roots) with arrows
for cause, (x, y) in causes.items():
    ax.annotate("", xy=(0.5, 0.5), xytext=(x, y),
                arrowprops=dict(facecolor="black", width=1.5, headwidth=6))
    ax.text(x, y, cause, fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"), ha="center")

# Add consequences (branches) with arrows
for consequence, (x, y) in consequences.items():
    ax.annotate("", xy=(0.5, 0.5), xytext=(x, y),
                arrowprops=dict(facecolor="black", width=1.5, headwidth=6))
    ax.text(x, y, consequence, fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"), ha="center")

# Title
plt.title("Árbol del Problema: Evaluación Psicológica de Conductores", fontsize=14, fontweight="bold")
plt.show()
