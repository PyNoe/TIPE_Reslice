# Fichiers pour analyser le suivi cinétique

Deux scripts python :
- `script.py` qui permet de transformer la vidéo en un dossier de captures d'écran prises toutes les 1 seconde.
- `VerifCinétique.py` qui permet de calculer l'intensité de chaque image en passant par le niveaux de gris. Une fois l'intensité calculée, on calcule l'absorbance avec $A=-\log_{10}(I/I_0)$. Puis on essaye de remonter à une loi d'ordre un avec une régression linéaire sur $\ln(A) = f(t)$.

Le reslice en question est le suivant : 
![](https://github.com/PyNoe/TIPE_Reslice/blob/main/Reslice.gif)
