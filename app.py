#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

# General Imports
# import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment

# SQLAlchemy Imports
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import lazyload
from flask_migrate import Migrate
from sqlalchemy import and_, or_, func

# Loggin Imports
import logging
from logging import Formatter, FileHandler

# Form Imports
from flask_wtf import Form
from forms import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

# Flask Config
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

# Database Config
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
  __tablename__ = 'Venue'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  genres = db.Column(db.String)
  address = db.Column(db.String(120))
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  website_link = db.Column(db.String(120))
  facebook_link = db.Column(db.String(120))
  seeking_talent = db.Column(db.Boolean, nullable=False)
  seeking_description = db.Column(db.String, nullable=True)
  image_link = db.Column(db.String(500))
  shows = db.relationship('Show', backref='venue', lazy=True)
  #shows = db.relationship('Show', backref='venue', lazy="joined")

  def __repr__(self):
    return f'<Venue {self.name}, {self.city}, {self.state}, {self.address}>'

class Artist(db.Model):
  __tablename__ = 'Artist'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  genres = db.Column(db.String(120))
  address = db.Column(db.String(120))
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  website_link = db.Column(db.String(120))
  facebook_link = db.Column(db.String(120))
  seeking_venue = db.Column(db.Boolean, nullable=False)
  seeking_description = db.Column(db.String, nullable=True)
  image_link = db.Column(db.String(500))
  shows = db.relationship('Show', backref='artist', lazy=True)

  def __repr__(self):
    return f'<Artist {self.name}, {self.genres}, {self.city}, {self.state}>'

class Show(db.Model):
  __tablename__ = 'Show'
  
  id = db.Column(db.Integer, primary_key=True)
  id_artist = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  id_venue = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)

  def __repr__(self):
    return f'<Show {self.start_time}, {self.artist.name}, {self.venue.name}>'

#----------------------------------------------------------------------------#
# Seed Database.
#----------------------------------------------------------------------------#

