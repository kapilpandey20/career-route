from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import ResumeForm
from .models import Resume, Career

from pypdf import PdfReader
import pytesseract
from pdf2image import convert_from_path

import re


# =========================================================
# CONFIGURATION
# =========================================================

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

POPPLER_PATH = (
    r"C:\Users\kapil\Downloads"
    r"\Release-26.02.0-0"
    r"\poppler-26.02.0"
    r"\Library\bin"
)

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# =========================================================
# SKILLS DATABASE
# =========================================================

SKILLS_LIST = [
    "Python",
    "Java",
    "JavaScript",
    "HTML",
    "CSS",
    "Django",
    "SQL",
    "MySQL",
    "Git",
    "GitHub",
    "React",
    "C++",
    "C",
    "Machine Learning",
    "Data Science",
    "Pandas",
    "NumPy",
    "Flask",
    "Bootstrap",
    "MongoDB",
    "PostgreSQL",
    "PHP",
    "REST API",
    "Matplotlib",
    "Scikit-learn",
    "TensorFlow",
    "Node.js",
    "Express.js",
]


# =========================================================
# LEARNING ROADMAP DATABASE
# =========================================================

ROADMAP_DATA = {

    "Python": {
        "level": "Foundation",
        "duration": "1-2 weeks",
        "topics": [
            "Python syntax and data types",
            "Conditions and loops",
            "Functions",
            "Lists, tuples, sets and dictionaries",
            "Object-oriented programming",
            "File handling",
            "Exception handling"
        ],
        "project": "Build a Python Expense Tracker or Student Management System."
    },

    "Data Science": {
        "level": "Foundation",
        "duration": "2-3 weeks",
        "topics": [
            "Data Science fundamentals",
            "Data collection and preprocessing",
            "Exploratory Data Analysis (EDA)",
            "Data visualization",
            "Statistics basics",
            "Feature understanding",
            "Working with real-world datasets"
        ],
        "project": "Analyze a real-world dataset and create an EDA dashboard."
    },

    "Pandas": {
        "level": "Foundation",
        "duration": "1 week",
        "topics": [
            "Series and DataFrame",
            "Reading CSV and Excel files",
            "Data filtering",
            "Sorting and grouping",
            "Missing value handling",
            "Data cleaning",
            "Data aggregation"
        ],
        "project": "Create a Sales Data Analysis project using Pandas."
    },

    "NumPy": {
        "level": "Foundation",
        "duration": "4-7 days",
        "topics": [
            "NumPy arrays",
            "Array indexing",
            "Array slicing",
            "Mathematical operations",
            "Broadcasting",
            "Statistical operations",
            "Matrix operations"
        ],
        "project": "Build a numerical data analysis project using NumPy."
    },

    "SQL": {
        "level": "Foundation",
        "duration": "1-2 weeks",
        "topics": [
            "Database fundamentals",
            "SELECT queries",
            "WHERE and ORDER BY",
            "GROUP BY and HAVING",
            "JOIN operations",
            "Subqueries",
            "Aggregate functions"
        ],
        "project": "Build a Student or Employee Database Management System."
    },

    "Machine Learning": {
        "level": "Intermediate",
        "duration": "3-4 weeks",
        "topics": [
            "Machine Learning fundamentals",
            "Supervised learning",
            "Unsupervised learning",
            "Training and testing datasets",
            "Feature engineering",
            "Model evaluation",
            "Overfitting and underfitting"
        ],
        "project": "Build a machine learning model for prediction using a real-world dataset."
    },

    "Matplotlib": {
        "level": "Foundation",
        "duration": "3-5 days",
        "topics": [
            "Line charts",
            "Bar charts",
            "Scatter plots",
            "Histograms",
            "Pie charts",
            "Labels and legends",
            "Data visualization"
        ],
        "project": "Create a data visualization dashboard using Matplotlib."
    },

    "Scikit-learn": {
        "level": "Intermediate",
        "duration": "1-2 weeks",
        "topics": [
            "Scikit-learn workflow",
            "Data preprocessing",
            "Train-test split",
            "Regression models",
            "Classification models",
            "Clustering",
            "Model evaluation"
        ],
        "project": "Build a classification or regression machine learning project."
    },

    "Java": {
        "level": "Foundation",
        "duration": "2-3 weeks",
        "topics": [
            "Java syntax",
            "OOP concepts",
            "Classes and objects",
            "Inheritance",
            "Polymorphism",
            "Exception handling",
            "Collections"
        ],
        "project": "Build a Java-based Student Management System."
    },

    "JavaScript": {
        "level": "Foundation",
        "duration": "2 weeks",
        "topics": [
            "Variables and data types",
            "Functions",
            "Arrays and objects",
            "DOM manipulation",
            "Events",
            "ES6 features",
            "Fetch API"
        ],
        "project": "Build an interactive web application using JavaScript."
    },

    "HTML": {
        "level": "Foundation",
        "duration": "3-5 days",
        "topics": [
            "HTML structure",
            "Forms",
            "Tables",
            "Semantic elements",
            "Links and images",
            "Accessibility basics"
        ],
        "project": "Create a professional portfolio website."
    },

    "CSS": {
        "level": "Foundation",
        "duration": "1 week",
        "topics": [
            "Selectors",
            "Box model",
            "Flexbox",
            "Grid",
            "Responsive design",
            "Animations",
            "Media queries"
        ],
        "project": "Create a responsive portfolio website."
    },

    "Django": {
        "level": "Intermediate",
        "duration": "2-3 weeks",
        "topics": [
            "Django project structure",
            "Models",
            "Views",
            "Templates",
            "Forms",
            "Authentication",
            "Django ORM",
            "REST APIs"
        ],
        "project": "Build a complete Django web application."
    },

    "React": {
        "level": "Intermediate",
        "duration": "2-3 weeks",
        "topics": [
            "Components",
            "Props",
            "State",
            "Hooks",
            "Events",
            "API integration",
            "React Router"
        ],
        "project": "Build a React-based job or career dashboard."
    },

    "Git": {
        "level": "Foundation",
        "duration": "3-5 days",
        "topics": [
            "Git basics",
            "Repositories",
            "Commit",
            "Branch",
            "Merge",
            "Pull and push",
            "Conflict resolution"
        ],
        "project": "Upload and manage one complete project using Git."
    },

    "GitHub": {
        "level": "Foundation",
        "duration": "2-3 days",
        "topics": [
            "GitHub repositories",
            "README files",
            "Branches",
            "Pull requests",
            "Issues",
            "Project documentation"
        ],
        "project": "Create a professional GitHub repository for your final-year project."
    },

    "MySQL": {
        "level": "Foundation",
        "duration": "1 week",
        "topics": [
            "Database creation",
            "Tables",
            "CRUD operations",
            "Primary keys",
            "Foreign keys",
            "Joins",
            "Indexes"
        ],
        "project": "Create a MySQL-based management system."
    },

    "PostgreSQL": {
        "level": "Intermediate",
        "duration": "1 week",
        "topics": [
            "PostgreSQL basics",
            "Tables",
            "Relationships",
            "Queries",
            "Indexes",
            "Transactions"
        ],
        "project": "Connect PostgreSQL with a Django application."
    },

    "MongoDB": {
        "level": "Intermediate",
        "duration": "1 week",
        "topics": [
            "MongoDB basics",
            "Documents",
            "Collections",
            "CRUD operations",
            "Queries",
            "Aggregation"
        ],
        "project": "Build a Node.js + MongoDB CRUD application."
    },

    "Flask": {
        "level": "Intermediate",
        "duration": "1-2 weeks",
        "topics": [
            "Flask basics",
            "Routes",
            "Templates",
            "Forms",
            "Database integration",
            "REST API"
        ],
        "project": "Build a Flask-based REST API."
    },

    "Bootstrap": {
        "level": "Foundation",
        "duration": "3-5 days",
        "topics": [
            "Grid system",
            "Cards",
            "Buttons",
            "Navbar",
            "Forms",
            "Responsive components"
        ],
        "project": "Create a responsive professional dashboard."
    },

    "REST API": {
        "level": "Intermediate",
        "duration": "1 week",
        "topics": [
            "HTTP methods",
            "GET, POST, PUT and DELETE",
            "JSON",
            "API authentication",
            "API testing",
            "Status codes"
        ],
        "project": "Create a REST API for a job portal."
    },

    "TensorFlow": {
        "level": "Advanced",
        "duration": "3-4 weeks",
        "topics": [
            "TensorFlow fundamentals",
            "Neural networks",
            "Model creation",
            "Training",
            "Validation",
            "Prediction"
        ],
        "project": "Build a basic deep-learning prediction system."
    },

    "Node.js": {
        "level": "Intermediate",
        "duration": "1-2 weeks",
        "topics": [
            "Node.js fundamentals",
            "Modules",
            "NPM",
            "File system",
            "HTTP server",
            "API development"
        ],
        "project": "Build a backend REST API using Node.js."
    },

    "Express.js": {
        "level": "Intermediate",
        "duration": "1 week",
        "topics": [
            "Express setup",
            "Routes",
            "Middleware",
            "Controllers",
            "REST APIs",
            "Error handling"
        ],
        "project": "Build a complete REST API using Express.js."
    },

    "PHP": {
        "level": "Foundation",
        "duration": "2 weeks",
        "topics": [
            "PHP syntax",
            "Forms",
            "Sessions",
            "Database connectivity",
            "CRUD operations"
        ],
        "project": "Build a PHP-based management system."
    },

    "C++": {
        "level": "Foundation",
        "duration": "2-3 weeks",
        "topics": [
            "C++ syntax",
            "OOP",
            "STL",
            "Arrays",
            "Strings",
            "Algorithms"
        ],
        "project": "Build a C++ console-based management system."
    },

    "C": {
        "level": "Foundation",
        "duration": "1-2 weeks",
        "topics": [
            "Variables",
            "Conditions",
            "Loops",
            "Functions",
            "Arrays",
            "Pointers",
            "Structures"
        ],
        "project": "Build a C-based Student Management System."
    },
}


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def normalize_text(text):

    if not text:
        return ""

    text = text.lower()

    # Fix PDF text such as:
    # P y t h o n
    # J a v a
    # H T M L

    text = re.sub(
        r'(?<![a-z])([a-z](?:\s+[a-z])+)(?![a-z])',
        lambda match: re.sub(
            r'\s+',
            '',
            match.group(1)
        ),
        text
    )

    text = re.sub(
        r'\s+',
        ' ',
        text
    )

    return text.strip()


