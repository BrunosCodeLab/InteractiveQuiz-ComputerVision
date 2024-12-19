# Interactive Quiz - Computer Vision ![Project Views](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FBrunosCodeLab%2FInteractiveQuiz-ComputerVision&count_bg=%235C9CFF&title_bg=%23008FC9&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)

<div align="center">
    <img src="https://github.com/BrunosCodeLab/Images/blob/main/InteractiveQuiz-CV/Interactive%20Quiz%20GIF.gif" alt="Banner" width="800" />
</div> 


## How It Works

This interactive quiz is implemented using Python and several libraries, including `cv2`, `csv`, `cvzone`, `sys`, and `random`. Follow these steps to get started:

1. Install the required packages listed in the `requirements.txt` file.
2. The program initializes by loading the necessary libraries and configuring the webcam to capture frames.

After initializing the hand detector (`HandDetector`), the program loads questions and answers from the `QnA.csv` file, creating objects for each question and answer. The questions are shuffled, and the first five are selected and stored in the `selectedQuestions` list.


##

### Main Program Flow

1. **Frame Processing**  
   Each webcam frame is captured and processed. The program detects the hand using `detector.findHands(img)` and identifies finger orientations to select an answer for the current question.
<br><br>
<div align="center">
    <img src="https://raw.githubusercontent.com/BrunosCodeLab/Images/refs/heads/main/InteractiveQuiz-CV/Hand.png" alt="Hand" width="800" />
</div>
<br><br>

2. The **finger orientation is stored** in the `selection` variable, where:
   - One raised finger corresponds to `1`,
   - Two raised fingers correspond to `2`,
   - And so on.
<br><br>
<div align="center">
    <img src="https://github.com/BrunosCodeLab/Images/blob/main/InteractiveQuiz-CV/Hands_Numbers.png" alt="Hands_Numbers" width="800" />
</div>
<br><br>

`selection` variable is compared to the correct answer stored in the `QnA.csv` file to determine if the player's choice is correct.
Example:

<br>
<div align="center">
    <img src="https://raw.githubusercontent.com/BrunosCodeLab/Images/refs/heads/main/InteractiveQuiz-CV/QnA_logic.png" alt="QnA_Logic" width="800" />
</div>
<br>

3. **Displaying Questions and Answers**  
   Questions and answers are displayed on the screen. Before this, the program ensures the current question index (`qNo`) is less than the total number of questions (`qTotal`). Information about the current question is stored in the `qna` variable, containing data from `selectedQuestions[qNo]`.

4. **Answer Selection and Feedback**  
   - When a hand gesture is detected, an ellipse is drawn around the selected answer. This provides players time to reconsider their choice.
   - The answer is finalized after three seconds (or 60 frames), when the ellipse completes a full rotation.
   - The program compares the `selection` with the correct answer (`qna.answer`):
     - **Correct Answer**: The score increases by 1, and the next question is loaded.
     - **Incorrect Answer**: No points are added, but the next question is still loaded.
   - After each selection, the selection timer (`counter`) resets, and a brief pause ensures no duplicate answers are recorded.

5. **Scoring System**  
   The program tracks the player’s answers, including:
   - Correct answers
   - Selected answers
   - Corresponding questions  

****
