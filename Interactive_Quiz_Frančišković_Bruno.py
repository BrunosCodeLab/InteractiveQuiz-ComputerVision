# pip install -r requirements.txt

import cv2
import csv
from cvzone.HandTrackingModule import HandDetector
import cvzone
import random
import sys

cap = cv2.VideoCapture(0) # 0 - default camera
cap.set(3,640) # Camera width
cap.set(4, 480) # Camera height

# Hand detector initialization
detector = HandDetector(detectionCon=0.8, maxHands=1)

class QnA():
    def __init__(self,data):
        self.question = data[0] # The question is at position 0 in the line
        self.choice1 = data[1] # Answer number 1
        self.choice2 = data[2] # Answer number 2
        self.choice3 = data[3] # Answer number 3
        self.choice4 = data[4] # Answer number 4
        self.answer = int(data[5]) # Correct answer

# Importing CSV
pathCSV = "QnA.csv" 
with open(pathCSV, newline='\n', encoding='utf-8') as f:
    reader = csv.reader(f)
    dataAll = list(reader)[1:] # Starts from the first question, without a header

# Creating an object for each question and answer (QnA)
QnAList = []
for q in dataAll:
    QnAList.append(QnA(q)) # Each object in QnAList represents one question with its answers

# Mixing questions and selecting the first 'X' questions. In this case 5
random.shuffle(QnAList) 
selectedQuestions = QnAList[:5] # Defining the number of questions in the quiz

qNo = 0 # Question number
qTotal = len(selectedQuestions) # Number of questions in the quiz saved in a variable

selection = -1 # Initialization of the selection, number different from the existing ones: 1,2,3 and 4
counter = 0 # The counter we use until the circle around the answer is filled
counterPause = 0 # Enables a pause between two answers
selectionSpeed = 5 # The speed with which the circle will close around the answer
modePositions = [(810,200), (810,350), (810,500), (810,650)] # Answer positions
score=0 # Current quiz score

