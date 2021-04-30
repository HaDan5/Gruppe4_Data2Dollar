import csv
import numpy as np
from collections import Counter
from matplotlib import pyplot as plt



plt.xkcd()

with open("immowelt_bearbeitet_Bezirke_Kopie.csv") as csv_file:
	csv_reader = csv.DictReader(csv_file)

	Bezirke_Counter = Counter()

	for row in csv_reader:
		Bezirke_Counter.update(row["Bezirke"].split(";"))


Bezirke = []
Anzahl_Objekte = []

for item in Bezirke_Counter.most_common(12):
	Bezirke.append(item[0])
	Anzahl_Objekte.append(item[1])


Bezirke.reverse()
Anzahl_Objekte.reverse()

plt.barh(Bezirke, Anzahl_Objekte, color=["#FFC900", "#FFB500", "#FF9800", "#FF8000", "#FF7500", "#FF7100", "#FF6700", "#FF5800", "#FF5300", "#FF4500", "#FF2C00", "#FF0000"])

plt.title("Verfügbare Objekte in Berlin")

plt.xlabel("Anzahl Objekte")

plt.tight_layout()


plt.show()

