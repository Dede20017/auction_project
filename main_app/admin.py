from django.contrib import admin
from .models import *

admin.site.register(AuctionUser)
admin.site.register(Area)
admin.site.register(Lot)
admin.site.register(Participant)
admin.site.register(Bid)