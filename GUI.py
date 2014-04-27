import Tkinter as tk
import os
import time
from PIL import Image, ImageTk
import eigenfaces as eigenfaces
import fisherfaces as fisherfaces
import utility as utility
import sift

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Page1(Page):
   def __init__(self, *args, **kwargs):
       tk.Frame.__init__(self, *args, **kwargs)
       self.string = tk.StringVar()
       label = tk.Label(self, textvariable=self.string)
       label.pack(side="top", fill="both", expand=True)

class Page2(Page):
   def __init__(self, *args, **kwargs):
       tk.Frame.__init__(self, *args, **kwargs)
       self.string = tk.StringVar()
       label = tk.Label(self, textvariable=self.string)
       label.pack(side="top", fill="both", expand=True)


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.db = ""
        self.testName = ""
        self.testImage = ""
        self.algoName = ""
        self.database = tk.Frame(self)
        self.home = tk.Frame(self)
        self.home.pack(side="top", fill="both", expand=True)


#        self.database = Page2(self)

#        self.database.pack(side="top", fill="x", expand=True)
        self.database.place(in_=self.home, x=0, y=0, relwidth=1, relheight=1)
        label = tk.Label(self.database,text="Choose Database:",anchor="w",fg='black',bg='white')
        label.pack(side="top")

        self.yale = tk.Frame(self)
        self.orl = tk.Frame(self)
        self.db3 = tk.Frame(self)

#        self.yale = Page2(self)
#        self.orl = Page2(self)
#        self.db3 = Page2(self)


#        self.yale.string.set("Yale Tests Window")
#        self.orl.string.set("ORL Tests Window")
#        self.db3.string.set("DB3 Tests Window")

        self.yale.place(in_=self.database, x=0, y=0, relwidth=1, relheight=1)
        self.orl.place(in_=self.database, x=0, y=0, relwidth=1, relheight=1)
        self.db3.place(in_=self.database, x=0, y=0, relwidth=1, relheight=1)


        button_yale = tk.Button(self.database, text="Yale",height=5, width=30,activebackground="red", command=lambda: self.selectedDatabase("yale"))
        button_orl = tk.Button(self.database, text="ORL",height=5, width=30, activebackground="red",command=lambda: self.selectedDatabase("orl"))
        button_db3 = tk.Button(self.database, text="DB3",height=5, width=30,activebackground="red", command=lambda: self.selectedDatabase("db3"))

        button_back1 = tk.Button(self.yale, text="Back", command=lambda: self.yale.lower())
        button_back2 = tk.Button(self.orl, text="Back",command=lambda: self.orl.lower())
        button_back3= tk.Button(self.db3, text="Back",command=lambda: self.db3.lower())
#        button = tk.Button(self.database, text="Algorithm",command=lambda:self.algorithm.lift())

        button_yale.pack(side="top")
        button_orl.pack(side="top")
        button_db3.pack(side="top")


        button_back3.pack(side="top")
#        button.pack(side="top")
        label1 = tk.Label(self.yale,text="Choose a test(Yale):",anchor="w",fg='black',bg='white')
        label1.pack(side="top")
        button_yale_general = tk.Button(self.yale, text="General Test", command=lambda: self.test('general'))
        button_yale_illumination = tk.Button(self.yale, text="Illumination Test", command=lambda: self.test('illumination'))
        button_yale_expression = tk.Button(self.yale, text="Expression Test", command=lambda: self.test('expression'))
        button_yale_glasses = tk.Button(self.yale, text="Glasses Test", command=lambda: self.test('glasses'))
        button_yale_choice = tk.Button(self.yale, text="Choose an Image to test", command=lambda:self.test('choice'))


        button_yale_general.pack(side="top")
        button_yale_illumination.pack(side="top")
        button_yale_expression.pack(side="top")
        button_yale_glasses.pack(side="top")
        button_yale_choice.pack(side="top")
        button_back1.pack(side="top")

        label2 = tk.Label(self.orl,text="Choose a test(ORL):",anchor="w",fg='white',bg='blue')
        label2.pack(side="top")
        button_orl_general = tk.Button(self.orl, text="General Test", command=lambda: self.test('general'))
        button_orl_pose = tk.Button(self.orl, text="Pose Test", command=lambda: self.test('pose'))
        button_orl_choice = tk.Button(self.orl, text="Choose an Image to test", command=lambda:self.test('choice'))

        button_orl_general.pack(side="top")
        button_orl_pose.pack(side="top")
        button_orl_choice.pack(side="top")
        button_back2.pack(side="top")

