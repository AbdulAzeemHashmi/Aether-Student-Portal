from flask import Flask, request, jsonify, send_from_directory, send_file
import os
from flask_cors import CORS
from pymongo import MongoClient, ASCENDING
import json

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# ──────────────────────────────────────────────
# MongoDB Configuration
# Change MONGO_URI to your Atlas connection string
# if you want to use MongoDB Atlas (cloud).
# Example Atlas URI:
#   "mongodb+srv://<user>:<pass>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
# ──────────────────────────────────────────────
MONGO_URI = "mongodb+srv://i240020:mharis10@cluster0.cpcgocr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGO_DB  = "AetherDB"

client = MongoClient(MONGO_URI)
db     = client[MONGO_DB]

# Collections (equivalent to MySQL tables)
users_col    = db["users"]
courses_col  = db["courses"]
progress_col = db["student_progress"]


def init_db():
    """Seed course data and create indexes on first run."""
    print("Checking Database Integrity...")

    # Unique index on roll_no for users
    users_col.create_index([("roll_no", ASCENDING)], unique=True)

    # Unique compound index for progress
    progress_col.create_index(
        [("roll_no", ASCENDING), ("course_code", ASCENDING)],
        unique=True
    )

    # Seed courses if the collection is empty
    if courses_col.count_documents({}) == 0:
        print("Seeding Course Data...")
        courses = [
            {"course_code": "CS1002", "course_name": "Introduction to Computing",    "credit_hours": 3, "semester_no": 1},
            {"course_code": "MT1003", "course_name": "Calculus & Analytical Geometry","credit_hours": 3, "semester_no": 1},
            {"course_code": "NS1001", "course_name": "Applied Physics",               "credit_hours": 3, "semester_no": 1},
            {"course_code": "SS1012", "course_name": "English Composition",           "credit_hours": 3, "semester_no": 1},
            {"course_code": "CS1004", "course_name": "Programming Fundamentals",      "credit_hours": 4, "semester_no": 2},
            {"course_code": "MT1005", "course_name": "Discrete Structures",           "credit_hours": 3, "semester_no": 2},
            {"course_code": "MT1008", "course_name": "Multivariable Calculus",        "credit_hours": 3, "semester_no": 2},
            {"course_code": "EE1005", "course_name": "Digital Logic Design",          "credit_hours": 4, "semester_no": 2},
            {"course_code": "SS1014", "course_name": "Expository Writing",            "credit_hours": 3, "semester_no": 2},
            {"course_code": "CS2001", "course_name": "Object Oriented Programming",   "credit_hours": 4, "semester_no": 3},
            {"course_code": "AI2001", "course_name": "Programming for AI",            "credit_hours": 4, "semester_no": 3},
            {"course_code": "MT1004", "course_name": "Linear Algebra",                "credit_hours": 3, "semester_no": 3},
            {"course_code": "AI2002", "course_name": "Artificial Intelligence",       "credit_hours": 4, "semester_no": 4},
            {"course_code": "CS2005", "course_name": "Database Systems",              "credit_hours": 4, "semester_no": 4},
            {"course_code": "CS2004", "course_name": "Software Engineering",          "credit_hours": 3, "semester_no": 4},
        ]
        courses_col.insert_many(courses)

    print("Database Ready.")


# ──────────────────────────────────────────────
# Static file serving (unchanged)
# ──────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory('.', 'login.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)


# ──────────────────────────────────────────────
# API Routes (response shapes are identical to before)
# ──────────────────────────────────────────────

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data     = request.get_json()
        roll     = data.get('roll')
        password = data.get('pass')

        user = users_col.find_one(
            {"roll_no": roll, "password": password},
            {"_id": 0}           # exclude Mongo's internal _id
        )

        if user:
            # Flatten profile_data into the response (same behaviour as before)
            p_data = user.get('profile_data')
            if p_data:
                if isinstance(p_data, str):
                    try:
                        p_data = json.loads(p_data)
                    except Exception:
                        p_data = {}
                user.update(p_data)
            return jsonify({"success": True, "user": user})

        return jsonify({"success": False, "message": "Invalid Roll Number or Password"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@app.route('/api/register', methods=['POST'])
def register():
    try:
        data     = request.get_json()
        name     = data.get('name')
        roll     = data.get('roll')
        password = data.get('pass')

        # Check if roll already exists
        if users_col.find_one({"roll_no": roll}):
            return jsonify({"success": False, "message": "Roll Number already registered"})

        # Insert user
        users_col.insert_one({
            "roll_no":      roll,
            "full_name":    name,
            "password":     password,
            "profile_data": None
        })

        # Initialise progress for every existing course as 'Locked'
        all_courses = list(courses_col.find({}, {"_id": 0, "course_code": 1}))
        if all_courses:
            progress_docs = [
                {"roll_no": roll, "course_code": c["course_code"], "status": "Locked"}
                for c in all_courses
            ]
            progress_col.insert_many(progress_docs)

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@app.route('/api/update-user', methods=['POST'])
def update_user():
    try:
        data      = request.json
        orig_roll = data.get('orig_roll')
        full_name = data.get('full_name')
        new_roll  = data.get('roll_number')
        password  = data.get('password')

        p_data = {
            "email": data.get('email'),
            "photo": data.get('photo')
        }

        # Update the user document
        users_col.update_one(
            {"roll_no": orig_roll},
            {"$set": {
                "full_name":    full_name,
                "roll_no":      new_roll,
                "password":     password,
                "profile_data": p_data
            }}
        )

        # If roll number changed, cascade to student_progress
        if orig_roll != new_roll:
            progress_col.update_many(
                {"roll_no": orig_roll},
                {"$set": {"roll_no": new_roll}}
            )

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@app.route('/api/get-profile', methods=['POST'])
def save_profile():
    try:
        data         = request.get_json()
        roll         = data.get('roll')
        profile_data = data.get('profile_data')

        users_col.update_one(
            {"roll_no": roll},
            {"$set": {"profile_data": profile_data}}
        )
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@app.route('/api/get-profile/<roll>', methods=['GET'])
def get_profile(roll):
    try:
        user = users_col.find_one({"roll_no": roll}, {"_id": 0, "profile_data": 1})
        if user and user.get('profile_data'):
            p = user['profile_data']
            # Handle both dict (stored natively) and JSON string (legacy)
            if isinstance(p, str):
                p = json.loads(p)
            return jsonify({"success": True, "profile": p})
        return jsonify({"success": True, "profile": None})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=3000, host='0.0.0.0')
