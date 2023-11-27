import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # pip install pillow
from tkinter.filedialog import askopenfilename
import re
import mysql.connector
import tkinter
import cv2



class FirstPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("bg_image.jpg")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image = photo
        label.place(x=0, y=0)

        border = tk.LabelFrame(self , bg='aqua', font=("verdana", 25,'italic bold underline'))
        border.pack(fill="both", expand="yes", padx=250, pady=250)

        L1 = tk.Label(border, text="Username", font=("verdana", 15), bg='aqua')
        L1.place(x=50, y=20)
        T1 = tk.Entry(border, width=35,bd=5)
        T1.place(x=200, y=20)

        L2 = tk.Label(border, text="Password", font=("verdana", 15), bg='aqua')
        L2.place(x=50, y=80)
        T2 = tk.Entry(border, width=35, show='*', bd=5)
        T2.place(x=200, y=80)

        L3 = tk.Label(border, text="MAKE SURE TO KEEP YOUR DATASET READY", font=("verdana",20), bg='orange')
        L3.place(x=50,y=150)

        def verify():
            '''
            try:
                with open("credential.txt", "r") as f:
                    info = f.readlines()
                    i  = 0
                    for e in info:
                        u, p =e.split(",")
                        if u.strip() == T1.get() and p.strip() == T2.get():
                            controller.show_frame(ThirdPage)
                            i = 1
                            break
                    if i==0:
                        messagebox.showinfo("Error", "Please provide correct username and password!!")
            except:
                messagebox.showinfo("Error", "Please provide correct username and password!!")
            '''
            try:
                # database connect
                mydb = mysql.connector.connect(host="localhost", user="root", passwd="root",
                                               database="brainproject")
                mycursor = mydb.cursor()

                sql = "SELECT * FROM registration WHERE username = %s and password = %s"
                val = (T1.get(), T2.get())
                mycursor.execute(sql, val)
                result = mycursor.fetchone()

                if result:
                    stored_password = result[2]
                    if T2.get() == stored_password:
                        messagebox.showinfo("Success", "Login successfull!")
                        controller.show_frame(ThirdPage)
                        # 1b1_result.config(text="login successfull!", fg="green")
                    else:
                        messagebox.showerror("Invalid password!")
                else:
                    messagebox.showerror("Error", "Invalid username or password")

                mycursor.close()
                mydb.close()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Database error: {err}")

        B1 = tk.Button(border, text="LOGIN", font=("verdana", 20,'bold underline'), bg='dark orange', command=verify)
        B1.place(x=250, y=230)

        def on_enter(e):
            B1['background'] = 'orange'

        def on_leave(e):
            B1['background'] = 'dark orange'

        B1.bind("<Enter>", on_enter)
        B1.bind("<Leave>", on_leave)

        def register():
            window = tk.Tk()
            window.resizable(50, 100)
            window.configure(bg="aqua")
            window.title("Register")

            l = tk.Label(window, text="Welcome Kindly Register", font=("verdana",25,'italic bold underline'), bg="dark orange")
            l.place(x=120,y=20)
            l1 = tk.Label(window, text="Username:", font=("verdana", 15), bg="aqua")
            l1.place(x=350, y=80)
            t1 = tk.Entry(window, width=30, bd=5)
            t1.place(x=650, y=80)
            t1.insert(tkinter.END, "enter your name")
            t1.bind("<Button-1>",lambda event: t1.delete(0,tkinter.END))

            l2 = tk.Label(window, text="Password:", font=("verdana", 15), bg="aqua")
            l2.place(x=350, y=150)
            t2 = tk.Entry(window, width=30, show="*", bd=5)
            t2.place(x=650, y=150)


            l3 = tk.Label(window, text="Re-enter pass:", font=("verdana", 15), bg="aqua")
            l3.place(x=350, y=230)
            t3 = tk.Entry(window, width=30, show="*", bd=5)
            t3.place(x=650, y=230)

            l4 = tk.Label(window, text="Identification number:", font=("verdana", 15), bg="aqua")
            l4.place(x=350, y=310)
            t4 = tk.Entry(window, width=30, bd=5)
            t4.place(x=650, y=310)


            def validate_password(password):
                if len(password) < 8:
                    return False
                if not re.search("[a-z]", password):
                    return False
                if not re.search("[A-Z]", password):
                    return False
                if not re.search("[0-9]", password):
                    return False
                if not re.search("[@$!%*#?&]", password):
                    return False
                return True

            def check():

                '''
                if not t1 or not t2 or not t3:
                   messagebox.showerror("ERROR","Please fill in all fields,")
                   return

                elif t2 != t3:
                   messagebox.showerror("ERROR","Password is not matching,")
                   return

                elif not validate_password(t2):
                  messagebox.showerror("Error","the password must contain with numbers,Alphabet and special charecters.")
                  return

                elif any (char.isdigit() for char in t1):
                  messagebox.showerror("Error","username cannot be numeric")
                  return

                #if email present , it should not be accessed it should print message  its already exits
                else:
                   # messagebox.showinfo("success","Registeration successfull!")
              #perform database operation
                    try:
                        #database connection
                        mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="dbforcovid")
                        mycursor = mydb.cursor()

                        #insert the registration data into database
                        sql = "INSERT INTO registration(username ,email_id  ,password,confirm_pass) VALUES (%s, %s, %s, %s)"
                        val = (t1,t2,t3)
                        mycursor.execute(sql,val)
                        # mycursor.execute("CREATE TABLE  registration("
                        #                  "username VARCHAR(200) NOT NULL,"
                        #                  "email_id VARCHAR(200) PRIMARY KEY,"
                        #                  "password VARCHAR(200) NOT NULL,"
                        #                  "confirm_pass VARCHAR(200) NOT NULL"
                        #                  ")")
                        mydb.commit()

                        messagebox.showinfo("success", "Registration successfull.")

                        #clear the entry fields
                        t1.delete(0, tk.END)
                        t2.delete(0, tk.END)
                        t3.delete(0, tk.END)

                    except mysql.connector.Error as err:
                         messagebox.showerror("Error",f"Database error: {err}")
                '''
                if t1.get() != "" and t2.get() != "" and t3.get() != "" and t4.get() != "":
                    if validate_password(t2.get()) and t2.get() == t3.get():
                        try:
                            # database connection
                            mydb = mysql.connector.connect(host="localhost", user="root", passwd="root",
                                                           database="brainproject")
                            mycursor = mydb.cursor()

                            # insert the registration data into database
                            sql = "INSERT INTO registration(username,password,confirm_pass,identity_no) VALUES (%s, %s, %s, %s)"
                            val = (str(t1.get()), str(t2.get()), str(t3.get()), str(t4.get()))
                            mycursor.execute(sql, val)
                            # mycursor.execute("CREATE TABLE  registration("
                            #                  "username VARCHAR(200) NOT NULL,"
                            #                  "email_id VARCHAR(200) PRIMARY KEY,"
                            #                  "password VARCHAR(200) NOT NULL,"
                            #                  "confirm_pass VARCHAR(200) NOT NULL"
                            #                  ")")
                            mydb.commit()

                            messagebox.showinfo("success", "Registration successfull.")

                            # clear the entry fields
                            t1.delete(0, tk.END)
                            t2.delete(0, tk.END)
                            t3.delete(0, tk.END)
                            t4.delete(0,tk.END)

                        except mysql.connector.Error as err:
                            messagebox.showerror("Error", f"Database error: {err}")

                        # messagebox.showinfo("Welcome","You are registered successfully!!")
                    else:
                        messagebox.showinfo("Error", "Your password didn't get match!! or Not a Strong Password")
                else:
                    messagebox.showinfo("log in", "If your already registered provide username and password!!") 



            #          B1 = tk.Button(border, text="Submit", font=("Arial", 20,'italic bold underline'), bg='grey', command=verify)
            #         B1.place(x=250, y=130)
            #
            #         def on_enter(e):
            #             B1['background'] = 'light blue'
            #
            #         def on_leave(e):
            #             B1['background'] = 'grey'
            #
            #         B1.bind("<Enter>", on_enter)
            #         B1.bind("<Leave>", on_leave)


            b1 = tk.Button(window, text="Sign in", font=("verdana", 20, 'bold underline'), bg="dark orange", command=check)
            b1.place(x=650, y=400)

            b2 = tk.Button(window, text="Back", font=("verdana", 20, 'bold underline'), bg="dark orange",
            command = check)
            b2.place(x=300, y=400)



            def on_enter(e):
                b1['background'] = 'orange'

            def on_leave(e):
                b1['background'] = 'dark orange'

            b1.bind("<Enter>", on_enter)
            b1.bind("<Leave>", on_leave)

            def on_enter(e):
                b2['background'] = 'orange'

            def on_leave(e):
                b2['background'] = 'dark orange'

            b2.bind("<Enter>", on_enter)
            b2.bind("<Leave>", on_leave)

            window.geometry("1500x800")
            window.mainloop()

        B2 = tk.Button(self, text="Register", bg="dark orange", font=("verdana", 25,'bold underline'), command=register)
        B2.place(x=50, y=20)


        label = tk.Label(self, text="PLEASE LOGIN", bg="orange", font=("verdana",30,'bold underline'))
        label.place(x=500, y=20)

        def on_enter(e):
            B2['background'] = 'orange'

        def on_leave(e):
            B2['background'] = 'dark orange'

        B2.bind("<Enter>", on_enter)
        B2.bind("<Leave>", on_leave)



class ThirdPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # load = Image.open("brain.png")
        # photo = ImageTk.PhotoImage(load)
        # label = tk.Label(self, image=photo)
        # label.image = photo
        # label.place(x=0, y=0)
        self.configure(bg='aqua')

        # Label = tk.Label(self, text="Store some content related to your \n project or what your application made for. \n All the best!!", bg = "orange", font=("Arial Bold", 25))
        # Label.place(x=40, y=150)
        w2 = tk.Label(self, text="WELCOME TO BRAINMOSAIC", bg="dark orange", fg="black", width=30, height=1,
                      font=('courier new', 30, 'italic bold underline'))
        w2.place(x=250, y=10)

        '''
        l=Button(self,text="Build Training Model", command=self.buildModel, bg="red"  ,fg="white"  ,width=20  ,height=1,font=('times', 20, 'italic bold underline'))
        l.place(x=200,y=200)
        '''
        k = tk.Button(self, text="PROVIDE MRI DATASET", command=self.showImgg, bg="orange", fg="black", width=20,
                      height=1, font=('times', 20, 'italic bold underline'))
        k.place(x=100, y=100)




        b1 = tk.Button(self, text="SHOW RESULT", command=self.Classify, bg="orange", fg="black", width=20,
                      height=1, font=('times', 20, 'italic bold underline'))
        b1.place(x=800, y=100)



        #  Button = tk.Button(self, text="Home", bg="dark orange", font=("Arial", 15),
        #                            command=lambda: controller.show_frame(FirstPage))
        #         Button.place(x=1100, y=50)

        Button = tk.Button(self, text="HOME", bg="dark orange", font=("courier new", 20, 'italic bold underline'),
                           command=lambda: controller.show_frame(FirstPage))
        Button.place(x=950, y=550)

    # Creation of init_window

    def Classify(self):
        print("Classify the Test Image")
        from tensorflow.keras.models import load_model
        model = load_model('brain_model.h5')

        # Compiling the model
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        # (model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy']))
        # Making New Prediction
        import numpy as np
        from tensorflow.keras.preprocessing import image
        from matplotlib import pyplot as plt

        test_image = image.load_img(self.load, target_size=(64, 64, 3))

        # im = Image.open(self.load)
        imgg = cv2.imread(self.load, cv2.IMREAD_GRAYSCALE)
        plt.imsave(r'input.png', imgg)
        img = cv2.imread('input.png')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # ShowImage('Brain MRI',gray,'gray')
        plt.imsave(r'gray.png', gray)

        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
        # ShowImage('Thresholding image',thresh,'gray')
        plt.imsave(r'thresh.png', thresh)
        im0 = Image.open('thresh.png')

        render = ImageTk.PhotoImage(im0)

        # labels can be text or images
        img01 = tkinter.Label(self, image=render, width=250, height=250)
        img01.image = render
        img01.place(x=450, y=200)

        ret, markers = cv2.connectedComponents(thresh)

        # Get the area taken by each component. Ignore label 0 since this is the background.
        marker_area = [np.sum(markers == m) for m in range(np.max(markers)) if m != 0]
        # Get label of largest component by area
        largest_component = np.argmax(marker_area) + 1  # Add 1 since we dropped zero above
        # Get pixels which correspond to the brain
        brain_mask = markers == largest_component

        brain_out = img.copy()
        # In a copy of the original image, clear those pixels that don't correspond to the brain
        brain_out[brain_mask == False] = (0, 0, 0)

        imgg = cv2.imread(self.load, cv2.IMREAD_GRAYSCALE)

        plt.imsave(r'input.png', imgg)
        img = cv2.imread('input.png')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # noise removal
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

        # sure background area
        sure_bg = cv2.dilate(opening, kernel, iterations=3)

        # Finding sure foreground area
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)

        # Marker labelling
        ret, markers = cv2.connectedComponents(sure_fg)

        # Add one to all labels so that sure background is not 0, but 1
        markers = markers + 1

        # Now, mark the region of unknown with zero
        markers[unknown == 255] = 0
        markers = cv2.watershed(img, markers)
        img[markers == -1] = [255, 0, 0]

        im1 = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
        # ShowImage('Watershed segmented image',im1,'gray')
        plt.imsave(r'Watershed.png', im1)

        brain_mask = np.uint8(brain_mask)
        kernel = np.ones((8, 8), np.uint8)
        closing = cv2.morphologyEx(brain_mask, cv2.MORPH_CLOSE, kernel)
        # ShowImage('Closing', closing, 'gray')
        plt.imsave(r'close.png', closing)

        # im2 = cv2.imread('thresh.png', cv2.IMREAD_GRAYSCALE)
        im2 = Image.open('Watershed.png')

        render = ImageTk.PhotoImage(im2)
        # SECOND WATER MARK IMAGE #
        # labels can be text or images
        img1 = tkinter.Label(self, image=render, width=350, height=200)
        img1.image = render
        img1.place(x=30, y=400)
