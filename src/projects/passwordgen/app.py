import math
from dataclasses import replace
import requests
import random
from flask import Flask, jsonify, render_template
from flask import Flask, render_template, request
app = Flask(__name__, template_folder='templates')



@app.route("/", methods = ['POST', 'GET'])
def index():
    
    return render_template('index.html')




digits = ["2","3","4","5","6","7","8","9"]
upperr = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H','J', 'K', 'L', 'M', 'N','P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
ul = upperr + lowercase
letter_and_digits = ul + digits
symbols = ['~', ':', "'", '+', '[', '\\', '@', '^', '{', '%', '(', '-', '"', '*', '|', ',', '&', '<', '`', '}', '.', '_', '=', ']', '!', '>', ';', '?', '#', '$', ')', '/']
sum = letter_and_digits + symbols
numberofPasswords = []

@app.route("/api/data", methods=["GET", "POST"])

def password():
    
    if request.method == "POST":
        
        passtype = str(request.form.get("type"))
        number = int(request.form.get("lengthofpass"))
        numberofpasswords = int(request.form.get("numberofpasswords"))
            
    
    
        if passtype == "digits":
            
            dig_list = digits
      
            for i in range(numberofpasswords):
                etp = []
                sub = int(math.log((len(dig_list)**number), 2))

                if sub < 40:
                    
                    etp.append("Avoid")
                elif sub > 40 and sub < 60:
                    etp.append("very weak")
                elif sub > 60 and sub < 80:
                    etp.append("weak")
                elif sub > 80 and sub < 100:
                    etp.append("strong")
                elif sub > 100:
                    etp.append("very strong")
                
                
                

                posional = random.sample(dig_list*10,number)
                
        
                password = "".join(posional)
            numberofPasswords.append(password)
            
            
            
        if passtype == "lowerCase":
            for i in range(numberofpasswords):
                etp = []
                sub = int(math.log((len(lowercase)**number), 2))

                if sub < 40:
                    
                    etp.append("Avoid")
                elif sub > 40 and sub < 60:
                    etp.append("very weak")
                elif sub > 60 and sub < 80:
                    etp.append("weak")
                elif sub > 80 and sub < 100:
                    etp.append("strong")
                elif sub > 100:
                    etp.append("very strong")

                posional = random.sample(lowercase*10,number)
            
                password = "".join(posional)
                numberofPasswords.append(password)

        if passtype == "upperr":
            for i in range(numberofpasswords):
                etp = []
                sub = int(math.log((len(upperr)**number), 2))

                if sub < 40:
                    
                    etp.append("Avoid")
                elif sub > 40 and sub < 60:
                    etp.append("very weak")
                elif sub > 60 and sub < 80:
                    etp.append("weak")
                elif sub > 80 and sub < 100:
                    etp.append("strong")
                elif sub > 100:
                    etp.append("very strong")

                posional = random.sample(upperr*10,number)
            
                password = "".join(posional)
                numberofPasswords.append(password)

        if passtype == "lowUpCase":
            for i in range(numberofpasswords):
                etp = []
                sub = int(math.log((len(ul)**number), 2))

                if sub < 40:
                    
                    etp.append("Avoid")
                elif sub > 40 and sub < 60:
                    etp.append("very weak")
                elif sub > 60 and sub < 80:
                    etp.append("weak")
                elif sub > 80 and sub < 100:
                    etp.append("strong")
                elif sub > 100:
                    etp.append("very strong")

                posional = random.sample(ul*10,number)
            
                password = "".join(posional)
                numberofPasswords.append(password)

        if passtype == "digitsandLetters":
            for i in range(numberofpasswords):
                etp = []
                sub = int(math.log((len(letter_and_digits)**number), 2))

                if sub < 40:
                    
                    etp.append("Avoid")
                elif sub > 40 and sub < 60:
                    etp.append("very weak")
                elif sub > 60 and sub < 80:
                    etp.append("weak")
                elif sub > 80 and sub < 100:
                    etp.append("strong")
                elif sub > 100:
                    etp.append("very strong")

                posional = random.sample(letter_and_digits*10,number)
            
                password = "".join(posional)
                numberofPasswords.append(password)
        
        if passtype == "specialCharacters":
            for i in range(numberofpasswords):
                etp = []
                sub = int(math.log((len(symbols)**number), 2))

                if sub < 40:
                    
                    etp.append("Avoid")
                elif sub > 40 and sub < 60:
                    etp.append("very weak")
                elif sub > 60 and sub < 80:
                    etp.append("weak")
                elif sub > 80 and sub < 100:
                    etp.append("strong")
                elif sub > 100:
                    etp.append("very strong")

                posional = random.sample(symbols*10,number)
            
                password = "".join(posional)
                numberofPasswords.append(password)

        if passtype == "All":
            for i in range(numberofpasswords):
                etp = []
                sub = int(math.log((len(sum)**number), 2))

                if sub < 40:
                    
                    etp.append("Avoid")
                elif sub > 40 and sub < 60:
                    etp.append("very weak")
                elif sub > 60 and sub < 80:
                    etp.append("weak")
                elif sub > 80 and sub < 100:
                    etp.append("strong")
                elif sub > 100:
                    etp.append("very strong")

                posional = random.sample(sum*10,number)
            
                password = "".join(posional)
                numberofPasswords.append(password)

        return render_template("results.html",p=numberofPasswords,k=etp)
    
    
    

    
    
    

@app.route("/api/phrase/", methods = ['POST', 'GET'])
def phraseu():

    return render_template("phrase.html")

    
wordlist = open("words", "r")

@app.route("/api/phrase/data", methods=["GET", "POST"]) 
def passphrase():
    wordlist = open("words", "r")
    wordS = []
    
    for line in wordlist:
        wordS.append(line)

    
    if request.method == "POST":
        
        numberofwords = int(request.form.get("numberwords"))
        
        number_of_passphrase= int(request.form.get("numberofphrases"))
        
        separator = str(request.form.get("separator"))
        nums = []
        # oop =[]
        for i in range(number_of_passphrase):
            
            etp = []
            sub = int(math.log((len(sum)**numberofwords), 2))

            if sub < 40:
                    
                    
                etp.append("Avoid")
            elif sub > 40 and sub < 60:
                 etp.append("very Weak")
            elif sub > 60 and sub < 80:
                etp.append("weak")
            elif sub > 80 and sub < 100:
                etp.append("Strong")
            elif sub > 100:
                etp.append("very strong")
                    
            x = random.sample(wordS, numberofwords)
           
            nums.append(f"{separator}".join(x))
        # oop.append(f"{separator}".join(nums))
            
        # nums = f'{separator}'.join
        
  
        # stringo = nums + separator
           
         
        
        return render_template("presu.html", ph=nums,k=etp)
    
    

if __name__ == "_main_":
    app.debug = True
    app.run()