def compact_text(text):

    if not text:
        return ""

    text = text.lower()

    text = re.sub(
        r'[\s\-_\/\\.,:;|]+',
        '',
        text
    )

    return text


# =========================================================
# PDF EXTRACTION
# =========================================================

def extract_resume_text(file_path):

    extracted_text = ""

    print("\n====================================")
    print("PDF TEXT EXTRACTION")
    print("====================================")

    try:

        reader = PdfReader(file_path)

        pages_text = []

        for page in reader.pages:

            try:

                page_text = page.extract_text()

                if page_text:
                    pages_text.append(page_text)

            except Exception as e:

                print(
                    "Page extraction error:",
                    e
                )

        extracted_text = "\n".join(
            pages_text
        )

    except Exception as e:

        print(
            "PDF extraction error:",
            e
        )

        extracted_text = ""


    print(
        "Characters:",
        len(extracted_text)
    )


    # =====================================================
    # OCR FALLBACK
    # =====================================================

    if len(extracted_text.strip()) < 50:

        print("\nStarting OCR...")

        try:

            pages = convert_from_path(
                file_path,
                poppler_path=POPPLER_PATH
            )

            ocr_text = []

            for page in pages:

                text = pytesseract.image_to_string(
                    page
                )

                if text:
                    ocr_text.append(text)

            extracted_text = "\n".join(
                ocr_text
            )

        except Exception as e:

            print(
                "OCR ERROR:",
                e
            )


    print("\n====================================")
    print("FINAL EXTRACTED TEXT")
    print("====================================")

    print(
        extracted_text[:10000]
    )

    return extracted_text


