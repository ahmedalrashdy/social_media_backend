from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        abstract = True













    


# # --- Reporting and Reviews ---
# class Report(TimeStampedModel):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     reporter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='submitted_reports', on_delete=models.SET_NULL, null=True)
#     reason = models.TextField()

    
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, help_text="The type of content being reported")
#     object_id = models.UUIDField(help_text="The ID of the content being reported") # Ensure parent IDs are UUIDs
#     reported_object = GenericForeignKey('content_type', 'object_id')

#     def __str__(self):
#         return f"Report by {self.reporter.username} on {self.content_type.model} ({self.object_id})"

# class Review(TimeStampedModel):
#     class Status(models.TextChoices):
#         PENDING = 'PEND', 'Pending'
#         APPROVED = 'APPR', 'Approved'
#         REJECTED = 'REJ', 'Rejected'
#         ACTION_TAKEN = 'ACT', 'Action Taken'

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews_conducted', on_delete=models.SET_NULL, null=True, blank=True)
#     report = models.ForeignKey(Report, related_name='reviews', on_delete=models.CASCADE) # Changed to ForeignKey assuming one review per report based on ERD N-1 line
#     comments = models.TextField(null=True, blank=True)
#     status = models.CharField(max_length=4, choices=Status.choices, default=Status.PENDING)
#     # reviewed_at handled by updated_at from TimeStampedModel

#     def __str__(self):
#         return f"Review for Report {self.report.id} ({self.get_status_display()})"

