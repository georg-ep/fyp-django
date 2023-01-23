from django.db import models

class SocialPlatforms(models.TextChoices):
    instagram = "instagram", "Instagram"
    twitter = "twitter", "Twitter"
    facebook = "facebook", "Facebook"
    youtube = "youtube", "YouTube"
    whatsapp = "whatsapp", "WhatsApp"
    tiktok = "tiktok", "TikTok"
    snapchat = "snapchat", "Snapchat"
    reddit = "reddit", "Reddit"
    telegram = "telegram", "Telegram"

class FeelingTypes(models.TextChoices):
    anxiety = "anxiety"
    depression = "depression"
    elavated = "elavation"
    irritability = "irritability"