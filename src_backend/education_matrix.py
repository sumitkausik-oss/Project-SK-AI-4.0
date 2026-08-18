"""
SK Enterprises | Universal STEM & Higher Education Cognitive Engine
Founder, Inventor & Sole Architect: Sumit Kumar
Platform V5.0 — Domain Hub: Education Matrix
"""
import random

# ──────────────────────────────────────────────────
# NCERT Subject Database (Class 1-12)
# ──────────────────────────────────────────────────
NCERT_SYLLABUS = {
    "Class 6-8": {
        "Science": ["Motion & Measurement", "Light", "Electricity", "Matter", "Cells & Living World"],
        "Mathematics": ["Integers", "Fractions", "Algebra", "Geometry", "Data Handling"],
        "Social Science": ["History of Medieval India", "Geography: Resources", "Political Science"]
    },
    "Class 9-10": {
        "Physics": ["Motion & Laws", "Gravitation", "Work & Energy", "Sound", "Light"],
        "Chemistry": ["Matter", "Atoms & Molecules", "Chemical Reactions", "Acids & Bases", "Metals"],
        "Biology": ["Cell", "Tissues", "Control & Coordination", "Reproduction", "Heredity"],
        "Mathematics": ["Number Systems", "Polynomials", "Coordinate Geometry", "Triangles", "Statistics"]
    },
    "Class 11-12": {
        "Physics": ["Kinematics", "Laws of Motion", "Work-Energy-Power", "Thermodynamics",
                    "Oscillations", "Electrostatics", "Current Electricity", "Optics", "Modern Physics"],
        "Chemistry": ["Atomic Structure", "Chemical Bonding", "Thermodynamics", "Equilibrium",
                      "Redox", "Organic Chemistry", "Biomolecules", "Polymers"],
        "Biology": ["Cell Biology", "Genetics", "Evolution", "Human Physiology", "Plant Physiology",
                    "Ecology", "Biotechnology"],
        "Mathematics": ["Sets & Functions", "Algebra", "Coordinate Geometry", "Calculus",
                        "Vector Algebra", "3D Geometry", "Statistics & Probability"]
    }
}

# ──────────────────────────────────────────────────
# JEE Main / Advanced PCM Question Bank Stubs
# ──────────────────────────────────────────────────
JEE_TOPICS = {
    "Physics": [
        {"topic": "Kinematics", "level": "JEE Main",
         "q": "A ball is thrown vertically upward with velocity 20 m/s. Time to reach maximum height?",
         "options": ["1s", "2s", "4s", "3s"], "ans": "2s",
         "hint": "Use v = u + at → 0 = 20 - 10t → t = 2s"},
        {"topic": "Laws of Motion", "level": "JEE Advanced",
         "q": "Two blocks of masses 3 kg and 5 kg are connected by a string on a frictionless surface. Force applied is 16 N. Find acceleration.",
         "options": ["1 m/s²", "2 m/s²", "3 m/s²", "4 m/s²"], "ans": "2 m/s²",
         "hint": "a = F / (m1 + m2) = 16 / 8 = 2 m/s²"},
        {"topic": "Optics", "level": "JEE Main",
         "q": "A concave mirror has focal length 10 cm. Object placed at 30 cm. Find image distance.",
         "options": ["-15 cm", "+15 cm", "-20 cm", "+20 cm"], "ans": "-15 cm",
         "hint": "1/v + 1/u = 1/f → 1/v = 1/(-10) - 1/(-30) = -3+1/30 → v = -15 cm"}
    ],
    "Chemistry": [
        {"topic": "Atomic Structure", "level": "JEE Main",
         "q": "Number of radial nodes in 3p orbital?",
         "options": ["0", "1", "2", "3"], "ans": "1",
         "hint": "Radial nodes = n - l - 1 = 3 - 1 - 1 = 1"},
        {"topic": "Chemical Bonding", "level": "JEE Advanced",
         "q": "Shape of XeF4?",
         "options": ["Tetrahedral", "Square planar", "See-saw", "T-shaped"], "ans": "Square planar",
         "hint": "XeF4 has 2 lone pairs on Xe → VSEPR → Square planar"}
    ],
    "Mathematics": [
        {"topic": "Calculus", "level": "JEE Main",
         "q": "∫(x² + 3x) dx = ?",
         "options": ["x³/3 + 3x²/2 + C", "2x + 3 + C", "x³ + 3x² + C", "x²/2 + 3 + C"],
         "ans": "x³/3 + 3x²/2 + C",
         "hint": "Integrate term by term: x³/3 + 3x²/2 + C"},
        {"topic": "Vectors", "level": "JEE Advanced",
         "q": "If |a⃗| = 3, |b⃗| = 4 and a⃗ · b⃗ = 6, find angle between them.",
         "options": ["30°", "45°", "60°", "90°"], "ans": "60°",
         "hint": "cos θ = a·b / (|a||b|) = 6/(3×4) = 0.5 → θ = 60°"}
    ]
}

