from database import connect_db

sample_complaints = [
    ("Water Leakage", "Water pipeline leaking continuously", "Water", "Mangaluru"),
    ("Road Damage", "Large potholes on the main road", "Road", "Mangaluru"),
    ("Garbage Overflow", "Garbage overflowing near public park", "Sanitation", "Mangaluru"),
    ("Electric Wire", "Dangerous electric wire hanging near school", "Electricity", "Mangaluru"),
    ("Street Light", "Street lights are not working", "Electricity", "Moodbidri"),
    ("Water Supply", "No water supply for two days", "Water", "Moodbidri"),
    ("Road Pothole", "Large potholes creating accident risk", "Road", "Moodbidri"),
    ("Drainage", "Drainage water overflowing onto road", "Sanitation", "Moodbidri"),
    ("Garbage Issue", "Garbage not collected for several days", "Sanitation", "Mangaluru"),
    ("Broken Road", "Road surface is badly damaged", "Road", "Udupi"),
    ("Water Leakage", "Pipeline leakage wasting drinking water", "Water", "Udupi"),
    ("Electric Hazard", "Electric wire fallen near houses", "Electricity", "Udupi"),
    ("Street Light", "Street lights not working at night", "Electricity", "Udupi"),
    ("Drain Block", "Drain blocked and water overflowing", "Sanitation", "Mangaluru"),
    ("Road Damage", "Potholes causing traffic problems", "Road", "Mangaluru"),
    ("Water Problem", "Water pipeline damaged", "Water", "Moodbidri"),
    ("Garbage", "Garbage piles near residential area", "Sanitation", "Udupi"),
    ("Electricity", "Exposed electric wire creating danger", "Electricity", "Mangaluru"),
    ("Road Issue", "Damaged road near bus stop", "Road", "Moodbidri"),
    ("Drainage Problem", "Blocked drainage causing overflow", "Sanitation", "Udupi")
]

conn = connect_db()
cursor = conn.cursor()

cursor.executemany("""
    INSERT INTO complaints
    (title, description, category, location)
    VALUES (?, ?, ?, ?)
""", sample_complaints)

conn.commit()
conn.close()

print("20 sample complaints added successfully!")