import json
import os
import re
import secrets
import sqlite3
from datetime import datetime, timedelta

import PyPDF2
from flask import Flask, jsonify, request, send_from_directory, session
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

# Get absolute paths for static files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "static"),
    static_url_path="/static",
    template_folder=os.path.join(BASE_DIR, "frontend"),
)
app.secret_key = secrets.token_hex(32)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)

CORS(app, supports_credentials=True)


# Database initialization
def init_db():
    # Get the project root directory (parent of backend folder)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_dir = os.path.join(project_root, "database")

    # Create database directory if it doesn't exist
    os.makedirs(db_dir, exist_ok=True)

    db_path = os.path.join(db_dir, "skilllens.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Users table
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        full_name TEXT NOT NULL,
        phone TEXT,
        location TEXT,
        bio TEXT,
        linkedin TEXT,
        github TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    # Resumes table
    c.execute("""CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        filename TEXT NOT NULL,
        extracted_text TEXT,
        skills_json TEXT,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )""")

    # Analysis table
    c.execute("""CREATE TABLE IF NOT EXISTS analysis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        resume_id INTEGER NOT NULL,
        target_role TEXT NOT NULL,
        skill_gap_json TEXT,
        roadmap_json TEXT,
        score INTEGER,
        analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (resume_id) REFERENCES resumes (id)
    )""")

    conn.commit()
    conn.close()


# Initialize database on startup
init_db()


# PDF text extraction
def extract_text_from_pdf(file_path):
    try:
        text = ""
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"


# AI Skill Extraction Engine
def extract_skills_from_resume(resume_text):
    """Advanced skill extraction using pattern matching and NLP"""

    # Comprehensive skill databases
    programming_languages = [
        "python",
        "java",
        "javascript",
        "c++",
        "c",
        "c#",
        "ruby",
        "go",
        "rust",
        "swift",
        "kotlin",
        "php",
        "typescript",
        "r",
        "matlab",
        "scala",
        "perl",
        "dart",
        "sql",
    ]

    web_technologies = [
        "html",
        "css",
        "react",
        "angular",
        "vue",
        "node.js",
        "express",
        "django",
        "flask",
        "spring boot",
        "asp.net",
        "next.js",
        "nuxt.js",
        "svelte",
        "bootstrap",
        "tailwind",
        "jquery",
        "webpack",
        "babel",
        "sass",
        "less",
        "rest api",
        "graphql",
    ]

    data_science = [
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "keras",
        "scikit-learn",
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "opencv",
        "nltk",
        "spacy",
        "data analysis",
        "statistics",
        "probability",
        "linear algebra",
        "calculus",
        "neural networks",
        "nlp",
        "computer vision",
        "recommendation systems",
        "time series",
        "regression",
        "classification",
    ]

    databases = [
        "mysql",
        "postgresql",
        "mongodb",
        "redis",
        "sqlite",
        "oracle",
        "cassandra",
        "dynamodb",
        "firebase",
        "mariadb",
        "neo4j",
        "elasticsearch",
    ]

    cloud_devops = [
        "aws",
        "azure",
        "gcp",
        "docker",
        "kubernetes",
        "jenkins",
        "git",
        "github",
        "gitlab",
        "ci/cd",
        "terraform",
        "ansible",
        "nginx",
        "apache",
        "linux",
        "bash",
        "shell scripting",
    ]

    tools_frameworks = [
        "jupyter",
        "vs code",
        "pycharm",
        "intellij",
        "eclipse",
        "git",
        "jira",
        "postman",
        "tableau",
        "power bi",
        "excel",
        "google analytics",
        "figma",
        "adobe xd",
        "photoshop",
    ]

    soft_skills = [
        "leadership",
        "communication",
        "teamwork",
        "problem solving",
        "critical thinking",
        "time management",
        "project management",
        "agile",
        "scrum",
        "presentation",
    ]

    # Convert resume to lowercase for matching
    text_lower = resume_text.lower()

    extracted = {
        "programming_languages": [],
        "web_technologies": [],
        "data_science": [],
        "databases": [],
        "cloud_devops": [],
        "tools_frameworks": [],
        "soft_skills": [],
        "certifications": [],
        "projects": [],
        "experience_years": 0,
        "career_level": "Beginner",
    }

    # Extract skills by category
    for lang in programming_languages:
        if re.search(r"\b" + re.escape(lang) + r"\b", text_lower):
            extracted["programming_languages"].append(lang.title())

    for tech in web_technologies:
        if re.search(r"\b" + re.escape(tech) + r"\b", text_lower):
            extracted["web_technologies"].append(tech.title())

    for skill in data_science:
        if re.search(r"\b" + re.escape(skill) + r"\b", text_lower):
            extracted["data_science"].append(skill.title())

    for db in databases:
        if re.search(r"\b" + re.escape(db) + r"\b", text_lower):
            extracted["databases"].append(db.upper() if len(db) <= 5 else db.title())

    for skill in cloud_devops:
        if re.search(r"\b" + re.escape(skill) + r"\b", text_lower):
            extracted["cloud_devops"].append(
                skill.upper() if len(skill) <= 5 else skill.title()
            )

    for tool in tools_frameworks:
        if re.search(r"\b" + re.escape(tool) + r"\b", text_lower):
            extracted["tools_frameworks"].append(tool.title())

    for skill in soft_skills:
        if re.search(r"\b" + re.escape(skill) + r"\b", text_lower):
            extracted["soft_skills"].append(skill.title())

    # Extract certifications
    cert_patterns = [
        r"certification[s]?[:\s]+([^\n]+)",
        r"certified[:\s]+([^\n]+)",
        r"certificate[:\s]+([^\n]+)",
    ]
    for pattern in cert_patterns:
        matches = re.findall(pattern, text_lower)
        extracted["certifications"].extend(matches)

    # Extract projects
    project_section = re.search(
        r"project[s]?[:\s]+(.*?)(?=experience|education|skills|certification|$)",
        text_lower,
        re.DOTALL,
    )
    if project_section:
        projects = re.findall(r"[-•]\s*([^\n]+)", project_section.group(1))
        extracted["projects"] = projects[:5]  # Top 5 projects

    # Determine experience level
    exp_patterns = [
        r"(\d+)\s*(?:\+)?\s*years?\s+(?:of\s+)?experience",
        r"experience[:\s]+(\d+)\s*years?",
    ]
    for pattern in exp_patterns:
        match = re.search(pattern, text_lower)
        if match:
            extracted["experience_years"] = int(match.group(1))
            break

    # Determine career level
    total_skills = sum(len(v) for k, v in extracted.items() if isinstance(v, list))
    if extracted["experience_years"] >= 3 or total_skills > 20:
        extracted["career_level"] = "Advanced"
    elif extracted["experience_years"] >= 1 or total_skills > 10:
        extracted["career_level"] = "Intermediate"
    else:
        extracted["career_level"] = "Beginner"

    return extracted


# Role-based skill requirements database
ROLE_REQUIREMENTS = {
    "Data Analyst": {
        "critical": [
            "Python",
            "SQL",
            "Excel",
            "Statistics",
            "Data Analysis",
            "Pandas",
            "Numpy",
            "Power BI",
            "Tableau",
        ],
        "important": [
            "Data Visualization",
            "Data Cleaning",
            "Business Intelligence",
            "Google Analytics",
            "Statistical Analysis",
        ],
        "nice_to_have": [
            "Machine Learning",
            "R",
            "Matplotlib",
            "Seaborn",
            "SPSS",
            "DAX",
        ],
    },
    "Full Stack Developer": {
        "critical": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Node.js",
            "SQL",
            "Git",
            "REST API",
        ],
        "important": [
            "Express",
            "MongoDB",
            "TypeScript",
            "Redux",
            "Bootstrap",
            "Responsive Design",
            "Authentication",
        ],
        "nice_to_have": [
            "Next.js",
            "GraphQL",
            "Docker",
            "AWS",
            "CI/CD",
            "Testing",
            "Webpack",
        ],
    },
    "Data Scientist": {
        "critical": [
            "Python",
            "Machine Learning",
            "Statistics",
            "Pandas",
            "Numpy",
            "SQL",
            "Deep Learning",
            "Data Analysis",
        ],
        "important": [
            "Tensorflow",
            "Pytorch",
            "Scikit-learn",
            "NLP",
            "Computer Vision",
            "Feature Engineering",
            "Model Deployment",
        ],
        "nice_to_have": [
            "Big Data",
            "Spark",
            "Hadoop",
            "MLOps",
            "A/B Testing",
            "Causal Inference",
        ],
    },
    "Backend Developer": {
        "critical": [
            "Python",
            "Node.js",
            "SQL",
            "REST API",
            "Git",
            "Database Design",
            "Authentication",
        ],
        "important": [
            "Express",
            "Django",
            "Flask",
            "PostgreSQL",
            "MongoDB",
            "Redis",
            "API Security",
            "Microservices",
        ],
        "nice_to_have": [
            "Docker",
            "Kubernetes",
            "GraphQL",
            "Message Queues",
            "AWS",
            "Performance Optimization",
        ],
    },
    "Frontend Developer": {
        "critical": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Responsive Design",
            "Git",
            "REST API Integration",
        ],
        "important": [
            "TypeScript",
            "Redux",
            "Webpack",
            "SASS",
            "Bootstrap",
            "Tailwind",
            "State Management",
        ],
        "nice_to_have": [
            "Next.js",
            "Vue",
            "Angular",
            "Testing Library",
            "Accessibility",
            "Performance Optimization",
        ],
    },
    "Machine Learning Engineer": {
        "critical": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "Tensorflow",
            "Pytorch",
            "Model Deployment",
            "MLOps",
        ],
        "important": [
            "Scikit-learn",
            "Feature Engineering",
            "Model Optimization",
            "Docker",
            "AWS",
            "API Development",
        ],
        "nice_to_have": [
            "Kubernetes",
            "Spark",
            "GPU Computing",
            "Reinforcement Learning",
            "AutoML",
        ],
    },
    "DevOps Engineer": {
        "critical": [
            "Linux",
            "Docker",
            "Kubernetes",
            "Git",
            "CI/CD",
            "AWS",
            "Bash",
            "Monitoring",
        ],
        "important": [
            "Jenkins",
            "Terraform",
            "Ansible",
            "Python",
            "Nginx",
            "Prometheus",
            "Grafana",
        ],
        "nice_to_have": [
            "Azure",
            "GCP",
            "Helm",
            "Service Mesh",
            "Infrastructure as Code",
            "Security",
        ],
    },
    "Mobile App Developer": {
        "critical": [
            "React Native",
            "Flutter",
            "Dart",
            "Mobile UI/UX",
            "REST API",
            "State Management",
            "Git",
        ],
        "important": [
            "Firebase",
            "Push Notifications",
            "App Store Deployment",
            "Android/iOS Guidelines",
            "Offline Storage",
        ],
        "nice_to_have": [
            "Native Development",
            "Performance Optimization",
            "Analytics",
            "A/B Testing",
            "In-App Purchases",
        ],
    },
    "Cloud Engineer": {
        "critical": [
            "AWS",
            "Azure",
            "Cloud Architecture",
            "Networking",
            "Security",
            "Linux",
            "Scripting",
        ],
        "important": [
            "Terraform",
            "Kubernetes",
            "Docker",
            "CI/CD",
            "Monitoring",
            "Cost Optimization",
        ],
        "nice_to_have": [
            "Serverless",
            "Multi-Cloud",
            "Compliance",
            "Disaster Recovery",
            "Cloud Migration",
        ],
    },
    "Cybersecurity Analyst": {
        "critical": [
            "Network Security",
            "Ethical Hacking",
            "Penetration Testing",
            "Security Tools",
            "Linux",
            "Cryptography",
        ],
        "important": [
            "Wireshark",
            "Metasploit",
            "SIEM",
            "Incident Response",
            "Vulnerability Assessment",
            "Firewalls",
        ],
        "nice_to_have": [
            "Cloud Security",
            "Malware Analysis",
            "Forensics",
            "Compliance",
            "Threat Intelligence",
        ],
    },
}


