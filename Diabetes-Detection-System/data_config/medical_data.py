# Data and configuration dictionary for Diabetes Detection System (DDS)

FIELD_GUIDANCE = {
    "pregnancies": {
        "title": "Number of Pregnancies",
        "description": "Total number of times pregnant.",
        "how_to_obtain": "Self-reported background detail.",
        "normal_range": "0 - 17",
        "unit": "count",
        "tip": "Gestational diabetes history increases long-term risk."
    },
    "glucose": {
        "title": "Plasma Glucose Concentration",
        "description": "Fasting blood sugar level measured 2 hours after an oral glucose tolerance test.",
        "how_to_obtain": "Obtained via a Fasting Blood Sugar (FBS) or Oral Glucose Tolerance Test (OGTT) at a diagnostic clinical lab or pharmacy.",
        "normal_range": "70 - 99 mg/dL (Fasting), < 140 mg/dL (Post-meal)",
        "unit": "mg/dL",
        "tip": "Fasting levels between 100-125 mg/dL indicate prediabetes, while 126+ mg/dL suggests diabetes."
    },
    "blood_pressure": {
        "title": "Diastolic Blood Pressure",
        "description": "The pressure in your arteries when your heart rests between beats.",
        "how_to_obtain": "Measured using an automatic digital Home BP Monitor, arm cuff at a clinic, or local pharmacy blood pressure kiosk.",
        "normal_range": "60 - 80 mm Hg",
        "unit": "mm Hg",
        "tip": "Consistently elevated BP (>80 mm Hg diastolic) increases cardiovascular and diabetes-related risks."
    },
    "skin_thickness": {
        "title": "Triceps Skinfold Thickness",
        "description": "A measurement of body subcutaneous fat layer thickness over the triceps muscle.",
        "how_to_obtain": "Measured using a skinfold caliper by a dietitian, fitness center clinician, or medical examiner.",
        "normal_range": "10 - 30 mm",
        "unit": "mm",
        "tip": "If unknown, standard population average is ~20 mm."
    },
    "insulin": {
        "title": "2-Hour Serum Insulin",
        "description": "Level of insulin hormone in blood 2 hours after consuming glucose.",
        "how_to_obtain": "Obtained through a blood test at a clinical pathology laboratory (Fasting or OGTT Insulin Test).",
        "normal_range": "16 - 166 mu U/ml",
        "unit": "mu U/ml",
        "tip": "High insulin levels indicate insulin resistance, where body cells do not respond effectively to insulin."
    },
    "bmi": {
        "title": "Body Mass Index (BMI)",
        "description": "Measure of body weight relative to height squared.",
        "how_to_obtain": "Calculated as Weight (kg) divided by Height squared (m²). You can use our built-in instant BMI Calculator widget!",
        "normal_range": "18.5 - 24.9 kg/m²",
        "unit": "kg/m²",
        "tip": "BMI 25.0 - 29.9 is Overweight; 30.0+ indicates Obesity."
    },
    "diabetes_pedigree": {
        "title": "Diabetes Pedigree Function",
        "description": "A genetic scoring function estimating hereditary diabetes risk based on family history.",
        "how_to_obtain": "Calculated based on documented direct relatives (parents, grandparents, siblings) diagnosed with diabetes.",
        "normal_range": "0.08 - 0.50 (Low/Normal family history score)",
        "unit": "score",
        "tip": "Scores > 0.50 reflect stronger genetic inclination towards diabetes."
    },
    "age": {
        "title": "Age",
        "description": "Current age in full years.",
        "how_to_obtain": "Self-reported current age.",
        "normal_range": "21 - 80+ years",
        "unit": "years",
        "tip": "Diabetes risk generally increases with age, particularly after age 45."
    }
}

HEALTHY_MEDIANS = {
    "pregnancies": 1,
    "glucose": 95.0,
    "blood_pressure": 70.0,
    "skin_thickness": 20.0,
    "insulin": 85.0,
    "bmi": 22.5,
    "diabetes_pedigree": 0.30,
    "age": 30
}

