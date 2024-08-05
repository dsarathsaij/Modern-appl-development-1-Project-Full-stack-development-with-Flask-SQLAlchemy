from flask import render_template, request, redirect, url_for,session, abort, flash
from .models import *
from .db import db
from datetime import datetime

from flask import current_app as app
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


#app.secret_key = 'your_secret_key'
credentials = {'email': 'admin@gmail.com', 'password': 'admin'}


@app.route('/')
def index():
    return render_template('main.html')

###############sponsor###################

@app.route('/sponsorlogin.html', methods=['GET', 'POST'])
def splogin():
    if request.method == 'POST':
        un = request.form['sp_un']
        password = request.form['sp_password']
        user = spodata.query.filter_by(sp_un=un).first()
        if user:
            if user.sp_password==password:
                session['user_id'] = user.sp_id 
                return redirect(f'/sponsor_page_id_{user.sp_id}')
            else:
                return "enter the password correctly"
        else:
            return "user doesn't exist"
    return render_template('sponsorlogin.html')

@app.route('/sponsorregister.html', methods=['GET', 'POST'])
def sporeg():
    if request.method == 'POST':
        un = request.form['sp_un']
        password = request.form['sp_password']
        role = request.form['sp_role']
        main_data = spodata(sp_un = un ,sp_password = password ,sp_role = role)
        db.session.add(main_data)
        db.session.commit()
        return redirect(url_for('splogin'))
    return render_template('sponsorregister.html')

@app.route('/sponsor_page_id_<int:sp_id>', methods=['GET', 'POST'])
def userforsp(sp_id):
    if 'user_id' not in session or session['user_id'] != sp_id:
        return redirect(url_for('splogin'))
    user = spodata.query.get(sp_id)
    if not user:
        return "User not found"
    ads=Adreq.query.filter_by(sp_id=session.get('user_id')).all()
    campaigns=Campaign.query.filter_by(sp_id=user.sp_id).all() or []
    if user.sp_flag == "True":
        return " You have been flagged by an admin."
    return render_template('sponsor_page.html',user=user,campaigns=campaigns,ads=ads)

@app.route('/sponsor_page/update/<int:campaign_id>', methods=['GET', 'POST'])
def updcamp(campaign_id):
    campaign=Campaign.query.get(campaign_id)
    if request.method=="POST":
        if campaign:
            campaign.campaign_name = request.form['edca']
            campaign.description = request.form['edde']
            campaign.start_date = datetime.strptime(request.form['edsd'], '%Y-%m-%d').date()
            campaign.end_date = datetime.strptime(request.form['eded'], '%Y-%m-%d').date()
            campaign.payment_amount = request.form['edbu']
            campaign.goals = request.form['edgo']
            campaign.item = request.form['edit']
            campaign.visibility = request.form['edvis']
            db.session.commit()
            user = spodata.query.filter_by(sp_id=campaign.sp_id).first()
            return redirect(url_for('userforsp', sp_id=user.sp_id))
    else:
        user = spodata.query.filter_by(sp_id=campaign.sp_id).first()
        return render_template('editcamp.html', campaign_id=campaign_id, campaign=campaign, user=user)
    
@app.route('/sponsor_page/updatead/<int:ad_id>', methods=['GET', 'POST'])
def updadreq(ad_id):
    adreq=Adreq.query.get(ad_id)
    if request.method=="POST":
        if adreq:
            adreq.campname = request.form['adca']
            adreq.message = request.form['adme']
            db.session.commit()
            user = spodata.query.filter_by(sp_id=adreq.sp_id).first()
            return redirect(url_for('userforsp', sp_id=user.sp_id))
    else:
        user = spodata.query.filter_by(sp_id=adreq.sp_id).first() or []
        campaigns = Campaign.query.all()
        return render_template('editadreq.html', ad_id=ad_id, adreq=adreq, user=user, campaigns = campaigns)
    
@app.route('/adreqtoinf/<int:influencer_id>', methods=['GET', 'POST'])
def adreqtoinf(influencer_id):
    campaigns = []
    if request.method == 'POST':
        campaign_name = request.form['campaign']
        message = request.form['message1']
        campaign = Campaign.query.get(campaign_name)
        if campaign:
            new_adreq = Adreq(
                in_id=influencer_id,
                campaign_id=campaign.campaign_id,
                sp_id=session.get('user_id'),
                status='pending',
                message=message,
                campname=campaign.campaign_name
            )
            db.session.add(new_adreq)
            db.session.commit()
            return redirect(url_for('userforsp', sp_id=campaign.sp_id))
    campaigns = Campaign.query.filter_by(sp_id=session.get('user_id')).all()
    return render_template('adreqtoinf.html', campaigns=campaigns,influencer_id=influencer_id)
    
