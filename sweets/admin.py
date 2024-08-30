from django.contrib import admin
from .models import User,Orders,Product,Cart_Wishlist,Sentiment

# Register your models here.
admin.site.register(User)
admin.site.register(Orders)
admin.site.register(Product)
admin.site.register(Cart_Wishlist)
admin.site.register(Sentiment)