WEEKLY_DIET_PLAN = [
    {
        "day": "Monday",
        "breakfast": "Steel-cut oatmeal topped with flaxseeds, chia seeds, and 5 almonds.",
        "lunch": "Grilled chicken/tofu salad with mixed green leafy vegetables, cucumber, and olive oil lemon dressing.",
        "dinner": "Steamed salmon/lentil soup with quinoa and sautéed broccoli/spinach.",
        "snack": "Handful of walnuts or sliced cucumber with hummus."
    },
    {
        "day": "Tuesday",
        "breakfast": "Greek yogurt (unsweetened) with fresh berries and cinnamon.",
        "lunch": "Brown rice with dal/chana, steamed beans, and a side of cucumber salad.",
        "dinner": "Baked turkey breast / Paneer tikka with sautéed bell peppers and zucchini.",
        "snack": "1 small apple with peanut butter."
    },
    {
        "day": "Wednesday",
        "breakfast": "Vegetable omelet (2 egg whites or scrambled tofu) with spinach and tomatoes.",
        "lunch": "Whole grain wrap filled with grilled veggies, avocado, and black beans.",
        "dinner": "Grilled fish / Chickpea curry with cauliflower rice and green salad.",
        "snack": "Roasted makhana (fox nuts) or pumpkin seeds."
    },
    {
        "day": "Thursday",
        "breakfast": "Chia seed pudding made with unsweetened almond milk and crushed walnuts.",
        "lunch": "Quinoa bowl with roasted chickpeas, cherry tomatoes, and kale.",
        "dinner": "Lentil curry (Moong dal) with boiled buckwheat/brown rice and sautéed asparagus.",
        "snack": "Carrot sticks with guacamole."
    },
    {
        "day": "Friday",
        "breakfast": "Multi-grain toast with mashed avocado and poached egg / cottage cheese.",
        "lunch": "Mediterranean salad bowl with feta, olives, chickpeas, cucumber, and tomato.",
        "dinner": "Herb-baked chicken / Tofu stir-fry with mixed vegetables and brown rice.",
        "snack": "Handful of almonds and a cup of green tea."
    },
    {
        "day": "Saturday",
        "breakfast": "Moong dal chilla / Buckwheat pancake with mint chutney.",
        "lunch": "Grilled fish/soya chunks with green garden salad and a small portion of sweet potato.",
        "dinner": "Vegetable soup with whole wheat garlic toast.",
        "snack": "Boiled edamame or pumpkin seeds."
    },
    {
        "day": "Sunday",
        "breakfast": "Smoothie made with spinach, unsweetened almond milk, protein powder, and flaxseeds.",
        "lunch": "Mixed grain rotis / quinoa with mixed vegetable curry and fresh curd.",
        "dinner": "Roasted paneer/chicken with steamed green beans and salad.",
        "snack": "Handful of roasted chickpeas."
    }
]

LIFESTYLE_RECOMMENDATIONS = [
    "Engage in at least 30 minutes of moderate aerobic exercise (brisk walking, cycling, swimming) 5 days a week.",
    "Include strength training or resistance exercises 2 times a week to improve cellular insulin sensitivity.",
    "Maintain adequate daily hydration — drink 2.5 to 3 liters of water throughout the day.",
    "Avoid sugary beverages, refined carbs (white bread, pastries), and processed high-glycemic foods.",
    "Aim for 7 to 8 hours of quality sleep per night; poor sleep adversely affects blood glucose regulation.",
    "Practice stress reduction techniques such as deep breathing exercises, yoga, or daily mindfulness meditation."
]

DOCTOR_ADVISORY = {
    "disclaimer": "This tool is powered by Machine Learning and serves as an educational screening aid. It DOES NOT replace a professional clinical diagnosis.",
    "immediate_consultation": {
        "condition": "Fasting Glucose > 180 mg/dL or Blood Pressure > 100 mm Hg or severe symptoms",
        "action": "Immediate Medical Consultation Required",
        "description": "Your reported medical parameters indicate significantly elevated blood sugar or blood pressure. Please consult a qualified doctor or visit an urgent care clinic promptly. Watch out for urgent symptoms like excessive thirst, frequent urination, blurred vision, or extreme fatigue."
    },
    "routine_consultation": {
        "condition": "Screening result indicates high diabetes risk (Probability > 50%)",
        "action": "Schedule a Consultation within 1-2 Weeks",
        "description": "Your screening result indicates a high probability of diabetes. We strongly advise scheduling an appointment with an Endocrinologist, Diabetologist, or General Physician for a formal clinical evaluation."
    },
    "recommended_specialists": [
        "Endocrinologist (Hormone & Diabetes Specialist)",
        "Diabetologist",
        "General Physician / Internal Medicine Specialist",
        "Certified Clinical Dietitian / Diabetic Educator"
    ],
    "diagnostic_tests_to_ask_for": [
        "HbA1c Test (Glycated Hemoglobin Test) — standard 3-month average glucose indicator",
        "Fasting Plasma Glucose (FPG) Test",
        "Oral Glucose Tolerance Test (OGTT)",
        "Lipid Profile & Kidney Function Test"
    ]
}
