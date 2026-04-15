from django.core.management.base import BaseCommand
## No Django models needed for direct MongoDB access
from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB directly for index creation
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        # Ensure unique index on email
        db.users.create_index('email', unique=True)
        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})
        # Insert test data
        marvel = {'name': 'Team Marvel', 'members': ['Iron Man', 'Captain America', 'Thor']}
        dc = {'name': 'Team DC', 'members': ['Superman', 'Batman', 'Wonder Woman']}
        marvel_id = db.teams.insert_one(marvel).inserted_id
        dc_id = db.teams.insert_one(dc).inserted_id
        users = [
            {'name': 'Tony Stark', 'email': 'ironman@marvel.com', 'team': marvel_id},
            {'name': 'Steve Rogers', 'email': 'cap@marvel.com', 'team': marvel_id},
            {'name': 'Clark Kent', 'email': 'superman@dc.com', 'team': dc_id},
            {'name': 'Bruce Wayne', 'email': 'batman@dc.com', 'team': dc_id},
        ]
        db.users.insert_many(users)
        activities = [
            {'user': 'Tony Stark', 'activity': 'Bench Press', 'reps': 10},
            {'user': 'Steve Rogers', 'activity': 'Running', 'distance_km': 5},
            {'user': 'Clark Kent', 'activity': 'Flying', 'duration_min': 60},
            {'user': 'Bruce Wayne', 'activity': 'Martial Arts', 'duration_min': 45},
        ]
        db.activities.insert_many(activities)
        leaderboard = [
            {'user': 'Tony Stark', 'score': 100},
            {'user': 'Clark Kent', 'score': 95},
        ]
        db.leaderboard.insert_many(leaderboard)
        workouts = [
            {'name': 'Super Strength', 'suggested_for': 'Team Marvel'},
            {'name': 'Stealth Training', 'suggested_for': 'Team DC'},
        ]
        db.workouts.insert_many(workouts)
        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
