# Importation des modules
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

def analyze_reslice(image_path):
    """
    Analyse un reslice pour suivre l'évolution de l'intensité et calculer l'absorbance.

    :param image_path: Chemin vers l'image du reslice.
    """

    # Charger l'image en niveaux de gris pour calculer l'intensité
    reslice = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if reslice is None:
        print("Impossible de charger l'image.")
        return

    # Calcul des intensités moyennes par colonne (chaque colonne correspond à 1 seconde)
    intensities = np.mean(reslice, axis=0) #axis = 0 veut dire qu'on moyenne chaque colonne du tableau et on renvoie un tableau de moyennes

    # Déterminer I_0 comme l'intensité maximale
    I0 = max(intensities)
    print(f"I_0 déterminé comme la valeur maximale d'intensité : {I0:.2f}")

    # Calcul de l'absorbance
    absorbance_values = -np.log10(intensities / I0)

    # Temps associé à chaque colonne
    times = np.arange(len(intensities))  # 1 colonne = 1 seconde

    # Ajustement logarithmique pour vérifier la cinétique d'ordre 1
    valid_indices = [i for i, A in enumerate(absorbance_values) if A > 0]   #Pour eviter les problèmes si l'absorbance est négative
    valid_times = times[valid_indices]
    valid_absorbances = absorbance_values[valid_indices]
    ln_absorbances = np.log(valid_absorbances)


    # Régression linéaire de la courbe de ln_absorbance = f(t)
    slope, intercept, r_value, p_value, std_err = linregress(valid_times, ln_absorbances)
    k_fit = -slope
    ln_A0_fit = intercept
    A0_fit = np.exp(ln_A0_fit)

    print(f"Paramètres ajustés : A0 = {A0_fit:.3f}, k = {k_fit:.3f}")
    print(f"Coefficient de corrélation : r^2 = {r_value**2:.3f}")

    # Tracer les résultats
    plt.figure(figsize=[6.4, 4.8])
    plt.plot(times, absorbance_values, 'o', label="Données Absorbance")
    plt.title("Évolution de l'absorbance au cours du temps")
    plt.xlabel(r"Temps ($s$)")
    plt.ylabel(r"Absorbance $A$")
    plt.legend()
    plt.grid()

    plt.savefig("Aborbance.pdf", bbox_inches='tight')

    plt.show()

    # Tracé des données logarithmiques et du fit
    ln_absorbance_fit = intercept + slope * valid_times
    plt.figure(figsize=[6.4, 4.8])
    plt.plot(valid_times, ln_absorbances, 'o', label=r"$\ln(A)$")
    plt.plot(valid_times, ln_absorbance_fit, '-', label=f"Fit linéaire (k = {k_fit:.3f})")
    plt.title("Vérification d'une cinétique d'ordre 1 (ln(Absorbance))")
    plt.xlabel(r"Temps ($s$)")
    plt.ylabel(r"$\ln(A)$ : Logarithme de l'absorbance")
    plt.legend()
    plt.grid()

    plt.savefig("LogAborbance.pdf", bbox_inches='tight')

    plt.show()

    # Créer une figure combinée avec le reslice en bas et la courbe logarithmique en haut
    fig, ax = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})

    # Tracé de la courbe logarithmique et du fit
    ax[0].plot(valid_times, ln_absorbances, 'o', label="ln(Absorbance)", markersize=4)
    ax[0].plot(valid_times, ln_absorbance_fit, '-', label=f"Fit linéaire (k = {k_fit:.3f})")
    ax[0].set_title("Vérification d'une cinétique d'ordre 1 (ln(Absorbance))")
    ax[0].set_xlabel("Temps (s)")
    ax[0].set_ylabel("ln(Absorbance)")
    ax[0].legend()
    ax[0].grid()

    reslice = cv2.imread(image_path, cv2.IMREAD_COLOR)  # Charger l'image en couleur
    reslice = cv2.cvtColor(reslice, cv2.COLOR_BGR2RGB)  # Convertir de BGR à RGB pour Matplotlib

    # Affichage du reslice en dessous
    ax[1].imshow(reslice, aspect='auto')
    ax[1].set_title("Reslice (suivi temporel)")
    ax[1].set_xlabel("Temps (s)")
    ax[1].set_ylabel("Position verticale (pixels)")

    # Ajuster l'espacement entre les sous-graphes
    plt.tight_layout()
    plt.savefig("LogAborbance_Reslice.pdf", bbox_inches='tight')

    plt.show()

    # Comparaison des données expérimentales et du modèle ajusté
    predicted_absorbances = A0_fit * np.exp(-k_fit * times)
    plt.plot(times, absorbance_values, 'o', label="Données expérimentales", markersize=4)
    plt.plot(times, predicted_absorbances, '-', label="Modèle ordre 1", linewidth=2)
    plt.title("Comparaison des absorbances expérimentales et ajustées")
    plt.xlabel("Temps (s)")
    plt.ylabel("Absorbance")
    plt.legend()

    plt.tight_layout()
    plt.show()


# Exemple d'utilisation
image_path = "/Users/noedaniel/Downloads/VideoAlice/Reslice1Pixel.png"
analyze_reslice(image_path)


"""
POUR VISUALISER LE RESLICE
"""

"""
reslice = cv2.imread(image_path, cv2.IMREAD_COLOR)  # Charger l'image en couleur
reslice = cv2.cvtColor(reslice, cv2.COLOR_BGR2RGB)  # Convertir de BGR à RGB pour Matplotlib

plt.figure(figsize=[9, 3])
plt.tick_params(left = False, right = False , labelleft = False , 
                labelbottom = True, bottom = True) 
plt.imshow(reslice, aspect='auto')
plt.xlabel(r"Temps [$s$]")
plt.ylabel(r'Colonne de 4 pixels de haut')
plt.title("Reslice - Evolution cinétique")

plt.savefig("reslice.pdf", bbox_inches='tight')

plt.show()
"""