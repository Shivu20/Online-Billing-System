from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk   #pip install pillow
from tkinter import messagebox
import mysql.connector

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

        password_entry=ttk.Entry(frame,textvariable=self.var_password,font=("times new roman",15,"bold"))
        password_entry.place(x=30,y=320,width=200)

        conpass=Label(frame,text="Confirm Password",font=("times new roman",15,"bold"),fg="black",bg="white")
        conpass.place(x=310,y=290)

        conpass_entry=ttk.Entry(frame,textvariable=self.var_conpass,font=("times new roman",15,"bold"))
        conpass_entry.place(x=310,y=320,width=200)

        #============================Check====================================================
        checkbtn=Checkbutton(frame,variable=self.var_check,text="I agree to the terms and condition.",font=("times new roman",15,"bold"),onvalue=1,offvalue=0)
        checkbtn.place(x=30,y=360)

        #=========================BUTTONS=====================================================
        img1=Image.open("image/register.jpg")
        img1=img1.resize((180,44),Image.ANTIALIAS)
        self.photoimg1=ImageTk.PhotoImage(img1)
        b1=Button(frame,image=self.photoimg1,command=self.register_data,borderwidth=0,cursor="hand2",font=("times new roman",15,"bold"))
        b1.place(x=30,y=410,width=180)

        img2=Image.open("image/logini.jpg")
        img2=img2.resize((180,44),Image.ANTIALIAS)
        self.photoimg2=ImageTk.PhotoImage(img2)
        b1=Button(frame,image=self.photoimg2,borderwidth=0,cursor="hand2",font=("times new roman",15,"bold"))
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

    














if __name__ == '__main__':
    root=Tk()
    app=Register_window(root)
    root.mainloop()