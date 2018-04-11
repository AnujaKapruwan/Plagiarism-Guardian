import os

from django.db import models
from django.core.exceptions import ValidationError

class ProtectedResource(models.Model):
    URL = 'URL'
    PDF = 'PDF'
    DOC = 'DOC'
    DOCX = 'DOCX'
    PPTX = 'PPTX'
    TXT = 'TXT'
    RESOURCE_TYPES = (
        (URL, 'Website address'),
        (PDF, 'PDF file'),
        (DOC, 'Word document, old format'),
        (DOCX, 'Word document, new format'),
        (PPTX, 'Powerpoint presentation'),
        (TXT, 'Standard text file'),
    )

    url = models.CharField(max_length=2048, blank=True)
    file = models.FileField(upload_to='userfiles/%Y/%m/%d', blank=True)
    type = models.CharField(max_length=4, choices=RESOURCE_TYPES, default=URL)
    original_filename = models.CharField(max_length=260, null=True, blank=True)  # If type not URL

    def __str__(self):
        return str(self.id) + ': ' + self.type

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

    def clean(self):
        # Either URL or File must be entered
        if self.url is None and self.file is None:
            raise ValidationError('URL or file required')


class Query(models.Model):
    query = models.CharField(max_length=250)

    def __str__(self):
        return str(self.id) + ': ' + self.query


class ScanLog(models.Model):
    H = 'H'
    C = 'C'
    FAILED_TYPE = (
        (H, 'HTTP error'),
        (C, 'No content candidates found (initial scan) or matched (post processing)'),
    )

    timestamp = models.DateTimeField(auto_now_add=True)
    protected_resource = models.ForeignKey(ProtectedResource, null=True, blank=True,on_delete=models.CASCADE)
    protected_source = models.TextField(null=True, blank=True)  # the text (source) of the protected resource
    queries = models.ManyToManyField(Query, null=True, blank=True)
    scoring_debug = models.TextField(null=True, blank=True)  # TODO Put reasons for scoring each chunk (etc) here
    fail_reason = models.CharField(max_length=500, null=True, blank=True)
    fail_type = models.CharField(max_length=1, choices=FAILED_TYPE, null=True, blank=True)
    user_ip = models.GenericIPAddressField(null=True, blank=True)  # Homepage trials set this, so you cannot (as easily) request results from other users

    def __str__(self):
        return str(self.id) + ': ' + self.timestamp.strftime("%b %d %Y %H:%M:%S")


class ScanResult(models.Model):
    result_log = models.ForeignKey(ScanLog,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    match_url = models.CharField(max_length=2048)
    match_display_url = models.CharField(max_length=2048)
    match_title = models.CharField(max_length=100)
    match_desc = models.CharField(max_length=500)
    post_scanned = models.BooleanField(default=False)
    post_fail_reason = models.CharField(max_length=500, null=True, blank=True)
    post_fail_type = models.CharField(max_length=1, choices=ScanLog.FAILED_TYPE, null=True, blank=True)
    perc_of_duplication = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # NNN.DD%

    def __str__(self):
        return str(self.id) + ': ' + self.timestamp.strftime("%b %d %Y %H:%M:%S")