def seed_artist():
  if (len(Artist.query.all()) == 0):
    artist1 = Artist(
       name="Guns N Petals",
       #genres=json.dumps(["Rock n Roll"]),
       genres="Rock n Roll",
       address="1015 Folsom Street",
       city="San Francisco",
       state="CA",
       phone="326-123-5000",
       website="https://www.gunsnpetalsband.com",
       facebook_link="https://www.facebook.com/GunsNPetals",
       seeking_venue=True,
       seeking_description="Looking for shows to perform at in the San Francisco Bay Area!",
       image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    )
    artist2 = Artist(
       name="Matt Quevedo",
       #genres=json.dumps(["Jazz"]),
       genres="Jazz",
       address="1015 Folsom Street",
       city="New York",
       state="NY",
       phone="300-400-5000",
       website="https://www.gunsnpetalsband.com",
       facebook_link="https://www.facebook.com/mattquevedo923251523",
       seeking_venue=False,
       image_link="https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    )
    artist3 = Artist(
       name="The Wild Sax Band",
       #genres=json.dumps(["Jazz", "Classical"]),
       genres="Jazz,Classical",
       address="1015 Folsom Street",
       city="San Francisco",
       state="CA",
       phone="432-325-5432",
       seeking_venue=False,
       image_link="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    )
    
    db.session.add(artist1)
    db.session.add(artist2)
    db.session.add(artist3)
    db.session.commit()

def seed_venue():
  if (len(Venue.query.all()) == 0):
    venue1 = Venue(
       name="The Musical Hop",
       #genres=json.dumps(["Jazz", "Reggae", "Swing", "Classical", "Folk"]),
       genres="Jazz,Reggae,Swing,Classical,Folk",
       address="1015 Folsom Street",
       city="San Francisco",
       state="CA",
       phone="123-123-1234",
       website_link="https://www.themusicalhop.com",
       facebook_link="https://www.facebook.com/TheMusicalHop",
       seeking_talent=True,
       seeking_description="We are on the lookout for a local artist to play every two weeks. Please call us.",
       image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    )
    venue2 = Venue(
       name="The Dueling Pianos Bar",
       #genres=json.dumps(["Classical", "R&B", "Hip-Hop"]),
       genres="Classical,R&B,Hip-Hop",
       address="335 Delancey Street",
       city="New York",
       state="NY",
       phone="914-003-1132",
       website_link="https://www.theduelingpianos.com",
       facebook_link="https://www.facebook.com/theduelingpianos",
       seeking_talent=False,
       image_link="https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    )
    venue3 = Venue(
       name="Park Square Live Music & Coffee",
       #genres=json.dumps(["Rock n Roll", "Jazz", "Classical", "Folk"]),
       genres="Rock n Roll,Jazz,Classical,Folk",
       address="34 Whiskey Moore Ave",
       city="San Francisco",
       state="CA",
       phone="415-000-1234",
       website_link="https://www.parksquarelivemusicandcoffee.com",
       facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
       seeking_talent=False,
       image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    )

    db.session.add(venue1)
    db.session.add(venue2)
    db.session.add(venue3)
    db.session.commit()

def seed_show():
  if (len(Show.query.all()) == 0):
    venue_musi = db.session.execute(db.select(Venue).filter_by(name="The Musical Hop")).scalar_one()
    venue_park = db.session.execute(db.select(Venue).filter_by(name="Park Square Live Music & Coffee")).scalar_one()
    
    artist_guns = db.session.execute(db.select(Artist).filter_by(name="Guns N Petals")).scalar_one()
    artist_matt = db.session.execute(db.select(Artist).filter_by(name="Matt Quevedo")).scalar_one()
    artist_wild = db.session.execute(db.select(Artist).filter_by(name="The Wild Sax Band")).scalar_one()
    
    show1 = Show(
       start_time = "2019-05-21T21:30:00.000Z",
       id_venue = venue_musi.id,
       id_artist = artist_guns.id
    )
    show2 = Show(
       start_time = "2019-06-15T23:00:00.000Z",
       id_venue = venue_park.id,
       id_artist = artist_matt.id
    )
    show3 = Show(
       start_time = "2035-04-01T20:00:00.000Z",
       id_venue = venue_park.id,
       id_artist = artist_wild.id
    )
    show4 = Show(
       start_time = "2035-04-08T20:00:00.000Z",
       id_venue = venue_park.id,
       id_artist = artist_wild.id
    )
    show5 = Show(
       start_time = "2035-04-15T20:00:00.000Z",
       id_venue = venue_park.id,
       id_artist = artist_wild.id
    )

    db.session.add(show1)
    db.session.add(show2)
    db.session.add(show3)
    db.session.add(show4)
    db.session.add(show5)
    db.session.commit()

def seed_database():
  seed_artist()
  seed_venue()
  seed_show()

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  seed_database()
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # get the values
  places = db.session.query(
    Venue.city,
    Venue.state
  ).distinct(
    Venue.city,
    Venue.state
  ).group_by(
    Venue.city,
    Venue.state
  ).order_by(
    Venue.city.desc()
  ).all()

  # format the results
  areas = []
  for place in places:
    results = Venue.query.filter_by(city = place.city).all()
    venues = []
    for result in results:
      venues.append({
        "id": result.id,
        "name": result.name,
        "num_upcoming_shows": len(result.shows)
      })
    areas.append({
      "city": place.city,
      "state": place.state,
      "venues": venues
    })

  # return the view
  return render_template('pages/venues.html', areas=areas)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # get the search term
  search_term = request.form.get('search_term', '')

  # search the venues that match the query
  venues = db.session.query(
      Venue.id,
      Venue.name,
      func.count(Show.id).label('num_upcoming_shows')
    ).group_by(
      Venue.id,
      Venue.name
    ).filter(
      Venue.name.ilike(f"%{search_term}%")
    ).all()
  
  # format the result
  response = {
    "count": len(venues),
    "data": [{
        "id": venue_id,
        "name": venue_name,
        "num_upcoming_shows": num_upcoming_shows
    } for venue_id, venue_name, num_upcoming_shows in venues]
  }

  # return the view
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id

  # get the venue
  venue = Venue.query.filter_by(id=venue_id).first()

  # get current datetime
  current_datetime = datetime.utcnow()

  # query the past shows
  past_shows = db.session.query(
      Artist.id.label("artist_id"),
      Artist.name.label("artist_name"),
      Artist.image_link.label("artist_image_link"),
      Show.start_time,
      Show.id_venue
    ).join(
      Artist
    ).filter(
      and_(
        Show.id_venue == venue_id,
        Show.start_time < current_datetime
      )
    ).all()
  
  # query the upcoming shows
  upcoming_shows = db.session.query(
      Artist.id.label("artist_id"),
      Artist.name.label("artist_name"),
      Artist.image_link.label("artist_image_link"),
      Show.start_time,
      Show.id_venue
    ).join(
      Artist
    ).filter(
      and_(
        Show.id_venue == venue_id,
        Show.start_time >= current_datetime
      )
    ).all()

  # format the result
  venue.genres = venue.genres.split(',')
  venue.past_shows = past_shows
  venue.past_shows_count = len(past_shows)
  venue.upcoming_shows = upcoming_shows
  venue.upcoming_shows_count = len(upcoming_shows)

  # return the view
  return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # validate the form
  form = VenueForm(request.form)
  
  if form.validate():
    try:
      # create a new artist
      new_venue = Venue(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        address=form.address.data,
        phone=form.phone.data,
        image_link=form.image_link.data,
        genres=','.join(form.genres.data),
        facebook_link=form.facebook_link.data,
        website_link=form.website_link.data,
        seeking_talent=form.seeking_talent.data,
        seeking_description=form.seeking_description.data
      )
      db.session.add(new_venue)
      db.session.commit()
      
      # success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
      # rollback transaction
      db.session.rollback()
      print(f'An error occurred: {str(e)}')
      flash('An error occurred. Venue ' + str(request.form['name']) + ' could not be listed.')
    finally:
      # close transaction
      db.session.close()
  else:
    # validation failed
    flash('Form was not valid.', 'danger')
    return render_template('forms/new_venue.html', form=form)
  
  # return to the home page
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    # get the venue by id
    venue = Venue.query.get(venue_id)

    # delete the venue from db
    db.session.delete(venue)
    db.session.commit()
    #flash('Success. The Venue was deleted.')
  except:
    # db error
    #flash('An error occurred. Venue was not deleted.')
    db.session.rollback()
  finally:
    db.session.close()
  
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists = Artist.query.all()
  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # search on artists with partial string search
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  # get the search term
  search_term = request.form.get('search_term', '')

  # search the artists that match the query
  artists = db.session.query(
      Artist.id,
      Artist.name,
      func.count(Show.id).label('num_upcoming_shows')
    ).group_by(
      Artist.id,
      Artist.name
    ).filter(
      Artist.name.ilike(f"%{search_term}%")
    ).all()
  
  # format the result
  response = {
    "count": len(artists),
    "data": [{
        "id": artist_id,
        "name": artist_name,
        "num_upcoming_shows": num_upcoming_shows
    } for artist_id, artist_name, num_upcoming_shows in artists]
  }

  # return the view
  return render_template('pages/search_artists.html', results = response, search_term = search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # get the artist
  artist = Artist.query.filter_by(id=artist_id).first()

  # get current datetime
  current_datetime = datetime.utcnow()

  # query the past shows
  past_shows = db.session.query(
      Venue.id.label("venue_id"),
      Venue.name.label("venue_name"),
      Venue.image_link.label("venue_image_link"),
      Show.start_time,
      Show.id_artist
    ).join(
      Venue
    ).filter(
      and_(
        Show.id_artist == artist_id,
        Show.start_time < current_datetime
      )
    ).all()
  
  # query the upcoming shows
  upcoming_shows = db.session.query(
      Venue.id.label("venue_id"),
      Venue.name.label("venue_name"),
      Venue.image_link.label("venue_image_link"),
      Show.start_time,
      Show.id_artist
    ).join(
      Venue
    ).filter(
      and_(
        Show.id_artist == artist_id,
        Show.start_time >= current_datetime
      )
    ).all()

  # format the result
  artist.genres = artist.genres.split(',')
  artist.past_shows = past_shows
  artist.past_shows_count = len(past_shows)
  artist.upcoming_shows = upcoming_shows
  artist.upcoming_shows_count = len(upcoming_shows)

  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # get the artist
  artist = Artist.query.filter_by(id=artist_id).first()

  # if the artist exists
  if artist is None:
    # return to the home with a message
    flash('Artist not found!')
    return render_template('pages/home.html')
  else:
    # populate form fields
    form = ArtistForm(
      name=artist.name,
      city=artist.city,
      state=artist.state,
      phone=artist.phone,
      image_link=artist.image_link,
      genres=artist.genres.split(','),
      facebook_link=artist.facebook_link,
      website_link=artist.website_link,
      seeking_venue=artist.seeking_venue,
      seeking_description=artist.seeking_description
    )

    # return the view
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # validate the form
  form = ArtistForm(request.form)

  if form.validate():
    # get the artist by id
    artist = Artist.query.get(artist_id)
    
    # update the artist
    artist.name = form.name.data
    artist.city = form.city.data
    artist.state = form.state.data
    artist.phone = form.phone.data
    artist.image_link = form.image_link.data
    artist.genres = ','.join(form.genres.data)
    artist.facebook_link = form.facebook_link.data
    artist.website_link = form.website_link.data
    artist.seeking_venue = form.seeking_venue.data
    artist.seeking_description = form.seeking_description.data
    db.session.commit()

    # Step 5: Redirect to a page showing the updated artist information
    flash('The artist informations were updated', 'success')
    return redirect(url_for('show_artist', artist_id = artist.id))
  else:
    # error in validation
    flash('Form was not valid.', 'danger')
    return render_template('edit_artist.html', artist_id = artist_id, form = form)

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # get the venue
  venue = Venue.query.filter_by(id=venue_id).first()

  # if the artist exists
  if venue is None:
    # return to the home with a message
    flash('Venue not found!')
    return render_template('pages/home.html')
  else:
    # populate form fields
    form = VenueForm(
      name=venue.name,
      genres=venue.genres.split(','),
      address=venue.address,
      city=venue.city,
      state=venue.state,
      phone=venue.phone,
      website_link=venue.website_link,
      facebook_link=venue.facebook_link,
      seeking_talent=venue.seeking_talent,
      seeking_description=venue.seeking_description,
      image_link=venue.image_link
    )

    # return the view
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # validate the form
  form = VenueForm(request.form)

  if form.validate():
    # get the venue by id
    venue = Venue.query.get(venue_id)
    
    # update the venue
    venue.name = form.name.data
    venue.genres = ','.join(form.genres.data)
    venue.address = form.address.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.phone = form.phone.data
    venue.website_link = form.website_link.data
    venue.facebook_link = form.facebook_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data
    venue.image_link = form.image_link.data
    db.session.commit()

    # Step 5: Redirect to a page showing the updated artist information
    flash('The venue informations were updated', 'success')
    return redirect(url_for('show_venue', venue_id = venue_id))
  else:
    # error in validation
    flash('Form was not valid.', 'danger')
    return render_template('edit_venue.html', venue_id = venue_id, form = form)


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # validate the form
  form = ArtistForm(request.form)
  
  if form.validate():
    try:
      # create a new artist
      new_artist = Artist(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        phone=form.phone.data,
        image_link=form.image_link.data,
        genres=','.join(form.genres.data),
        facebook_link=form.facebook_link.data,
        website_link=form.website_link.data,
        seeking_venue=form.seeking_venue.data,
        seeking_description=form.seeking_description.data
      )
      db.session.add(new_artist)
      db.session.commit()
      
      # success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
      # rollback transaction
      db.session.rollback()
      flash('An error occurred. Artist ' + str(request.form['name']) + ' could not be listed.')
    finally:
      # close transaction
      db.session.close()
  else:
    # validation failed
    flash('Form was not valid.', 'danger')
    return render_template('forms/new_artist.html', form=form)
  
  # return to the home page
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  query = db.select(
    Venue.id.label("venue_id"),
    Venue.name.label("venue_name"),
    Artist.id.label("artist_id"),
    Artist.name.label("artist_name"),
    Artist.image_link.label("artist_image_link"),
    Show.start_time
  ).join_from(
    Show,
    Venue
  ).join_from(
    Show,
    Artist,
  )
  shows = db.session.execute(query).all()
  
  return render_template('pages/shows.html', shows=shows)

@app.route('/shows/search', methods=['POST'])
def search_shows():
  # search a show with partial string search

  # get the search term
  search_term = request.form.get('search_term', '')

  # search the shows that match the query
  shows = db.session.query(
      Artist.id,
      Artist.name,
      Artist.image_link,
      Venue.id,
      Venue.name,
      Show.start_time
    ).join(
      Artist
    ).join(
      Venue
    ).filter(
      or_(
        Artist.name.ilike(f"%{search_term}%"),
        Venue.name.ilike(f"%{search_term}%")
      )
    ).all()
  
  # format the result
  response = {
    "count": len(shows),
    "data": [{
        "artist_id": artist_id,
        "artist_name": artist_name,
        "artist_image_link": artist_image_link,
        "venue_id": venue_id,
        "venue_name": venue_name,
        "start_time": start_time,
    } for artist_id, artist_name, artist_image_link, venue_id, venue_name, start_time in shows]
  }

  # return the view
  return render_template('pages/search_shows.html', results = response, search_term = search_term)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # validate the form
  form = ShowForm(request.form)
  
  if form.validate():
    try:
      # create a new show
      new_show = Show(
        artist_id=form.artist_id.data,
        venue_id=form.venue_id.data,
        start_time=form.start_time.data
      )
      db.session.add(new_show)
      db.session.commit()
      
      # success
      flash('Show was successfully listed!')
    except:
      # rollback transaction
      db.session.rollback()
      flash('An error occurred. Show could not be listed.')
    finally:
      # close transaction
      db.session.close()
  else:
    # validation failed
    flash('Form was not valid.', 'danger')
    return render_template('forms/new_show.html', form=form)
  
  # return to the home page
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()
