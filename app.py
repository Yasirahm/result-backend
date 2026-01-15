from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

df = pd.read_csv("data/result.csv")
TOTAL_MARKS = 500

def value_in_society(percentage):
    if percentage >= 90:
        return "Excellent"
    elif percentage >= 75:
        return "Very Good"
    elif percentage >= 60:
        return "Good"
    else:
        return "Average"

def after_10th_guidance(percentage):
    if percentage >= 85:
        return {
            "stream": "Science",
            "career": "Engineering / Medical / Research",
            "skills": "Mathematics, Science, Logical thinking",
            "readiness": "High",
            "message": "You have strong potential. Stay focused."
        }
    elif percentage >= 70:
        return {
            "stream": "Science or Commerce",
            "career": "Engineering / IT / Commerce",
            "skills": "Problem solving, Computer basics",
            "readiness": "Medium",
            "message": "Consistency will take you far."
        }
    elif percentage >= 60:
        return {
            "stream": "Commerce",
            "career": "Business / Banking / IT",
            "skills": "Accounts, Communication",
            "readiness": "Medium",
            "message": "Skills matter more than marks."
        }
    else:
        return {
            "stream": "Arts",
            "career": "Govt Jobs / Arts / Skill-based fields",
            "skills": "Communication, General knowledge",
            "readiness": "Growing",
            "message": "Never underestimate yourself."
        }

@app.route("/api/result", methods=["GET"])
def get_result():
    roll = request.args.get("roll")

    if not roll:
        return jsonify({"error": "Roll number required"}), 400

    student = df[df["roll_number"] == int(roll)]
    if student.empty:
        return jsonify({"error": "Roll number not found"}), 404

    student = student.iloc[0]
    marks = int(student["marks"])
    percentage = round((marks / TOTAL_MARKS) * 100, 2)

    same_marks_students = (
        df[(df["marks"] == marks) & (df["roll_number"] != int(roll))]
        [["roll_number", "name"]]
        .to_dict(orient="records")
    )

    return jsonify({
        "roll_number": roll,
        "name": student["name"],
        "marks": marks,
        "percentage": percentage,
        "value_in_society": value_in_society(percentage),
        "after_10th_guidance": after_10th_guidance(percentage),
        "same_marks_students": same_marks_students
    })

@app.route("/")
def home():
    return "Result API is running"

if __name__ == "__main__":
    app.run(debug=True)
