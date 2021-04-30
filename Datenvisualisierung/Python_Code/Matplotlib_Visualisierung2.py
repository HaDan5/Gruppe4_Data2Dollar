import pandas as pd
from matplotlib import pyplot as plt

plt.style.use("seaborn")

data = pd.read_csv("Immowelt_bearbeitet_Bezirke_Kopie.csv")
Baujahr = data["Baujahr"]
Mietpreise = data["Kaltmiete"]
Wohnfläche = data["Wohnfläche"]

plt.scatter(Mietpreise, Wohnfläche, c=Baujahr, cmap="afmhot", edgecolor="black", linewidth=1, alpha=0.75)

cbar = plt.colorbar()
cbar.set_label("Baujahr des Objektes")

plt.xscale("log")
plt.yscale("log")

plt.title("Kaltmiete pro Wohnfläche & Baujahr")
plt.xlabel("Kaltmiete")
plt.ylabel("Wohnfläche")

plt.tight_layout()

plt.savefig("Visualisierung_2.png")
plt.show()
