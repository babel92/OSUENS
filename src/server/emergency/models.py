from django.db import models
from django.utils.html import format_html,mark_safe

class Entry(models.Model):
    submit_time = models.DateTimeField('Submit time')
    original_email = models.TextField(max_length=10000)
    ET_HARASSMENT='HR'
    ET_BURGLARY='BG'
    ET_ROBBERY='RB'
    ET_THEFT='TH'
    ET_ARSON='AR'
    ET_ASSAULT='AS'
    ET_MURDER='MD'
    ET_OTHER='OT'
    ET_CHOICES = ((ET_HARASSMENT,'Harassment'),
    (ET_BURGLARY,'Burglary'),
    (ET_ROBBERY,'Robbery'),
    (ET_THEFT,'Theft'),
    (ET_ARSON,'Arson'),
    (ET_ASSAULT,'Assault'),
    (ET_MURDER,'Murder'),
    (ET_OTHER,'Other'))
    ET_DICT=dict(ET_CHOICES)
    emergency_type = models.CharField(max_length=2,
        choices=ET_CHOICES,
        default=ET_OTHER
        )
    suspect_name = models.CharField(max_length=200,blank=True)
    marker_script = models.TextField(max_length=1000,blank=True)
    address = models.TextField(max_length=100,blank=True)
    suspect_traits = models.CharField(max_length=400,blank=True)
    time = models.CharField(max_length=50,blank=True)
    image_url = models.CharField(max_length=200,blank=True)
    optional_info = models.TextField(max_length=1000,blank=True)


    def generate_MarkerScript(self):
        return format_html('<a id="geogen" class="button">Generate</a>'
    '<script type="text/javascript">{}</script>',
        mark_safe('$("#geogen").click(function(){'
            '$.get("/api/geo?addr="+encodeURIComponent($("#id_address").val()),function(data){'
                '$("#id_marker_script").val(data);'
            '});'
        '});'))
