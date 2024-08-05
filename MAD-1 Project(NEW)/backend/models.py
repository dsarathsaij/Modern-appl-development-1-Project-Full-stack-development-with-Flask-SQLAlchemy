from .db import db

class infdata(db.Model):
    in_id = db.Column(db.Integer, primary_key=True,autoincrement=True,nullable=False)
    in_un = db.Column(db.String(255), unique=True,nullable=False)
    in_password = db.Column(db.String(255), nullable=False)
    in_role = db.Column(db.String(50), nullable=False)
    in_platform = db.Column(db.String(50), nullable=False)
    in_reach = db.Column(db.Integer, nullable=False)
    in_flag=db.Column(db.String(50), default="False")
    

class spodata(db.Model):
    sp_id = db.Column(db.Integer, primary_key=True,autoincrement=True,nullable=False)
    sp_un = db.Column(db.String(255), unique=True,nullable=False)
    sp_password = db.Column(db.String(255), nullable=False)
    sp_role = db.Column(db.String(50), nullable=False)
    sp_flag=db.Column(db.String(50), default="False")

class Campaign(db.Model):
    sp_id = db.Column(db.String(255), db.ForeignKey('spodata.sp_id'), nullable=False)
    campaign_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)    
    goals = db.Column(db.String(), nullable=False)    
    item= db.Column(db.String(50), nullable=True)
    visibility = db.Column(db.String(50), nullable=True, default="public")
    spodata_entry = db.relationship('spodata', backref=db.backref('campaigns', lazy=True))
    in_id = db.Column(db.Integer, db.ForeignKey('infdata.in_id'))
    infdata_entry = db.relationship('infdata', backref=db.backref('campaigns', lazy=True))
    ### 
    ad_requests = db.relationship('Adreq', backref='campaign', cascade='all, delete')


class Adreq(db.Model):
    ad_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    in_id = db.Column(db.Integer, db.ForeignKey('infdata.in_id'))
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.campaign_id'))
    sp_id = db.Column(db.Integer, db.ForeignKey('spodata.sp_id'))
    status = db.Column(db.String(255), nullable=False, default='pending')
    message=db.Column(db.String(),nullable=False)
    campname=db.Column(db.String(),nullable=False)

    