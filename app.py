from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import itertools

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fifa_tournament.db'
app.config['SECRET_KEY'] = 'clean_edition_v3'
db = SQLAlchemy(app)

# --- REAL LEAGUES DATABASE (Simplified) ---
LEAGUE_DATA = {
    "premier_league": {
        "name": "Premier League",
        "teams": [
            {"name": "Arsenal", "logo": "https://resources.premierleague.com/premierleague/badges/t3.svg"},
            {"name": "Aston Villa", "logo": "https://resources.premierleague.com/premierleague/badges/t7.svg"},
            {"name": "Chelsea", "logo": "https://resources.premierleague.com/premierleague/badges/t8.svg"},
            {"name": "Liverpool", "logo": "https://resources.premierleague.com/premierleague/badges/t14.svg"},
            {"name": "Man City", "logo": "https://resources.premierleague.com/premierleague/badges/t43.svg"},
            {"name": "Man Utd", "logo": "https://resources.premierleague.com/premierleague/badges/t1.svg"},
            {"name": "Newcastle", "logo": "https://resources.premierleague.com/premierleague/badges/t4.svg"},
            {"name": "Spurs", "logo": "https://resources.premierleague.com/premierleague/badges/t6.svg"},
            {"name": "West Ham", "logo": "https://resources.premierleague.com/premierleague/badges/t21.svg"},
            {"name": "Wolves", "logo": "https://resources.premierleague.com/premierleague/badges/t39.svg"}
        ]
    },
    "laliga": {
        "name": "La Liga",
        "teams": [
            {"name": "Real Madrid", "logo": "https://assets.laliga.com/assets/2019/06/07/small/real-madrid.png"},
            {"name": "Barcelona", "logo": "https://assets.laliga.com/assets/2019/06/07/small/barcelona.png"},
            {"name": "Atletico", "logo": "https://assets.laliga.com/assets/2019/06/07/small/atletico-de-madrid.png"},
            {"name": "Sevilla", "logo": "https://assets.laliga.com/assets/2019/06/07/small/sevilla.png"},
            {"name": "Real Betis", "logo": "https://assets.laliga.com/assets/2022/09/15/small/real-betis.png"}
        ]
    },
    "bundesliga": {
        "name": "Bundesliga",
        "teams": [
            {"name": "Bayern", "logo": "https://upload.wikimedia.org/wikipedia/commons/1/1b/FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg"},
            {"name": "Dortmund", "logo": "https://upload.wikimedia.org/wikipedia/commons/6/67/Borussia_Dortmund_logo.svg"},
            {"name": "Leverkusen", "logo": "https://upload.wikimedia.org/wikipedia/en/5/59/Bayer_04_Leverkusen_logo.svg"}
        ]
    }
}

# --- DB MODELS ---
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    team = db.Column(db.String(50))
    logo = db.Column(db.String(500)) 
    played = db.Column(db.Integer, default=0)
    wins = db.Column(db.Integer, default=0)
    draws = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    points = db.Column(db.Integer, default=0)
    gf = db.Column(db.Integer, default=0)
    ga = db.Column(db.Integer, default=0)
    gd = db.Column(db.Integer, default=0)
    clean_sheets = db.Column(db.Integer, default=0)
    form = []

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home_name = db.Column(db.String(50))
    away_name = db.Column(db.String(50))
    home_score = db.Column(db.Integer, nullable=True)
    away_score = db.Column(db.Integer, nullable=True)
    is_played = db.Column(db.Boolean, default=False)
    scheduled_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='Pending') 
    notes = db.Column(db.String(200), nullable=True)

