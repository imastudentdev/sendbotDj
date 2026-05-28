from django.db import models

class SiteConfig(models.Model):
    bot_token = models.CharField(max_length=300, verbose_name="Bot Token")
    chat_id = models.CharField(max_length=100, verbose_name="Chat ID")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Sayt Sozlamalari"
        verbose_name_plural = "Sayt Sozlamalari"

    def __str__(self):
        return "Asosiy Sozlamalar"

    @classmethod
    def get_config(cls):
        config = cls.objects.first()
        if not config:
            config = cls.objects.create(
                bot_token="YOUR_BOT_TOKEN_HERE",
                chat_id="YOUR_CHAT_ID_HERE"
            )
        return config