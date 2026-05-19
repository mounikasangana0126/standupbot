from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class StandupEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries')
    did = models.TextField(help_text="What did you do yesterday?")
    doing = models.TextField(help_text="What are you doing today?")
    blockers = models.TextField(blank=True, help_text="Any blockers? (optional)")
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['date', 'user'])]

    def __str__(self):
        return f"{self.user.username} – {self.date}"

    @property
    def has_blockers(self):
        return bool(self.blockers.strip())

    @classmethod
    def todays_entries(cls):
        return cls.objects.filter(date=timezone.now().date()).select_related('user')

    @classmethod
    def user_posted_today(cls, user):
        return cls.objects.filter(user=user, date=timezone.now().date()).exists()
