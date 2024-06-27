import os
from flask import Flask, request, jsonify
import pandas as pd
from pandas import DataFrame, read_pickle
from training_data import TrainingClass
import joblib
import pickle
from pandas import DataFrame, read_pickle
from numpy import concatenate
from sklearn.preprocessing import StandardScaler
from category_encoders import TargetEncoder
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from pickle import dump, load

df_google_sin_duplicados = read_pickle(r'Modelo/df_google_sin_duplicados.pkl')
x_train_ = read_pickle(r"C:/Users/gcruz_li35hm9/Desktop/Bootcamp_UDD_Ciencia_de_Datos/Proyecto_7_Bootcamp/Repositorio_Proyecto_7/Modelo/df_x_train_transformed.pkl")
y_train_ = read_pickle(r"Modelo/y_train.pkl")

app = Flask(__name__)

model_class = TrainingClass()
model_class.load_model("trained_model.pkl")

@app.route('/predict', methods=['POST'])

def predict():
    try:
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
        
        # Convertir las columnas numéricas a su tipo adecuado
        numeric_columns = ["Reviews", "Size", "Installs"]
        df_rankings[numeric_columns] = df_rankings[numeric_columns].apply(pd.to_numeric, errors='coerce')

        # Realizar la predicción
        predictions = model_class.predict(df_rankings)
        print(predictions)

        # Devolver la respuesta en formato JSON
        return jsonify({"response": predictions.tolist()})
    except Exception as e:
        # Captura cualquier excepción y devuelve un mensaje de error
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)