@app.route('/sponsor_page/delete/<int:campaign_id>', methods=['GET', 'POST'])
def delcamp(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if campaign is None:
        return abort(404, description="Campaign not found")
    user = spodata.query.filter_by(sp_id=campaign.sp_id).first()
    if user is None:
        return abort(404, description="User not found")    
    db.session.delete(campaign)
    db.session.commit()
    return redirect(url_for('userforsp', sp_id=user.sp_id))

@app.route('/sponsor_page/deletead/<int:ad_id>', methods=['GET', 'POST'])
def deladreq(ad_id):
    adreq = Adreq.query.get(ad_id)
    if adreq is None:
        return abort(404, description="Adreq not found")
    user = spodata.query.filter_by(sp_id=adreq.sp_id).first()
    db.session.delete(adreq)
    db.session.commit()
    return redirect(url_for('userforsp', sp_id=user.sp_id))
            
@app.route('/create_campaign_id_<int:sp_id>', methods=['GET', 'POST'])
def creacamp(sp_id):
    if request.method == 'POST':
        campaign_name = request.form['campaignName']
        description = request.form['description']
        start_date = request.form['startDate']
        end_date = request.form['endDate']
        payment_amount = request.form['paymentAmount']
        goals = request.form.get('goals')
        item = request.form['item']
#        visibility = request.form['visibility']
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        new = Campaign(sp_id=session['user_id'],campaign_name=campaign_name,description=description,start_date=start_date,end_date=end_date,payment_amount=payment_amount,goals=goals,item=item)
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('userforsp',sp_id=sp_id))
    user1= spodata.query.get(sp_id)
    return render_template('createcampaign.html',user=user1)

@app.route('/campaigns')
def list_campaigns():
    return redirect(url_for('userforsp'))

@app.route('/searchinf.html',methods=['GET', 'POST'])
def search_influencers():
    
    query = request.args.get('query')
    min_reach = request.args.get('min_reach')
    
    filters = []
    if query:
        filters.append(infdata.in_un.ilike(f'%{query}%'))
    if min_reach:
        filters.append(infdata.in_reach >= int(min_reach))
    
    influencers = infdata.query.filter(*filters).all()
    
    
    return render_template('searchinf.html', influencers=influencers)

 # Adjust according to your actual import


@app.route('/view_details/<int:campaign_id>', methods=['GET'])
def view_details(campaign_id):
    campaign = Campaign.query.filter_by(campaign_id=campaign_id).first()
    return render_template("view_details.html",campaign=campaign)


         

#######end of sponsor ################


#=============================================================================================================================================================================================================


@app.route('/influencerlogin.html', methods=['GET', 'POST'])
def inlogin():
    if request.method == 'POST':
        un = request.form['in_un']
        password = request.form['in_password']
        user = infdata.query.filter_by(in_un=un).first()
        if user:
            if user.in_password==password:
                session['inf_id'] = user.in_id 
                return redirect(f'/influencer_page_id_{user.in_id}')
            else:
                return "enter the password correctly"
        else:
            return "user doesn't exist"
    return render_template('influencerlogin.html')

@app.route('/influencerregister.html', methods=['GET', 'POST'])
def infreg():
    if request.method == 'POST':
        un = request.form['in_un']
        password = request.form['in_password']
        role = request.form['in_role']
        platform = request.form['in_platform']
        reach = request.form['in_reach']
        main_data = infdata(in_un=un,in_password=password,in_role=role,in_platform=platform,in_reach=reach)
        db.session.add(main_data)
        db.session.commit()
        return redirect(url_for('inlogin'))
    return render_template('influencerregister.html')


@app.route('/influencer_page_id_<int:in_id>', methods=['GET', 'POST'])
def userforin(in_id):
    user = infdata.query.get(in_id)
    if 'inf_id' not in session or session['inf_id'] != in_id:
        return redirect(url_for('splogin'))
    user = infdata.query.get(in_id)
    ads=Adreq.query.filter_by(in_id=user.in_id).all() or []
    if user.in_flag == "True":
        return " You have been flagged by an admin."
    return render_template('influencer_page.html',ads=ads)


@app.route('/influencer_dashboard/logout')
def inlogout():
    session.pop('inf_id')
    return render_template("influencerlogin.html")

@app.route('/searchcamp.html')
def searchcamp():
    query1 = request.args.get('query14')
    min_reach1 = request.args.get('item14')
    filters = []
    if query1:
        filters.append(Campaign.campaign_name.ilike(f'%{query1}%'))
    if min_reach1:
        filters.append(Campaign.item.ilike(f'%{min_reach1}%'))
    pubcamps=Campaign.query.filter(*filters).all()
    return render_template('searchcamp.html',pubcamps=pubcamps)
    
@app.route('/searchcampbyadm.html')
def scba():
    query1 = request.args.get('query13')
    min_reach1 = request.args.get('item13')
    visibility1 = request.args.get('visibility13')
    
    filters = []
    if query1:
        filters.append(Campaign.campaign_name.ilike(f'%{query1}%'))
    if min_reach1:
        filters.append(Campaign.item.ilike(f'{min_reach1}'))
    if visibility1:
        filters.append(Campaign.visibility.ilike(f'{visibility1}'))
    
    campaigns = Campaign.query.filter(*filters).all()
    return render_template('searchcampbyadm.html',campaigns=campaigns)
