import os
from flask import Flask, request, jsonify
import pandas as pd
from pandas import DataFrame, to_numeric, read_pickle
import pickle
from model_clean import ModeloPredictivo

app = Flask(__name__)

# Ruta para realizar predicciones
@app.route('/predict', methods=['POST'])
def predict():
    # obtener los datos de form-data de la solicitud
    features = {
        "Reviews": request.form["Reviews"],
        "Size": request.form["Size"],
        "Installs": request.form["Installs"],
        "Type": str(request.form["Type"]),
        "Content Rating": str(request.form["Content Rating"]),
        "Genres": str(request.form["Genres"]),
        "Last Updated": str(request.form["Last Updated"]),
        "Current Ver": str(request.form["Current Ver"]),
        "Android Ver": str(request.form["Android Ver"])
    }

    # Crear un dataframe con los datos recibidos
    df_rankings = DataFrame([features])

    # Cargar el modelo y los escaladores
    model_path = 'Modelo/modelo_predictivo_2.pkl'
    object_scaler_path = 'Modelo/object_scaler.pkl'
    numerical_scaler_path = 'Modelo/numerical_scaler.pkl'
    model, numerical_scaler, object_scaler = ModeloPredictivo.load_model(model_path, numerical_scaler_path, object_scaler_path)

    # Realizar preprocesamiento en los datos de entrada
    df_rankings = model.preparar_datos()

    # Realizar la predicción
    predictions = model.ejecutar()
    print(predictions)

    # Devolver la respuesta en formato JSON
    return jsonify({"response": predictions.tolist()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