#########
#  DB3  #
#########
        label3 = tk.Label(self.db3,text="Choose a test (db3):",anchor="w",fg='white',bg='blue')
        label3.pack(side="top")
        button_back3.pack(side="top")

        self.algorithm = tk.Frame(self)
        self.eigenface = tk.Frame(self)
        self.fisherface = tk.Frame(self)
        self.sift = tk.Frame(self)
        self.lem = tk.Frame(self)
        self.yolo = tk.Frame(self)


#        self.algorithm = Page1(self)
#        self.eigenface = Page1(self)
#        self.fisherface = Page1(self)
#        self.sift = Page1(self)
#        self.lem = Page1(self)

        self.algorithm.place(in_=self.database, x=0, y=0, relwidth=1, relheight=1)
        self.algoInfo = tk.StringVar()
        label4 = tk.Label(self.algorithm,textvariable=self.algoInfo,anchor="w",fg='white',bg='blue')
        label4.pack(side="top")

        self.eigenface.place(in_=self.algorithm, x=0, y=0, relwidth=1, relheight=1)
        self.fisherface.place(in_=self.algorithm, x=0, y=0, relwidth=1, relheight=1)
        self.sift.place(in_=self.algorithm, x=0, y=0, relwidth=1, relheight=1)
        self.lem.place(in_=self.algorithm, x=0, y=0, relwidth=1, relheight=1)
        self.yolo.place(in_=self.algorithm, x=0, y=0, relwidth=1, relheight=1)

