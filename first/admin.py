from django.contrib import admin
from .models import User,Moving,Staying,PassPort,Holiday,LimitsOfDate,Ready1,PaperPassport,PaperMoving,PaperStaying

# Register your models here.
admin.site.register(User)
admin.site.register(Moving)
admin.site.register(Staying)
admin.site.register(PassPort)
admin.site.register(Holiday)
admin.site.register(LimitsOfDate)
admin.site.register(Ready1)
admin.site.register(PaperPassport)
admin.site.register(PaperMoving)
admin.site.register(PaperStaying)