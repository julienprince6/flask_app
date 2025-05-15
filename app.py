from flask import Flask, render_template, request, redirect, url_for,flash
from database import db, Produit, Client, Facture, LigneFacture
from datetime import datetime
from flask import make_response
from xhtml2pdf import pisa
from io import BytesIO
from collections import defaultdict
from sqlalchemy import func



app = Flask(__name__)
app.secret_key = '74917823497uiyfgiusdfuisyj7w469qeghtrfqoe8jfwehti8qjwery09'  # Définir la clé secrète
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base_donnee.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)



with app.app_context():
    db.create_all()


# 
@app.route('/')
def dashboard():
    return render_template('dashboard.html')


# =======================
# ROUTES PRODUITS
# =======================

@app.route('/produits')
def liste_produits():
    produits = Produit.query.all()
    return render_template('produits.html', produits=produits)

@app.route("/produits/ajouter", methods=["GET", "POST"])
def ajouter_produits():
    if request.method == "POST":
        i = 1
        while True:
            nom = request.form.get(f'nom_{i}')
            description = request.form.get(f'description_{i}')
            prix = request.form.get(f'prix_{i}')
            
            if not nom or not prix:
                break  # On arrête si un champ essentiel est vide

            produit = Produit(
                nom=nom,
                description=description or "",
                prix=float(prix)
            )
            db.session.add(produit)
            i += 1

        db.session.commit()
#        flash("Produits ajoutés avec succès.")
        return redirect(url_for("liste_produits"))

    # En GET : on affiche la page
    produits = Produit.query.all()
    return render_template("ajouter_produit.html", produits=produits)





@app.route('/produits/modifier/<int:id>', methods=['GET', 'POST'])
def modifier_produit(id):
    produit = Produit.query.get_or_404(id)
    if request.method == 'POST':
        produit.nom = request.form['nom']
        produit.prix = float(request.form['prix'])
        produit.description = request.form['description']
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de la modification du produit : {e}")
        return redirect(url_for('liste_produits'))
    return render_template('modifier_produit.html', produit=produit)

@app.route('/produits/supprimer/<int:id>')
def supprimer_produit(id):
    produit = Produit.query.get_or_404(id)
    db.session.delete(produit)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la suppression du produit : {e}")
    return redirect(url_for('liste_produits'))


# =======================
# ROUTES CLIENTS
# =======================


@app.route("/clients")
def liste_clients():
    clients = Client.query.all()
    return render_template("clients.html", clients=clients)

@app.route('/recherche_client')
def recherche_client():
    query = request.args.get('q', '').lower()
    clients = Client.query.filter(
        (Client.nom.ilike(f'%{query}%')) | 
        (Client.prenom.ilike(f'%{query}%')) |
        (Client.email.ilike(f'%{query}%')) |
        (Client.telephone.ilike(f'%{query}%'))
    ).all()
    return render_template('partials/_clients_table.html', clients=clients)

@app.route('/factures_client/<int:client_id>')




@app.route('/factures/client/<int:client_id>')
def factures_client(client_id):
    client = Client.query.get_or_404(client_id)
    factures = Facture.query.filter(Facture.client_id == client_id).all()

    for facture in factures:
        total_ht = sum(ligne.produit.prix * ligne.quantite for ligne in facture.lignes)
        taux_tva = facture.tva if facture.tva else 0.1925
        montant_tva = total_ht * taux_tva
        total_ttc = total_ht + montant_tva

        facture.total_ht = total_ht
        facture.montant_tva = montant_tva
        facture.total_ttc = total_ttc

    return render_template('factures_client.html', client=client, factures=factures)




# =======================
# ROUTES FACTURE
# =======================


@app.route("/factures")
def liste_factures():
    recherche_id = request.args.get("recherche_id", type=int)
    factures_data = []

    if recherche_id:
        facture = Facture.query.get(recherche_id)
        if facture:
            total_ht = sum(ligne.produit.prix * ligne.quantite for ligne in facture.lignes)
            total_ttc = total_ht * (1 + facture.tva if facture.tva else 1.1925)
            factures_data.append({
                "facture": facture,
                "total_ht": total_ht,
                "total_ttc": total_ttc
            })
    else:
        factures = Facture.query.all()
        for facture in factures:
            total_ht = sum(ligne.produit.prix * ligne.quantite for ligne in facture.lignes)
            total_ttc = total_ht * (1 + facture.tva if facture.tva else 1.1925)
            factures_data.append({
                "facture": facture,
                "total_ht": total_ht,
                "total_ttc": total_ttc
            })

    return render_template("factures.html", factures=factures_data)

