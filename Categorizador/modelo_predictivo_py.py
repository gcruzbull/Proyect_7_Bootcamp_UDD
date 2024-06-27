# -*- coding: utf-8 -*-
"""modelo_predictivo.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DPmB8Z4vJHUfmBEIHdf1gzCPuUhm3QmY
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install category_encoders
# !pip install pickle5
# !pip install google.colab


from pandas import DataFrame, to_numeric, to_pickle, read_pickle, isna
from numpy import concatenate, nan, isnan
from sklearn.preprocessing import StandardScaler
from category_encoders import TargetEncoder
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from pickle import dump, load
import pickle

df_google_sin_duplicados = read_pickle(r'Modelo\df_google_sin_duplicados.pkl')

class ModeloPredictivo:
    def __init__(self, df=None):
        self.df = df
        self.df_google_sin_duplicados = df_google_sin_duplicados.copy()
        self.df_x_train_transformed = None
        self.df_x_test_transformed = None
        self.y_train = None
        self.y_test = None
        self.model = None
        self.numerical_scaler = None
        self.object_scaler = None

    def eliminar_duplicados(self):
        self.df_google_sin_duplicados = self.df.drop_duplicates().reset_index(drop=True)
        print("Duplicados eliminados")
        print(self.df_google_sin_duplicados.isna().sum())

    def convertir_reviews(self):
        self.df_google_sin_duplicados['Reviews'] = self.df_google_sin_duplicados['Reviews'].replace(',', '')
        self.df_google_sin_duplicados['Reviews'] = to_numeric(self.df_google_sin_duplicados['Reviews'], errors='coerce')
        print("Reviews convertidos")
        print(self.df_google_sin_duplicados['Reviews'].isna().sum())

    @staticmethod
    def convert_size(size):
        if isinstance(size, str):
            size = size.strip()
            if size.endswith('M'):
                return float(size[:-1]) * 1_000
            elif size.endswith('k'):
                return float(size[:-1])
            elif size == 'Varies with device':
                return nan
            else:
                try:
                    return float(size)
                except ValueError:
                    return nan
        return nan

    def convertir_tamano(self):
        self.df_google_sin_duplicados['Size'] = self.df_google_sin_duplicados['Size'].apply(self.convert_size).astype(float)
        print("Tamaño convertido")
        print(self.df_google_sin_duplicados['Size'].isna().sum())

    @staticmethod
    def convert_installs(installs):
        if isinstance(installs, str):
            installs_clean = installs.replace(',', '').replace('+', '')
            if installs_clean.isdigit():
                return int(installs_clean)
        return nan

    def convertir_installs(self):
        self.df_google_sin_duplicados['Installs'] = self.df_google_sin_duplicados['Installs'].apply(self.convert_installs).astype(float)
        print("Installs convertidos")
        print(self.df_google_sin_duplicados['Installs'].isna().sum())

    def imputar_nans(self):
        self.df_google_sin_duplicados["Rating"] = self.df_google_sin_duplicados["Rating"].fillna(self.df_google_sin_duplicados["Rating"].median())
        self.df_google_sin_duplicados["Size"] = self.df_google_sin_duplicados["Size"].fillna(self.df_google_sin_duplicados["Size"].mean())
        self.df_google_sin_duplicados["Installs"] = self.df_google_sin_duplicados["Installs"].fillna(self.df_google_sin_duplicados["Installs"].mean())
        self.df_google_sin_duplicados["Type"] = self.df_google_sin_duplicados["Type"].fillna("Free")
        self.df_google_sin_duplicados["Current Ver"] = self.df_google_sin_duplicados["Current Ver"].fillna("Varies with device")
        self.df_google_sin_duplicados["Android Ver"] = self.df_google_sin_duplicados["Android Ver"].fillna("4.1 and up")
        print("NaNs imputados")
        print(self.df_google_sin_duplicados.isna().sum())

    @staticmethod
    def rango_intercuartilico(columna):
        Q1 = columna.quantile(0.25)
        Q3 = columna.quantile(0.75)
        IQR = Q3 - Q1
        valor_min = Q1 - (1.5 * IQR)
        valor_max = Q3 + (1.5 * IQR)
        return valor_min, valor_max

    def imputar_outliers(self, columns):
        columns = ['Reviews', 'Size', 'Installs']
        for col in columns:
            inf, sup = self.rango_intercuartilico(self.df_google_sin_duplicados[col])
            self.df_google_sin_duplicados[col] = self.df_google_sin_duplicados[col].apply(lambda x: inf if x < inf else sup if x > sup else x)
        print("Outliers imputados")
        print(self.df_google_sin_duplicados.isna().sum())

    def preparar_datos(self):
        y = self.df_google_sin_duplicados[['Rating']]
        x = self.df_google_sin_duplicados.drop(columns="Rating", axis=1)
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42, shuffle=True)

        numeric_cols = x.select_dtypes(include=["float64", "int64"])
        categorical_cols = x.select_dtypes(include="object")

        self.object_scaler = TargetEncoder(cols=categorical_cols.columns)
        self.numerical_scaler = StandardScaler()

        x_train_num = x_train.select_dtypes(include=["float64", "int64"])
        x_test_num = x_test.select_dtypes(include=["float64", "int64"])
        x_train_obj = x_train.select_dtypes(include=(["object"]))
        x_test_obj = x_test.select_dtypes(include=(["object"]))

        x_train_num_transformed = self.numerical_scaler.fit_transform(x_train_num, y_train)
        x_train_obj_transformed = self.object_scaler.fit_transform(x_train_obj, y_train)
        x_test_num_transformed = self.numerical_scaler.transform(x_test_num)
        x_test_obj_transformed = self.object_scaler.transform(x_test_obj)

        x_test_transformed = concatenate((x_test_num_transformed, x_test_obj_transformed), axis=1)
        x_train_transformed = concatenate((x_train_num_transformed, x_train_obj_transformed), axis=1)

        self.df_x_train_transformed = DataFrame(x_train_transformed, columns=numeric_cols.columns.tolist() + categorical_cols.columns.tolist())
        self.df_x_test_transformed = DataFrame(x_test_transformed, columns=numeric_cols.columns.tolist() + categorical_cols.columns.tolist())
        self.y_train = y_train
        self.y_test = y_test

        print("Datos preparados")
        print("X_train NaNs:", self.df_x_train_transformed.isna().sum().sum())
        print("X_test NaNs:", self.df_x_test_transformed.isna().sum().sum())

    def entrenar_modelo(self):
        self.model = LinearRegression().fit(self.df_x_train_transformed, self.y_train)
        print("Modelo entrenado")

    def predecir(self):
        return self.model.predict(self.df_x_test_transformed)

    def guardar_modelo(self, modelo_path, object_scaler_path, numerical_scaler_path):
        with open(modelo_path, 'wb') as modelo_file:
            pickle.dump(self.model, modelo_file)
        with open(numerical_scaler_path, 'wb') as numerical_scaler_file:
            pickle.dump(self.numerical_scaler, numerical_scaler_file)
        with open(object_scaler_path, 'wb') as object_scaler_file:
            pickle.dump(self.object_scaler, object_scaler_file)
        print("Modelo guardado")

    @staticmethod
    def load_model(model_path, numerical_scaler_path, object_scaler_path):
        # Load your model and scalers from their respective paths
        with open(model_path, 'rb') as model_file:
            model = pickle.load(model_file)

        with open(numerical_scaler_path, 'rb') as numerical_scaler_file:
            numerical_scaler = pickle.load(numerical_scaler_file)

        with open(object_scaler_path, 'rb') as object_scaler_file:
            object_scaler = pickle.load(object_scaler_file)

        return model, numerical_scaler, object_scaler

    def ejecutar(self):
        self.eliminar_duplicados()
        self.convertir_reviews()
        self.convertir_tamano()
        self.convertir_installs()
        self.imputar_nans()
        self.imputar_outliers(['Reviews', 'Size', 'Installs'])
        self.preparar_datos()
        self.entrenar_modelo()
        return self.predecir()