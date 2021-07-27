from Detector import main_app
from create_classifier import train_classifer
from create_dataset import start_capture
import tkinter as tk
from tkinter import font as tkf
from tkinter import messagebox, PhotoImage

names = set()


class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        with open("Detected Names/nameslist.txt", "r") as f:
            x = f.read()
            z = x.rstrip().split(" ")
            for i in z:
                names.add(i)
        self.title_font = tkf.Font(family='Helvetica', size=19, weight="bold")
        self.title("Face Recognition by 6th Sem")
        self.resizable(False, False)
        self.geometry("700x360")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        container = tk.Frame(self)
        container.grid(sticky="")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def on_closing(self):

        # if messagebox.askokcancel("Quit", "Are you sure?"):
        #     global names
        #     f = open("nameslist.txt", "a+")
        #     for i in names:
        #         f.write(i + " ")
        self.destroy()

    # Making first page User Interface


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        render = PhotoImage(file='files/homepagepic.png')
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=1, column=0, rowspan=2, sticky="nsew")
        render1 = PhotoImage(file='files/cosmos.png')
        img1 = tk.Label(self, image=render1)
        img1.image = render1
        img1.grid(row=1, column=1, rowspan=2, sticky="nsew")
        render2 = PhotoImage(file='files/homepagepic.png')
        img2 = tk.Label(self, image=render2)
        img2.image = render2
        img2.grid(row=1, column=2, rowspan=2, sticky="nsew")
        label1 = tk.Label(self, text="Face Recognition System", font=self.controller.title_font, fg="#263942")
        label1.grid(row=0, columnspan=6, sticky="ew")
        # line1= canvas.create_line(15, 25, 200, 25)
        button1 = tk.Button(self, text="   Register a new User  ", fg="#ffffff", bg="#263942",
                            command=lambda: self.controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="   Check existing User  ", fg="#ffffff", bg="#263942",
                            command=lambda: self.controller.show_frame("PageTwo"))
        button3 = tk.Button(self, text="         Quit         ", fg="#ffffff", bg="red", command=self.on_closing)
        button1.grid(row=5, column=0, ipady=3, ipadx=7)
        button2.grid(row=5, column=1, ipady=3, ipadx=7)
        button3.grid(row=5, column=2, ipady=3, ipadx=32)

    def on_closing(self):
        # if messagebox.askokcancel("Quit", "Are you sure?"):
        #     global names
        #     with open("nameslist.txt", "w") as f:
        #         for i in names:
        #             f.write(i + " ")
        self.controller.destroy()

    # Making register page of user


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label1 = tk.Label(self, text="Face Recognition System", font=self.controller.title_font, fg="#263942")
        label1.grid(row=0, columnspan=8, sticky="w", padx=50, ipadx=100)
        render1 = PhotoImage(file='files/cosmos.png')
        img1 = tk.Label(self, image=render1)
        img1.image = render1
        img1.grid(row=1, column=4, rowspan=3, columnspan=3, sticky="nsew")
        tk.Label(self, text="Enter the name", fg="#263942", font='Helvetica 13 bold').grid(row=5, column=4, pady=10,
                                                                                           padx=5)
        self.user_name = tk.Entry(self, borderwidth=2, bg="lightgrey", font='Helvetica 12')
        self.user_name.grid(row=5, column=5, pady=10, padx=10)
        self.buttoncanc = tk.Button(self, text="Cancel", bg="red", fg="#ffffff",
                                    command=lambda: controller.show_frame("StartPage"))
        self.buttonext = tk.Button(self, text="  Next  ", fg="#ffffff", bg="#263942", command=self.start_training)
        self.buttoncanc.grid(row=6, column=4, pady=10, ipadx=5, ipady=4)
        self.buttonext.grid(row=6, column=5, pady=10, ipadx=5, ipady=4)

    def start_training(self):
        global names
        if self.user_name.get() == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif self.user_name.get() in names:
            messagebox.showerror("Error", "User already exists!")
            return
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        name = self.user_name.get()
        names.add(name)
        self.controller.active_name = name
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")

    # Making face detection page


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        self.controller = controller
        tk.Label(self, text="Select user", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, padx=10,
                                                                                        pady=10)
        self.buttoncanc = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("StartPage"),
                                    bg="#ffffff", fg="#263942")
        self.menuvar = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(self, self.menuvar, *names)
        self.dropdown.config(bg="lightgrey")
        self.dropdown["menu"].config(bg="lightgrey")
        self.buttonext = tk.Button(self, text="Next", command=self.nextfoo, fg="#ffffff", bg="#263942")
        self.dropdown.grid(row=0, column=1, ipadx=8, padx=10, pady=10)
        self.buttoncanc.grid(row=1, ipadx=5, ipady=4, column=0, pady=10)
        self.buttonext.grid(row=1, ipadx=5, ipady=4, column=1, pady=10)

    def nextfoo(self):
        if self.menuvar.get() == "None":
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.menuvar.get()
        self.controller.show_frame("PageFour")

    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))

    # Image capturing and testing


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.numimglabel = tk.Label(self, text="Number of images captured = 0", font='Helvetica 12 bold', fg="#263942")
        self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        self.capturebutton = tk.Button(self, text="Capture Data Set", fg="#ffffff", bg="#263942", command=self.capimg)
        self.trainbutton = tk.Button(self, text="Train The Model", fg="#ffffff", bg="#263942", command=self.trainmodel)
        self.buttoncanc = tk.Button(self, text="Back", bg="red", fg="#ffffff",
                                    command=lambda: controller.show_frame("PageOne"))
        self.capturebutton.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.trainbutton.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)
        self.buttoncanc.grid(row=2, ipadx=5, ipady=4, column=0, pady=10)

    def capimg(self):
        self.numimglabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("INSTRUCTIONS", "We will Capture 100 pic of your Face.")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images captured = " + str(x)))

    def trainmodel(self):
        if self.controller.num_of_images < 100:
            messagebox.showerror("ERROR", "No enough Data, Capture at least 100 images!")
            return
        train_classifer(self.controller.active_name)
        messagebox.showinfo("SUCCESS", "The model has been successfully trained!")
        self.controller.show_frame("PageFour")


class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Face Recognition", font='Helvetica 16 bold')
        label.grid(row=0, column=0, sticky="ew")
        button1 = tk.Button(self, text="Recognize Face", command=self.openwebcam, fg="#ffffff", bg="#263942")
        button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"),
                            bg="#ffffff", fg="#263942")
        buttoncanc = tk.Button(self, text="Back", bg="red", fg="#ffffff",
                               command=lambda: controller.show_frame("PageTwo"))
        button1.grid(row=1, column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button4.grid(row=1, column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        buttoncanc.grid(row=1, column=2, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

    def openwebcam(self):
        main_app(self.controller.active_name)


app = MainUI()
app.iconphoto(True, tk.PhotoImage(file='files/icon.ico'))
app.mainloop()