@app.route('/factures/creer', methods=['GET', 'POST'])
def creer_facture():
    produits = Produit.query.all()

    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        sexe = request.form['sexe']
        adresse = request.form['adresse']
        email = request.form['email']
        telephone = request.form['telephone']
        tva_form = request.form.get('tva', type=float, default=0.1925)

        client_existant = Client.query.filter_by(email=email).first()
        if client_existant:
            client = client_existant
        else:
            client = Client(nom=nom, prenom=prenom, sexe=sexe, adresse=adresse, email=email, telephone=telephone)
            db.session.add(client)
            db.session.commit()

        facture = Facture(date=datetime.now(), client_id=client.id, tva=tva_form)
        db.session.add(facture)
        db.session.commit()

        i = 1
        while True:
            produit_id = request.form.get(f'produit_id_{i}')
            quantite = request.form.get(f'quantite_{i}')
            if not produit_id or not quantite:
                break
            ligne = LigneFacture(
                facture_id=facture.id,
                produit_id=int(produit_id),
                quantite=int(quantite)
            )
            db.session.add(ligne)
            i += 1

        db.session.commit()
        return redirect(url_for('voir_facture', id=facture.id))

    return render_template('creer_facture.html', produits=produits)

@app.route('/facture/modifier/<int:id>', methods=['GET', 'POST'])
def modifier_facture(id):
    facture = Facture.query.get_or_404(id)
    produits = Produit.query.all()

    if request.method == 'POST':
        for ligne in facture.lignes:
            db.session.delete(ligne)

        db.session.commit()

        facture.tva = request.form.get('tva', type=float, default=0.1925)

        for i in range(len(request.form.getlist('produit_id'))):
            produit_id = int(request.form.getlist('produit_id')[i])
            quantite = int(request.form.getlist('quantite')[i])
            ligne = LigneFacture(facture_id=facture.id, produit_id=produit_id, quantite=quantite)
            db.session.add(ligne)

        db.session.commit()
        flash('Facture mise à jour avec succès.', 'success')
        return redirect(url_for('voir_factures'))

    return render_template('modifier_facture.html', facture=facture, produits=produits)

@app.route("/recherche_facture")
def recherche_facture():
    id_facture = request.args.get("id", type=int)
    nom_prenom = request.args.get("nom_prenom", type=str)

    factures_data = []
    query = Facture.query

    if id_facture:
        query = query.filter(Facture.id == id_facture)

    if nom_prenom:
        nom_prenom = nom_prenom.lower()
        query = query.join(Client).filter(
            (Client.nom.ilike(f"%{nom_prenom}%")) |
            (Client.prenom.ilike(f"%{nom_prenom}%"))
        )

    factures = query.all()

    for facture in factures:
        total_ht = sum(ligne.produit.prix * ligne.quantite for ligne in facture.lignes)
        total_ttc = total_ht * (1 + facture.tva if facture.tva else 1.1925)
        factures_data.append({
            "facture": facture,
            "total_ht": total_ht,
            "total_ttc": total_ttc
        })

    return render_template("partials/_factures_table.html", factures=factures_data)

@app.route('/factures/voir/<int:id>')
def voir_facture(id):
    facture = Facture.query.get_or_404(id)
    total_ht = sum(ligne.produit.prix * ligne.quantite for ligne in facture.lignes)
    taux_tva = facture.tva if facture.tva else 0.1925
    montant_tva = total_ht * taux_tva
    total_ttc = total_ht + montant_tva

    return render_template(
        'voir_facture.html',
        facture=facture,
        total_ht=total_ht,
        montant_tva=montant_tva,
        total_ttc=total_ttc,
        taux_tva=taux_tva
    )

@app.route('/factures/supprimer/<int:id>')
def supprimer_facture(id):
    facture = Facture.query.get_or_404(id)
    db.session.delete(facture)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la suppression de la facture : {e}")
    return redirect(url_for('liste_factures'))

@app.route('/factures/pdf/<int:id>')
def telecharger_facture(id):
    facture = Facture.query.get_or_404(id)
    total_ht = sum(ligne.produit.prix * ligne.quantite for ligne in facture.lignes)
    taux_tva = facture.tva if facture.tva else 0.1925
    montant_tva = total_ht * taux_tva
    total_ttc = total_ht + montant_tva

    html = render_template(
        'facture_pdf.html',
        facture=facture,
        total_ht=total_ht,
        montant_tva=montant_tva,
        total_ttc=total_ttc,
        taux_tva=taux_tva
    )

    result = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=result)

    if pisa_status.err:
        return "Erreur lors de la génération du PDF", 500

    response = make_response(result.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=facture_{facture.id}.pdf'
    return response








# =======================
# LANCEMENT
# =======================

if __name__ == '__main__':
    app.run(debug=True)