# Skill Gap Analysis
def analyze_skill_gap(extracted_skills, target_role):
    """Compare extracted skills with role requirements"""

    if target_role not in ROLE_REQUIREMENTS:
        return {"error": "Invalid role selected"}

    requirements = ROLE_REQUIREMENTS[target_role]
    all_extracted = []

    # Flatten all extracted skills
    for category, skills in extracted_skills.items():
        if isinstance(skills, list):
            all_extracted.extend([s.lower() for s in skills])

    # Analysis results
    analysis = {
        "present_skills": [],
        "critical_missing": [],
        "important_missing": [],
        "nice_to_have_missing": [],
        "score": 0,
        "gap_summary": "",
    }

    # Check critical skills
    for skill in requirements["critical"]:
        if skill.lower() in all_extracted:
            analysis["present_skills"].append(skill)
        else:
            analysis["critical_missing"].append(skill)

    # Check important skills
    for skill in requirements["important"]:
        if skill.lower() not in all_extracted:
            analysis["important_missing"].append(skill)
        else:
            analysis["present_skills"].append(skill)

    # Check nice-to-have skills
    for skill in requirements["nice_to_have"]:
        if skill.lower() not in all_extracted:
            analysis["nice_to_have_missing"].append(skill)
        else:
            analysis["present_skills"].append(skill)

    # Calculate score
    total_skills = (
        len(requirements["critical"])
        + len(requirements["important"])
        + len(requirements["nice_to_have"])
    )
    present_count = len(analysis["present_skills"])
    critical_weight = len(requirements["critical"]) * 3
    important_weight = len(requirements["important"]) * 2
    nice_weight = len(requirements["nice_to_have"]) * 1

    critical_present = len(requirements["critical"]) - len(analysis["critical_missing"])
    important_present = len(requirements["important"]) - len(
        analysis["important_missing"]
    )
    nice_present = len(requirements["nice_to_have"]) - len(
        analysis["nice_to_have_missing"]
    )

    score = (
        ((critical_present * 3) + (important_present * 2) + (nice_present * 1))
        / (critical_weight + important_weight + nice_weight)
        * 100
    )
    analysis["score"] = int(score)

    # Generate summary
    if score >= 80:
        analysis["gap_summary"] = (
            f"Excellent fit! You have {present_count}/{total_skills} required skills. Focus on advanced topics."
        )
    elif score >= 60:
        analysis["gap_summary"] = (
            f"Good foundation with {present_count}/{total_skills} skills. Work on {len(analysis['critical_missing'])} critical gaps."
        )
    elif score >= 40:
        analysis["gap_summary"] = (
            f"Moderate preparation needed. Missing {len(analysis['critical_missing'])} critical skills. Follow roadmap."
        )
    else:
        analysis["gap_summary"] = (
            f"Significant learning required. Start with foundational skills and follow structured roadmap."
        )

    return analysis


