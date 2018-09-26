import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Check wether username given is blank, already taken or valid
def verify_username(username):
    if username == "":
        return "noUser"
        
    # open users_test.txt and check wether the username is already taken
    with open("data/users.txt", "r") as file:
        users = file.read().splitlines()
        
    for user in users:
        if user == username:
            return "notUnique"
    return True

#Takes username as an input value
def add_username():
    username = request.form["username"]
    
    # If username is verified
    if verify_username(username) == "noUser":
      return "noUser"
    elif verify_username(username) == "notUnique":
      return "notUnique"
    else:
      with open("data/users.txt", "a") as file:
        file.write(username + "\n")
        file.close()
      return username
      
#Gets Questions from questions.txt
def get_questions():
    questions = []
    answers = []
    
    # reads questions_test.txt and splits even lines into questions and odd lines into answers
    with open("data/questions.txt", "r") as file:
        lines = file.read().splitlines()
        
    for i, text in enumerate(lines):
        if i%2 == 0:
            questions.append(text)
        else:
            answers.append(text)
    
    return questions, answers
    
    
# Checks Wether guess is correct, inncorect or is a pass
def check_guess(answer, guess, lives, question_num, questions_score, passed_on, btn, bg, username):
  
  status = ""
  def url(status, question_num, questions_score, passed_on, btn, bg, lives):
    return redirect("/questions/" + status + "/" + question_num + "/" + questions_score + "/" + passed_on + "/" + lives + "/" + guess + "/" + btn + "/" + bg + "/" + username)
 
  if( guess == answer ):
    questions_score = str(int(questions_score) + 50)
    question_num = str(int(question_num) + 1)
    status = "correct"
    btn = "primary"
    bg = "0"
    return url(status, question_num, questions_score, passed_on, btn, bg, lives)
    
    
  elif ( guess == "pass" ):
    status = "pass"
    question_num = str(int(question_num) + 1)
    passed_on = str(int(passed_on) + 1)
    
    if ( int(passed_on) == 2 ):
      btn = "warning"
      
    elif ( int(passed_on) == 3 ):
      lives = str(int(lives) - 1)
      passed_on = "0"
      btn = "primary"
      bg = "FF4D4C"
      
    else:
      btn = "primary"
      bg = "0"
    return url(status, question_num, questions_score, passed_on, btn, bg, lives)
    
    
  else:
    status = "wrong"
    lives = str(int(lives) - 1)
    bg = "FF4D4C"
    return url(status, question_num, questions_score, passed_on, btn, bg, lives)


@app.route('/' , methods=["GET", "POST"])
def index():
    userText = "Enter A Username To Begin"
    if request.method == "POST":
        user = add_username()
        if user == "noUser":
          userText = "Oops! Please Enter A Username To Begin"
        elif user == "notUnique":
          userText = "Oops! That Username Is Already Taken"
        else:
          return redirect("/questions/0/1/0/0/5/0/primary/0/" + request.form["username"])
    return render_template("index.html", user=userText)
    


@app.route('/questions/<status>/<question_num>/<questions_score>/<passed_on>/<lives>/<guess>/<btn>/<bg>/<username>', methods=["GET", "POST"])
def questions(status, question_num, questions_score, passed_on, lives, guess, btn, bg, username):
  questions = get_questions()
  q_num = int(question_num) - 1
  question = questions[0][q_num]
  answer = questions[1][q_num]
  message = ""
  
  if ( status == "wrong" ):
    message = "'{0}', Was Incorrect".format(guess)
  elif ( status == "pass" ):
    message = "Question Passed"
    
    
    
  if request.method == "POST":
    guess = request.form["answer"]
    
    url = check_guess(answer, guess, lives, question_num, questions_score, passed_on, btn, bg, username)
    
    return url
    
  return render_template(
    "questions.html",
    message=message,
    question=question,
    lives=lives,
    questionNum=question_num,
    questionsScore=questions_score,
    passed=passed_on,
    bg=bg,
    btn=btn,
    username=username
    ) 
    
    
    
@app.route('/about')
def about():
  
  return render_template("about.html")
    
@app.route('/instructions')
def instructions():
  return render_template("instructions.html")
    
@app.route('/contact')
def contact():
  return render_template("contact.html")
    

app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)