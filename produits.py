import sqlite3
from app import db
from database import Produit

# Connexion à la base de données SQLite
conn = sqlite3.connect('base_donnee.db')
cursor = conn.cursor()



# Liste des produits à ajouter
produits = [
    ("Smartphone Galaxy S22", "Smartphone haut de gamme avec écran AMOLED 6,1 pouces et processeur Exynos 2200.", 799.99),
    ("Ordinateur portable Dell Inspiron", "Ordinateur portable avec processeur Intel Core i5, 8 Go de RAM et SSD 512 Go.", 699.99),
    ("Casque Bose QuietComfort 35 II", "Casque Bluetooth avec réduction de bruit active et autonomie de 20 heures.", 299.99),
    ("Montre Fitbit Charge 5", "Montre connectée avec suivi d'activité, GPS intégré et batterie de 7 jours.", 149.99),
    ("Clé USB 64 Go Kingston", "Clé USB 64 Go avec transfert rapide de données, idéale pour les sauvegardes.", 19.99),
    ("Souris Logitech MX Master 3", "Souris sans fil ergonomique avec 7 boutons programmables et capteur 4000 DPI.", 99.99),
    ("Écouteurs Apple AirPods Pro", "Écouteurs sans fil avec réduction active du bruit et autonomie de 24 heures.", 249.99),
    ("Télévision Samsung 55\" QLED", "Télévision QLED 4K Ultra HD avec technologie de réduction du flou et Smart TV.", 999.99),
    ("Appareil photo Canon EOS 90D", "Appareil photo reflex numérique avec capteur APS-C 32,5 MP et vidéo 4K.", 1199.99),
    ("Tablette Apple iPad Pro 11\"", "Tablette avec processeur A12Z, écran Liquid Retina et 128 Go de stockage.", 799.99),
    ("Tasse en céramique personnalisée", "Tasse en céramique blanche personnalisable, idéale pour le café.", 12.99),
    ("Lampe de bureau LED réglable", "Lampe LED avec intensité lumineuse ajustable et angle de lumière réglable.", 39.99),
    ("Housse de coussin en lin", "Housse de coussin en lin de haute qualité, douce et confortable.", 19.99),
    ("Chaise de bureau ergonomique", "Chaise de bureau avec support lombaire et assise en mousse à mémoire de forme.", 129.99),
    ("Montre Garmin Forerunner 245", "Montre GPS de sport avec suivi de fréquence cardiaque et autonomie de 7 jours.", 229.99),
    ("Tablette Samsung Galaxy Tab S6", "Tablette avec écran Super AMOLED et 128 Go de stockage.", 629.99),
    ("Appareil photo Sony Alpha 7 III", "Appareil photo plein format avec capteur 24,2 MP et vidéo 4K.", 2099.99),
    ("Robot aspirateur Roomba i7+", "Robot aspirateur avec fonction nettoyage automatique et cartographie intelligente.", 699.99),
    ("Chargeur solaire portable", "Chargeur solaire portable de 10 000 mAh pour recharger vos appareils en extérieur.", 29.99),
    ("Montre analogique Fossil", "Montre analogique avec bracelet en cuir et cadran minimaliste.", 89.99),
    ("Sac à dos de randonnée", "Sac à dos de 40L avec multiples poches et système de suspension pour un confort optimal.", 59.99),
    ("Batterie externe Anker PowerCore", "Batterie externe de 20 000 mAh avec deux ports USB pour charger vos appareils en déplacement.", 39.99),
    ("Imprimante Canon PIXMA TS5350", "Imprimante multifonction avec impression sans fil et compatible avec Apple AirPrint.", 69.99),
    ("Montre Suunto 9", "Montre de sport avec GPS, fréquence cardiaque et autonomie de 120 heures.", 499.99),
    ("Tapis de yoga antidérapant", "Tapis de yoga avec surface antidérapante pour une pratique plus sûre et confortable.", 29.99),
    ("Écouteurs Sony WH-1000XM4", "Casque sans fil avec réduction de bruit et autonomie de 30 heures.", 349.99),
    ("Pied de micro ajustable", "Pied de micro réglable pour une utilisation professionnelle ou amateur.", 19.99),
    ("Station météo connectée Netatmo", "Station météo avec capteurs de température, humidité et pression atmosphérique, compatible avec l'app mobile.", 179.99),
    ("Barre de son Bose Soundbar 500", "Barre de son Dolby Atmos avec assistance vocale Alexa et Google Assistant.", 499.99),
    ("Écran Dell UltraSharp U2720Q", "Écran 27 pouces 4K Ultra HD avec des couleurs précises pour les professionnels.", 699.99),
    ("Casque gaming Razer Kraken", "Casque gaming avec son surround 7.1, microphone cardioïde et coussinets en mousse à mémoire de forme.", 89.99),
    ("Brosse à dents électrique Oral-B", "Brosse à dents électrique avec minuterie intégrée et 5 modes de nettoyage.", 49.99),
    ("Mélangeur KitchenAid Artisan", "Mélangeur sur socle avec moteur puissant et différents accessoires pour tous vos besoins culinaires.", 499.99),
    ("Vélo électrique VTC", "Vélo électrique avec moteur de 250W, autonomie de 70 km et cadre en aluminium léger.", 1299.99),
    ("Casque JBL Charge 4", "Haut-parleur Bluetooth avec son stéréo et batterie longue durée (20 heures).", 149.99),
    ("Vapeur verticale Philips GC362", "Fer à repasser à vapeur verticale, idéal pour les vêtements délicats et les rideaux.", 99.99),
    ("Montre TicWatch Pro 3", "Montre connectée avec GPS intégré, suivi d’activité et autonomie de 72 heures.", 299.99),
    ("Sèche-cheveux Dyson Supersonic", "Sèche-cheveux haute technologie avec moteur numérique pour un séchage rapide et doux.", 399.99),
    ("Projecteur Epson EF-100", "Projecteur compact avec résolution Full HD et compatible avec les appareils Android et Apple.", 799.99),
    ("Chaise de gaming DXRacer Formula Series", "Chaise de gaming ergonomique avec support lombaire et repose-tête ajustables.", 249.99),
    ("Tapis de souris Logitech G640", "Tapis de souris de jeu avec une surface lisse pour un contrôle précis de la souris.", 29.99),
    ("Grille-pain Philips HD2581", "Grille-pain avec 6 niveaux de brunissement et un tiroir à miettes facile à nettoyer.", 39.99),
    ("Chaussures de running Nike Air Zoom Pegasus", "Chaussures de course avec amorti Zoom Air et tige en mesh pour une respirabilité optimale.", 119.99),
    ("Appareil photo Fujifilm X-T4", "Appareil photo sans miroir avec capteur 26,1 MP, vidéo 4K et stabilisation d'image.", 1499.99),
    ("Lampe solaire extérieure", "Lampe solaire pour éclairage extérieur avec détection de mouvement et lumière LED.", 24.99),
    ("Barbecue électrique Tefal", "Barbecue électrique avec surface antiadhésive et contrôle de la température.", 99.99),
    ("Coffret de couteaux de cuisine", "Coffret comprenant 5 couteaux en acier inoxydable avec support en bois.", 79.99),
    ("Épilation laser Silk'n Infinity", "Appareil d'épilation à lumière pulsée avec 400 000 impulsions pour un traitement à domicile.", 299.99),
    ("Doudoune Columbia", "Doudoune légère avec doublure en duvet et imperméabilité pour les randonnées hivernales.", 129.99),
    ("Lunettes de soleil Ray-Ban Aviator", "Lunettes de soleil iconiques avec verres polarisants et monture en métal.", 159.99)
]

# Ajout des produits à la base de données
for produit_data in produits:
    produit = Produit(
        nom=produit_data[0],
        description=produit_data[1],
        prix=produit_data[2]
    )
    db.session.add(produit)

db.session.commit()

print("Produits ajoutés avec succès!")