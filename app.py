from flask.helpers import url_for
from flask.templating import render_template
from flask import request, redirect
from flask import Flask
from lem import *
import eigenfaces as eigenfaces
import fisherfaces as fisherfaces
import sift as sift
import lem as lem
import input as input
import utility as utility
import os,atexit,platform,sys
from time import clock
app=Flask(__name__)

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/startTest')
def startTest():
    return render_template("database.html")

@app.route('/yaleDB-A')
def yaleA():
    global database
    database = "yale A"
    print database
    return render_template("yaleATest.html")

@app.route('/yaleDB-B')
def yaleB():
    global database
    database = "yale B"
    print database
    return render_template("yaleBTest.html")

@app.route('/orlDB')
def orl():
    global database
    database = "orl"
    print database
    return render_template("orlTest.html")

@app.route('/test/<testame>')
def chooseAlgo(testame):
    global testName
    testName = testame
    print testName
    return render_template("algorithm.html")

@app.route('/algorithm/<chosenAlgo>')
def test(chosenAlgo):
    global algoName
    global success
    global failure
    global accuracy
    global singleTime
    global totalTime
    global countHits
    global trainLength
    global testLength
#    global intermediate
    
    algoName = chosenAlgo
    print database, testName, algoName
    if(algoName == "eigenface"):
        if(database == "yale A"):
            if(testName == "choice"):
                global testing
                global testing
                global training_answer
                global W
                global mu
                global projections
                global testing_answer
                print "FETCHING TEST IMAGES"
                testing, training_answer, W, mu, projections, testing_answer = eigenfaces.test_yale(testName)
                print testing_answer
                return render_template("choice.html",images =  testing_answer, db = "/static/images/yalefaces/")
            else:
                failure, success, accuracy, singleTime, totalTime, trainLength, testLength, countHits= eigenfaces.test_yale(testName)
                print countHits
        elif(database == "yale B"):
            pass
        elif(database == "orl"):
            if(testName == "choice"):
                global testing
                global testing
                global training_answer
                global W
                global mu
                global projections
                global testing_answer
                testing, training_answer, W, mu, projections, testing_answer = eigenfaces.test_orl(testName)
                return render_template("choice.html", images = testing_answer, db = "/static/images/orl_faces/")
            else:
                failure, success, accuracy, singleTime, totalTime, trainLength, testLength, countHits = eigenfaces.test_orl(testName)        
    elif(algoName == "fisherface"):
        if(database == "yale A"):
            if(testName == "choice"):
                global testing
                global testing
                global training_answer
                global W
                global mu
                global projections
                global testing_answer
                testing, training_answer, W, mu, projections, testing_answer = fisherfaces.test_yale(testName)
                return render_template("choice.html", images =  testing_answer, db = "/static/images/yalefaces/")
            else:
                failure, success, accuracy, singleTime, totalTime, trainLength, testLength, countHits = fisherfaces.test_yale(testName)
        elif(database == "yale B"):
            pass
        elif(database == "orl"):
            if(testName == "choice"):
                global testing
                global testing
                global training_answer
                global W
                global mu
                global projections
                global testing_answer
                testing, training_answer, W, mu, projections, testing_answer = fisherfaces.test_orl(testName)
                return render_template("choice.html", images= testing_answer, db = "/static/images/orl_faces/")
            else:
                failure, success, accuracy, singleTime, totalTime, trainLength, testLength, countHits = fisherfaces.test_orl(testName)
    elif(algoName == "sift"):
        if(database == "yale A"):
            if(testName == "choice"):
                global descriptors_testing
                global training_answer
                global descriptors_training
                global testing_answer
                descriptors_testing, training_answer, descriptors_training, testing_answer = sift.test_yale(testName)
                return render_template("choice.html", images= testing_answer, db = "/static/images/yalefaces/")
            else:
                failure, success, accuracy, singleTime, totalTime, trainLength, testLength, countHits = sift.test_yale(testName)
        elif(database == "yale B"):
            pass
        elif(database == "orl"):
            if(testName == "choice"):
                global descriptors_testing
                global training_answer
                global descriptors_training
                global testing_answer
                descriptors_testing, training_answer, descriptors_training, testing_answer = sift.test_orl(testName)
                return render_template("choice.html",images= testing_answer, db="/static/images/orl_faces/")
            else:
                failure, success, accuracy, singleTime, totalTime, trainLength, testLength, countHits = sift.test_orl(testName)
    elif(algoName == "lem"):
        if(database == "yale A"):
            if(testName == "choice"):
                global testing_corners
                global training_corners
                global training_answer
                global testing_answer
                testing_corners, training_corners, training_answer, testing_answer = lem.test_yale(testName)
                return render_template("choice.html",images= testing_answer, db="/static/images/yalefaces/")
            else:
                failure, success, accuracy, singleTime, totalTime, trainLength, testLength, countHits = lem.test_yale(testName)
        elif(database == "yale B"):
            pass
        elif(database == "orl"):
            if(testName == "choice"):
                global testing_corners
                global training_corners
                global training_answer
                global testing_answer
                testing_corners, training_corners, training_answer, testing_answer = lem.test_orl(testName)
                return render_template("choice.html",images= testing_answer, db="/static/images/orl_faces/")
            else:
                failure, success, accuracy, singleTime, totalTime, trainLength, testLength, countHits = lem.test_orl(testName)
    acc=str(accuracy)[:6]+"%" 
    print acc
    return render_template("chooseResult.html",accuracy=acc, singleTime=singleTime, totalTime=totalTime, training_set_length=trainLength, testing_set_length=testLength, countHits=countHits)