# =========================================================
# SKILL DETECTION
# =========================================================

def detect_skills(text):

    if not text:
        return []


    normalized = normalize_text(text)

    compact = compact_text(normalized)

    detected = []


    for skill in SKILLS_LIST:

        skill_lower = skill.lower()


        # -------------------------------------------------
        # C SPECIAL CASE
        # -------------------------------------------------

        if skill_lower == "c":

            patterns = [
                r'(?<![a-z])c(?![a-z])',
                r'\bc\s+programming\b',
                r'\bc\s+language\b',
            ]

            if any(
                re.search(
                    pattern,
                    normalized
                )
                for pattern in patterns
            ):

                detected.append(skill)

            continue


        # -------------------------------------------------
        # COMPACT MATCH
        # -------------------------------------------------

        skill_compact = compact_text(
            skill_lower
        )

        if (
            skill_compact
            and skill_compact in compact
        ):

            detected.append(skill)

            continue


        # -------------------------------------------------
        # NORMAL WORD MATCH
        # -------------------------------------------------

        if re.search(
            r'\b'
            + re.escape(skill_lower)
            + r'\b',
            normalized
        ):

            detected.append(skill)


    return list(
        dict.fromkeys(detected)
    )


# =========================================================
# RESUME UPLOAD
# =========================================================

