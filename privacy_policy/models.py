from django.db import models

class BaseContent(models.Model):
    description = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.description[:50]  # Return first 50 characters of description

class PrivacyPolicy(BaseContent):
    pass

class TrustSafety(BaseContent):
    pass

class TermsConditions(BaseContent):
    pass