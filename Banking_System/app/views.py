from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from app.models import UserRegister,UserTransaction
import datetime 
from django.contrib.auth.decorators import login_required

# Cashier Login => @Cashier => Bank@123

# Home View
def Home(request):
    return render(request,'index.html')


# Registartion Form Data Fetching  Registartion Form View
def Register(request):
    if request.method == "POST":
        # Getting Form Data From name Feild
        FullName =request.POST.get('Fname')
        Email =request.POST.get('email')
        Mobile =request.POST.get('tel')
        AdharNo =request.POST.get('AdharNo')
        Address =request.POST.get('Address')
        DOB =request.POST.get('DOB')
        Gender =request.POST.get('gender')
        Image =request.POST.get('image')
        UserName =request.POST.get('UserName')
        Password =request.POST.get('pswd')
        C_Password =request.POST.get('C_pwd')
        
        # DOB Validation & Age Calculations
        currentDate = datetime.date.today()
        currentYear = int(currentDate.year)
        DOB_a = int(DOB[0:4])
        Age = currentYear - DOB_a
        
        # Data Printing
        print(FullName,Email,Mobile,AdharNo,Address,DOB,Gender,Image,UserName,Password,C_Password)
        
        # Password Validation 
        if str(Password) == str(C_Password):
            if len(str(Password)) >= 5 and len(str(C_Password)) >= 5:
                # Age Validation
                if Age >= 18: 
                    # Checking Username , Adhar No and Email is Already Exist
                    if User.objects.filter(username = UserName).exists():
                        messages.error(request,"Username is Already Exist...!")
                    elif UserRegister.objects.filter(AdharNo = AdharNo).exists():
                        messages.error(request,"Adhar Number is Already Exist...!")
                    elif UserRegister.objects.filter(Email = Email).exists():
                        messages.error(request,"Email is Already Exist...!")
                    else:
                        # Data Storing in User And UserRegister Models.
                        user = User.objects.create_user(username=UserName,password=Password)
                        user.save() 
                        
                        # Data Storing in UserRegister modal with all Form Details
                        RegUser = UserRegister(FullName=FullName,Email=Email,Mobile=Mobile,AdharNo=AdharNo,Address=Address,DOB=DOB,Gender=Gender,Image=Image,UserName=UserName,Password=Password,Age=Age)
                        RegUser.save()
                        messages.success(request,"Registartion Successfully Done ...!")  
                else:
                    # Error message
                    messages.error(request,"Age Must Be 18 or Greater Than 18 Year ...!")  
            else:
                # success
                messages.error(request,"Password & Confirm Password Must Be Above 5 Digit...!")
        else:
            messages.error(request,"Password & Confirm Password is Not Matching ...!")
    # Home Page rendering After Url enter
    return render(request,'index.html')

# User Login Page Only For Register User
def UserLogin(request):
    if request.method == "POST":
        # Login User Username & Password
        UserName =request.POST.get('L_UserName')
        Password =request.POST.get('L_pswd')
        
        # authenticating to user in User modal and checking user is exist
        user=authenticate(request,username=UserName,password=Password)
        
        # User is Exist
        if user is not None:
            
            # If User is Exist Login
            login(request,user)
            messages.success(request,"Account Successfully Loged in...!")
            return redirect('userDashboard')
        # User is Not Exist
        else:
            messages.error(request,"Something Went wrong...!")
            return redirect('home')
    return render(request,'index.html')

# Logout Function
def LogOut(request):
    
    logout(request)
    messages.success(request,"Account Loged Out...!")
    return redirect("home")


# login_required for User Dashboard
@login_required(login_url='/userlogin/')
# User Dashboard only for Login User
def UserDashboard(request):
    # Getting Active User From request
    user = request.user
    print(user)
    
    # User And DB 
    Active_User = UserRegister.objects.filter(UserName=user)
    All_Entry = UserRegister.objects.all()
    Transaction = UserTransaction.objects.filter(UserName=user)
    Notifi = UserTransaction.objects.filter(UserName = user)[::-1]
    
    # Last 5 Notifications
    Notifi = Notifi[0:5]
    # User Image
    for i in Active_User:
        print(i.Image.url)
    
    # Total Amount in User Account
    TotalAmountInDashboard = []
    for i in Transaction:
        TotalAmountInDashboard.append(i.TotalAmount)
    if len(TotalAmountInDashboard)>=1:
        TotalAmountInDashboard=TotalAmountInDashboard[-1]
    else:
        Ta = 0
        TotalAmountInDashboard = float(Ta)
    context = {
        'Active_User': Active_User,
        'All_Entry' : All_Entry,
        'Transaction':Transaction,
        'TotalAmountInDashboard':TotalAmountInDashboard,
        'Notifi':Notifi
    }
    # /media/{{ i.P_Image }}
    return render(request,'userDashboard.html',context)
      
# Cashier Login Page 
def CashierLogin(request):
    if request.method == "POST":
        # Login Cashier Username & Password
        UserName =request.POST.get('C_UserName')
        Password =request.POST.get('C_pswd')
        # authenticating to Cashier in User modal and checking user is exist
        user1=authenticate(request,username=UserName,password=Password)
        if user1 is not None:
            login(request,user1)
            messages.success(request,"Account Successfully Loged in...!")
            return redirect('CashierLoginD')
        else:
            messages.error(request,"Something Went wrong...!")
            return redirect('home')
    return render(request,'index.html')