@app.route('/choiceResult/<dbName>/<imageName>')
@app.route('/choiceResult/<dbName>/<imageName>/<temp>')
def choiceResult(dbName,imageName,temp=""):
    print "Choice --- Executing."
    if(not(temp == "")):
        testImage = dbName+"/"+imageName+"/"+temp
    else:
        testImage = dbName+"/"+imageName
    print testImage
    if platform.system()=="Windows":
        look="\\"
    else:
        look="/"
    choiceImage = ""
    #do a prediction based on algorithm
    if(algoName == "eigenface"):
        result = utility.predict(testing[testing_answer.index(testImage)], training_answer, W, mu, projections)
        choiceImage = "eigenface_yale_choice"
    elif(algoName == "fisherface"):
        result = utility.predict(testing[testing_answer.index(testImage)], training_answer, W, mu, projections)
        choiceImage = "fisherface_yale_choice"
    elif(algoName == "sift"):
        result = sift.localPredict(descriptors_testing[testing_answer.index(testImage)], training_answer, descriptors_training)
        choiceImage = "sift_yale_choice"
    elif(algoName == "lem"):
        result = lem.predict_hausdroff(testing_corners[testing_answer.index(testImage)], training_corners, training_answer)
        choiceImage = "lem_yale_choice"

    #test the image for success based on databases
    if(database == "yale A"):
        heading=result[result.find(look)+len(look):result.find('.')]+" MATCHED WITH "+ testImage[testImage.find(look)+len(look):testImage.find('.')]
        if(result[:result.find('.')] == testImage[:testImage.find('.')]):
            print "HIT!"
            status="hit"
        else:
            status="miss"
        
    elif(database == "orl"):
        heading=result[result.find(look)+len(look):result.find(look,11)]+" MATCHED WITH "+ testImage[testImage.find(look)+len(look):testImage.find(look,11)]
        if(result[:result.find(look,12)] == testImage[:testImage.find(look,12)]):
            print "HIT"
            status="hit"
        else:
            status="miss"
    elif(database == "yale B"):
        pass

    #plot the visuals
    utility.choicePlot(testImage, result, choiceImage)
    os.system("convert "+choiceImage+" "+choiceImage+".png")
    os.system("rm static/images/"+choiceImage+".png")
    os.system("mv "+choiceImage+".png static/images/"+choiceImage+".png")
    return render_template("choiceResult.html", filename = "/static/images/"+choiceImage+".png", status=status, heading=heading)

@app.route('/result/<res>')
def showResult(res):
    global resultType
    resultType = res
    print resultType
    if(resultType == "Success"):
        x = "/static/images/"+success
    elif(resultType == "Failure"):
        x = "/static/images/"+failure
    elif(resultType == "Intermediate"):
        x = "/static/images/"+intermediate

    return render_template("result.html", filename = x, name = resultType)


if __name__ == "__main__":
    app.config["CACHE_TYPE"] = "null"
    app.run()
