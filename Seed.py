import csv
import os
from config import db, app
from models import Episode, Guest, Appearance

# The seed script creates initial data for testing the application
def seed_database():
    with app.app_context():
        print("Clearing existing data...")
        # We delete in order to avoid foreign key constraint issues
        Appearance.query.delete()
        Episode.query.delete()
        Guest.query.delete()
        
        # Seed Episodes: We check if a CSV exists, otherwise we use hardcoded dummy data
        episodes = []
        if os.path.exists('episodes.csv'):
            print("Reading episodes from CSV...")
            with open('episodes.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    episode = Episode(date=row['date'], number=int(row['number']))
                    episodes.append(episode)
                    db.session.add(episode)
        else:
            print("CSV file episodes.csv not found. Using fallback data...")
            fallback_episodes = [
                {'date': '1/11/99', 'number': 1},
                {'date': '1/12/99', 'number': 2},
                {'date': '1/13/99', 'number': 3},
                {'date': '1/14/99', 'number': 4},
                {'date': '1/15/99', 'number': 5},
            ]
            for data in fallback_episodes:
                episode = Episode(**data)
                episodes.append(episode)
                db.session.add(episode)
        
        db.session.commit()
        
        # Seed Guests
        guests = []
        if os.path.exists('guests.csv'):
            print("Reading guests from CSV...")
            with open('guests.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    guest = Guest(name=row['name'], occupation=row['occupation'])
                    guests.append(guest)
                    db.session.add(guest)
        else:
            print("CSV file guests.csv not found. Using fallback data...")
            fallback_guests = [
                {'name': 'Michael J. Fox', 'occupation': 'actor'},
                {'name': 'Sandra Bernhard', 'occupation': 'Comedian'},
                {'name': 'Tracey Ullman', 'occupation': 'television actress'},
                {'name': 'Gillian Anderson', 'occupation': 'film actress'},
                {'name': 'David Duchovny', 'occupation': 'television actor'},
            ]
            for data in fallback_guests:
                guest = Guest(**data)
                guests.append(guest)
                db.session.add(guest)
        
        db.session.commit()
        
        # Create some sample appearances
        print("Creating sample appearances...")
        appearances_data = [
            {'rating': 4, 'episode_id': episodes[0].id, 'guest_id': guests[0].id},
            {'rating': 5, 'episode_id': episodes[0].id, 'guest_id': guests[1].id},
            {'rating': 3, 'episode_id': episodes[1].id, 'guest_id': guests[1].id},
            {'rating': 4, 'episode_id': episodes[1].id, 'guest_id': guests[2].id},
            {'rating': 5, 'episode_id': episodes[2].id, 'guest_id': guests[0].id},
            {'rating': 4, 'episode_id': episodes[2].id, 'guest_id': guests[2].id},
        ]
        
        for data in appearances_data:
            appearance = Appearance(**data)
            db.session.add(appearance)
        
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()