# login_required for User Dashboard
@login_required(login_url='/CashierLogin/')
# login_required for Cashier Dashboard
def CashierLoginD(request):
    # All User Registration details
    AllUser = UserRegister.objects.all()
    # All Transaction History
    AllTransactionHistory = UserTransaction.objects.all()
    context = {
        'AllUser':AllUser,
        'AllTransactionHistory':AllTransactionHistory
    }
    return render(request,'Cashier.html',context)

# Amount Deposite and Withdraw Action
def ActionAmount(request):
    if request.method == "POST":
        UserName = request.POST.get('Ac_UserName')
        Action = request.POST.get('Action')
        Amount = request.POST.get('Amount')
        Date = datetime.date.today()
        print("============",UserName,Action,Amount,Date,"==========")
        lastTran = UserTransaction.objects.filter(UserName = UserName)
        
        Amount = float(Amount)
        # Total Amount List
        LTran = []   
        print(LTran)
        for i in lastTran:
            LTran.append(i.TotalAmount)    
        # print(LTran[0])
        print(LTran)
        # Deposite Action
        if str(Action)=="D":
            # Total Amount
            if len(LTran)>=1:
                # Total Amount + New Amount Adding
                TAmount = LTran[-1] + Amount 
            else:
                a=0
                # First Time Adding Money
                TAmount = a + Amount    
            Msg = f"Your Account {UserName} has been Credited {Amount} Rs."
            
            # Deposite Money in User Account
            AmountD = UserTransaction(UserName=UserName,Action=Action,Date=Date,TransactionAmount=Amount,TotalAmount=TAmount,Notifications=Msg)
            AmountD.save()
            messages.success(request,"Account Has Been Credited")
            return redirect('CashierLoginD')
        # WithDraw
        if str(Action)=="W":
            # Total Amount
            if len(LTran)>=1:
                if LTran[-1] > Amount:
                    # Withdraw money from total amount - new amount
                    TAmount = LTran[-1] - Amount
                    Msg = f"Your Account {UserName} has been Debited {Amount} Rs."
                    # Withdraw Money From User Account
                    AmountD = UserTransaction(UserName=UserName,Action=Action,Date=Date,TransactionAmount=Amount,TotalAmount=TAmount,Notifications=Msg)
                    AmountD.save()
                    messages.success(request,"Account Has Been Debited")
                    return redirect('CashierLoginD')
                else:
                    messages.error(request,"Insufficient Balance ...!")
                    return redirect('CashierLoginD')        
            else:
                messages.error(request,"Insufficient Balance ...!")
                return redirect('CashierLoginD')   
        return redirect('CashierLoginD')
    return redirect(request,'CashierLoginD')


# Funds Transfer Action only for User Dashboard
def FundsTransfer(request):
    if request.method == "POST":
        UserName = request.POST.get('UserName')
        Action = request.POST.get('Action')
        Amount = request.POST.get('Amount')
        SendTo = request.POST.get('sendTo')
        Date = datetime.date.today()
        
        print(UserName,Action,Amount,SendTo,Date)
        # Which User is Transfering Money - User
        Fuser = UserTransaction.objects.filter(UserName = UserName)
        FTran = []
        print(FTran)
        for i in Fuser:
            FTran.append(i.TotalAmount)
        # print(FTran[-1])
        if len(FTran) >=1:
            
            FT_Total_Amount = float(FTran[-1])
        else:
            FT_Total_Amount = float(0)
        if FT_Total_Amount > float(Amount):
            if UserRegister.objects.filter(UserName = SendTo).exists():
                Msg = f"Your Account {SendTo} has been Credited {Amount} Rs. By {UserName}"
                S_To_user = UserTransaction.objects.filter(UserName = SendTo)
                S = []
                for i in S_To_user:
                    S.append(i.TotalAmount)    
                if len(S)>=1:
                    TAmount = S[-1] + float(Amount) 
                
                else:
                    TAmount = float(Amount)  
                TAction = "D"    
                S_User_Amt = UserTransaction(UserName=SendTo,Action=TAction,Date=Date,TransactionAmount=Amount,TotalAmount=TAmount,Notifications=Msg)
                S_User_Amt.save()
                
                FT_Amount_Total = FT_Total_Amount - float(Amount)
                Msg = f"Funds Transfer to {SendTo} Account is Debited by Rs {Amount}"
                SFuser = UserTransaction(UserName=UserName,Action=Action,Date=Date,TransactionAmount=Amount,TotalAmount=FT_Amount_Total,Notifications=Msg)
                SFuser.save()
                messages.success(request,"Fund is Transfered ...!")
                return redirect('userDashboard')  
            else:
                messages.error(request,"User is Not Exist ...!")
                return redirect('userDashboard') 
        else:
            messages.error(request,"Insufficient Balance ...!")
            return redirect('userDashboard')  
            
        
    return redirect(request,'userDashboard')