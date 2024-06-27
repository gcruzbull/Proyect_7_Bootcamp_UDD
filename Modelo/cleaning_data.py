from pandas import DataFrame, to_numeric, read_pickle
from numpy import concatenate, nan
from sklearn.preprocessing import StandardScaler
from category_encoders import TargetEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

class CleaningClass:
    def __init__(self, df=None):
        self.df = df
        self.df_x_train_transformed = None
        self.df_x_test_transformed = None
        self.y_train = None
        self.y_test = None
        self.model = None
        self.numerical_scaler = None
        self.object_scaler = None

    def eliminar_duplicados(self):
        self.df = self.df.drop_duplicates().reset_index(drop=True)

    def convertir_reviews(self):
        self.df['Reviews'] = self.df['Reviews'].replace(',', '')
        self.df['Reviews'] = to_numeric(self.df['Reviews'], errors='coerce')

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
        self.df['Size'] = self.df['Size'].apply(self.convert_size).astype(float)

    @staticmethod
    def convert_installs(installs):
        if isinstance(installs, str):
            installs_clean = installs.replace(',', '').replace('+', '')
            if installs_clean.isdigit():
                return int(installs_clean)
        return nan

    def convertir_installs(self):
        self.df['Installs'] = self.df['Installs'].apply(self.convert_installs).astype(float)

    def imputar_nans(self):
        for column in self.df.columns:
            if self.df[column].dtype == 'object':
                self.df[column].fillna(self.df[column].mode()[0], inplace=True)
            else:
                self.df[column].fillna(self.df[column].mean(), inplace=True)

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
            inf, sup = self.rango_intercuartilico(self.df[col])
            self.df[col] = self.df[col].apply(lambda x: inf if x < inf else sup if x > sup else x)

    