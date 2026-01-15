def check_eligibility(percentage):
    exams = []

    if percentage >= 75:
        exams.append("JEE")
    if percentage >= 50:
        exams.append("NEET")
    if percentage >= 60:
        exams.append("NDA")

    return exams
