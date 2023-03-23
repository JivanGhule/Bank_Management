from django.contrib import admin
from app.models import UserRegister,UserTransaction
# Register your models here.
class UserRegisterAdmin(admin.ModelAdmin):
  list_display = ("FullName","UserName","Email","Mobile","AdharNo","Address","DOB","Age","Gender","Image","Password") 
admin.site.register(UserRegister, UserRegisterAdmin)

class UserTransactionAdmin(admin.ModelAdmin):
  list_display = ("UserName","Date","TransactionAmount","TotalAmount","Action","Notifications")  
admin.site.register(UserTransaction, UserTransactionAdmin)