from flask import Flask, request, jsonify, send_from_directory
from database import connect_db
from ai.analyzer import analyze_complaint, generate_action_recommendation
app = Flask(__name__, static_folder="frontend", static_url_path="")


# HOME PAGE
@app.route("/")
def home():
    return send_from_directory("frontend", "index.html")


# SUBMIT COMPLAINT
@app.route("/api/complaints", methods=["POST"])
def submit_complaint():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT description, id FROM complaints")
    existing_reports = cursor.fetchall()

    analysis = analyze_complaint(
        data["description"],
        data["category"],
        data["location"],
        existing_reports
    )

    cursor.execute("""
        INSERT INTO complaints
        (title, description, category, location)
        VALUES (?, ?, ?, ?)
    """, (
        data["title"],
        data["description"],
        data["category"],
        data["location"]
    ))

    complaint_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Complaint submitted successfully!",
        "complaint_id": complaint_id,
        "ai_analysis": analysis
    })


# ADMIN PAGE
@app.route("/admin")
def admin():
    return send_from_directory("frontend", "admin.html")


# GET ALL COMPLAINTS
@app.route("/api/complaints", methods=["GET"])
def get_complaints():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, description, category,
               location, status
        FROM complaints
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    complaints = []

    for row in rows:

        analysis = analyze_complaint(
            row[2], row[3], row[4], []
        
        )
        recommendation = generate_action_recommendation(
    row[3],
    analysis["priority"],
    row[2]
)

        complaints.append({
    "id": row[0],
    "title": row[1],
    "description": row[2],
    "category": row[3],
    "location": row[4],
    "status": row[5],
    "priority": analysis["priority"],
    "recommendation": recommendation
})

    return jsonify(complaints)


# UPDATE COMPLAINT STATUS
@app.route("/api/complaints/<int:complaint_id>", methods=["PUT"])
def update_status(complaint_id):

    data = request.get_json()

    allowed = ["Pending", "In Progress", "Resolved"]

    if not data or data.get("status") not in allowed:
        return jsonify({"error": "Invalid status"}), 400

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE complaints
        SET status = ?
        WHERE id = ?
    """, (data["status"], complaint_id))

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Complaint not found"}), 404

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Status updated successfully"
    })

# AI HOTSPOT DETECTION
@app.route("/api/hotspots", methods=["GET"])
def get_hotspots():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT location, COUNT(*)
        FROM complaints
        GROUP BY location
        ORDER BY COUNT(*) DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    hotspots = []

    for row in rows:
        hotspots.append({
            "location": row[0],
            "complaint_count": row[1]
        })

    return jsonify(hotspots)
# START FLASK SERVER
if __name__ == "__main__":
    app.run(debug=True)