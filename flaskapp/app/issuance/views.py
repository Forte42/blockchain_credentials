from . import issuance_blueprint
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required
from ..extensions import db
from ..models import Issuance, Wallet, Credential
from .forms import RevokeForm
from datetime import datetime

@issuance_blueprint.route("/<int:credential_id>", methods=['GET', 'POST'])
def index(credential_id):
    form = RevokeForm()
    credential = Credential.query.get(credential_id)
    issuances = credential.issuances
    active_issuances = [] 
    for issuance in issuances:
        if issuance.active == True:
            active_issuances.append(issuance)
    # credential_issuance = db.session.query(Credential).join(Issuance, Credential.id==Issuance.credential_id).filter(Issuance.credential_id == credential_id).all()
    


    if request.method == 'GET':
        return render_template("issuance/index.html", active_issuances = active_issuances, credential = credential, form=form)

    elif request.method == 'POST':
        
        if form.validate_on_submit():     
            # Request the revoked issuance 
            issuance_id = request.form.get('revokeButton')
            wallet = Wallet.query.filter_by(id=issuance.wallet_id).first()

            # Delete the issuances that the administrator checked
            issuance = Issuance.query.filter_by(id=int(issuance_id)).first()
            issuance.revoked_at = datetime.utcnow()
            issuance.active = False
            db.session.commit()
            flash(f"Successfully deleted issuance for: {wallet.address}")
        return render_template("issuance/index.html", active_issuances = active_issuances, credential = credential, form=form)


