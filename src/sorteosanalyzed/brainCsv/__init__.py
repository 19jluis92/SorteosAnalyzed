import datetime
import logging
import ssl
import pandas as pd
import urllib.request
import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


class BrainCSV:

    def __init__(self, props, sorteoId=3, start=datetime.datetime(2007, 12, 9), end=datetime.datetime.now()):
        self.logger = logging.getLogger('sorteosLogger');
        self.logger.info("STARTING BRAIN CSV");
        self._sorteoId = sorteoId;
        self._start = start;
        self._end = end;
        self.props = props;

    def downloadCSV(self):
        """Intenta descargar el CSV y guardarlo localmente."""
        urlStr = self.props.get("URL").data
        local_csv = self.props.get("CSV").data  # Ej: Melate.csv

        self.logger.info("Intentando descargar: " + urlStr)

        try:
            # Crear contexto SSL sin verificación (porque el cert de Pronósticos está roto)
            ssl_context = ssl._create_unverified_context()

            response = urllib.request.urlopen(urlStr, context=ssl_context)
            data = response.read()

            # Guardar archivo local
            with open(local_csv, "wb") as f:
                f.write(data)

            self.logger.info("CSV descargado y guardado como: " + local_csv)
            return local_csv

        except Exception as e:
            self.logger.error(f"Error en descarga: {e}")
            return None

    def loadCsvPandas(self):

        local_csv = self.props.get("CSV").data  # Ej: Melate.csv

        # 1. Intentar descargar el archivo
        downloaded_file = self.downloadCSV()

        # 2. Si se descargó, usarlo
        if downloaded_file and os.path.exists(downloaded_file):
            return pd.read_csv(downloaded_file)

        # 3. Si no se descargó pero existe local
        if os.path.exists(local_csv):
            self.logger.info("Usando CSV local existente")
            return pd.read_csv(local_csv)

        # 4. Si no existe nada → error
        raise FileNotFoundError(
            f"No se pudo obtener el archivo CSV.\n"
            f"- URL falló (certificado inválido)\n"
            f"- Archivo local '{local_csv}' no existe."
        )

    def melateAnalyzedPandas(self):
        # ReadCSV example https://naps.com.mx/blog/3-ejemplos-explicados-de-machine-learning-en-python/
        datasetNumeros = self.loadCsvPandas();
        self.logger.info("Inforation Size: " + str(len(datasetNumeros)));

        # TODO calculate here whaterever you want
        datos_numericos = datasetNumeros.select_dtypes(np.number);

        # Although we already selected only the numeric values, some of these contain NaN (Not a Number) values,
        # so we are going to replace them with 0
        datos_numericos = datasetNumeros.select_dtypes(np.number).fillna(0);

        objetivos = datos_numericos[['R1', 'R2', 'R3', 'R4', 'R5', 'R6']];
        # The independent variables would be all the others except 'R1','R2','R3','R4','R5','R6'
        # independientes = datos_numericos.drop(columns=objetivos).columns;
        independientes = datos_numericos[['CONCURSO']];

        modelo = LinearRegression();
        modelo.fit(X=independientes, y=objetivos);
        # datasetNumeros[["prediccion"]] = modelo.predict(datos_numericos[independientes]);
        datasetNumeros[['R1', 'R2', 'R3', 'R4', 'R5', 'R6']] = modelo.predict(independientes)
        self.logger.info(datasetNumeros[["CONCURSO", "R1", 'R2', 'R3', 'R4', 'R5', 'R6']].head())
        self.logger.info("Analyzed end ");
        self.logger.info("resultTest " + str(len(datasetNumeros)));
        return str(int(datasetNumeros["R1"][0]))+" | "+str(int(datasetNumeros["R2"][0]))+" | "+str(int(datasetNumeros["R3"][0]))+" | "+str(int(datasetNumeros["R4"][0]))+" | "+str(int(datasetNumeros["R5"][0]))+" | "+str(int(datasetNumeros["R6"][0]));