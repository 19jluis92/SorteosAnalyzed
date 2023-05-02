import datetime
import logging
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

from brain.NumerosModel import NumerosModel


class BrainCSV:


    def __init__(self, props,sorteoId = 3 , start = datetime.datetime(2007, 12, 9), end = datetime.datetime.now()):
        self.logger = logging.getLogger('sorteosLogger');
        self.logger.info("STARTING BRAIN CSV");
        self._sorteoId =sorteoId;
        self._start = start;
        self._end = end;
        self.props = props;

    def loadCsvPandas(self):
        self.logger.info("CSV "+self.props.get("CSV").data);
        numeros = pd.read_csv(self.props.get("CSV").data)
        return numeros

    def melateAnalyzedPandas(self):
        #ReadCSV example https://naps.com.mx/blog/3-ejemplos-explicados-de-machine-learning-en-python/
        datasetNumeros = self.loadCsvPandas();

        #load to Model
        # for item in result:
        #     model = NumerosModel(item[0],item[1],item[2],item[3]);
        #     winnerList.append(str(item[1]));
        #     self.logger.debug("Item :"+str(model));
        #     numerosList.append(model);
        # self.numerosList = numerosList;

        #TODO calculate here whaterever you want
        datos_numericos = datasetNumeros.select_dtypes(np.number);

        #Although we already selected only the numeric values, some of these contain NaN (Not a Number) values,
        #so we are going to replace them with 0
        datos_numericos = datasetNumeros.select_dtypes(np.number).fillna(0);

        objetivos = datos_numericos[['R1','R2','R3','R4','R5','R6']];
        #The independent variables would be all the others except 'R1','R2','R3','R4','R5','R6'
        #independientes = datos_numericos.drop(columns=objetivos).columns;
        independientes = datos_numericos[['CONCURSO']];

        modelo = LinearRegression();
        modelo.fit(X=independientes, y=objetivos);
        #datasetNumeros[["prediccion"]] = modelo.predict(datos_numericos[independientes]);
        datasetNumeros[['R1','R2','R3','R4','R5','R6']] = modelo.predict(independientes)
        print (datasetNumeros[["CONCURSO", "R1",'R2','R3','R4','R5','R6']].head())
        self.logger.info("Analyzed end ");