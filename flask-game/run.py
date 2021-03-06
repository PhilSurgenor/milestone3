import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

#####################
# USERNAME SECTION #
###################

# This section takes the input from the landing page and checks it against usernames saved in the users.txt file
# This keeps the score bord tidy as you can have repeat usernames
# It also means it is harder to cheat as you can't have another go with the same username

# Check wether username given is blank, already taken or valid
def verify_username(username):
    if username == "":
        return "noUser"
        
    # open users_test.txt and check wether the username is already taken
    with open("data/users.txt", "r") as file:
        users = file.read().splitlines()
        
    for user in users:
      if user.replace(" ", "").lower() == username.replace(" ", "").lower():
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
      
###############################################################



#####################
# QUESTIONS SECTION #
###################
  
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
    
    
# Checks How many questions are left
def check_question_num(question_num):
    questions = get_questions()
    questions_len = len(questions[0])
    
    if ( int(question_num) > questions_len ):
      return True
    else:
      return False
      
###############################################################




################################
# QUESTION AND ANSWER SECTION #
###############################

# This section is where most of the logic happens
# The check_guess function takes in 9 arguments

   
# Checks Wether guess is correct, inncorect or is a pass
def check_guess(answer, guess, lives, question_num, questions_score, passed_on, btn, bg, username):
  
  status = ""
  
  # This function is used to construct the url that is then passed back to the question function
  def url(status, question_num, questions_score, passed_on, btn, bg, guess, lives):
    return redirect("/questions/" + status + "/" + question_num + "/" + questions_score + "/" + passed_on + "/" + lives + "/" + guess + "/" + btn + "/" + bg + "/" + username)
 
  # If the guess is correct the following happens
  # the .lower() and .replace() is used to strip the spaces and make the user input lowercase
  # This means the question will match the answer even if they use capital letters
  # Most mobile phones will give a capital letter when typing in a text field
  if( guess.replace(" ", "").lower() == answer.replace(" ", "").lower() ):
    questions_score = str(int(questions_score) + 50)
    question_num = str(int(question_num) + 1)
    
    # Checks if all the question have been asked
    if (check_question_num(question_num)):
      question_num = str(int(question_num) - 1)
      status = "game-over"
      bg = "4cff95"
      return url(status, question_num, questions_score, passed_on, btn, bg, guess, lives)
      
    status = "correct"
    bg = "4cff95"
    return url(status, question_num, questions_score, passed_on, btn, bg, guess, lives)
    
  
  # Checks if pass has been pressed
  # There are three outcomes if this happens
  # If they pass on last question the game will end
  elif ( guess == "pass" ):
    status = "pass"
    question_num = str(int(question_num) + 1)
    if (check_question_num(question_num)):
      question_num = str(int(question_num) - 1)
      status = "game-over"
      bg = "0"
      return url(status, question_num, questions_score, passed_on, btn, bg, guess, lives)
    
    # If they pass for a second time the pass button will change colour to warn them
    passed_on = str(int(passed_on) + 1)
    if ( int(passed_on) == 2 ):
      btn = "warning"
    
    # If they pass for a third time, they will lose a life
    elif ( int(passed_on) == 3 ):
      lives = str(int(lives) - 1)
      if ( int(lives) == 0 ):
        question_num = str(int(question_num) - 1)
        bg = "FF4D4C"
        status = "game-over"
        return url(status, question_num, questions_score, passed_on, btn, bg, guess, lives)
        
      passed_on = "0"
      btn = "primary"
      bg = "FF4D4C"
      
    # If it's their first pass, nothing happens, they just move to the next question 
    else:
      btn = "primary"
      bg = "0"
    return url(status, question_num, questions_score, passed_on, btn, bg, guess, lives)
    
  # If guess is blank they will be told to enter a guess
  elif ( guess == "" ):
    status = "blank"
    guess = "0"
    bg = "0s"
    return url(status, question_num, questions_score, passed_on, btn, bg, guess, lives)
    
  # If they get the question wrong they will lose a life
  # If they have no lives left the game will end
  else:
    status = "wrong"
    lives = str(int(lives) - 1)
    if ( int(lives) == 0 ):
        bg = "FF4D4C"
        status = "game-over"
        return url(status, question_num, questions_score, passed_on, btn, bg, guess, lives)
    bg = "FF4D4C"
    return url(status, question_num, questions_score, passed_on, btn, bg, guess, lives)
    
    