#=================================================================================================================================================================================================================================================================================================================================================================================================================


@app.route('/accept_campaign/<int:campaign_id>')
def accept_campaign(campaign_id):
    campaign = Adreq.query.get(campaign_id)
    campaign.status = 'accepted'
    db.session.commit()
    return redirect(f'/influencer_page_id_{campaign.in_id}')

@app.route('/reject_campaign/<int:campaign_id>')
def reject_campaign(campaign_id):
    campaign = Adreq.query.get(campaign_id)
    campaign.status = 'rejected'
    db.session.commit()
    return redirect(f'/influencer_page_id_{campaign.in_id}')




#=================================================================================================================================================
def create_pie_chart(ic,sc,tc):
    import matplotlib.pyplot as plt
    labels = 'Influencers', 'Sponsors', 'Total Users'
    sizes = [ic, sc, tc]
    colors = ['#ff6384', '#36a2eb', '#4bc0c0']
    explode = (0.1, 0, 0)  # explode 1st slice (Influencers)
    if sum([ic, sc, tc]) == 0:
        raise ValueError("No influencer, sponsor, user found.")

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.title('Distribution of Influencers, Sponsors, and Total Users')

    # Save the figure to a file
    plt.savefig('static/images/pie_chart.png') 
    plt.close()
    
def create_pie_chart_dup(cc,ac,tc):
    import matplotlib.pyplot as plt
    labels = 'Campaigns', 'Adrequests', 'Total Users'
    sizes = [cc, ac, tc]
    colors = ['#ff6384', '#36a2eb', '#4bc0c0']
    explode = (0.1, 0, 0)  # explode 1st slice (Influencers)
    if sum([cc, ac, tc]) == 0:
        raise ValueError("No campaign or adrequest or users found.")

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.title('Distribution of Campaigns, Adrequests, and Total users')

    # Save the figure to a file
    plt.savefig('static/images/pie_chart1.png') 
    plt.close()

@app.route('/admin_page.html')
def admin_page():
    ic=infdata.query.count()
    sc=spodata.query.count()
    tc=ic + sc
    cc=Campaign.query.count()
    ac=Adreq.query.count()
    create_pie_chart(ic,sc,tc)
    create_pie_chart_dup(cc,ac,tc)
    return render_template('admin_page.html',ic=ic,sc=sc,tc=tc,ac=ac,cc=cc)


@app.route('/adminlogin.html', methods=['POST','GET'])
def admin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if credentials['email'] == email:
            if credentials['password'] == password:
                return redirect(url_for('admin_page'))
            else:
                    return "enter the password correctly"
        else:
            return "user doesn't exist"
    return render_template('adminlogin.html')

@app.route('/searchinfbyadm.html', methods=['POST','GET'])
def siba():
    query1 = request.args.get('query1')
    min_reach1 = request.args.get('min_reach1')
    
    filters = []
    if query1:
        filters.append(infdata.in_un.ilike(f'%{query1}%'))
    if min_reach1:
        filters.append(infdata.in_reach >= int(min_reach1))
    
    influencers = infdata.query.filter(*filters).all()
    return render_template('searchinfbyadm.html',influencers=influencers)

@app.route('/admin_page/delete/<int:in_id>', methods=['GET', 'POST'])
def delinf(in_id):
    inf = infdata.query.get(in_id)
    if inf is None:
        return abort(404, description="Influencer not found")  
    db.session.delete(inf)
    db.session.commit()
    return redirect(url_for('siba'))

@app.route('/admin_page/flag/<int:in_id>', methods=['GET', 'POST'])
def flaginf(in_id):
    inf=infdata.query.get(in_id)
    if inf:
        inf.in_flag= "True"
        db.session.commit()
    return redirect(url_for('siba'))

@app.route('/searchspobyadm.html', methods=['POST','GET'])
def ssba():
    query1 = request.args.get('query12')
    min_reach1 = request.args.get('min_reach12')
    
    filters = []
    if query1:
        filters.append(spodata.sp_un.ilike(f'%{query1}%'))
    if min_reach1:
        filters.append(spodata.sp_role.ilike(f'{min_reach1}'))
    
    influencers = spodata.query.filter(*filters).all()
    return render_template('searchspobyadm.html',influencers=influencers)

@app.route('/admin_page/deletesp/<int:sp_id>', methods=['GET', 'POST'])
def delspo(sp_id):
    spo = spodata.query.get(sp_id)
    if spo is None:
        return abort(404, description="Sponsor not found")  
    db.session.delete(spo)
    db.session.commit()
    return redirect(url_for('ssba'))

@app.route('/admin_page/flagsp/<int:sp_id>', methods=['GET', 'POST'])
def flagspo(sp_id):
    spo=spodata.query.get(sp_id)
    if spo:
        spo.sp_flag= "True"
        db.session.commit()
    return redirect(url_for('ssba'))