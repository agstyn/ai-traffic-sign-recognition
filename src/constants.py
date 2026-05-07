CLASS_NAMES = [
    "Speed limit 20", "Speed limit 30", "Speed limit 50",
    "Speed limit 60", "Speed limit 70", "Speed limit 80",
    "End speed limit 80", "Speed limit 100", "Speed limit 120",
    "No passing", "No passing >3.5t", "Right of way",
    "Priority road", "Yield", "Stop", "No vehicles",
    "No vehicles >3.5t", "No entry", "General caution",
    "Dangerous curve left", "Dangerous curve right", "Double curve",
    "Bumpy road", "Slippery road", "Road narrows right",
    "Road work", "Traffic signals", "Pedestrians", "Children crossing",
    "Bicycles crossing", "Ice/snow", "Wild animals crossing",
    "End restrictions", "Turn right ahead", "Turn left ahead",
    "Ahead only", "Go straight or right", "Go straight or left",
    "Keep right", "Keep left", "Roundabout", "End no passing",
    "End no passing >3.5t"
]

ADVISORY = {
    "Speed limit 20":        "Reduce speed to 20 km/h immediately.",
    "Speed limit 30":        "Reduce speed to 30 km/h.",
    "Speed limit 50":        "Maintain speed below 50 km/h.",
    "Speed limit 60":        "Maintain speed below 60 km/h.",
    "Speed limit 70":        "Maintain speed below 70 km/h.",
    "Speed limit 80":        "Maintain speed below 80 km/h.",
    "End speed limit 80":    "Speed limit restriction lifted.",
    "Speed limit 100":       "Maintain speed below 100 km/h.",
    "Speed limit 120":       "Maintain speed below 120 km/h.",
    "No passing":            "No overtaking allowed in this zone.",
    "No passing >3.5t":      "No overtaking for vehicles over 3.5 tonnes.",
    "Right of way":          "You have right of way at the next junction.",
    "Priority road":         "You are on a priority road.",
    "Yield":                 "Yield to oncoming traffic ahead.",
    "Stop":                  "STOP! Come to a complete halt now.",
    "No vehicles":           "No vehicles permitted beyond this point.",
    "No vehicles >3.5t":     "No heavy vehicles beyond this point.",
    "No entry":              "Wrong way! No entry permitted.",
    "General caution":       "Exercise general caution ahead.",
    "Dangerous curve left":  "Dangerous left curve ahead. Slow down.",
    "Dangerous curve right": "Dangerous right curve ahead. Slow down.",
    "Double curve":          "Double curve ahead. Reduce speed.",
    "Bumpy road":            "Bumpy road ahead. Reduce speed.",
    "Slippery road":         "Slippery road ahead. Drive carefully.",
    "Road narrows right":    "Road narrows on the right. Stay alert.",
    "Road work":             "Road work ahead. Slow down.",
    "Traffic signals":       "Traffic signals ahead. Be prepared.",
    "Pedestrians":           "Pedestrian zone. Watch for people.",
    "Children crossing":     "Children crossing! Slow down now.",
    "Bicycles crossing":     "Bicycle crossing ahead. Stay alert.",
    "Ice/snow":              "Icy road ahead. Drive with caution.",
    "Wild animals crossing": "Wild animals may cross. Stay alert.",
    "End restrictions":      "All restrictions lifted.",
    "Turn right ahead":      "Turn right at the next junction.",
    "Turn left ahead":       "Turn left at the next junction.",
    "Ahead only":            "Proceed straight ahead only.",
    "Go straight or right":  "Go straight or turn right.",
    "Go straight or left":   "Go straight or turn left.",
    "Keep right":            "Keep to the right side.",
    "Keep left":             "Keep to the left side.",
    "Roundabout":            "Roundabout ahead. Give way.",
    "End no passing":        "Overtaking permitted again.",
    "End no passing >3.5t":  "Heavy vehicle overtaking permitted.",
}

SIGN_CATEGORIES = {
    "Prohibitory": list(range(0, 9)) + [9, 10, 15, 16, 17, 41, 42],
    "Warning":     list(range(18, 32)),
    "Mandatory":   list(range(33, 43)),
    "Priority":    [11, 12, 13, 14, 32],
}

def get_category(class_id):
    for cat, ids in SIGN_CATEGORIES.items():
        if class_id in ids:
            return cat
    return "Other"

# Shared CSS
STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Google+Sans+Display&display=swap');

html, body, [class*="css"] {
    font-family: 'Google Sans', sans-serif !important;
}
.page-title {
    font-size: 2rem; font-weight: 700;
    color: #202124; margin-bottom: 0.2rem;
}
.page-sub {
    color: #5f6368; font-size: 0.95rem;
    margin-bottom: 2rem;
}
.card {
    background: #f8f9fa;
    border: 1px solid #e8eaed;
    border-radius: 12px;
    padding: 1.2rem;
}
.stat-num {
    font-size: 1.8rem; font-weight: 700; color: #1a73e8;
}
.stat-lbl {
    font-size: 0.78rem; color: #5f6368;
    text-transform: uppercase; letter-spacing: 0.5px;
}
.chip {
    display: inline-block;
    background: #e8f0fe; color: #1a73e8;
    border-radius: 20px; padding: 2px 10px;
    font-size: 0.78rem; font-weight: 500;
    margin: 2px;
}
.chip.warn  { background:#fef7e0; color:#b06000; }
.chip.stop  { background:#fce8e6; color:#c5221f; }
.chip.go    { background:#e6f4ea; color:#137333; }
</style>
"""