#        self.eigenface.string.set("Eigenface window")
#        self.fisherface.string.set("Fisherface window")
#        self.sift.string.set("SIFT window")
#        self.lem.string.set("LEM window")


        b1 = tk.Button(self.algorithm, text="Eigenface", command=lambda: self.faceRec('eigenface'))
        b2 = tk.Button(self.algorithm, text="FisherFace", command=lambda: self.faceRec('fisherface'))
        b3 = tk.Button(self.algorithm, text="SIFT", command=lambda: self.faceRec('sift'))
        b4 = tk.Button(self.algorithm, text="LEM", command=lambda: self.faceRec('lem'))
        button_back_database = tk.Button(self.algorithm, text="Back", command=lambda: self.backAlgo())

        b1.pack(side="top")
        b2.pack(side="top")
        b3.pack(side="top")
        b4.pack(side="top")

        button_back_database.pack(side="top")

        self.database.lift()

    def selectedDatabase(self, db):
        self.db = db
        print self.db
        if(db == "yale"):
            self.yale.lift()
        elif(db == "orl"):
            self.orl.lift()
        elif(db == "db3"):
            self.db3.lift()
    
    def backAlgo(self):
        if(self.db == "yale"):
            self.yale.lift()
        elif(self.db == "orl"):
            self.orl.lift()
        elif(self.db == "db3"):
            self.db3.lift()

    def test(self, testName):
        self.testName = testName
        print self.testName
        self.algoInfo.set("Choose an Algorithm:("+self.db+","+self.testName+")")
        self.algorithm.lift()

    def myfunction(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=1000, height=500)

    def choiceFrame(self):
        if(self.db=="yale"):
            folder = "yalefaces/"
        elif(self.db=="orl"):
            folder = "orl_faces/"
        self.choiceT = tk.Frame(self,width=1000, height=500,bd=1)
        self.choiceT.place(in_=self.algorithm, x=0, y=0, relwidth=1, relheight=1)
        self.canvas = tk.Canvas(self.choiceT)
        self.choice = tk.Frame(self.canvas)
        i=0
        scroll = tk.Scrollbar(self.choiceT, orient="vertical",command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right",fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0,0),window=self.choice)
        self.choice.bind("<Configure>",self.myfunction)

#        self.choice.grid(row=0,column=0,sticky="NSEW")
        while(i<len(self.testing_answer)):
            img = ImageTk.PhotoImage(file=folder+self.testing_answer[i])
            tempButton=tk.Button(self.choice, image=img, text=self.testing_answer[i], command=lambda m=self.testing_answer[i]:self.rest(m))
            tempButton.image = img
            tempButton.grid(row=i/3,column=0)
#            tempButton.pack(side="top")
            img = ImageTk.PhotoImage(file=folder+self.testing_answer[i+1])
            tempButton=tk.Button(self.choice, image=img, text=self.testing_answer[i+1], command=lambda m=self.testing_answer[i+1]:self.rest(m))
            tempButton.image = img
            tempButton.grid(row=i/3,column=1)
#            tempButton.pack(side="top")
            img = ImageTk.PhotoImage(file=folder+self.testing_answer[i+2])
            tempButton=tk.Button(self.choice, image=img, text=self.testing_answer[i+2], command=lambda m=self.testing_answer[i+2]:self.rest(m))
            tempButton.image = img
            tempButton.grid(row=i/3,column=2)
#            tempButton.pack(side="top")
            i+=3
#        self.choice.lift()
        print "Done choosing and running Algorithm"
        return

    def rest(self, x):
        self.testImage = x
        if(self.algoName == "eigenface"):
            self.eigenTest()
            return
        elif(self.algoName == "fisherface"):
            self.eigenTest()
            return
        elif(self.algoName == "sift"):
            pass
            return
        elif(self.algoName == "lem"):
            pass
            return
        return

    def eigenTest(self):
        result = utility.predict(self.testing[self.testing_answer.index(self.testImage)], self.training_answer, self.W, self.mu, self.projections)
        print result, self.testImage
        if(result[6:9] == self.testImage[6:9]):
            print "HIT!"
        if(self.db == "yale"):
            utility.choicePlot("yalefaces/"+self.testImage, "yalefaces/"+result, self.choiceImage)
            print "Finished plotting image"
        elif(self.db == "orl"):
            utility.choicePlot("orl_faces/"+self.testImage, "orl_faces/"+result, self.choiceImage)
        elif(self.db == "db3"):
            pass
        self.choiceResult = tk.Frame(self)
        self.choiceResult.place(in_=self.algorithm, x=0,y=0,relwidth=1,relheight=1)
        choiceImage = ImageTk.PhotoImage(file=self.choiceImage)
        labelChoice = tk.Label(self.choiceResult, image=choiceImage)
        labelChoice.image = choiceImage
        labelChoice.pack(side="top")
        print "should happen"
        choiceBack = tk.Button(self.choiceResult, text="Back", command=lambda: self.algorithm.lift())
        choiceBack.pack(side="top")
        self.choiceResult.lift()


    def remove(self, b1, b2, b3, b4):
        b1.pack_forget()
        b2.pack_forget()
        b3.pack_forget()
        b4.pack_forget()
        self.algorithm.lift()

    def faceRec(self,name):
        if(name=="eigenface"):
            self.algoName = "eigenface"
            if(self.db == "yale"):
                    if(self.testName=="choice"):
                        self.testing, self.training_answer, self.W, self.mu, self.projections, self.testing_answer = eigenfaces.test_yale(self.testName)
                        self.choiceImage = "Eigenface_choice_yale"
                    else:
                        image1, image2, accuracy = eigenfaces.test_yale(self.testName)
            elif(self.db == "orl"):
                    if(self.testName=="choice"):
                        self.testing, self.training_answer, self.W, self.mu, self.projections, self.testing_answer = eigenfaces.test_orl(self.testName)
                        self.choiceImage = "Eigenface_choice_orl"
                    else:
                        image1, image2, accuracy = eigenfaces.test_orl(self.testName)                        
            elif(self.db == "db3"):
                pass
            if(self.testName=="choice"):
                self.testImage =''
                self.choiceFrame()
            else:
                print image1, image2
                self.eigenface_success = tk.Frame(self)
                self.eigenface_fail = tk.Frame(self)
                self.eigenface_intermediate = tk.Frame(self)

                self.eigenface_success.place(in_=self.eigenface, x=250, y=120, relwidth=1, relheight=1)
                self.eigenface_fail.place(in_=self.eigenface, x=250, y=120, relwidth=1, relheight=1)            
                self.eigenface_intermediate.place(in_=self.eigenface, x=250, y=120, relwidth=1, relheight=1)

                eigenButton1 = tk.Button(self.eigenface, text = "Success", command=lambda:self.eigenface_success.lift())
                eigenButton2 = tk.Button(self.eigenface, text = "Failure", command=lambda:self.eigenface_fail.lift())
                eigenButton3 = tk.Button(self.eigenface, text = "Intermediate", command=lambda:self.eigenface_intermediate.lift())
    
                eigenButton4 = tk.Button(self.eigenface, text="Back",command=lambda:self.remove(eigenButton1, eigenButton2, eigenButton3, eigenButton4))

                eigenButton1.pack(side="top")
                eigenButton2.pack(side="top")
                eigenButton3.pack(side="top")
        
                eigenButton4.pack(side="top")

                failure = ImageTk.PhotoImage(file=image1)
                success = ImageTk.PhotoImage(file=image2)
                labelFail = tk.Label(self.eigenface_fail, image = failure)
                labelFail.image = failure
                labelFail.pack(side="left")
                labelSuccess = tk.Label(self.eigenface_success, image = success)
                labelSuccess.image = success
                labelSuccess.pack(side="left")
                self.eigenface.lift()

        elif(name=="fisherface"):
            self.algoName = "fisherface"
            if(self.db == "yale"):
                    if(self.testName=="choice"):
                        self.testing, self.training_answer, self.W, self.mu, self.projections, self.testing_answer = fisherfaces.test_yale(self.testName)
                        self.choiceImage = "Fisherface_choice_yale"
                    else:
                        image1, image2, accuracy = fisherfaces.test_yale(self.testName)
            elif(self.db == "orl"):
                    if(self.testName=="choice"):
                        self.testing, self.training_answer, self.W, self.mu, self.projections, self.testing_answer = fisherfaces.test_orl(self.testName)
                        self.choiceImage = "Fisherface_choice_orl"
                    else:
                        image1, image2, accuracy = fisherfaces.test_orl(self.testName)                        
            elif(self.db == "db3"):
                pass
            if(self.testName=="choice"):
                self.choiceFrame()
            else:
                print image1, image2
                self.fisherface_success = tk.Frame(self)
                self.fisherface_fail = tk.Frame(self)
                self.fisherface_intermediate = tk.Frame(self)

                self.fisherface_success.place(in_=self.fisherface, x=250, y=100, relwidth=1, relheight=1)
                self.fisherface_fail.place(in_=self.fisherface, x=250, y=100, relwidth=1, relheight=1)            
                self.fisherface_intermediate.place(in_=self.fisherface, x=250, y=100, relwidth=1, relheight=1)

                fisherButton1 = tk.Button(self.fisherface, text = "Success", command=lambda:self.fisherface_success.lift())
                fisherButton2 = tk.Button(self.fisherface, text = "Failure", command=lambda:self.fisherface_fail.lift())
                fisherButton3 = tk.Button(self.fisherface, text = "Intermediate", command=lambda:self.fisherface_intermediate.lift())
    
                fisherButton4 = tk.Button(self.fisherface, text="Back",command=lambda:self.remove(fisherButton1, fisherButton2, fisherButton3, fisherButton4))
                fisherButton1.pack(side="top")
                fisherButton2.pack(side="top")
                fisherButton3.pack(side="top")
        
                fisherButton4.pack(side="top")
        
                failure = ImageTk.PhotoImage(file=image1)
                success = ImageTk.PhotoImage(file=image2)
                labelFail = tk.Label(self.fisherface_fail, image = failure)
                labelFail.image = failure
                labelFail.pack(side="left")
                labelSuccess = tk.Label(self.fisherface_success, image = success)
                labelSuccess.image = success
                labelSuccess.pack(side="left")
                self.fisherface.lift()

        elif(name=="sift"):
            self.algoName = "sift"
            if(self.db == "yale"):
                image1, image2, accuracy = sift.test_yale(self.testName)
            elif(self.db == "orl"):
                image1, image2, accuracy = sift.test_orl(self.testName)
            elif(self.db == "db3"):
                pass            
            print image1, image2
            self.sift_success = tk.Frame(self)
            self.sift_fail = tk.Frame(self)
            self.sift_intermediate = tk.Frame(self)

            self.sift_success.place(in_=self.sift, x=250, y=100, relwidth=1, relheight=1)
            self.sift_fail.place(in_=self.sift, x=250, y=100, relwidth=1, relheight=1)            
            self.sift_intermediate.place(in_=self.sift, x=250, y=100, relwidth=1, relheight=1)
    
            siftButton1 = tk.Button(self.sift, text = "Success", command=lambda:self.sift_success.lift())
            siftButton2 = tk.Button(self.sift, text = "Failure", command=lambda:self.sift_fail.lift())
            siftButton3 = tk.Button(self.sift, text = "Intermediate", command=lambda:self.sift_intermediate.lift())
    
            siftButton4 = tk.Button(self.sift, text="Back",command=lambda:self.remove(siftButton1, siftButton2, siftButton3, siftButton4))

            siftButton1.pack(side="top")
            siftButton2.pack(side="top")
            siftButton3.pack(side="top")
    
            siftButton4.pack(side="top")

            failure = ImageTk.PhotoImage(file=image1)
            success = ImageTk.PhotoImage(file=image2)
            labelFail = tk.Label(self.sift_fail, image = failure)
            labelFail.image = failure
            labelFail.pack(side="left")
            labelSuccess = tk.Label(self.sift_success, image = success)
            labelSuccess.image = sugridccess
            labelSuccess.pack(side="left")
            self.sift.lift()

        elif(name=="lem"):
            self.algoName = "lem"
            if(self.db == "yale"):
                pass
            elif(self.db == "orl"):
                pass
            elif(self.db == "db3"):
                pass
            self.lem.lift()

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()
