# Late Show Flask API - Implementation Plan

## Information Gathered

From the task instructions:

- Build a Flask API for a "Late Show" application
- Models: Episode, Guest, Appearance (with relationships)
- Relationships: Episode has many Guests through Appearance, Guest has many Episodes through Appearance
- Appearance belongs to Episode and Guest with cascade deletes
- Validations: Appearance rating must be between 1-5
- Routes needed: GET /episodes, GET /episodes/:id, GET /guests, POST /appearances
- Seed data from CSV file
- Create README with proper documentation

## Plan

### Phase 1: Project Setup

1. Create requirements.txt with Flask, Flask-SQLAlchemy, Flask-Migrate
2. Create config.py for Flask configuration
3. Create app.py as the main Flask application

### Phase 2: Database Models

4. Create models.py with:
   - Episode model (id, date, number)
   - Guest model (id, name, occupation)
   - Appearance model (id, rating, episode_id, guest_id)
   - Set up relationships with cascade deletes
   - Add rating validation (1-5)

### Phase 3: Routes

5. Create routes.py with:
   - GET /episodes - return list of episodes
   - GET /episodes/:id - return episode with appearances and nested guest info
   - GET /guests - return list of guests
   - POST /appearances - create new appearance with validation

### Phase 4: Seeding

6. Create seed.py to populate database from CSV
7. Create sample CSV file with guest and episode data

### Phase 5: Documentation

8. Create comprehensive README.md

## Dependent Files to be Created

- requirements.txt
- config.py
- app.py
- models.py
- routes.py
- seed.py
- guests.csv (sample data)
- README.md

## Followup Steps (ALL COMPLETED)

1. ✅ Created requirements.txt
2. ✅ Created config.py for Flask configuration
3. ✅ Created app.py as main application
4. ✅ Created models.py with Episode, Guest, Appearance models
5. ✅ Created routes.py with all required endpoints
6. ✅ Created seed.py for database seeding
7. ✅ Created sample CSV files (episodes.csv, guests.csv)
8. ✅ Created comprehensive README.md
9. ✅ Installed dependencies
10. ✅ Created database tables
11. ✅ Seeded database
12. ✅ Tested all API endpoints (all passing)

## Test Results

- GET /episodes: ✅ 200 OK
- GET /episodes/:id: ✅ 200 OK (with appearances and nested guests)
- GET /episodes/:id (not found): ✅ 404 with error message
- GET /guests: ✅ 200 OK
- POST /appearances: ✅ 201 Created
- POST /appearances (invalid rating): ✅ 400 with validation errors