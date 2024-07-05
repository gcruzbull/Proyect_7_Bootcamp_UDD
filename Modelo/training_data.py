from pandas import DataFrame, to_numeric, read_pickle
from numpy import concatenate
from sklearn.preprocessing import StandardScaler
from category_encoders import TargetEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

df_google_sin_duplicados = read_pickle(r'Modelo/df_google_sin_duplicados.pkl')
x_train_ = read_pickle(r"Modelo/df_x_train_transformed.pkl")
y_train_ = read_pickle(r"Modelo/y_train.pkl")

class TrainingClass:
    def __init__(self, df=None):
        self.df = df
        self.df_google_sin_duplicados = df_google_sin_duplicados
        self.df_x_train_transformed = None
        self.df_x_test_transformed = None
        self.y_train = None
        self.y_test = None
        self.model = None
        self.numerical_scaler = None
        self.object_scaler = None
        
    def training_model(self):
        
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

        self.model = LinearRegression().fit(self.df_x_train_transformed, self.y_train)
        print("Modelo entrenado")

    def save_model(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump({
                'model': self.model,
                'numerical_scaler': self.numerical_scaler,
                'object_scaler': self.object_scaler
            }, file)
        print("Modelo guardado")

    def load_model(self, filename):
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.numerical_scaler = data['numerical_scaler']
            self.object_scaler = data['object_scaler']
        print("Modelo cargado")
        
    def predict(self, df):
        # Preprocesar los datos de entrada igual que los datos de entrenamiento
        df_num = df.select_dtypes(include=["float64", "int64"])
        df_obj = df.select_dtypes(include="object")

        if df_num.empty or df_obj.empty:
            raise ValueError("Los datos de entrada no contienen las columnas numéricas y/o categóricas necesarias.")

        df_num_transformed = self.numerical_scaler.transform(df_num)
        df_obj_transformed = self.object_scaler.transform(df_obj)

        df_transformed = concatenate((df_num_transformed, df_obj_transformed), axis=1)
        
        return self.model.predict(df_transformed)
    

# Crear instancia y entrenar modelo
model_class = TrainingClass()
model_class.training_model()
model_class.save_model("trained_model.pkl")





