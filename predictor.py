def predict_health(glucose, haemoglobin, cholesterol):

    if glucose > 140:
        return "High Diabetes Risk"

    elif cholesterol > 240:
        return "High Cholesterol Risk"

    elif haemoglobin < 12:
        return "Possible Anemia Risk"

    else:
        return "Normal Health Indicators"