from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Almacenamiento temporal en memoria (sin base de datos, según lo solicitado)
interacciones = []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/respuesta", methods=["POST"])
def respuesta():
    data = request.get_json(silent=True) or {}

    respuesta_valor = data.get("respuesta")
    intentos = data.get("intentos", 0)

    if respuesta_valor not in ("si", "no"):
        return jsonify({"success": False, "error": "Respuesta inválida"}), 400

    registro = {
        "respuesta": respuesta_valor,
        "intento": intentos,
        "hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    interacciones.append(registro)

    return jsonify({
        "success": True,
        "respuesta": respuesta_valor,
        "intentos": intentos
    })


@app.route("/estadisticas")
def estadisticas():
    veces_no = sum(1 for i in interacciones if i["respuesta"] == "no")
    veces_si = sum(1 for i in interacciones if i["respuesta"] == "si")

    return jsonify({
        "total_interacciones": len(interacciones),
        "veces_no": veces_no,
        "veces_si": veces_si
    })


if __name__ == "__main__":
    app.run(debug=True)