# ──────────────────────────────────────────────────
# NEET Medical Question Bank Stubs
# ──────────────────────────────────────────────────
NEET_TOPICS = {
    "Biology": [
        {"topic": "Cell Biology", "level": "NEET",
         "q": "The powerhouse of the cell is?",
         "options": ["Nucleus", "Mitochondria", "Ribosome", "Golgi body"], "ans": "Mitochondria",
         "hint": "Mitochondria produce ATP via oxidative phosphorylation"},
        {"topic": "Genetics", "level": "NEET",
         "q": "In Mendel's dihybrid cross, phenotypic ratio in F2 is?",
         "options": ["9:3:3:1", "3:1", "1:2:1", "1:1:1:1"], "ans": "9:3:3:1",
         "hint": "Two independent traits → 9:3:3:1 phenotypic ratio in F2"}
    ],
    "Physics": [
        {"topic": "Human Eye", "level": "NEET",
         "q": "The far point of a myopic eye is 80 cm. Power of corrective lens?",
         "options": ["-1.25 D", "+1.25 D", "-2.5 D", "+2.5 D"], "ans": "-1.25 D",
         "hint": "P = 1/f (m). Concave lens needed. f = -80 cm = -0.8 m → P = -1.25 D"}
    ]
}

# ──────────────────────────────────────────────────
# Engineering Library (B.Tech Core)
# ──────────────────────────────────────────────────
BTECH_MODULES = {
    "Computer Science": ["Data Structures", "DBMS", "OS", "Computer Networks",
                         "Theory of Computation", "Compiler Design", "Software Engineering"],
    "Mechanical": ["Thermodynamics", "Fluid Mechanics", "Manufacturing Processes",
                   "Strength of Materials", "Theory of Machines"],
    "Electrical": ["Circuit Theory", "Electromagnetic Fields", "Power Systems",
                   "Machines", "Control Systems"],
    "Civil": ["Structural Analysis", "Geotechnical Engineering", "Fluid Mechanics",
              "Transportation", "Construction Management"]
}


class UniversalSTEMMatrix:
    """
    SK Enterprises — Universal STEM Engine
    Serves NCERT, JEE, NEET, B.Tech queries.
    Inventor: Sumit Kumar
    """

    @staticmethod
    def get_ncert_topics(class_range: str, subject: str = None) -> dict:
        if class_range not in NCERT_SYLLABUS:
            return {"error": f"Class range '{class_range}' not found.", "available": list(NCERT_SYLLABUS.keys())}
        data = NCERT_SYLLABUS[class_range]
        if subject:
            subj_data = {k: v for k, v in data.items() if subject.lower() in k.lower()}
            return {"class_range": class_range, "subject": subject, "topics": subj_data or data}
        return {"class_range": class_range, "topics": data}

    @staticmethod
    def generate_jee_questions(subject: str = "Physics", count: int = 3,
                               level: str = "JEE Main") -> dict:
        bank = JEE_TOPICS.get(subject, JEE_TOPICS["Physics"])
        filtered = [q for q in bank if q["level"] == level] or bank
        sampled = (filtered * (count // len(filtered) + 1))[:count]
        return {
            "exam": "JEE",
            "subject": subject,
            "level": level,
            "question_count": count,
            "questions": sampled,
            "generated_by": "Universal STEM Matrix — Sumit Kumar (SK Enterprises)"
        }

    @staticmethod
    def generate_neet_questions(subject: str = "Biology", count: int = 2) -> dict:
        bank = NEET_TOPICS.get(subject, NEET_TOPICS["Biology"])
        sampled = (bank * (count // len(bank) + 1))[:count]
        return {
            "exam": "NEET",
            "subject": subject,
            "question_count": count,
            "questions": sampled,
            "generated_by": "Universal STEM Matrix — Sumit Kumar (SK Enterprises)"
        }

    @staticmethod
    def get_btech_syllabus(branch: str = "Computer Science") -> dict:
        branch_data = BTECH_MODULES.get(branch)
        if not branch_data:
            return {"error": f"Branch '{branch}' not found.", "available": list(BTECH_MODULES.keys())}
        return {
            "branch": branch,
            "core_subjects": branch_data,
            "generated_by": "Universal STEM Matrix — Sumit Kumar (SK Enterprises)"
        }

    @staticmethod
    def analyze_student_performance(correct: int, total: int, exam: str = "JEE Main") -> dict:
        pct = round((correct / total) * 100, 2) if total > 0 else 0
        grade = ("Excellent 🏆" if pct >= 80 else
                 "Good ✅" if pct >= 60 else
                 "Needs Improvement 📚" if pct >= 40 else
                 "Critical — Revise Fundamentals ⚠️")
        return {
            "exam": exam,
            "score": f"{correct}/{total}",
            "percentage": pct,
            "grade": grade,
            "recommendation": f"Focus on weak topics. Current performance: {grade}",
            "generated_by": "Universal STEM Matrix — Sumit Kumar (SK Enterprises)"
        }
