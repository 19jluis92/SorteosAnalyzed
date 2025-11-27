import datetime
import logging

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
        urlStr = self.props.get("URL").data;
        self.logger.info("URL " + urlStr);
        url = (
            urlStr
        );
        self.csv = url;

    def loadCsvPandas(self):

        try:
            self.logger.info("DOWNLOAD CSV ");
            self.downloadCSV();
            numeros = pd.read_csv(self.csv,sep=",");
        except Exception as e:
            self.logger.error(e);
            self.logger.info("CSV " + self.props.get("CSV").data);
            numeros = pd.read_csv( self.props.get("CSV").data);
        # num_df.loc[num_df['a'] == 2]
        # filter the last change of the rules start = datetime.datetime(2007, 12, 9), end = datetime.datetime.now()
        return numeros.loc[numeros["CONCURSO"] >= int(self.props.get("FILTER").data)];

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
        return  str(len(datasetNumeros));