# Learning Roadmap Generator
def generate_roadmap(skill_gap, target_role, career_level):
    """Generate personalized learning roadmap"""

    roadmap = {
        "beginner": {"duration": "0-4 weeks", "skills": [], "projects": []},
        "intermediate": {"duration": "1-3 months", "skills": [], "projects": []},
        "advanced": {"duration": "3-6 months", "skills": [], "projects": []},
    }

    # Beginner phase - Critical skills
    if skill_gap["critical_missing"]:
        roadmap["beginner"]["skills"] = skill_gap["critical_missing"][:3]

        if target_role == "Data Analyst":
            roadmap["beginner"]["projects"] = [
                "Sales data analysis with Python and Pandas",
                "Interactive dashboard using Excel",
                "SQL queries on sample database",
            ]
        elif target_role == "Full Stack Developer":
            roadmap["beginner"]["projects"] = [
                "Personal portfolio website",
                "To-Do list app with CRUD operations",
                "Weather app using API",
            ]
        elif target_role == "Data Scientist":
            roadmap["beginner"]["projects"] = [
                "Exploratory data analysis on Kaggle dataset",
                "Linear regression model",
                "Data visualization dashboard",
            ]

    # Intermediate phase - Important skills
    if skill_gap["important_missing"]:
        roadmap["intermediate"]["skills"] = skill_gap["important_missing"][:4]

        if target_role == "Data Analyst":
            roadmap["intermediate"]["projects"] = [
                "Customer segmentation analysis",
                "Power BI/Tableau interactive reports",
                "A/B testing analysis",
            ]
        elif target_role == "Full Stack Developer":
            roadmap["intermediate"]["projects"] = [
                "E-commerce website with cart functionality",
                "Blog platform with authentication",
                "Real-time chat application",
            ]
        elif target_role == "Data Scientist":
            roadmap["intermediate"]["projects"] = [
                "Classification model (e.g., loan prediction)",
                "NLP sentiment analysis",
                "Time series forecasting",
            ]

    # Advanced phase - Nice-to-have skills
    if skill_gap["nice_to_have_missing"]:
        roadmap["advanced"]["skills"] = skill_gap["nice_to_have_missing"][:3]

        if target_role == "Data Analyst":
            roadmap["advanced"]["projects"] = [
                "Predictive analytics dashboard",
                "Business intelligence system",
                "Automated reporting pipeline",
            ]
        elif target_role == "Full Stack Developer":
            roadmap["advanced"]["projects"] = [
                "Social media clone with microservices",
                "Video streaming platform",
                "Cloud-deployed SaaS application",
            ]
        elif target_role == "Data Scientist":
            roadmap["advanced"]["projects"] = [
                "Deep learning image classifier",
                "Recommendation system",
                "End-to-end ML pipeline deployment",
            ]

    return roadmap


