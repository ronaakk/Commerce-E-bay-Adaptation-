from django.contrib import admin
from .models import *

# Register your models here.

# To retreive the listing by id
class ListingAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(PersonalWatchList)