# --- ROUTES ---
@app.route('/')
def index():
    try:
        players = Player.query.order_by(Player.points.desc(), Player.gd.desc(), Player.gf.desc()).all()
    except:
        return redirect(url_for('hard_reset'))

    scheduled = Match.query.filter_by(is_played=False, status='Scheduled').order_by(Match.scheduled_time.desc()).all()
    pending = Match.query.filter_by(is_played=False, status='Pending').all()
    completed = Match.query.filter_by(is_played=True).order_by(Match.id.desc()).all()

    for p in players: p.form = get_form(p.name)
    
    top_scorer = Player.query.order_by(Player.gf.desc()).first()
    champion = players[0] if len(pending) == 0 and len(scheduled) == 0 and len(completed) > 0 else None
    
    return render_template('index.html', leagues=LEAGUE_DATA, players=players, 
                           scheduled=enrich_matches(scheduled, players), pending=enrich_matches(pending, players), completed=enrich_matches(completed, players),
                           top_scorer=top_scorer, champion=champion, season_over=(champion is not None))

# --- SETUP & MANAGE ---
@app.route('/setup', methods=['POST'])
def setup():
    db.session.query(Player).delete(); db.session.query(Match).delete()
    names = request.form.getlist('player_name[]'); teams = request.form.getlist('player_team_name[]'); logos = request.form.getlist('player_team_logo[]')
    
    created = []
    for n, t, l in zip(names, teams, logos):
        if n.strip():
            p = Player(name=n, team=t, logo=l)
            db.session.add(p); created.append(p)
    db.session.commit()

    for p1, p2 in itertools.combinations(created, 2):
        db.session.add(Match(home_name=p1.name, away_name=p2.name, status='Pending'))
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_player_midseason', methods=['POST'])
def add_player_midseason():
    name = request.form.get('name'); team = request.form.get('team_name'); logo = request.form.get('team_logo')
    if name and team:
        new_p = Player(name=name, team=team, logo=logo)
        db.session.add(new_p); db.session.commit()
        for p in Player.query.filter(Player.id != new_p.id).all():
            db.session.add(Match(home_name=new_p.name, away_name=p.name, status='Pending'))
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/remove_player_midseason/<int:player_id>', methods=['POST'])
def remove_player_midseason(player_id):
    p = Player.query.get(player_id)
    if p:
        Match.query.filter(((Match.home_name==p.name)|(Match.away_name==p.name)) & (Match.is_played==False)).delete()
        db.session.delete(p); db.session.commit()
    return redirect(url_for('index'))

@app.route('/hard_reset')
def hard_reset():
    db.drop_all(); db.create_all()
    return redirect(url_for('index'))

# --- HELPERS ---
def get_form(player_name):
    matches = Match.query.filter((Match.is_played==True) & ((Match.home_name==player_name) | (Match.away_name==player_name))).order_by(Match.id.desc()).limit(5).all()
    form = []
    for m in reversed(matches):
        is_home = m.home_name == player_name
        my = m.home_score if is_home else m.away_score
        opp = m.away_score if is_home else m.home_score
        if my > opp: form.append('W')
        elif my < opp: form.append('L')
        else: form.append('D')
    return form

def enrich_matches(matches, players):
    pmap = {p.name: p for p in players}
    res = []
    for m in matches:
        hp = pmap.get(m.home_name); ap = pmap.get(m.away_name)
        ht = hp.team if hp else m.home_name; at = ap.team if ap else m.away_name
        hl = hp.logo if hp else ''; al = ap.logo if ap else ''
        res.append({'id': m.id, 'home_player': m.home_name, 'away_player': m.away_name, 'home_team': ht, 'away_team': at, 'home_logo': hl, 'away_logo': al, 'home_score': m.home_score, 'away_score': m.away_score, 'notes': m.notes, 'is_played': m.is_played})
    return res

