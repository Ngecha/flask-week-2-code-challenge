from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

# Importing the models and database setup from models.py
from models import db, Episode, Guest, Appearance

# Initialize Flask app
app = Flask(__name__)

# Configure the database URI and settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///late_show.db'
app.config['SQLALCHEMY_TRACK_MODIFICACTION'] = False 
app.json.compact = False 

# Set up database migrations and initialize the database
migrate = Migrate(app, db)
db.init_app(app)

# Initialize Flask-RESTful API
api = Api(app)


class Episodes(Resource):
    def get(self):
        episodes = [episode.to_dict(rules=('-appearance',)) for episode in Episode.query.all()]
        
        response = make_response(episodes, 200)
        return response

api.add_resource(Episodes, '/episodes')


class Episode_with_id(Resource):
    def get(self, id):
        # Retrieve the episode by ID (returns first match, or None if not found)
        episode = Episode.query.filter(Episode.id == id).first()
        
        if episode:
            # If episode exists, serialize it to a dictionary and send in the response
            episode_dict = episode.to_dict()
            body = episode_dict
            status = 200
        else:
            # If episode not found, return an error message with 404 status
            body = {"error": "Episode not found"}
            status = 404
            
        return make_response(body, status)

api.add_resource(Episode_with_id, '/episodes/<int:id>')

class Guests(Resource):
    def get(self):
        guests = [guest.to_dict(rules=('-appearance',)) for guest in Guest.query.all()]
        
        response = make_response(guests, 200)
        return response

api.add_resource(Guests, '/guests')

class Appearances(Resource):
    def post(self):
        try:
            # Create a new Appearance instance
            appearance = Appearance(
                rating=request.json.get('rating'),
                episode_id=request.json.get('episode_id'),
                guest_id=request.json.get('guest_id'),
            )
        
            # Add the new appearance to the database and commit the changes
            db.session.add(appearance)
            db.session.commit()
        
            appearance_dict = appearance.to_dict()
            response = make_response(appearance_dict, 201)
        
            return response
    
        except ValueError:
            # Handle validation errors
            body = {"errors": ["validation errors"]} 
            status = 400
            return make_response(body, status)

api.add_resource(Appearances, '/appearance')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