# Course Recommendations
def recommend_courses(missing_skills):
    """Recommend courses for each missing skill"""

    course_db = {
        "python": {
            "platform": "Coursera / FreeCodeCamp",
            "reason": "Comprehensive Python fundamentals",
        },
        "sql": {
            "platform": "SQLBolt / Khan Academy",
            "reason": "Interactive SQL practice",
        },
        "excel": {
            "platform": "Excel Exposure / Chandoo",
            "reason": "Free Excel tutorials",
        },
        "statistics": {
            "platform": "Khan Academy / StatQuest",
            "reason": "Visual statistics learning",
        },
        "data analysis": {
            "platform": "Google Data Analytics (Coursera)",
            "reason": "Industry-recognized certificate",
        },
        "machine learning": {
            "platform": "Andrew Ng ML Course (Coursera)",
            "reason": "Gold standard ML course",
        },
        "react": {
            "platform": "React Docs / Scrimba",
            "reason": "Official docs + interactive",
        },
        "node.js": {
            "platform": "NodeSchool / FreeCodeCamp",
            "reason": "Hands-on exercises",
        },
        "html": {
            "platform": "MDN Web Docs / FreeCodeCamp",
            "reason": "Best web dev resources",
        },
        "css": {
            "platform": "CSS Tricks / FreeCodeCamp",
            "reason": "Practical CSS learning",
        },
        "javascript": {
            "platform": "JavaScript.info / FreeCodeCamp",
            "reason": "Modern JS comprehensive guide",
        },
        "git": {"platform": "GitHub Learning Lab", "reason": "Learn by doing"},
        "docker": {
            "platform": "Docker Docs / KodeKloud",
            "reason": "Practical containerization",
        },
        "aws": {
            "platform": "AWS Free Tier / Cloud Academy",
            "reason": "Hands-on cloud practice",
        },
        "pandas": {
            "platform": "Kaggle Learn / DataCamp",
            "reason": "Quick practical tutorials",
        },
        "numpy": {
            "platform": "NumPy Docs / YouTube",
            "reason": "Free and comprehensive",
        },
        "power bi": {"platform": "Microsoft Learn", "reason": "Official free training"},
        "tableau": {
            "platform": "Tableau Public / YouTube",
            "reason": "Free visualization tool",
        },
    }

    recommendations = []
    for skill in missing_skills:
        skill_lower = skill.lower()
        if skill_lower in course_db:
            recommendations.append(
                {
                    "skill": skill,
                    "platform": course_db[skill_lower]["platform"],
                    "reason": course_db[skill_lower]["reason"],
                }
            )
        else:
            recommendations.append(
                {
                    "skill": skill,
                    "platform": "Udemy / YouTube",
                    "reason": "Search for latest tutorials",
                }
            )

    return recommendations


