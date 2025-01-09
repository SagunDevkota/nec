from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

def parse_mcq_file(filepath, shuffle=False):
    questions = []
    
    with open(filepath, 'r') as file:
        lines = file.readlines()
    
    question = {}
    
    for line in lines:
        line = line.strip()
        
        if line.startswith("Answer:"):
            question["answer"] = line.replace("Answer:", "").strip()
            questions.append(question)
            question = {}
        elif line.startswith(("A)", "B)", "C)", "D)", "a)", "b)", "c)", "d)","A.", "B.", "C.", "D.", "a.", "b.", "c.", "d.","(A)", "(B)", "(C)", "(D)", "(a)", "(b)", "(c)", "(d)")):
            question["options"].append(line)
        elif line:
            if "question" not in question:
                question["question"] = line
                question["options"] = []
            else:
                # Append to the question if it's multi-line
                question["question"] += " " + line
    
    if(shuffle):
	    # Randomize the order of the questions
	    random.shuffle(questions)

    return questions

# Load questions from file
mcq_file_path = "mcq_test.txt"  # Replace with your file path
global_questions = None

@app.route("/", methods=["GET", "POST"])
def mcq_test():
    global global_questions

    if request.method == "POST":
        user_answers = request.form
        score = 0
        results = []
        for i, question in enumerate(global_questions):
            correct_answer = question["answer"]
            user_answer = user_answers.get(f"question_{i+1}", "No answer")
            is_correct = correct_answer == user_answer
            if is_correct:
                score += 1
            results.append({
                "question": question["question"],
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct
            })
        return render_template("result.html", results=results, score=score, total=len(global_questions))
    else:
    	questions = parse_mcq_file(mcq_file_path, shuffle=True)
    	global_questions = questions
    
    return render_template("mcq.html", questions=questions)


if __name__ == "__main__":
    app.run(debug=True)