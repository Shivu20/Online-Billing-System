from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk   #pip install pillow
import random,os
from tkinter import messagebox
import tempfile 
from time import strftime
import mysql.connector

def main():
    win=Tk()
    app=Login_window(win)
    win.mainloop()


class Login_window:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x800+0+0")
        self.root.title("Login")

        img=Image.open("image/3.jpg")
        img=img.resize((1530,800),Image.ANTIALIAS)
        self.photoimg=ImageTk.PhotoImage(img)

        lbl_img=Label(self.root,image=self.photoimg)
        lbl_img.place(x=0,y=0,width=1530,height=800)

        frame=Frame(self.root,bg="black")
        frame.place(x=480,y=120,width=340,height=450)

        img1=Image.open("image/Loginicon.jpg")
        img1=img1.resize((100,100),Image.ANTIALIAS)
        self.photoimg1=ImageTk.PhotoImage(img1)

        lbl_img1=Label(image=self.photoimg1,bg="black",borderwidth=0)
        lbl_img1.place(x=600,y=125,width=100,height=100)

        get_str=Label(frame,text="Get Started",font=("times new roman",20,"bold"),fg="orange",bg="black")
        get_str.place(x=95,y=100)

        #label1
        username=lbl=Label(frame,text="Username",font=("times new roman",20,"bold"),fg="white",bg="black")
        username.place(x=55,y=145)

        self.txtuser=ttk.Entry(frame,font=("times new roman",15,"bold"))
        self.txtuser.place(x=25,y=180,width=270)

        password=lbl=Label(frame,text="Password",font=("times new roman",20,"bold"),fg="white",bg="black")
        password.place(x=55,y=215)

        self.txtpass=ttk.Entry(frame,font=("times new roman",15,"bold"),show="*")
        self.txtpass.place(x=25,y=250,width=270)

        #============ICON IMAGE========================================
        img2=Image.open("image/LOGIN.png")
        img2=img2.resize((25,21),Image.ANTIALIAS)
        self.photoimg2=ImageTk.PhotoImage(img2)

        lbl_img2=Label(image=self.photoimg2,bg="black",borderwidth=0)
        lbl_img2.place(x=510,y=275,width=25,height=21)

        img3=Image.open("image/passwords.jpg")
        img3=img3.resize((25,25),Image.ANTIALIAS)
        self.photoimg3=ImageTk.PhotoImage(img3)

        lbl_img3=Label(image=self.photoimg3,bg="black",borderwidth=0)
        lbl_img3.place(x=500,y=340,width=25,height=25)

        #LoginButton
        loginbtn=Button(frame,command=self.login,text="Login",borderwidth=3,relief=RAISED,cursor="hand2",font=("times new roman",15,"bold"),fg="white",bg="red",activeforeground="white",activebackground="red")
        loginbtn.place(x=110,y=290,width=120,height=35)

        #RegisterButton
        registerbtn=Button(frame,text=" New User Register",command=self.register_window,font=("times new roman",10,"bold"),borderwidth=0,fg="white",bg="black",activeforeground="white",activebackground="black")
        registerbtn.place(x=10,y=360,width=110)

        #forgetpasswordButton
        forgetpasswordbtn=Button(frame,text="Forget Password",command=self.forgot_password_window,font=("times new roman",10,"bold"),borderwidth=0,fg="white",bg="black",activeforeground="white",activebackground="black")
        forgetpasswordbtn.place(x=10,y=390,width=100)

    def register_window(self):
        self.new_window=Toplevel(self.root)
        self.app=Register_window(self.new_window)


    def login(self):
        if self.txtuser.get()=="" or self.txtpass.get()=="":
            messagebox.showerror("Error","Fill the required details.")
        elif self.txtuser.get()=="shivam" and self.txtpass.get()=="gupta":
            messagebox.showinfo("Success","Welcome to Online Billing System.")
        else:
            conn=mysql.connector.connect(host="localhost",username="root",password="kaka#@12",database="billing")
            my_cursor=conn.cursor()
            my_cursor.execute("Select * from login where Email=%s and Password=%s",(
                                                                                    self.txtuser.get(),
                                                                                    self.txtpass.get()
                                                                                ))
            row=my_cursor.fetchone()
            if row==None:
                messagebox.showerror("Error","Invalid Username and Password")
            else:
                open_main=messagebox.askyesno("YesNo","Access only admin")
                if open_main>0:
                    self.new_window=Toplevel(self.root)
                    self.app=Bill_App(self.new_window)
                else:
                    if not open_main:
                        return

            conn.commit()
            conn.close()

    #============================Reset Password=======================================================
    def reset_pass(self):
            if self.combo_security_q.get()=="Select":
                messagebox.showerror("Error","Select security Question",parent=self.root2)
            elif self.txt_secans.get()=="":
                messagebox.showerror("Error","Please enter the answer",parent=self.root2)
            elif self.txt_newpass.get()=="":
                messagebox.showerror("Error","Please enter the new password",parent=self.root2)
            else:
                conn=mysql.connector.connect(host="localhost",username="root",password="kaka#@12",database="billing")
                my_cursor=conn.cursor()
                query=("Select * from login where Email=%s and Security_q=%s and Security_a=%s")
                value=(self.txtuser.get(),self.combo_security_q.get(),self.txt_secans.get())
                my_cursor.execute(query,value)
                row=my_cursor.fetchone()
                if row==None:
                    messagebox.showerror("Error","Please enter correct answer",parent=self.root2)
                else:
                    query=("update login set Password=%s where Email=%s")
                    value=(self.txt_newpass.get(),self.txtuser.get())
                    my_cursor.execute(query,value)

                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Info","Your Password has been reset successfully.",parent=self.root2)
                    self.root2.destroy()


    #================================Forget Password===================================================
    def forgot_password_window(self):
        if self.txtuser.get()=="":
            messagebox.showerror("Error","Please enter the username to reset the password.")
        else:
            conn=mysql.connector.connect(host="localhost",username="root",password="kaka#@12",database="billing")
            my_cursor=conn.cursor()
            query=("Select * from login where Email=%s")
            value=(self.txtuser.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()

            if row==None:
                messagebox.showerror("My Error","Please enter the valid username")
            else:
                conn.close()
                self.root2=Toplevel()
                self.root2.title("Forget Password")
                self.root2.geometry("340x450+610+170")

                l=Label(self.root2,text="Forgot Password",font=("times new roman",20,"bold"),fg="white",bg="black")
                l.place(x=0,y=10,relwidth=1)

                security_q=Label(self.root2,text="Select Security Question ",font=("times new roman",15,"bold"),fg="black")
                security_q.place(x=30,y=80)

                self.combo_security_q=ttk.Combobox(self.root2,font=("times new roman",15,"bold"),state="randomly")
                self.combo_security_q["values"]=("Select","Your Birth place","Your pet name","Your favourite game")
                self.combo_security_q.place(x=30,y=120,width=200)
                self.combo_security_q.current(0)

                secans=Label(self.root2,text="Security Answer",font=("times new roman",15,"bold"),fg="black")
                secans.place(x=30,y=160)

                self.txt_secans=ttk.Entry(self.root2,font=("times new roman",15,"bold"))
                self.txt_secans.place(x=30,y=190,width=200)

                newpass=Label(self.root2,text="New Password",font=("times new roman",15,"bold"),fg="black")
                newpass.place(x=30,y=230)

                self.txt_newpass=ttk.Entry(self.root2,font=("times new roman",15,"bold"),show="*")
                self.txt_newpass.place(x=30,y=260,width=200)

                resetbtn=Button(self.root2,command=self.reset_pass,text="Reset Password",font=("times new roman",15,"bold"),fg="white",bg="red")
                resetbtn.place(x=80,y=310,width=160,height=40)

class Register_window:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x800+0+0")
        self.root.title("Register")

        #==================Variables==================================================
        self.var_fname=StringVar()
        self.var_lname=StringVar()
        self.var_contact=StringVar()
        self.var_email=StringVar()
        self.var_securityq=StringVar()
        self.var_secans=StringVar()
        self.var_password=StringVar()
        self.var_conpass=StringVar()
        self.var_check=IntVar()

        img=Image.open("image/wallpaper.jpg")
        img=img.resize((1530,800),Image.ANTIALIAS)
        self.photoimg=ImageTk.PhotoImage(img)

        lbl_img=Label(self.root,image=self.photoimg)
        lbl_img.place(x=-20,y=0,width=1530,height=700)

        #================== Register window============================================
        frame=Frame(self.root,bg="white")
        frame.place(x=400,y=120,width=600,height=500)

        register_lbl=Label(frame,text="Register Here",font=("times new roman",20,"bold"),fg="Green",bg="white")
        register_lbl.place(x=20,y=20)

        #====================Labels===================================================
        fname=Label(frame,text="First Name",font=("times new roman",15,"bold"),fg="black",bg="white")
        fname.place(x=30,y=80)

        fname_entry=ttk.Entry(frame,textvariable=self.var_fname,font=("times new roman",15,"bold"))
        fname_entry.place(x=30,y=110,width=200)

        lname=Label(frame,text="Last Name",font=("times new roman",15,"bold"),fg="black",bg="white")
        lname.place(x=310,y=80)

        lname_entry=ttk.Entry(frame,textvariable=self.var_lname,font=("times new roman",15,"bold"))
        lname_entry.place(x=310,y=110,width=200)

        contact=Label(frame,text="Contact Number ",font=("times new roman",15,"bold"),fg="black",bg="white")
        contact.place(x=30,y=150)

        contact_entry=ttk.Entry(frame,textvariable=self.var_contact,font=("times new roman",15,"bold"))
        contact_entry.place(x=30,y=180,width=200)

        email=Label(frame,text="E-mail",font=("times new roman",15,"bold"),fg="black",bg="white")
        email.place(x=310,y=150)

        email_entry=ttk.Entry(frame,textvariable=self.var_email,font=("times new roman",15,"bold"))
        email_entry.place(x=310,y=180,width=200)

        security_q=Label(frame,text="Select Security Question ",font=("times new roman",15,"bold"),fg="black",bg="white")
        security_q.place(x=30,y=220)

        self.combo_security_q=ttk.Combobox(frame,textvariable=self.var_securityq,font=("times new roman",15,"bold"),state="randomly")
        self.combo_security_q["values"]=("Select","Your Birth place","Your pet name","Your favourite game")
        self.combo_security_q.place(x=30,y=250,width=200)
        self.combo_security_q.current(0)

        secans=Label(frame,text="Security Answer",font=("times new roman",15,"bold"),fg="black",bg="white")
        secans.place(x=310,y=220)

        secans_entry=ttk.Entry(frame,textvariable=self.var_secans,font=("times new roman",15,"bold"))
        secans_entry.place(x=310,y=250,width=200)

        password=Label(frame,text="Password ",font=("times new roman",15,"bold"),fg="black",bg="white")
        password.place(x=30,y=290)

        password_entry=ttk.Entry(frame,textvariable=self.var_password,font=("times new roman",15,"bold"),show="*")
        password_entry.place(x=30,y=320,width=200)

        conpass=Label(frame,text="Confirm Password",font=("times new roman",15,"bold"),fg="black",bg="white")
        conpass.place(x=310,y=290)

        conpass_entry=ttk.Entry(frame,textvariable=self.var_conpass,font=("times new roman",15,"bold"))
        conpass_entry.place(x=310,y=320,width=200)

        #============================Check================================================================================
        checkbtn=Checkbutton(frame,variable=self.var_check,text="I agree to the terms and condition.",font=("times new roman",15,"bold"),onvalue=1,offvalue=0)
        checkbtn.place(x=30,y=360)

        #=========================BUTTONS===========================================================================
        img1=Image.open("image/register.jpg")
        img1=img1.resize((180,44),Image.ANTIALIAS)
        self.photoimg1=ImageTk.PhotoImage(img1)
        b1=Button(frame,image=self.photoimg1,command=self.register_data,borderwidth=0,cursor="hand2",font=("times new roman",15,"bold"))
        b1.place(x=30,y=410,width=180)

        img2=Image.open("image/logini.jpg")
        img2=img2.resize((180,44),Image.ANTIALIAS)
        self.photoimg2=ImageTk.PhotoImage(img2)
        b1=Button(frame,image=self.photoimg2,command=self.return_login,borderwidth=0,cursor="hand2",font=("times new roman",15,"bold"))
        b1.place(x=290,y=410,width=180)

    #=================================Fuction declaration========================================

    def register_data(self):
        if self.var_fname.get()=="" or self.var_email.get()=="" or self.var_securityq.get()=="Select":
            messagebox.showerror("Error","Fill the required details.")
        elif self.var_password.get()!=self.var_conpass.get():
            messagebox.showerror("Error","Passord and Confirm Password must be same.")
        elif self.var_check.get()==0:
            messagebox.showerror("Error","Please agree the terms and condition")
        else:
            conn=mysql.connector.connect(host="localhost",username="root",password="kaka#@12",database="billing")
            my_cursor=conn.cursor()
            query=("Select * from login where email=%s")
            value=(self.var_email.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            if row!=None:
                messagebox.showerror("Error","User already exist, Please try another email")
            else:
                my_cursor.execute("insert into login values(%s,%s,%s,%s,%s,%s,%s)",(
                                                                                    self.var_fname.get(),
                                                                                    self.var_lname.get(),
                                                                                    self.var_contact.get(),
                                                                                    self.var_email.get(),
                                                                                    self.var_securityq.get(),
                                                                                    self.var_secans.get(),
                                                                                    self.var_password.get()
                                                                                        
                                                                                   ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success","Register successfully")

    def return_login(self):
        self.root.destroy()


class Bill_App:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x800+0+0")
        self.root.title("Online Billing System Software")

        #========================================Variables==========================================================
        self.c_name=StringVar()
        self.c_phone=StringVar()
        self.bill_no=StringVar()
        self.bill_no=IntVar()
        self.c_email=StringVar()
        self.search_bill=StringVar()
        self.product=StringVar()
        self.prices=IntVar()
        self.qty=IntVar()
        self.qtyavail=IntVar()
        self.sub_total=StringVar()
        self.tax_input=StringVar()
        self.total=StringVar()

        #Product Category list
        self.Category=["Select Option","Clothing","Households","Mobiles","Electronics"]

        #Sub Category Clothing list
        self.SubcategoryClothing=["Select Option","Pant","T-shirt","Shirt","Jeans","Jacket","Undergarments","Suit","Kurta","Blanket"]
        self.pant=["Select Option","Levis","Mufti","Spykar"]
        self.price_Levis=1500
        self.price_Mufti=1800
        self.price_Spykar=2000

        self.Tshirt=["Select Option","Polo","Roadster","Jack & Jones"]
        self.price_Polo=1000
        self.price_Roadster=800
        self.price_JackandJones=500

        self.Shirt=["Select Option","Tommy Hilfiger","Peter England","Allen Solly Shirt"]
        self.price_TommyHilfiger=1000
        self.price_PeterEngland=1200
        self.price_AllenSollyShirt=1400

        self.Jeans=["Select Option","Levis Jeans","Wrangler","Lee"]
        self.price_LevisJeans=3000
        self.price_Wrangler=2800
        self.price_Lee=2500

        self.Jacket=["Select Option","Denim","Allen Solly","Roadster Jacket"]
        self.price_Denim=6000
        self.price_AllenSolly=4800
        self.price_RoadsterJacket=3500

        self.Undergarments=["Select Option","Calvein","Rupa","LUX"]
        self.price_Calvein=500
        self.price_Rupa=100
        self.price_LUX=200

        self.Suit=["Select Option","Emporio Armani","Blackberry","Bunaai"]
        self.price_EmporioArmani=15000
        self.price_Blackberry=18000
        self.price_Bunaai=20000

        self.Kurta=["Select Option","Manyavar","Jompers","Sojanya"]
        self.price_Manyavar=2300
        self.price_Jompers=2300
        self.price_Sojanya=1900

        self.Blanket=["Select Option","Signature","Black Magic","HUESLAND"]
        self.price_Signature=10000
        self.price_BlackMagic=5800
        self.price_HUESLAND=9760

        #Sub Category Households list
        self.SubcategoryHouseholds=["Select Option","Kitchen item","Cleaning item","kids item"]
        self.Kitchenitem=["Select Option","Oil","Salt","Milk","Vinegar","Mustard","Rice","Dal","Lavang","Jeera","Curd","Peppercorn","Saffron","Sugar","Beans","Butter","Sauces","Vegetables","Fruit","Flour","Cashew","Tea leaf","Spices","Aluminum foil","Pots & pans","Utensils","Wheat","MatchStick","Turmeric Powder"]
        self.price_Oil=150
        self.price_Salt=24
        self.price_Milk=20
        self.price_Vinegar=50
        self.price_Mustard=35
        self.price_Rice=130
        self.price_Dal=80
        self.price_Lavang=800
        self.price_Jeera=400
        self.price_Curd=18
        self.price_Peppercorn=30
        self.price_Saffron=75
        self.price_Sugar=55
        self.price_Beans=40
        self.price_Butter=85
        self.price_Sauces=120
        self.price_Vegetables=40
        self.price_Fruit=80
        self.price_Flour=90
        self.price_Cashew=180
        self.price_Tealeaf=300
        self.price_Spices=75
        self.price_Aluminumfoil=480
        self.price_Potsandpans=120
        self.price_Utensils=200
        self.price_Wheat=135
        self.price_MatchStick=5
        self.price_TurmericPowder=65


        self.Cleaningitem=["Select Option","Bath wash","Face wash","Surf","Soap","Toilet Cleaner","Tooth paste"]
        self.price_Bathwash=40
        self.price_Facewash=180
        self.price_Surf=55
        self.price_Soap=10
        self.price_ToiletCleaner=75
        self.price_Toothpaste=79
        
        self.kidsitem=["Select Option","Chocolate","IceCream","Toffee","Pepsi","Chips","Maggie","Cake","Popcorn","Oatmeal","Olives","Bread","Nuts","Ketchup","Biscuits","Namkeen"]
        self.price_Chocolate=40
        self.price_IceCream=180
        self.price_Toffee=55
        self.price_Pepsi=10
        self.price_Chips=75
        self.price_Maggie=79
        self.price_Cake=250
        self.price_Popcorn=100
        self.price_Oatmeal=45
        self.price_Olives=30
        self.price_Bread=20
        self.price_Nuts=60
        self.price_Ketchup=38
        self.price_Biscuits=30
        self.price_Namkeen=90

        #Sub Category Mobiles list
        self.SubcategoryMobiles=["Select Option","Iphone","Xiaomi","oneplus","Samsung","Realme","Vivo","Oppo"]
        self.Iphone=["Select Option","Iphone 11","Iphone SE","Iphone 12","Iphone 12 Mini","Iphone 12 pro","Iphone 13","Iphone 13 Mini","Iphone 13 pro","Iphone X"]
        self.price_Iphone11=45000
        self.price_IphoneSE=34000
        self.price_Iphone12=72000
        self.price_Iphone12mini=74000
        self.price_Iphone12pro=121000
        self.price_Iphone13=89000
        self.price_Iphone13mini=92000
        self.price_Iphone13pro=145000
        self.price_IphoneX=34000

        self.Xiaomi=["Select Option","Mi 11 ultra 5g","Mi 11 Pro","Mi 10i","Mi 10 Lite","Mi 10S","Mi 10 Pro","Mi 8 Lite","Mi 6","Mi 5X"]
        self.price_Mi11ultra5g=19890
        self.price_Mi11Pro=17999
        self.price_Mi10i=16999
        self.price_Mi10Lite=15999
        self.price_Mi10S=14999
        self.price_Mi10Pro=13999
        self.price_Mi8Lite=12999
        self.price_Mi6=9999
        self.price_Mi5X=8999

        self.oneplus=["Select Option","oneplus Nord 2 5G","oneplus  Nord CE 5G","oneplus Nord N10 5G","oneplus Nord","oneplus 9 Series","oneplus 8T","oneplus 8 Series","oneplus 7T Pro","oneplus 7 Series"]
        self.price_oneplusNordCE5G=45000
        self.price_oneplusNord25G=42000
        self.price_oneplusNordN105G=40000
        self.price_oneplusNord=34000
        self.price_oneplus9Series=39000
        self.price_oneplus8T=29000
        self.price_oneplus7TPro=27000
        self.price_oneplus7Series=21000
        

        self.Samsung=["Select Option","Samsung S20 ultra","Samsung S20 ultra 5G","Samsung M31","Samsung A11","Samsung M21","Samsung A31","Samsung A41"]
        self.price_SamsungS20ultra=69000
        self.price_SamsungS20ultra5g=76000
        self.price_SamsungM31=46000
        self.price_SamsungA11=39000
        self.price_SamsungM21=33000
        self.price_SamsungA31=24000
        self.price_SamsungA41=29000

        self.Realme=["Select Option","Realme C20","Realme Narzo 50A","Realme Narzo 30 Pro","Realme X7","Realme 7","Realme 8","Realme 8i","Realme 8s","Realme GT Neo 2",]
        self.price_RealmeC20=7499
        self.price_RealmeNarzo50A=12499
        self.price_RealmeNarzo30Pro=16999
        self.price_RealmeX7=18999
        self.price_Realme7=14999
        self.price_Realme8=16999
        self.price_Realme8i=13899
        self.price_Realme8s=17999
        self.price_RealmeGTNeo2=31599

        
        self.Vivo=["Select Option","Vivo X70 Pro Plus","Vivo Y21","Vivo X70 Pro","Vivo Y20","Vivo X60","Vivo V20","Vivo V21","Vivo Y20G","Vivo Y3S",]
        self.price_VivoX70ProPlus=79990
        self.price_VivoY21=13479
        self.price_VivoX70Pro=46990
        self.price_VivoY20=12494
        self.price_VivoX60=34990
        self.price_VivoV20=22990
        self.price_VivoV20G=14990
        self.price_VivoY3S=9490
        
        self.Oppo=["Select Option","Oppo Reno 6","Oppo A53s","Oppo Reno 6 Pro","Oppo A74","Oppo F19 Pro","Oppo F19s","Oppo F19 Pro plus","Oppo A54","Oppo Reno 3 Pro",]
        self.price_OppoReno6=29990
        self.price_OppoA53s=14990
        self.price_OppoReno6Pro=39990
        self.price_OppoA74=29990
        self.price_OppoF19Pro=19990
        self.price_OppoF19s=18990
        self.price_OppoF19Proplus=34990
        self.price_OppoA54=13459
        self.price_OppoReno3Pro=29990

        #Sub Category Electronics list
        self.SubcategoryElectronics=["Select Option","TV","Radio","Washing Machine","Freezer","Earphones","Trimmer","Tubelight","Bulb","Monitor","Mouse","Keyboard","Printer","Gyser"]
        self.TV=["Select Option","Sony","LG","Samsung","Mi","Videocon"]
        self.price_Sony=29990
        self.price_LG=54990
        self.price_Samsung=39990
        self.price_Mi=29990
        self.price_Videocon=19990

        self.Radio=["Select Option","Revo Radio","Ruark Audio","VQ","Philips Radio","iBELL FM","Panasonic Radio"]
        self.price_RevoRadio=2999
        self.price_RuarkAudio=1499
        self.price_VQ=1699
        self.price_PhilipsRadio=2900
        self.price_iBELLFM=1999
        self.price_PanasonicRadio=1490

        self.WashingMachine=["Select Option","Whirlpool","LG Washing Machine","Samsung Washing Machine","Bosch"]
        self.price_Whirlpool=28990
        self.price_LGWashingMachine=44990
        self.price_SamsungWashingMachine=47000
        self.price_Bosch=38990

        self.Freezer=["Select Option","Haier","LG Freezer","Bosch Freezer","Summit"]
        self.price_Haier=7499
        self.price_LGFreezer=54990
        self.price_BoschFreezer=39990
        self.price_Summit=29990

        self.Earphones=["Select Option","Boat","Apple","Samsung Galaxy","JBL","Sony WI","Realme Buds","Boat Rockerz","One Plus blast","Boat Airdopes"]
        self.price_Boat=1299
        self.price_Apple=20990
        self.price_SamsungGalaxy=11999
        self.price_JBL=3999
        self.price_SonyWI=4590
        self.price_RealmeBuds=690
        self.price_BoatRockerz=1460
        self.price_OnePlusblast=249
        self.price_BoatAirdopes=3999

        self.Trimmmer=["Select Option","Havelles","Phillips Beared trimmer series","Goldtech","Syska"]
        self.price_Havelles=1676
        self.price_PhillipsBearedtrimmerseries=1199
        self.price_Goldtech=3705
        self.price_Syska=749

        self.Tubelight=["Select Option","Everready ","Sony Tubelight","LG Tubelight","Crompton","HALCO","Phillips Tubelight"]
        self.price_Everready=249
        self.price_SonyTubelight=199
        self.price_LGTubelight=299
        self.price_Crompton=129
        self.price_HALCO=149
        self.price_PhillipsTubelight=295

        self.Bulb=["Select Option","Everready Bulb","Sony Bulb","LG Bulb","Crompton Bulb","HALCO Bulb","Phillips Bulb"]
        self.price_EverreadyBulb=49
        self.price_SonyBulb=99
        self.price_LGBulb=99
        self.price_CromptonBulb=29
        self.price_HALCOBulb=49
        self.price_PhillipsBulb=95

        self.Monitor=["Select Option","HP","Dell","Acer","Asus","Lenovo","Apple Monitor","LG Monitor","Samsung Monitor"]
        self.price_HP=45999
        self.price_Dell=54990
        self.price_Acer=28990
        self.price_Asus=39990
        self.price_Lenovo=29990
        self.price_AppleMonitor=114990
        self.price_LGMonitor=39990
        self.price_SamsungMonitor=29990

        self.Mouse=["Select Option","HP Mouse","Dell Mouse","Acer Mouse","Asus Mouse","Lenovo Mouse"]
        self.price_HPMouse=499
        self.price_DellMouse=399
        self.price_AcerMouse=289
        self.price_AsusMouse=549
        self.price_LenovoMouse=249

        self.Keyboard=["Select Option","HP Keyboard","Dell Keyboard","Acer Keyboard","Asus Keyboard","Lenovo Keyboard"]
        self.price_HPKeyboard=4599
        self.price_DellKeyboard=5499
        self.price_AcerKeyboard=2899
        self.price_AsusKeyboard=3999
        self.price_LenovoKeyboard=2999

        self.Printer=["Select Option","HP Printer","Dell Printer","Acer Printer","Asus Printer","Lenovo Printer"]
        self.price_HPPrinter=15999
        self.price_DellPrinter=14990
        self.price_AcerPrinter=18940
        self.price_AsusPrinter=19990
        self.price_LenovoPrinter=17990

        self.Gyser=["Select Option","Bajaj","Venus","Usha","Morphy Richards"]
        self.price_Bajaj=6599
        self.price_Venus=4499
        self.price_Usha=3899
        self.price_MorphyRichards=2999

        #IMAGE1
        img=Image.open("image/6.jpg")
        img=img.resize((450,130),Image.ANTIALIAS)
        self.photoimg=ImageTk.PhotoImage(img)

        lbl_img=Label(self.root,image=self.photoimg)
        lbl_img.place(x=0,y=0,width=450,height=130)

        lbl_title=Label(self.root,text="BILLING SOFTWARE                ",font=("times new roman",55,"bold"),bg="white",fg="black")
        lbl_title.place(x=460,y=0,width=1080,height=130)

        def time():
            string = strftime('%H:%M:%S %p')
            lbl.config(text = string)
            lbl.after(1000,time)

        lbl =Label(lbl_title, font=('times new roman',16,'bold'),background='white',foreground='blue')
        lbl.place(x=650,y=90,width=120,height=50)
        time()

        Main_Frame=Frame(self.root,bd=5,relief=GROOVE,bg="white")
        Main_Frame.place(x=0,y=140,width=1530,height=620)

        #CUSTOMER LABEL FRAME
        Cust_Frame=LabelFrame(Main_Frame,text="CUSTOMER",font=("times new roman",12,"bold"),bg="white",fg="red")
        Cust_Frame.place(x=10,y=5,width=330,height=130)

        self.lbl_Cmob=Label(Cust_Frame,text="Mobile No.:",font=("times new roman",12,"bold"),bg="white")
        self.lbl_Cmob.grid(row=0,column=0,stick=W,padx=4,pady=2)

        self.entry_Cmob=ttk.Entry(Cust_Frame,textvariable=self.c_phone,font=("times new roman",12,"bold"),width=20)
        self.entry_Cmob.grid(row=0,column=1)

        self.lblCname=Label(Cust_Frame,font=("arial",12,"bold"),bg="white",text="Customer Name:",bd=4)
        self.lblCname.grid(row=1,column=0,stick=W,padx=4,pady=2)

        self.txtCname=ttk.Entry(Cust_Frame,textvariable=self.c_name,font=("arial",11,"bold"),width=20)
        self.txtCname.grid(row=1,column=1)

        self.lblCemail=Label(Cust_Frame,font=("arial",12,"bold"),bg="white",text="E-Mail:",bd=4)
        self.lblCemail.grid(row=2,column=0,stick=W,padx=4,pady=2)

        self.txtCemail=ttk.Entry(Cust_Frame,textvariable=self.c_email,font=("arial",11,"bold"),width=20)
        self.txtCemail.grid(row=2,column=1)

        #PRODUCT LABEL FRAME
        Prod_Frame=LabelFrame(Main_Frame,text="PRODUCT",font=("times new roman",12,"bold"),bg="white",fg="red")
        Prod_Frame.place(x=340,y=5,width=510,height=130)

        self.lbl_Category=Label(Prod_Frame,font=("arial",12,"bold"),bg="white",text="Select Category :",bd=4)
        self.lbl_Category.grid(row=0,column=0,stick=W,padx=4,pady=2)

        self.Combo_Category=ttk.Combobox(Prod_Frame,value=self.Category,font=("arial",11,"bold"),width=20)
        self.Combo_Category.current(0)
        self.Combo_Category.grid(row=0,column=1)
        self.Combo_Category.bind("<<ComboboxSelected>>",self.Categories)

        self.lbl_subcategory=Label(Prod_Frame,font=("arial",12,"bold"),bg="white",text="Sub Category :",bd=4)
        self.lbl_subcategory.grid(row=1,column=0,stick=W,padx=4,pady=2)

        self.Combo_subcategory=ttk.Combobox(Prod_Frame,value=[""],font=("arial",11,"bold"),width=20)
        self.Combo_subcategory.grid(row=1,column=1)
        self.Combo_subcategory.bind("<<ComboboxSelected>>",self.Product_name)

        self.lbl_prname=Label(Prod_Frame,font=("arial",12,"bold"),bg="white",text="Product Name :",bd=4)
        self.lbl_prname.grid(row=2,column=0,stick=W,padx=4,pady=2)

        self.Combo_prname=ttk.Combobox(Prod_Frame,textvariable=self.product,font=("arial",11,"bold"),width=20)
        self.Combo_prname.grid(row=2,column=1)
        self.Combo_prname.bind("<<ComboboxSelected>>",self.Price)

        self.lbl_billn=Label(Prod_Frame,font=("arial",12,"bold"),bg="white",text="Bill No. :")
        self.lbl_billn.grid(row=0,column=2,stick=W,padx=4,pady=2)

        self.entry_billn=ttk.Entry(Prod_Frame,textvariable=self.bill_no,font=("arial",8,"bold"),width=13 )
        self.entry_billn.grid(row=0,column=3)

        self.lbl_price=Label(Prod_Frame,font=("arial",12,"bold"),bg="white",text="Price :",bd=4)
        self.lbl_price.grid(row=1,column=2,stick=W,padx=4,pady=2)

        self.Combo_price=ttk.Combobox(Prod_Frame,textvariable=self.prices,font=("arial",8,"bold"),width=10)
        self.Combo_price.grid(row=1,column=3)

        self.lbl_qty=Label(Prod_Frame,font=("arial",12,"bold"),bg="white",text="Qty :")
        self.lbl_qty.grid(row=2,column=2,stick=W,padx=4,pady=2)

        self.entry_qty=ttk.Entry(Prod_Frame,textvariable=self.qty,font=("arial",8,"bold"),width=13)
        self.entry_qty.grid(row=2,column=3)

        #Middle Frame
        MiddleFrame=Frame(Main_Frame,bd=8)
        MiddleFrame.place(x=0,y=140,width=845,height=250)

        #IMAGE1
        img1=Image.open("image/13.png")
        img1=img1.resize((845,250),Image.ANTIALIAS)
        self.photoimg1=ImageTk.PhotoImage(img1)

        lbl_img1=Label(MiddleFrame,image=self.photoimg1)
        lbl_img1.place(x=0,y=0,width=845,height=250)

        #Search
        Search_Frame=Frame(Main_Frame,bd=2,bg="white")
        Search_Frame.place(x=850,y=13,width=410,height=40)

        self.lblBill=Label(Search_Frame,text="Bill Number",font=("times new roman",12,"bold"),bg="red",fg="white")
        self.lblBill.grid(row=0,column=0,stick=W,padx=1)

        self.entry_Search=ttk.Entry(Search_Frame,textvariable=self.search_bill,font=("times new roman",10,"bold"),width=24)
        self.entry_Search.grid(row=0,column=1,stick=W,padx=2)

        self.BtnSearch=Button(Search_Frame,command=self.find_bill,height=1,text="  Search  ",font=('arial',8,'bold'),bg="Pink",fg="white")
        self.BtnSearch.grid(row=0,column=2)

        #Billing
        Bill_Frame=LabelFrame(Main_Frame,text="Billing",font=("times new roman",12,"bold"),bg="white",fg="red")
        Bill_Frame.place(x=850,y=43,width=410,height=340)

        scroll_y=Scrollbar(Bill_Frame,orient=VERTICAL)
        self.textarea=Text(Bill_Frame,yscrollcommand=scroll_y.set,bg="white",fg="Blue",font=("times new roman",12,"bold"))
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_y.config(command=self.textarea.yview)
        self.textarea.pack(fill=BOTH,expand=1)

        
        #Bill Counter LABEL FRAME
        BillC_Frame=LabelFrame(Main_Frame,text="Bill Counter",font=("times new roman",10,"bold"),bg="white",fg="red")
        BillC_Frame.place(x=0,y=385,width=1520,height=105)

        self.lbl_subtotal=Label(BillC_Frame,text="Sub Total:",font=("times new roman",10,"bold"),bg="white")
        self.lbl_subtotal.grid(row=0,column=0,stick=W,padx=4,pady=2)

        self.entry_subtotal=ttk.Entry(BillC_Frame,textvariable=self.sub_total,font=("times new roman",10,"bold"),width=25)
        self.entry_subtotal.grid(row=0,column=1)

        self.lbl_tax=Label(BillC_Frame,font=("times new roman",10,"bold"),bg="white",text="Tax :",bd=4)
        self.lbl_tax.grid(row=1,column=0,stick=W,padx=4,pady=2)

        self.entry_tax=ttk.Entry(BillC_Frame,textvariable=self.tax_input,font=("arial",9,"bold"),width=25)
        self.entry_tax.grid(row=1,column=1)

        self.lbl_total=Label(BillC_Frame,font=("times new roman",10,"bold"),bg="white",text="Total :",bd=4)
        self.lbl_total.grid(row=2,column=0,stick=W,padx=4,pady=2)

        self.entry_total=ttk.Entry(BillC_Frame,textvariable=self.total,font=("arial",9,"bold"),width=25)
        self.entry_total.grid(row=2,column=1)

        #Button Frame
        Btn_Frame=Frame(BillC_Frame,bd=2,bg="black")
        Btn_Frame.place(x=300,y=0)

        self.BtnAddToCart=Button(Btn_Frame,command=self.AddItem, height=2,text=" Add To Cart ",font=('arial',15,'bold'),bg="Pink",fg="white")
        self.BtnAddToCart.grid(row=0,column=0)

        self.Btngeneratebill=Button(Btn_Frame,command=self.gen_bill,height=2,text=" Generate Bill ",font=('arial',15,'bold'),bg="Pink",fg="white")
        self.Btngeneratebill.grid(row=0,column=1)

        self.Btnsavebill=Button(Btn_Frame,command=self.save_bill,height=2,text="  Save Bill  ",font=('arial',15,'bold'),bg="Pink",fg="white")
        self.Btnsavebill.grid(row=0,column=2)

        self.Btnprint=Button(Btn_Frame,command=self.iprint,height=2,text="   Print   ",font=('arial',15,'bold'),bg="Pink",fg="white")
        self.Btnprint.grid(row=0,column=3)

        self.Btnclear=Button(Btn_Frame,command=self.clear,height=2,text="  Clear  ",font=('arial',15,'bold'),bg="Pink",fg="white")
        self.Btnclear.grid(row=0,column=4)

        self.Btnupdate=Button(Btn_Frame,command=self.update,height=2,text="  Update  ",font=('arial',15,'bold'),bg="Pink",fg="white")
        self.Btnupdate.grid(row=0,column=5)

        self.Btnclear=Button(Btn_Frame,command=self.delete,height=2,text="  Delete  ",font=('arial',15,'bold'),bg="Pink",fg="white")
        self.Btnclear.grid(row=0,column=6)

        self.Btnexit=Button(Btn_Frame,command=self.root.destroy,height=2,text="    Exit   ",font=('arial',15,'bold'),bg="Pink",fg="white")
        self.Btnexit.grid(row=0,column=7)
        self.welcome()
        

        self.l=[]
    #==========================================Calculation==============================================================
    def welcome(self):
            self.textarea.delete(1.0,END)
            self.textarea.insert(END,"\t Welcome To Billing System")
            self.textarea.insert(END,f"\n Bill Number:{self.bill_no.get()}")
            self.textarea.insert(END,f"\n Customer Name:{self.c_name.get()}")
            self.textarea.insert(END,f"\n Phone Number:{self.c_phone.get()}")
            self.textarea.insert(END,f"\n Customer Email:{self.c_email.get()}")
           
            self.textarea.insert(END,"\n ==========================================")
            self.textarea.insert(END,f"\n Products\t\tQty\t\tPrice")
            self.textarea.insert(END,"\n ==========================================\n")

    def AddItem(self):
            Tax=1
            self.n=self.prices.get()
            self.m=self.qty.get()*self.n
            self.l.append(self.m)
            if self.product.get()=="":
                messagebox.showerror("Error","Please Select the Product Name.")
            else:
                self.textarea.insert(END,f"\n {self.product.get()}\t\t{self.qty.get()}\t\t{self.m}")
                self.sub_total.set(str('Rs.%.2f'%(sum(self.l))))
                self.tax_input.set(str('Rs.%.2f'%((((sum(self.l))-(self.prices.get()))*Tax)/100)))
                self.total.set(str('Rs.%.2f'%(((sum(self.l))+((((sum(self.l))-(self.prices.get()))*Tax)/100))))) 

    def gen_bill(self):
            if self.product.get()=="":
                messagebox.showerror("Error","Please Add to Cart Product.")
            else:
                text=self.textarea.get(10.0,(10.0+float(len(self.l))))
                self.welcome()
                self.textarea.insert(END,text)
                self.textarea.insert(END,"\n ==========================================")
                self.textarea.insert(END,f"\n Sub Amount:\t\t{self.sub_total.get()}")
                self.textarea.insert(END,f"\n Tax Amount:\t\t{self.tax_input.get()}")
                self.textarea.insert(END,f"\n Total Amount:\t\t{self.total.get()}")
                self.textarea.insert(END,"\n ==========================================")

    def save_bill(self):
        op=messagebox.askyesno("Save Bill","Do you want to save the bill")
        if op>0:
            self.bill_data=self.textarea.get(1.0,END)
            f1=open('bills/'+str(self.bill_no.get())+".txt",'w')
            f1.write(self.bill_data)
            op=messagebox.showinfo("Saved",f"Bill no.:{self.bill_no.get()} saved successfully.")
            f1.close()

    def iprint(self):
        q=self.textarea.get(1.0,"end-1c")
        filename=tempfile.mktemp('.txt')
        open(filename,'w').write(q)
        os.startfile(filename,"print")

    def find_bill(self):
        found="no"
        for i in os.listdir("bills/"):
            if i.split('.')[0]==self.search_bill.get():
                f1=open(f'bills/{i}','r')
                self.textarea.delete(1.0,END)
                for d in f1:
                    self.textarea.insert(END,d)
                f1.close()
                found="yes"
            if found=="no":
                messagebox.showerror("Error","Invalid Bill Number")

    def update(self): 
        conn=mysql.connector.connect(host="localhost",username="root",password="kaka#@12",database="billing")
        my_cursor=conn.cursor()
        my_cursor.execute("insert into bills values(%s,%s,%s,%s,%s,%s,%s)",(self.bill_no.get(),
                                                            self.c_name.get(),
                                                            self.c_phone.get(),
                                                            self.c_email.get(),
                                                            self.sub_total.get(),
                                                            self.tax_input.get(),
                                                            self.total.get()
                                                            ))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success","Data has been inserted successfully")

    def delete(self):
        if self.search_bill.get()=="":
            messagebox.showerror("Error","Please Enter the Bill No.")
        else:
            conn=mysql.connector.connect(host="localhost",username="root",password="kaka#@12",database="billing")
            my_cursor=conn.cursor()
            query="delete from bills where Bill_No.%s"
            value=(self.search_bill.get(),)
            my_cursor.execute(query,value)

            conn.commit()
            self.clear()
            conn.close()

            messagebox.showinfo("Success","Data has been deleted successfully")

    def clear(self):
        self.textarea.delete(1.0,END)
        self.c_name.set("")
        self.c_phone.set("")
        self.c_email.set("")
        z=random.randint(10000,99999)
        self.bill_no.set(str(z))
        self.search_bill.set("")
        self.product.set("")
        self.prices.set("")
        self.qty.set("")
        self.l=[0]
        self.sub_total.set("")
        self.tax_input.set("")
        self.total.set("")
        self.welcome()

    def Categories(self,event=""):
        if self.Combo_Category.get()=="Clothing":
            self.Combo_subcategory.config(value=self.SubcategoryClothing)
            self.Combo_subcategory.current(0)
        
        if self.Combo_Category.get()=="Households":
            self.Combo_subcategory.config(value=self.SubcategoryHouseholds)
            self.Combo_subcategory.current(0)

        if self.Combo_Category.get()=="Mobiles":
            self.Combo_subcategory.config(value=self.SubcategoryMobiles)
            self.Combo_subcategory.current(0)

        if self.Combo_Category.get()=="Electronics":
            self.Combo_subcategory.config(value=self.SubcategoryElectronics)
            self.Combo_subcategory.current(0)

    def Product_name(self,event=""):
        if self.Combo_subcategory.get()=="Pant":
            self.Combo_prname.config(value=self.pant)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="T-shirt":
            self.Combo_prname.config(value=self.Tshirt)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="Shirt":
            self.Combo_prname.config(value=self.Shirt)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="Jeans":
            self.Combo_prname.config(value=self.Jeans)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="Jacket":
            self.Combo_prname.config(value=self.Jacket)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="Undergarments":
            self.Combo_prname.config(value=self.Undergarments)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="Suit":
            self.Combo_prname.config(value=self.Suit)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="Kurta":
            self.Combo_prname.config(value=self.Kurta)
            self.Combo_prname.current(0)

        #Electronics
        if self.Combo_subcategory.get()=="TV":
            self.Combo_prname.config(value=self.TV)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="Radio":
            self.Combo_prname.config(value=self.Radio)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="Washing Machine":
            self.Combo_prname.config(value=self.WashingMachine)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="Freezer":
            self.Combo_prname.config(value=self.Freezer)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="Earphones":
            self.Combo_prname.config(value=self.Earphones)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="Trimmer":
            self.Combo_prname.config(value=self.Trimmmer)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="Tubelight":
            self.Combo_prname.config(value=self.Tubelight)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="Bulb":
            self.Combo_prname.config(value=self.Bulb)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="Monitor":
            self.Combo_prname.config(value=self.Monitor)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="Mouse":
            self.Combo_prname.config(value=self.Mouse)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="Keyboard":
            self.Combo_prname.config(value=self.Keyboard)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="Printer":
            self.Combo_prname.config(value=self.Printer)
            self.Combo_prname.current(0) 

        if self.Combo_subcategory.get()=="Gyser":
            self.Combo_prname.config(value=self.Gyser)
            self.Combo_prname.current(0)   

        #Lifestyle
        if self.Combo_subcategory.get()=="Kitchen item":
            self.Combo_prname.config(value=self.Kitchenitem)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="Cleaning item":
            self.Combo_prname.config(value=self.Cleaningitem)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="kids item":
            self.Combo_prname.config(value=self.kidsitem)
            self.Combo_prname.current(0)

        #Mobiles
        if self.Combo_subcategory.get()=="Iphone":
            self.Combo_prname.config(value=self.Iphone)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="Xiaomi":
            self.Combo_prname.config(value=self.Xiaomi)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="oneplus":
            self.Combo_prname.config(value=self.oneplus)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="Samsung":
            self.Combo_prname.config(value=self.Samsung)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="Realme":
            self.Combo_prname.config(value=self.Realme)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="Vivo":
            self.Combo_prname.config(value=self.Vivo)
            self.Combo_prname.current(0)

        if self.Combo_subcategory.get()=="Oppo":
            self.Combo_prname.config(value=self.Oppo)
            self.Combo_prname.current(0)

    def Price(self,event=""):
        if self.Combo_prname.get()=="Levis":
            self.Combo_price.config(value=self.price_Levis)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Mufti":
            self.Combo_price.config(value=self.price_Mufti)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Spykar":
            self.Combo_price.config(value=self.price_Spykar)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Polo":
            self.Combo_price.config(value=self.price_Polo)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Roadster":
            self.Combo_price.config(value=self.price_Levis)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Jack & Jones":
            self.Combo_price.config(value=self.price_JackandJones)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Tommy Hilfiger":
            self.Combo_price.config(value=self.price_TommyHilfiger)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Peter England":
            self.Combo_price.config(value=self.price_PeterEngland)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Allen Solly Shirt":
            self.Combo_price.config(value=self.price_AllenSollyShirt)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Levis Jeans":
            self.Combo_price.config(value=self.price_LevisJeans)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Wrangler":
            self.Combo_price.config(value=self.price_Wrangler)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Lee":
            self.Combo_price.config(value=self.price_Lee)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Denim":
            self.Combo_price.config(value=self.price_Denim)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Allen Solly":
            self.Combo_price.config(value=self.price_AllenSolly)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Roadster Jacket":
            self.Combo_price.config(value=self.price_RoadsterJacket)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Calvein":
            self.Combo_price.config(value=self.price_Calvein)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Rupa":
            self.Combo_price.config(value=self.price_Rupa)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="LUX":
            self.Combo_price.config(value=self.price_LUX)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Emporio Armani":
            self.Combo_price.config(value=self.price_EmporioArmani)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Blackberry":
            self.Combo_price.config(value=self.price_Blackberry)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Bunaai":
            self.Combo_price.config(value=self.price_Bunaai)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Manyavar":
            self.Combo_price.config(value=self.price_Manyavar)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Jompers":
            self.Combo_price.config(value=self.price_Jompers)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Sojanya":
            self.Combo_price.config(value=self.price_Sojanya)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Signature":
            self.Combo_price.config(value=self.price_Signature)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Black Magic":
            self.Combo_price.config(value=self.price_BlackMagic)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="HUESLAND":
            self.Combo_price.config(value=self.price_HUESLAND)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Oil":
            self.Combo_price.config(value=self.price_Oil)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Salt":
            self.Combo_price.config(value=self.price_Salt)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Milk":
            self.Combo_price.config(value=self.price_Milk)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Mustard":
            self.Combo_price.config(value=self.price_Mustard)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Rice":
            self.Combo_price.config(value=self.price_Rice)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Dal":
            self.Combo_price.config(value=self.price_Dal)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Vinegar":
            self.Combo_price.config(value=self.price_Vinegar)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Lavang":
            self.Combo_price.config(value=self.price_Lavang)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Jeera":
            self.Combo_price.config(value=self.price_Jeera)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Curd":
            self.Combo_price.config(value=self.price_Curd)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Peppercorn":
            self.Combo_price.config(value=self.price_Peppercorn)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Saffron":
            self.Combo_price.config(value=self.price_Saffron)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Sugar":
            self.Combo_price.config(value=self.price_Sugar)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Beans":
            self.Combo_price.config(value=self.price_Beans)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Butter":
            self.Combo_price.config(value=self.price_Butter)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Sauces":
            self.Combo_price.config(value=self.price_Sauces)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Vegetables":
            self.Combo_price.config(value=self.price_Vegetables)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Fruit":
            self.Combo_price.config(value=self.price_Fruit)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Flour":
            self.Combo_price.config(value=self.price_Flour)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Cashew":
            self.Combo_price.config(value=self.price_Cashew)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Tea leaf":
            self.Combo_price.config(value=self.price_Tealeaf)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Spices":
            self.Combo_price.config(value=self.price_Spices)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Aluminum foil":
            self.Combo_price.config(value=self.price_Aluminumfoil)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Pots & pans":
            self.Combo_price.config(value=self.price_Potsandpans)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Utensils":
            self.Combo_price.config(value=self.price_Utensils)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Wheat":
            self.Combo_price.config(value=self.price_Wheat)
            self.Combo_price.current(0)    
            self.qty.set(1)
        
        if self.Combo_prname.get()=="MatchStick":
            self.Combo_price.config(value=self.price_MatchStick)
            self.Combo_price.current(0)    
            self.qty.set(1)
        
        if self.Combo_prname.get()=="Turmeric Powder":
            self.Combo_price.config(value=self.price_TurmericPowder)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Bath wash":
            self.Combo_price.config(value=self.price_Bathwash)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Face wash":
            self.Combo_price.config(value=self.price_Facewash)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Surf":
            self.Combo_price.config(value=self.price_Surf)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Soap":
            self.Combo_price.config(value=self.price_Soap)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Toilet Cleaner":
            self.Combo_price.config(value=self.price_ToiletCleaner)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Tooth paste":
            self.Combo_price.config(value=self.price_Toothpaste)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Chocolate":
            self.Combo_price.config(value=self.price_Chocolate)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="IceCream":
            self.Combo_price.config(value=self.price_IceCream)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Pepsi":
            self.Combo_price.config(value=self.price_Pepsi)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Chips":
            self.Combo_price.config(value=self.price_Chips)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Toffee":
            self.Combo_price.config(value=self.price_Toffee)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Maggie":
            self.Combo_price.config(value=self.price_Maggie)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Cake":
            self.Combo_price.config(value=self.price_Cake)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Popcorn":
            self.Combo_price.config(value=self.price_Popcorn)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Oatmeal":
            self.Combo_price.config(value=self.price_Oatmeal)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Olives":
            self.Combo_price.config(value=self.price_Olives)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Bread":
            self.Combo_price.config(value=self.price_Bread)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Nuts":
            self.Combo_price.config(value=self.price_Nuts)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Ketchup":
            self.Combo_price.config(value=self.price_Ketchup)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Biscuits":
            self.Combo_price.config(value=self.price_Biscuits)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Namkeen":
            self.Combo_price.config(value=self.price_Namkeen)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Iphone 11":
            self.Combo_price.config(value=self.price_Iphone11)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Iphone 12":
            self.Combo_price.config(value=self.price_Iphone12)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Iphone 12 mini":
            self.Combo_price.config(value=self.price_Iphone12mini)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Iphone 12 pro":
            self.Combo_price.config(value=self.price_Iphone12pro)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Iphone 13":
            self.Combo_price.config(value=self.price_Iphone13)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Iphone 13 mini":
            self.Combo_price.config(value=self.price_Iphone13mini)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Iphone 13 pro":
            self.Combo_price.config(value=self.price_Iphone13pro)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Iphone SE":
            self.Combo_price.config(value=self.price_IphoneSE)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Iphone X":
            self.Combo_price.config(value=self.price_IphoneX)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Mi 10i":
            self.Combo_price.config(value=self.price_Mi10i)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Mi 10 Lite":
            self.Combo_price.config(value=self.price_Mi10Lite)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Mi 10 Pro":
            self.Combo_price.config(value=self.price_Mi10Pro)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Mi 10S":
            self.Combo_price.config(value=self.price_Mi10S)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Mi 11 Pro":
            self.Combo_price.config(value=self.price_Mi11Pro)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Mi 11 ultra 5g":
            self.Combo_price.config(value=self.price_Mi11ultra5g)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Mi 5X":
            self.Combo_price.config(value=self.price_Mi5X)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Mi 6":
            self.Combo_price.config(value=self.price_Mi6)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="oneplus 7 Series":
            self.Combo_price.config(value=self.price_oneplus7Series)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="oneplus 7T Pro":
            self.Combo_price.config(value=self.price_oneplus7TPro)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="oneplus 8T":
            self.Combo_price.config(value=self.price_oneplus8T)
            self.Combo_price.current(0)    
            self.qty.set(1)
        
        if self.Combo_prname.get()=="oneplus 9 Series":
            self.Combo_price.config(value=self.price_oneplus9Series)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="oneplus Nord":
            self.Combo_price.config(value=self.price_oneplusNord)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="oneplus Nord 2 5G":
            self.Combo_price.config(value=self.price_oneplusNord25G)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="oneplus Nord CE 5G":
            self.Combo_price.config(value=self.price_oneplusNordCE5G)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="oneplus Nord N10 5G":
            self.Combo_price.config(value=self.price_oneplusNordN105G)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Samsung A11":
            self.Combo_price.config(value=self.price_SamsungA11)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Samsung A31":
            self.Combo_price.config(value=self.price_SamsungA31)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Samsung A41":
            self.Combo_price.config(value=self.price_SamsungA41)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Samsung M21":
            self.Combo_price.config(value=self.price_SamsungM21)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Samsung M31":
            self.Combo_price.config(value=self.price_SamsungM31)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Samsung S20 ultra":
            self.Combo_price.config(value=self.price_SamsungS20ultra)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Samsung S20 ultra 5G":
            self.Combo_price.config(value=self.price_SamsungS20ultra5g)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Realme 8s":
            self.Combo_price.config(value=self.price_Realme8s)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Realme 8i":
            self.Combo_price.config(value=self.price_Realme8i)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Realme 8":
            self.Combo_price.config(value=self.price_Realme8)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Realme 7":
            self.Combo_price.config(value=self.price_Realme7)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Realme C20":
            self.Combo_price.config(value=self.price_RealmeC20)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Realme GT Neo 2":
            self.Combo_price.config(value=self.price_RealmeGTNeo2)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Realme Narzo 30 Pro":
            self.Combo_price.config(value=self.price_RealmeNarzo30Pro)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Realme Narzo 50A":
            self.Combo_price.config(value=self.price_RealmeNarzo50A)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Realme X7":
            self.Combo_price.config(value=self.price_RealmeX7)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Vivo Y3S":
            self.Combo_price.config(value=self.price_VivoY3S)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Vivo V20G":
            self.Combo_price.config(value=self.price_VivoV20G)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Vivo V20":
            self.Combo_price.config(value=self.price_VivoV20)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Vivo X60":
            self.Combo_price.config(value=self.price_VivoX60)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Vivo X70 Pro":
            self.Combo_price.config(value=self.price_VivoX70Pro)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Vivo X70 Pro Plus":
            self.Combo_price.config(value=self.price_VivoX70ProPlus)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Vivo Y20":
            self.Combo_price.config(value=self.price_VivoY20)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Vivo Y21":
            self.Combo_price.config(value=self.price_VivoY21)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Vivo Y3S":
            self.Combo_price.config(value=self.price_VivoY3S)
            self.Combo_price.current(0)    
            self.qty.set(1)
        
        if self.Combo_prname.get()=="Oppo A53s":
            self.Combo_price.config(value=self.price_OppoA53s)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Oppo A54":
            self.Combo_price.config(value=self.price_OppoA54)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Oppo A74":
            self.Combo_price.config(value=self.price_OppoA74)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Oppo F19 Pro":
            self.Combo_price.config(value=self.price_OppoF19Pro)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Oppo F19 Pro plus":
            self.Combo_price.config(value=self.price_OppoF19Proplus)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Oppo F19s":
            self.Combo_price.config(value=self.price_OppoF19s)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Oppo F19 Pro":
            self.Combo_price.config(value=self.price_OppoF19Pro)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Oppo Reno 3 Pro":
            self.Combo_price.config(value=self.price_OppoReno3Pro)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Oppo Reno 6":
            self.Combo_price.config(value=self.price_OppoReno6)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Oppo Reno 6 Pro":
            self.Combo_price.config(value=self.price_OppoReno6Pro)
            self.Combo_price.current(0)    
            self.qty.set(1)
        
        if self.Combo_prname.get()=="Sony":
            self.Combo_price.config(value=self.price_Sony)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="LG":
            self.Combo_price.config(value=self.price_LG)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Samsung":
            self.Combo_price.config(value=self.price_Samsung)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Mi":
            self.Combo_price.config(value=self.price_Mi)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Videocon":
            self.Combo_price.config(value=self.price_Videocon)
            self.Combo_price.current(0)    
            self.qty.set(1)
        
        if self.Combo_prname.get()=="Revo Radio":
            self.Combo_price.config(value=self.price_RevoRadio)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Ruark Audio":
            self.Combo_price.config(value=self.price_RuarkAudio)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="VQ":
            self.Combo_price.config(value=self.price_VQ)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Philips Radio":
            self.Combo_price.config(value=self.price_PhilipsRadio)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="iBELL FM":
            self.Combo_price.config(value=self.price_iBELLFM)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Panasonic Radio":
            self.Combo_price.config(value=self.price_PanasonicRadio)
            self.Combo_price.current(0)    
            self.qty.set(1)
        
        if self.Combo_prname.get()=="Whirlpool":
            self.Combo_price.config(value=self.price_Whirlpool)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="LG Washing Machine":
            self.Combo_price.config(value=self.price_LGWashingMachine)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Samsung Washing Machine":
            self.Combo_price.config(value=self.price_SamsungWashingMachine)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Bosch":
            self.Combo_price.config(value=self.price_Bosch)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Haier":
            self.Combo_price.config(value=self.price_Haier)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="LG Freezer":
            self.Combo_price.config(value=self.price_LGFreezer)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Bosch Freezer":
            self.Combo_price.config(value=self.price_BoschFreezer)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Summit":
            self.Combo_price.config(value=self.price_Summit)
            self.Combo_price.current(0)    
            self.qty.set(1)
        
        if self.Combo_prname.get()=="Boat":
            self.Combo_price.config(value=self.price_Boat)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Apple":
            self.Combo_price.config(value=self.price_Apple)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Samsung Galaxy":
            self.Combo_price.config(value=self.price_SamsungGalaxy)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="JBL":
            self.Combo_price.config(value=self.price_JBL)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Sony WI":
            self.Combo_price.config(value=self.price_SonyWI)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Realme Buds":
            self.Combo_price.config(value=self.price_RealmeBuds)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Boat Rockerz":
            self.Combo_price.config(value=self.price_BoatRockerz)
            self.Combo_price.current(0)    
            self.qty.set(1)
       
        if self.Combo_prname.get()=="One Plus blast":
            self.Combo_price.config(value=self.price_OnePlusblast)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Boat Airdopes":
            self.Combo_price.config(value=self.price_BoatAirdopes)
            self.Combo_price.current(0)    
            self.qty.set(1)
        
        if self.Combo_prname.get()=="Havelles":
            self.Combo_price.config(value=self.price_Havelles)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Phillips Beared trimmer series":
            self.Combo_price.config(value=self.price_PhillipsBearedtrimmerseries)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Goldtech":
            self.Combo_price.config(value=self.price_Goldtech)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Syska":
            self.Combo_price.config(value=self.price_Syska)
            self.Combo_price.current(0)    
            self.qty.set(1)
        
        if self.Combo_prname.get()=="Everready":
            self.Combo_price.config(value=self.price_Everready)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Sony Tubelight":
            self.Combo_price.config(value=self.price_SonyTubelight)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="LG Tubelight":
            self.Combo_price.config(value=self.price_LGTubelight)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Crompton":
            self.Combo_price.config(value=self.price_Crompton)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="HALCO":
            self.Combo_price.config(value=self.price_HALCO)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Phillips Tubelight":
            self.Combo_price.config(value=self.price_PhillipsTubelight)
            self.Combo_price.current(0)    
            self.qty.set(1)
        
        if self.Combo_prname.get()=="Everready Bulb":
            self.Combo_price.config(value=self.price_EverreadyBulb)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Sony Bulb":
            self.Combo_price.config(value=self.price_SonyBulb)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="LG Bulb":
            self.Combo_price.config(value=self.price_LGBulb)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Crompton Bulb":
            self.Combo_price.config(value=self.price_CromptonBulb)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="HALCO Bulb":
            self.Combo_price.config(value=self.price_HALCOBulb)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Phillips Bulb":
            self.Combo_price.config(value=self.price_PhillipsBulb)
            self.Combo_price.current(0)    
            self.qty.set(1)
        
        if self.Combo_prname.get()=="HP":
            self.Combo_price.config(value=self.price_HP)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="DELL":
            self.Combo_price.config(value=self.price_DELL)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Acer":
            self.Combo_price.config(value=self.price_Acer)
            self.Combo_price.current(0)    
            self.qty.set(1)
        
        if self.Combo_prname.get()=="Asus":
            self.Combo_price.config(value=self.price_Asus)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Lenovo":
            self.Combo_price.config(value=self.price_Lenovo)
            self.Combo_price.current(0)    
            self.qty.set(1)
       
        if self.Combo_prname.get()=="Apple Monitor":
            self.Combo_price.config(value=self.price_AppleMonitor)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="LG Monitor":
            self.Combo_price.config(value=self.price_LGMonitor)
            self.Combo_price.current(0)    
            self.qty.set(1)
        
        if self.Combo_prname.get()=="Samsung Monitor":
            self.Combo_price.config(value=self.price_SamsungMonitor)
            self.Combo_price.current(0)    
            self.qty.set(1)
        
        if self.Combo_prname.get()=="HP Mouse":
            self.Combo_price.config(value=self.price_HPMouse)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Dell Mouse":
            self.Combo_price.config(value=self.price_DellMouse)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Acer Mouse":
            self.Combo_price.config(value=self.price_AcerMouse)
            self.Combo_price.current(0)    
            self.qty.set(1)
        
        if self.Combo_prname.get()=="Asus Mouse":
            self.Combo_price.config(value=self.price_AsusMouse)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Lenovo Mouse":
            self.Combo_price.config(value=self.price_LenovoMouse)
            self.Combo_price.current(0)    
            self.qty.set(1)
        
        if self.Combo_prname.get()=="HP Keyboard":
            self.Combo_price.config(value=self.price_HPKeyboard)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Dell  Keyboard":
            self.Combo_price.config(value=self.price_DellKeyboard)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Acer Keyboard":
            self.Combo_price.config(value=self.price_AcerKeyboard)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Asus Keyboard":
            self.Combo_price.config(value=self.price_AsusKeyboard)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Lenovo Keyboard":
            self.Combo_price.config(value=self.price_LenovoKeyboard)
            self.Combo_price.current(0)    
            self.qty.set(1)
   
        if self.Combo_prname.get()=="HP Printer":
            self.Combo_price.config(value=self.price_HPPrinter)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Dell Printer":
            self.Combo_price.config(value=self.price_DellPrinter)
            self.Combo_price.current(0)    
            self.qty.set(1)
        
        if self.Combo_prname.get()=="Acer Printer":
            self.Combo_price.config(value=self.price_AcerPrinter)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Asus Printer":
            self.Combo_price.config(value=self.price_AsusPrinter)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Lenovo Printer":
            self.Combo_price.config(value=self.price_LenovoPrinter)
            self.Combo_price.current(0)    
            self.qty.set(1)
        
        if self.Combo_prname.get()=="Bajaj":
            self.Combo_price.config(value=self.price_Bajaj)
            self.Combo_price.current(0)    
            self.qty.set(1)
        
        if self.Combo_prname.get()=="Venus":
            self.Combo_price.config(value=self.price_Venus)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Usha":
            self.Combo_price.config(value=self.price_Usha)
            self.Combo_price.current(0)    
            self.qty.set(1)

        if self.Combo_prname.get()=="Morphy Richards":
            self.Combo_price.config(value=self.price_MorphyRichards)
            self.Combo_price.current(0)    
            self.qty.set(1)

if __name__ == '__main__':
    main()