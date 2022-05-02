import json
from string import ascii_lowercase, ascii_uppercase
from flask import Flask, Response, jsonify
import random
from flask import Flask, jsonify, render_template
from numpy import append

from requests import request

app = Flask(__name__)
# CORS(app)

digits = ["1","2","3","4","5","6","7","8","9"]
uppercase = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
all_letters = uppercase + lowercase
letter_and_digits = all_letters + digits
special_characters = ['~', ':', "'", '+', '[', '\\', '@', '^', '{', '%', '(', '-', '"', '*', '|', ',', '&', '<', '`', '}', '.', '_', '=', ']', '!', '>', ';', '?', '#', '$', ')', '/']
all = letter_and_digits + special_characters
number_of_passwords = int(request.form.get("numberofpasswords"))
length_of_passwords = int(request.form.get("lengthofPasswords"))
characters_type = str(request.form.get("character_type"))

@app.route("/api/v1/digits") 
def get_digits():
    
    random.shuffle(digits)
    digits_passwords = []
    
    
    for i in range(number_of_passwords):
        # entropy =[]
        temp = ""
        for i in range(0,length_of_passwords):
            temp = temp + random.choice(digits)
            
        digits_passwords.append(temp)
        
        
    print(digits_passwords)
        
    return render_template("password.html", results =digits_passwords)
            
            
            

        
    
    
    
    
   
    # upperbody = [
    #     "Push Up: No equipments needed", 
    #     "Bench press: Take two seconds to lower down and two seconds to press back up. Dumbells or Barbell",
    #     "Overhead press: ress the bar overhead, pushing your head forward and shrugging your traps as the bar passes your face.Dumbells or Barbell",
    #     "Landmine press: Load the opposite end with weight and grasp it toward the end of the sleeve with your left hand. Stand with feet shoulder width and press the bar. Barbell",
    #     "Inverted row: Hang from the bar so your body forms a straight line. Squeeze your shoulder blades together and pull ",
    #     "Chinup/Pullup:  pull yourself up until your chin is over the bar",
    #     "Hammer curl: Keeping your upper arms against your sides, curl both weights",
    #     "Triceps pushdown: ush the weight down to lock out your elbows and then let your elbows drift back slightly on the way up so you feel a stretch in your triceps ropes sre required",
    #     "Arnold Press: Press the dumbbells up above your head, rotating your palms out so that when you reach the overhead position, they face away from your body",
    #     "Skull crusher press: Press the weight straight overhead Dumbells or Barbell",
    #     "Triceps kickback:As you exhale, hold your upper arms still while you straighten your elbows by pushing your forearms backward and engaging your triceps",
       
    # ]
    random_name = random.choice(upperbody)
    res = Response(json.dumps
    ({
        "name": random_name,
    }))
    res.headers["Access-Control-Allow-Origin"] = "*"
    res.headers["Content-Type"] = "application/json"
    return res

@app.route("/api/v1/coreworkout")
def get_coreworkout():
    coreworkout = [
        "Plank:Position your head so that your neck is in a neutral position and your gaze is on your hands  No equipments needed", 
        "Panther Shoulder Tap:Tap your right hand to your left shoulder, and then your left hand to your right shoulder, while using your core strength to keep your hips as still as you can",
        "Butterfly Sit-up: Using your core, roll your body up until you are sitting upright. Reach forward to touch your toes",
        "Tuck and crunch: Simultaneously raise your torso and draw your knees towards your chest",
        "Inverted row: Hang from the bar so your body forms a straight line. Squeeze your shoulder blades together and pull ",
        "Crunch:Raise your torso using your abs",
        "Seated Russian twist: Your torso should be at the top of the crunch position, forming a 45° angle to the ground. Twist your torso from side to side, moving in a smooth and controlled manner.",
        
        
       
    ]
    random_name = random.choice(coreworkout)
    res = Response(json.dumps
    ({
        "name": random_name,
    }))
    res.headers["Access-Control-Allow-Origin"] = "*"
    res.headers["Content-Type"] = "application/json"
    return res





@app.route("/api/v1/lowerbody")
def get_lowerbody():
    lowerbody = [
        "Goblet Swuat:Stand with feet hip-width apart and hold a weight in front of chest, elbows pointing toward the floor. Push hips back and bend knees to lower into a squat. Push yourself back to start. That's one rep", 
        "Lateral walk:Place a mini resistance band a few inches above ankles, and stand with feet hip-width apart, knees slightly bent. Maintaining a tight core, step left foot out to the side, followed by right. That’s one rep",
        "Single-Leg Deadlift: Holding a weight in either hand, stand on left leg with palms facing toward thighs. Keep left leg slightly bent while hinging forward at hips, extending right leg straight behind you, until torso is parallel to the floor. Weights should be lowered straight down as you move until they're almost touching the floor. Drive into left heel to return to standing. That’s one rep",
        "Sumo Deadlift: Holding two kettlebells or dumbbells, stand with feet slightly wider than hip-width apart, toes pointed out. Position weights in front of thighs, palms facing in. Keeping knees slightly bent, press hips back as you hinge at the waist and lower the weights toward the floor. Squeeze glutes to return to standing. That's one rep",
        "Stability Ball Bridge: Start lying on back with arms by sides, legs bent at 90 degrees (shins parallel to mat) and feet on stability ball. Push down into soles, upper back, and arms to lift hips off ground a few inches. Return to start. That's one rep ",
        "Squat with HeelStand: with heels wider then shoulder-distance apart, toes turned out slightly. Bend knees, reach hips back, and lower down into a squat. Drop arms down in between legs. Then, drive in into heels to stand up, circling arms out to the sides. At the top, lift arms straight up overhead and press up onto toes. That's one rep",
        "Suitcase Deadlift: Hold a weight with left hand, feet shoulder-width apart and right hand clenched in fist. Keeping abs engaged and knees soft, sit hips back to slowly lower weight until it reaches middle of left shin. Back should be parallel to the floor. Pressing through heels and engaging abs, quickly return to start. Squeeze glutes once completely upright. That's one rep",
        "Bulgarian Split Squat:Start standing about two feet in front of a step, holding a weight in each hand. Extend left leg back and place left foot on step. Bend knees to lower body as far as you can (or until knee hovers right above the ground), keeping shoulders back and chest up. Pause, then press through right heel to return to start. That's one rep",
        
        
       
    ]
    random_name = random.choice(lowerbody)
    res = Response(json.dumps
    ({
        "name": random_name,
    }))
    res.headers["Access-Control-Allow-Origin"] = "*"
    res.headers["Content-Type"] = "application/json"
    return res




    

if __name__ == "__main__":
    app.run("0.0.0.0")