# --- MATCH LOGIC ---
@app.route('/record/<int:match_id>', methods=['POST'])
def record_match(match_id):
    m = Match.query.get(match_id)
    try: h = int(request.form.get('h_score', 0)); a = int(request.form.get('a_score', 0))
    except: h=0; a=0
    m.home_score = h; m.away_score = a; m.notes = request.form.get('notes'); m.is_played = True; m.status = 'Completed'
    
    h_p = Player.query.filter_by(name=m.home_name).first(); a_p = Player.query.filter_by(name=m.away_name).first()
    if h_p and a_p:
        h_p.played += 1; a_p.played += 1; h_p.gf += h; h_p.ga += a; a_p.gf += a; a_p.ga += h; h_p.gd = h_p.gf - h_p.ga; a_p.gd = a_p.gf - a_p.ga
        if h > a: h_p.wins += 1; h_p.points += 3; a_p.losses += 1
        elif a > h: a_p.wins += 1; a_p.points += 3; h_p.losses += 1
        else: h_p.draws += 1; a_p.draws += 1; h_p.points += 1; a_p.points += 1
        if a == 0: h_p.clean_sheets += 1
        if h == 0: a_p.clean_sheets += 1
    db.session.commit(); return redirect(url_for('index'))

@app.route('/schedule/<int:match_id>', methods=['POST'])
def schedule_match(match_id):
    m = Match.query.get(match_id); m.status = 'Scheduled'; m.scheduled_time = datetime.now(); db.session.commit(); return redirect(url_for('index'))

@app.route('/create_match', methods=['POST'])
def create_match():
    h = request.form.get('home_name'); a = request.form.get('away_name')
    if h and a and h!=a: db.session.add(Match(home_name=h, away_name=a, status='Scheduled', scheduled_time=datetime.now())); db.session.commit()
    return redirect(url_for('index'))
    
@app.route('/delete_match/<int:match_id>', methods=['POST'])
def delete_match(match_id):
    m = Match.query.get(match_id)
    if m:
        if m.is_played:
            h = Player.query.filter_by(name=m.home_name).first(); a = Player.query.filter_by(name=m.away_name).first()
            if h and a:
                h.played -= 1; a.played -= 1; h.gf -= m.home_score; h.ga -= m.away_score; a.gf -= m.away_score; a.ga -= m.home_score; h.gd -= (m.home_score-m.away_score); a.gd -= (m.away_score-m.home_score)
                if m.home_score > m.away_score: h.wins -= 1; h.points -= 3; a.losses -= 1
                elif m.away_score > m.home_score: a.wins -= 1; a.points -= 3; h.losses -= 1
                else: h.draws -= 1; a.draws -= 1; h.points -= 1; a.points -= 1
                if m.away_score == 0: h.clean_sheets -= 1
                if m.home_score == 0: a.clean_sheets -= 1
        db.session.delete(m); db.session.commit()
    return redirect(url_for('index'))

@app.route('/player_details/<int:id>')
def player_details(id):
    p = Player.query.get(id)
    matches = Match.query.filter(((Match.home_name == p.name) | (Match.away_name == p.name))).order_by(Match.is_played.desc(), Match.id.desc()).all()
    enrich = []
    for m in matches:
        score = f"{m.home_score}-{m.away_score}" if m.is_played else "VS"
        is_home = m.home_name == p.name
        opp_name = m.away_name if is_home else m.home_name
        opp = Player.query.filter_by(name=opp_name).first()
        color = "text-gray-500"
        if m.is_played:
            my = m.home_score if is_home else m.away_score; op = m.away_score if is_home else m.home_score
            color = "text-green-500" if my > op else ("text-red-500" if my < op else "text-gray-400")
        enrich.append({'opponent_team': opp.team if opp else opp_name, 'score': score, 'color': color})
    return jsonify({'id': p.id, 'name': p.name, 'team': p.team, 'logo': p.logo, 'matches': enrich, 'stats': {'played': p.played, 'wins': p.wins, 'goals': p.gf, 'clean_sheets': p.clean_sheets}})

@app.route('/update_player/<int:player_id>', methods=['POST'])
def update_player(player_id):
    p = Player.query.get(player_id); p.name = request.form.get('name'); p.team = request.form.get('team'); p.logo = request.form.get('logo'); db.session.commit(); return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context(): db.create_all()
    app.run(debug=True)