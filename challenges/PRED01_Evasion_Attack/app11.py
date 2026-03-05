from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Modèle de détection de fraude simplifié (Logique "Black Box" pour l'utilisateur)
def model_predict(amount, distance, velocity):
    # Le modèle considère suspect : gros montant + grande distance + vitesse de transaction élevée
    score = (amount / 2000) + (distance / 100) + (velocity / 10)
    if score > 1.5:
        return "FRAUDE DÉTECTÉE", round(min(0.99, score/2), 2)
    return "TRANSACTION AUTORISÉE", round(score/2, 2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        res, conf = model_predict(float(data['amount']), float(data['distance']), float(data['velocity']))
        # Le flag est révélé si l'utilisateur fait passer une transaction de > 2000€ en "Autorisée"
        flag = "FLAG{EVASION_SUCCESS_442}" if res == "TRANSACTION AUTORISÉE" and float(data['amount']) > 2000 else None
        return jsonify({"status": res, "confidence": conf, "flag": flag})
    except:
        return jsonify({"error": "Données invalides"}), 400

if __name__ == '__main__':
    # Utilisation du port 5011 comme défini par votre logique main.py
    app.run(host="0.0.0.0", port=5011)
