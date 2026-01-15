from flask import request, jsonify
from config import app, db
from models import Episode, Guest, Appearance

# GET /episodes : Returns a simple list of all episodes
@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    # We use .to_dict(only=...) to limit the fields returned to just id, date, and number.
    return jsonify([episode.to_dict(only=('id', 'date', 'number')) for episode in episodes]), 200

# GET /episodes/:id : Returns detailed information about a single episode
@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode_by_id(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    
    # By default, to_dict() will include nested appearances because of serialize_rules in models.py
    return jsonify(episode.to_dict()), 200

# DELETE /episodes/:id
@app.route('/episodes/<int:id>', methods=['DELETE'])
def delete_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    
    db.session.delete(episode)
    db.session.commit()
    
    return jsonify({"message": "Episode deleted successfully"}), 200

# GET /guests
@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    # Format: [{"id": 1, "name": "Michael J. Fox", "occupation": "actor"}, ...]
    return jsonify([guest.to_dict(only=('id', 'name', 'occupation')) for guest in guests]), 200

# POST /appearances : Creates a new entry linking a guest to an episode
@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()
    
    try:
        # Create the new instance. Validations in models.py will trigger here.
        appearance = Appearance(
            rating=data.get('rating'),
            episode_id=data.get('episode_id'),
            guest_id=data.get('guest_id')
        )
        
        db.session.add(appearance)
        db.session.commit()
        # Returns the newly created appearance with its nested episode and guest data.
        return jsonify(appearance.to_dict()), 201

    except (ValueError, IntegrityError) as e:
        # Catching ValueError (from our @validates) or IntegrityError (db constraints)
        return jsonify({"errors": ["validation errors"]}), 400
    except Exception as e:
        # Catch-all for any other unexpected errors
        return jsonify({"errors": [str(e)]}), 400

from sqlalchemy.exc import IntegrityError