###############################################################
    


################################
# END OF GAME #
###############################

# Add username and score to final_scores.txt  
def check_final_scores(username):
  
  # open final_scores.txt and check wether the username is already there
  users = []
  with open("data/final_scores.txt", "r") as file:
    lines = file.read().splitlines()
      
  for i, text in enumerate(lines):
    if i%2 == 0:
      users.append(text)
        
  for user in users:
    if user.replace(" ", "").lower() == username.replace(" ", "").lower():
      return False
      
  return True
      
      
#save final score and username in final_scores.txt
def save_final_scores(username, questions_score):
  with open("data/final_scores.txt", "a") as file:
    file.write("{0}\n".format(username))
    file.write("{0}\n".format(questions_score))
      
  
# Show All Final Scores and Users    
def show_final_scores():
    users = []
    scores = []
    
    # reads final_scores.txt and splits even lines into users and odd lines into scores
    with open("data/final_scores.txt", "r") as file:
        lines = file.read().splitlines()
        
    for i, text in enumerate(lines):
        if i%2 == 0:
            users.append(text)
        else:
            scores.append(text)
        
    #The zip() function gives a user and score tuple 
    users_and_scores = zip(users, scores)
    
    # The following code was produced with the help of PythonCentral (https://www.pythoncentral.io/how-to-sort-a-list-tuple-or-object-with-sorted-in-python/)
    def getKey(item):
      return int(item[1])
      
    users_and_scores_sorted = sorted(users_and_scores, key=getKey, reverse=True)
      
    return users_and_scores_sorted
    
###############################################################



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
    return render_template("index.html", userText=userText)
    

# This is the main url route for the game
# All of the info that is needed is passed to the url
# Another way to pass info, is through sessions, although I choose to use this method.
# It works well for this situation. If the information is more sensitive I would have use sessions
@app.route('/questions/<status>/<question_num>/<questions_score>/<passed_on>/<lives>/<guess>/<btn>/<bg>/<username>', methods=["GET", "POST"])
def questions(status, question_num, questions_score, passed_on, lives, guess, btn, bg, username):
  questions = get_questions()
  q_num = int(question_num) - 1
  question = questions[0][q_num]
  answer = questions[1][q_num]
  message = ""
  
  
  if ( status == "blank" ):
    message = "Please submit a guess or press pass to continue"
  elif ( status == "wrong" ):
    message = "'{0}', Was Incorrect".format(guess)
  elif ( status == "pass" ):
    message = "Question Passed"
  elif ( status == "game-over" ):
    
    if check_final_scores(username) :
      save_final_scores(username, questions_score)
      
    userScores = show_final_scores()
    return render_template(
    "game-over.html",
    lives=lives,
    questionNum=question_num,
    score=questions_score,
    bg=bg,
    username=username,
    questionsAnswers=zip(questions[0],questions[1]),
    userScores=userScores
    )
    
    
  # Take the info form the form on the frontend.  
  if request.method == "POST":
    guess = request.form["answer"]
    
    url = check_guess(answer, guess, lives, question_num, questions_score, passed_on, btn, bg, username)
    
    return url
    
  return render_template(
    "question.html",
    message=message,
    question=question,
    lives=lives,
    questionNum=question_num,
    score=questions_score,
    passed=passed_on,
    bg=bg,
    btn=btn,
    username=username
    ) 
    
    
    
    
@app.route('/instructions')
def instructions():
  return render_template("instructions.html")
    
@app.route('/leaderboard')
def leaderboard():
  userScores = show_final_scores()
  return render_template(
  "leaderboard.html",
  userScores=userScores
  )
    

app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)