# The main part of the code
while True:
    # Recording every frame from the webcam
    success, img = cap.read() # 'success' will be True if the frame was successfully recorded, 'img' contains the web camera
    img = cv2.resize(img, (640, 480)) # Changing the size of the camera to match the one defined at the beginning of the code

    # Finding the hand in the current frame
    hands, img = detector.findHands(img)

    if qNo < qTotal: # Checking if the current number of questions is less than the total number of questions
        qna = selectedQuestions[qNo] # Contains information about the current issue

    imgBackground = cv2.imread(r"Background.png") 

    imgBackground, bbox = cvzone.putTextRect(imgBackground, qna.question,[500,80],
                                    2, 2, offset=20, border=2, 
                                    colorR=(0,0,0), colorB=(255,255,255), colorT=(255,255,255))

    imgBackground, bbox = cvzone.putTextRect(imgBackground, qna.choice1,[900,210],
                                    2, 2, offset=20, border=2, 
                                    colorR=(0,0,0), colorB=(255,255,255), colorT=(255,255,255))
    
    imgBackground, bbox = cvzone.putTextRect(imgBackground, qna.choice2,[900,360],
                                    2, 2, offset=20, border=2, 
                                    colorR=(0,0,0), colorB=(255,255,255), colorT=(255,255,255))
    
    imgBackground, bbox = cvzone.putTextRect(imgBackground, qna.choice3,[900,510],
                                    2, 2, offset=20, border=2, 
                                    colorR=(0,0,0), colorB=(255,255,255), colorT=(255,255,255))

    imgBackground, bbox = cvzone.putTextRect(imgBackground, qna.choice4,[900,660],
                                    2, 2, offset=20, border=2, 
                                    colorR=(0,0,0), colorB=(255,255,255), colorT=(255,255,255))
    

    
    if hands and counterPause == 0:

        # Getting information for the first discovered hand
        hand1 = hands[0]  # First hand detection

        # The number of fingers that are oriented upwards for the first hand
        fingers1 = detector.fingersUp(hand1)
        print(f'{fingers1}')  # Print the position of the hand/fingers in the air

        if fingers1 == [0, 1, 0, 0, 0]: # Number 1 shown by hand
            if selection != 1:
                counter = 1
            selection = 1

        elif fingers1 == [0, 1, 1, 0, 0]: # Number 2 shown by hand
            if selection != 2:
                counter = 1
            selection = 2

        elif fingers1 == [0, 1, 1, 1, 0]: # Number 3 shown by hand
            if selection != 3:
                counter = 1
            selection = 3

        elif fingers1 == [0, 1, 1, 1, 1]: # Number 4 shown by hand
            if selection != 4:
                counter = 1
            selection = 4
        
        else: # If there is no hand, hands is empty or counterPause is not 0
            selection = -1 # A value that does not match any answer
            counter = 0 # Returning the counters to the beginning

        if counter > 0: # If the counter is greater than 0, the position of the finger is recognized
            counter += 1 # Increase the counters by 1
            print(counter) # Printing of the reservation

            cv2.ellipse(imgBackground, modePositions[selection-1], (50,50), 0, 0,
                         counter*selectionSpeed, (0,255,0), 10) # Drawing an ellipse on the image imgBackground

            # If counter*selectionSpeed>360 "lock" is the response
            if counter*selectionSpeed>360: # If the angle of the ellipse is greater than 360 degrees
                if selection == qna.answer: # If the selection is equal to the correct answer
                    qNo +=1         # Next question
                    counter = 0     # Counter reset
                    selection = -1  # Reset selection
                    score+=1        # Increasing results
                    counterPause = 1  # Pauses before the system accepts the same answer again

                elif selection != qna.answer: # If the selection is not equal to the correct answer
                    qNo +=1         # Next question
                    counter = 0     # Resetiranje brojaca
                    selection = -1  # Reset selection
                    counterPause = 1 # Pauses before the system accepts the same answer again


    finalScore = round((score / qTotal) * 100, 2) # Calculation of the current total result
    #print(f'This is your score {finalScore}%')

    if counterPause > 0: # If it is greater than 0
        counterPause += 1 # Increase by 1
        if counterPause > 60: # Pause until > 60 is reached
            counterPause = 0 # if hands and counterPause == 0:' the program is executed again


    # Draw a progress bar
    barWidth = 645
    barHeight = 50
    barX = 50
    barY = 650

    barCenterX = barX + barWidth // 2
    barCenterY = barY + barHeight // 2

    # Calculation that the value of the bar (barValue) does not exceed the right limit
    barValue = min(barX + (barWidth // qTotal) * qNo, barX + barWidth) 

    # Progress is filled in green
    cv2.rectangle(imgBackground, (barX, barY), (barValue, barY + barHeight), (0, 255, 0), cv2.FILLED)
    # Frame of the progress bar
    cv2.rectangle(imgBackground, (barX, barY), (barX + barWidth, barY + barHeight), (0, 0, 0), 5) 

    percentage = round((qNo / qTotal) * 100) # Quiz solution percentage

    # Shows how many % of quizzes have been solved
    imgBackground, _ = cvzone.putTextRect(imgBackground, f'{percentage}% is completed', [55, 80],
                                        2, 2, offset=20, border=2, 
                                        colorR=(0, 0, 0), colorB=(255, 255, 255), colorT=(255, 255, 255))   


    if percentage == 100:

            imgBackground = cv2.imread(r"BackgroundFin.png") 

            imgBackground, _ = cvzone.putTextRect(imgBackground, f'{percentage}% has been completed', [150, 80],
                                            2, 2, offset=20, border=2, 
                                            colorR=(0, 0, 0), colorB=(255, 255, 255), colorT=(255, 255, 255))
            
            imgBackground, _ = cvzone.putTextRect(imgBackground, 'Thanks for playing!', [210, 680],
                                            2, 2, offset=20, border=2, 
                                            colorR=(0, 0, 0), colorB=(255, 255, 255), colorT=(255, 255, 255))
            
            imgBackground, _ = cvzone.putTextRect(imgBackground, "The Quiz is over!", [875, 250],
                                                        2, 2, offset=20, border=2, 
                                                        colorR=(0,0,0), colorB=(255,255,255), colorT=(255,255,255))
                    
            imgBackground, _ = cvzone.putTextRect(imgBackground, f'Your final score is: {finalScore}%', [780, 350],
                                                        2, 2, offset=20, border=2, 
                                                        colorR=(0,0,0), colorB=(255,255,255), colorT=(255,255,255))
            
            imgBackground, _ = cvzone.putTextRect(imgBackground, "Exit -> 'Q'", [930, 450],
                                                        2, 2, offset=20, border=2, 
                                                        colorR=(0,0,0), colorB=(255,255,255), colorT=(255,255,255))            


    key = cv2.waitKey(1) & 0xFF # 'q' key
    
    if chr(key).lower() == 'q': # If the 'q' key is pressed
        cv2.destroyAllWindows() 
        sys.exit()


    # Overlay webcam video on background image
    imgBackground[139:139+480, 50:50+640] = img

    cv2.imshow("IT Quiz", imgBackground)
    cv2.waitKey(1)