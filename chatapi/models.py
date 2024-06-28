from django.db import models
from authuser.models import Profile , User
from django.db.models.signals import post_save
from django.utils import timezone
from django.dispatch import receiver

# Create your models here.
class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="received_messages")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ['timestamp']
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"{self.sender} - {self.receiver}"

    @property
    def sender_profile(self):
        try:
            return Profile.objects.get(user=self.sender)
        except Profile.DoesNotExist:
            return None

    @property
    def receiver_profile(self):
        try:
            return Profile.objects.get(user=self.receiver)
        except Profile.DoesNotExist:
            return None

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()