###################################################################################################################
        # im02 = Image.open('close.png')
        #
        # render = ImageTk.PhotoImage(im02)
        #
        # # labels can be text or images
        # img02 = tkinter.Label(self, image=render,width=500,height=300)
        # img02.image = render
        # img02.place(x=400, y=400)
        #
        # plt.figure(figsize=(8,8))
        # plt.imshow(thresh,cmap="gray")
        # plt.axis('off')
        # plt.title("Threshold Image")
        # plt.show()

#################################################################################################################
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = model.predict(test_image)

        print(result)
        print(result[0][0])

        if result[0][0] == 1.0:
            a = "No Tumor Present   "
            print("Classified Output is No Tumor Present")
        elif result[0][1] == 1.0:
            a = "Malignant - 1 stage"
            print("Classified Output is Tumor Present with 1 stage")
        elif result[0][2] == 1.0:
            a = "Malignant - 2 stage"
            print("Classified Output is Tumor Present with 2 stage")
        elif result[0][3] == 1.0:
            a = "Malignant - 3 stage"
            print("Classified Output is Tumor Present with 3 stage")
        else:
            a = "Image             "
            print("Invalid Image")

        s = tkinter.Label(self, text=a, font=("arial", 25))
        s.place(x=900, y=500)

    def showImgg(self):
        self.load = askopenfilename(filetypes=[("Image File", '.jpg .jpeg .png')])

        im = Image.open(self.load)
        im = im.resize((300, 150))
        render = ImageTk.PhotoImage(im)

        # labels can be text or images
        img = tkinter.Label(self, image=render, width=250, height=150)
        img.image = render
        img.place(x=50, y=200)


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a window
        window = tk.Frame(self)
        window.pack()

        window.grid_rowconfigure(0, minsize=800)
        window.grid_columnconfigure(0, minsize=1300)

        self.frames = {}
        for F in (FirstPage, ThirdPage):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(FirstPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("Application")


app = Application()
app.maxsize(1300, 800)
app.mainloop()
