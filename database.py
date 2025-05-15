from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    sexe = db.Column(db.String(10), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    telephone = db.Column(db.String(15), nullable=False)

    factures = db.relationship('Facture', backref='client', lazy=True)

class Produit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))  # Ajoute cette ligne


class Facture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    tva= db.Column(db.Float, nullable=False)
    lignes = db.relationship('LigneFacture', backref='facture', lazy=True)

class LigneFacture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facture_id = db.Column(db.Integer, db.ForeignKey('facture.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)

    produit = db.relationship('Produit', backref='lignes_factures')
