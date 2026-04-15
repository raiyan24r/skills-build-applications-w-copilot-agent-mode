from django.test import TestCase
from .models import User, Team, Activity, Leaderboard, Workout

class BasicModelTest(TestCase):
    def test_team_creation(self):
        team = Team.objects.create(name='Test Team', members=['A', 'B'])
        self.assertEqual(team.name, 'Test Team')
    def test_user_creation(self):
        team = Team.objects.create(name='Test Team', members=['A', 'B'])
        user = User.objects.create(name='Test User', email='test@example.com', team=team)
        self.assertEqual(user.email, 'test@example.com')
