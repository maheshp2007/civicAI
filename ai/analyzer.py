from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def analyze_complaint(description, category, location, existing_reports):

    # 1. Generate a short summary
    summary = description[:120]

    # 2. Detect priority
    urgent_words = [
        "danger", "accident", "flood",
        "emergency", "injury", "electric",
        "overflow", "blocked"
    ]

    medium_words = [
        "damage", "broken", "garbage",
        "water", "pothole"
    ]

    text = description.lower()

    if any(word in text for word in urgent_words):
        priority = "High"
        reason = "Contains potentially urgent safety-related keywords."

    elif any(word in text for word in medium_words):
        priority = "Medium"
        reason = "Contains keywords indicating a public infrastructure issue."

    else:
        priority = "Low"
        reason = "No urgent keywords detected."

    # 3. Duplicate detection using TF-IDF
    duplicate = None
    highest_similarity = 0

    if existing_reports:

        descriptions = [
            report[0] for report in existing_reports
        ]

        descriptions.append(description)

        vectorizer = TfidfVectorizer()

        vectors = vectorizer.fit_transform(descriptions)

        similarities = cosine_similarity(
            vectors[-1],
            vectors[:-1]
        )[0]

        highest_similarity = float(max(similarities))

        if highest_similarity >= 0.40:

            index = similarities.argmax()

            duplicate = {
                "complaint_id": existing_reports[index][1],
                "similarity": round(highest_similarity * 100, 2)
            }

    return {
        "summary": summary,
        "priority": priority,
        "reason": reason,
        "duplicate": duplicate
    }
def generate_action_recommendation(category, priority, description):

    category = category.lower()
    description = description.lower()

    if priority == "High":
        if "electric" in category or "wire" in description:
            return "Immediately alert the electricity department and secure the affected area."

        elif "water" in category or "flood" in description:
            return "Send an emergency response team to inspect the affected area."

        elif "road" in category:
            return "Place safety warnings and dispatch an urgent road repair team."

        else:
            return "Escalate this complaint immediately to the responsible department."

    elif category == "sanitation":
        return "Assign a sanitation team to inspect and clean the affected location."

    elif category == "water":
        return "Assign a water department team to inspect the pipeline and restore supply."

    elif category == "road":
        return "Schedule a road inspection and plan necessary repairs."

    elif category == "electricity":
        return "Forward the complaint to the electricity maintenance department."

    else:
        return "Assign this complaint to the relevant municipal department for inspection."