# ==================== API ENDPOINTS ====================


# Serve frontend
@app.route("/")
def serve_frontend():
    frontend_dir = os.path.join(BASE_DIR, "frontend")
    return send_from_directory(frontend_dir, "index.html")


@app.route("/dashboard.html")
def serve_dashboard():
    frontend_dir = os.path.join(BASE_DIR, "frontend")
    return send_from_directory(frontend_dir, "dashboard.html")


@app.route("/<path:filename>")
def serve_static(filename):
    # Try frontend directory first
    frontend_dir = os.path.join(BASE_DIR, "frontend")
    if os.path.exists(os.path.join(frontend_dir, filename)):
        return send_from_directory(frontend_dir, filename)
    # Fallback to static directory
    static_dir = os.path.join(BASE_DIR, "static")
    return send_from_directory(static_dir, filename)


# User Registration
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    full_name = data.get("full_name")

    if not email or not password or not full_name:
        return jsonify({"error": "All fields required"}), 400

    try:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(project_root, "database", "skilllens.db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Check if user exists
        c.execute("SELECT id FROM users WHERE email = ?", (email,))
        if c.fetchone():
            return jsonify({"error": "Email already registered"}), 400

        # Create user
        hashed_password = generate_password_hash(password)
        c.execute(
            "INSERT INTO users (email, password, full_name) VALUES (?, ?, ?)",
            (email, hashed_password, full_name),
        )
        conn.commit()

        user_id = c.lastrowid
        conn.close()

        session["user_id"] = user_id
        session["email"] = email
        session["full_name"] = full_name
        session.permanent = True

        return jsonify(
            {
                "success": True,
                "user": {"id": user_id, "email": email, "full_name": full_name},
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# User Login
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    try:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(project_root, "database", "skilllens.db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute("SELECT id, password, full_name FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        conn.close()

        if not user or not check_password_hash(user[1], password):
            return jsonify({"error": "Invalid credentials"}), 401

        session["user_id"] = user[0]
        session["email"] = email
        session["full_name"] = user[2]
        session.permanent = True

        return jsonify(
            {
                "success": True,
                "user": {"id": user[0], "email": email, "full_name": user[2]},
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# User Logout
@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True})


# Check Authentication
@app.route("/api/check-auth", methods=["GET"])
def check_auth():
    if "user_id" in session:
        return jsonify(
            {
                "authenticated": True,
                "user": {
                    "id": session["user_id"],
                    "email": session["email"],
                    "full_name": session["full_name"],
                },
            }
        )
    return jsonify({"authenticated": False})


# Upload Resume
@app.route("/api/upload-resume", methods=["POST"])
def upload_resume():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["resume"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files allowed"}), 400

    try:
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{session['user_id']}_{timestamp}_{filename}"

        # Get absolute path for uploads
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        uploads_dir = os.path.join(project_root, app.config["UPLOAD_FOLDER"])
        os.makedirs(uploads_dir, exist_ok=True)

        filepath = os.path.join(uploads_dir, filename)

        file.save(filepath)

        # Extract text
        extracted_text = extract_text_from_pdf(filepath)

        # Extract skills
        skills = extract_skills_from_resume(extracted_text)

        # Save to database
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(project_root, "database", "skilllens.db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute(
            "INSERT INTO resumes (user_id, filename, extracted_text, skills_json) VALUES (?, ?, ?, ?)",
            (session["user_id"], filename, extracted_text, json.dumps(skills)),
        )
        conn.commit()
        resume_id = c.lastrowid
        conn.close()

        return jsonify(
            {
                "success": True,
                "resume_id": resume_id,
                "skills": skills,
                "text_preview": extracted_text[:500],
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Analyze Skills
@app.route("/api/analyze", methods=["POST"])
def analyze():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    data = request.json
    resume_id = data.get("resume_id")
    target_role = data.get("target_role")

    if not resume_id or not target_role:
        return jsonify({"error": "Resume ID and target role required"}), 400

    try:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(project_root, "database", "skilllens.db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Get resume skills
        c.execute(
            "SELECT skills_json FROM resumes WHERE id = ? AND user_id = ?",
            (resume_id, session["user_id"]),
        )
        result = c.fetchone()

        if not result:
            return jsonify({"error": "Resume not found"}), 404

        skills = json.loads(result[0])

        # Analyze skill gap
        gap_analysis = analyze_skill_gap(skills, target_role)

        # Generate roadmap
        roadmap = generate_roadmap(gap_analysis, target_role, skills["career_level"])

        # Recommend courses
        all_missing = (
            gap_analysis["critical_missing"] + gap_analysis["important_missing"]
        )
        courses = recommend_courses(all_missing[:10])

        # Save analysis
        c.execute(
            "INSERT INTO analysis (user_id, resume_id, target_role, skill_gap_json, roadmap_json, score) VALUES (?, ?, ?, ?, ?, ?)",
            (
                session["user_id"],
                resume_id,
                target_role,
                json.dumps(gap_analysis),
                json.dumps(roadmap),
                gap_analysis["score"],
            ),
        )
        conn.commit()
        analysis_id = c.lastrowid
        conn.close()

        return jsonify(
            {
                "success": True,
                "analysis_id": analysis_id,
                "gap_analysis": gap_analysis,
                "roadmap": roadmap,
                "course_recommendations": courses,
                "career_level": skills["career_level"],
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get User Dashboard
@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    try:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(project_root, "database", "skilllens.db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Get recent analyses
        c.execute(
            """SELECT a.id, a.target_role, a.score, a.analyzed_at, r.filename
                     FROM analysis a
                     JOIN resumes r ON a.resume_id = r.id
                     WHERE a.user_id = ?
                     ORDER BY a.analyzed_at DESC
                     LIMIT 10""",
            (session["user_id"],),
        )

        analyses = []
        for row in c.fetchall():
            analyses.append(
                {
                    "id": row[0],
                    "target_role": row[1],
                    "score": row[2],
                    "date": row[3],
                    "filename": row[4],
                }
            )

        conn.close()

        return jsonify({"success": True, "analyses": analyses})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get User Profile
@app.route("/api/profile", methods=["GET"])
def get_profile():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    try:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(project_root, "database", "skilllens.db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Get user profile
        c.execute(
            """SELECT id, email, full_name, phone, location, bio, linkedin, github, created_at
               FROM users WHERE id = ?""",
            (session["user_id"],),
        )
        user = c.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Get statistics
        c.execute(
            "SELECT COUNT(*) FROM resumes WHERE user_id = ?", (session["user_id"],)
        )
        resume_count = c.fetchone()[0]

        c.execute(
            "SELECT COUNT(*), AVG(score) FROM analysis WHERE user_id = ?",
            (session["user_id"],),
        )
        stats = c.fetchone()
        analysis_count = stats[0]
        avg_score = int(stats[1]) if stats[1] else 0

        conn.close()

        return jsonify(
            {
                "success": True,
                "profile": {
                    "id": user[0],
                    "email": user[1],
                    "full_name": user[2],
                    "phone": user[3],
                    "location": user[4],
                    "bio": user[5],
                    "linkedin": user[6],
                    "github": user[7],
                    "created_at": user[8],
                },
                "stats": {
                    "resume_count": resume_count,
                    "analysis_count": analysis_count,
                    "avg_score": avg_score,
                },
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Update User Profile
@app.route("/api/profile", methods=["PUT"])
def update_profile():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    data = request.json
    full_name = data.get("full_name")
    email = data.get("email")
    phone = data.get("phone", "")
    location = data.get("location", "")
    bio = data.get("bio", "")
    linkedin = data.get("linkedin", "")
    github = data.get("github", "")

    if not full_name or not email:
        return jsonify({"error": "Full name and email are required"}), 400

    try:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(project_root, "database", "skilllens.db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Check if email is already taken by another user
        c.execute(
            "SELECT id FROM users WHERE email = ? AND id != ?",
            (email, session["user_id"]),
        )
        if c.fetchone():
            return jsonify({"error": "Email already in use"}), 400

        # Update user profile
        c.execute(
            """UPDATE users
               SET full_name = ?, email = ?, phone = ?, location = ?, bio = ?, linkedin = ?, github = ?
               WHERE id = ?""",
            (
                full_name,
                email,
                phone,
                location,
                bio,
                linkedin,
                github,
                session["user_id"],
            ),
        )
        conn.commit()
        conn.close()

        # Update session
        session["full_name"] = full_name
        session["email"] = email

        return jsonify({"success": True, "message": "Profile updated successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Change Password
@app.route("/api/change-password", methods=["POST"])
def change_password():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    data = request.json
    current_password = data.get("current_password")
    new_password = data.get("new_password")

    if not current_password or not new_password:
        return jsonify({"error": "All fields required"}), 400

    if len(new_password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    try:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(project_root, "database", "skilllens.db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Verify current password
        c.execute("SELECT password FROM users WHERE id = ?", (session["user_id"],))
        user = c.fetchone()

        if not user or not check_password_hash(user[0], current_password):
            return jsonify({"error": "Current password is incorrect"}), 401

        # Update password
        hashed_password = generate_password_hash(new_password)
        c.execute(
            "UPDATE users SET password = ? WHERE id = ?",
            (hashed_password, session["user_id"]),
        )
        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "Password updated successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Delete Account
@app.route("/api/delete-account", methods=["DELETE"])
def delete_account():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    try:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(project_root, "database", "skilllens.db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Delete user's analyses
        c.execute("DELETE FROM analysis WHERE user_id = ?", (session["user_id"],))

        # Delete user's resumes
        c.execute("DELETE FROM resumes WHERE user_id = ?", (session["user_id"],))

        # Delete user
        c.execute("DELETE FROM users WHERE id = ?", (session["user_id"],))

        conn.commit()
        conn.close()

        # Clear session
        session.clear()

        return jsonify({"success": True, "message": "Account deleted successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==================== RUN SERVER ====================

if __name__ == "__main__":
    # Get project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Ensure required directories exist
    os.makedirs(os.path.join(project_root, "database"), exist_ok=True)
    os.makedirs(os.path.join(project_root, "uploads"), exist_ok=True)

    # Initialize database
    init_db()

    # Run Flask app
    print("=" * 50)
    print("🧠 SkillLens AI - Career Intelligence Platform")
    print("=" * 50)
    print("\n✅ Server starting...")
    print("📍 Open your browser and navigate to:")
    print("   http://127.0.0.1:5000")
    print("\n📝 Press Ctrl+C to stop the server\n")
    print("=" * 50)

    app.run(debug=True, host="0.0.0.0", port=5000)