@login_required
def upload_resume(request):

    if request.method == "POST":

        form = ResumeForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            resume = form.save(
                commit=False
            )

            resume.user = request.user

            resume.save()


            text = extract_resume_text(
                resume.file.path
            )


            detected_skills = detect_skills(
                text
            )


            print("\n====================================")
            print("DETECTED SKILLS")
            print("====================================")

            print(
                detected_skills
            )

            print(
                "Total skills:",
                len(detected_skills)
            )

            print("====================================")


            return render(
                request,
                "skills/skills_result.html",
                {
                    "skills": detected_skills,
                    "resume": resume,
                }
            )


    else:

        form = ResumeForm()


    return render(
        request,
        "skills/upload_resume.html",
        {
            "form": form
        }
    )


# =========================================================
# CHOOSE CAREER
# =========================================================

@login_required
def choose_career(request):

    careers = Career.objects.all()

    return render(
        request,
        "skills/career.html",
        {
            "careers": careers
        }
    )


# =========================================================
# CREATE PERSONALIZED ROADMAP
# =========================================================

def create_roadmap(missing_skills):

    roadmap = []

    for index, skill in enumerate(
        missing_skills,
        start=1
    ):

        data = ROADMAP_DATA.get(
            skill
        )


        if data:

            roadmap.append(
                {
                    "step": index,
                    "skill": skill,
                    "level": data["level"],
                    "duration": data["duration"],
                    "topics": data["topics"],
                    "project": data["project"],
                }
            )

        else:

            # Fallback for a skill that
            # doesn't exist in ROADMAP_DATA

            roadmap.append(
                {
                    "step": index,
                    "skill": skill,
                    "level": "Foundation",
                    "duration": "1-2 weeks",
                    "topics": [
                        f"Learn {skill} fundamentals",
                        f"Practice {skill} syntax and concepts",
                        f"Work with real-world examples",
                        f"Build a small project using {skill}",
                    ],
                    "project": (
                        f"Build a beginner-level "
                        f"project using {skill}."
                    ),
                }
            )


    return roadmap


# =========================================================
# SKILL GAP ANALYSIS
# =========================================================

@login_required
def skill_gap(
    request,
    career_id
):

    career = get_object_or_404(
        Career,
        id=career_id
    )


    # -----------------------------------------------------
    # GET LATEST RESUME
    # -----------------------------------------------------

    resume = (
        Resume.objects
        .filter(
            user=request.user
        )
        .order_by(
            "-uploaded_at"
        )
        .first()
    )


    detected_skills = []


    if resume:

        text = extract_resume_text(
            resume.file.path
        )

        detected_skills = detect_skills(
            text
        )


    # -----------------------------------------------------
    # REQUIRED CAREER SKILLS
    # -----------------------------------------------------

    required_skills = [
        skill.strip()
        for skill in career.required_skills.split(",")
        if skill.strip()
    ]


    # -----------------------------------------------------
    # NORMALIZE DETECTED SKILLS
    # -----------------------------------------------------

    detected_normalized = {
        compact_text(skill)
        for skill in detected_skills
    }


    matched_skills = []

    missing_skills = []


    for skill in required_skills:

        normalized_skill = compact_text(
            skill
        )


        if normalized_skill in detected_normalized:

            matched_skills.append(
                skill
            )

        else:

            missing_skills.append(
                skill
            )


    # -----------------------------------------------------
    # MATCH PERCENTAGE
    # -----------------------------------------------------

    if required_skills:

        match_percentage = round(
            (
                len(matched_skills)
                / len(required_skills)
            ) * 100
        )

    else:

        match_percentage = 0


    # -----------------------------------------------------
    # PERSONALIZED ROADMAP
    # -----------------------------------------------------

    roadmap = create_roadmap(
        missing_skills
    )


    # -----------------------------------------------------
    # TOTAL ROADMAP DURATION
    # -----------------------------------------------------

    total_learning_steps = len(
        roadmap
    )


    return render(
        request,
        "skills/skills_gap.html",
        {
            "career": career,

            "resume": resume,

            "detected_skills": detected_skills,

            "required_skills": required_skills,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "match_percentage": match_percentage,

            "roadmap": roadmap,

            "total_learning_steps":
                total_learning_steps,
        }
    )