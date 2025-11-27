import datetime
import database
import logging
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

from brain.NumerosModel import NumerosModel


class Brain:


    def __init__(self, props,sorteoId = 3 , start = datetime.datetime(2007, 12, 9), end = datetime.datetime.now()):
        self.logger = logging.getLogger('sorteosLogger');
        self.logger.info("STARTING BRAIN");
        self._sorteoId =sorteoId;
        self._start = start;
        self._end = end;
        self.props = props;

    def parseNumber(self,numero):
        temp = numero[0:2]+","+numero[2:4]+","+numero[4:6]+","+numero[6:8]+","+numero[8:10]+","+numero[10:12];
        return temp;


    def melateAnalyzedPandas(self):
        numerosList= list();
        winnerList= list();
        #Connect to database
        db = database.Database(self.props.get("DBNAME").data,self.props.get("USERDB").data,self.props.get("PASSDB").data);
        #Execute Query to read numeros
        result = db.queryMany("Select *  FROM sorteos.numeros where sorteoId = "+str(self._sorteoId)+" and date >= '"
                              +self._start.strftime("%Y-%m-%d")+"' and date <= '"+ self._end.strftime("%Y-%m-%d")+"'  order by numeroSorteo desc");
        #Close connection
        db.__exit__();
        #load to Model
        # for item in result:
        #     model = NumerosModel(item[0],self.parseNumber(str(item[1])),item[2],item[3]);
        #     winnerList.append(self.parseNumber(str(item[1])));
        #     self.logger.debug("Item :"+str(model));
        #     numerosList.append(model);
        # self.numerosList = numerosList;

        #load Pandas model
        pdList = [];
        for item in result:
            numero = item[1];
            self.logger.debug("Item :"+str(numero));
            pdList.append([item[3],numero[0:2], numero[2:4], numero[4:6], numero[6:8], numero[8:10], numero[10:12]]);
            # winnerList.append(self.parseNumber(str(item[1])));
        #convert db information to pandas DataFrame
        #using PANDAS
        columnList = ['CONCURSO','R1','R2','R3','R4','R5','R6'];
        datasetNumeros = pd.DataFrame(pdList, columns=columnList)
        self.logger.info("Inforation Size: "+str(len(datasetNumeros)));

        #TODO calculate here whaterever you want
        #datos_numericos = datasetNumeros.select_dtypes(np.number);

        #Although we already selected only the numeric values, some of these contain NaN (Not a Number) values,
        #so we are going to replace them with 0
        #datos_numericos = datasetNumeros.select_dtypes(np.number).fillna(0);

        objetivos = datasetNumeros[['R1','R2','R3','R4','R5','R6']];
        #The independent variables would be all the others except 'R1','R2','R3','R4','R5','R6'
        #independientes = datos_numericos.drop(columns=objetivos).columns;
        independientes = datasetNumeros[['CONCURSO']];

        modelo = LinearRegression();
        modelo.fit(X=independientes, y=objetivos);
        #datasetNumeros[["prediccion"]] = modelo.predict(datos_numericos[independientes]);
        datasetNumeros[['R1','R2','R3','R4','R5','R6']] = modelo.predict(independientes)
        self.logger.info(datasetNumeros[["CONCURSO", "R1",'R2','R3','R4','R5','R6']].head())
        self.logger.info("Analyzed end ");

        self.logger.info("resultTest "+str(len(pdList)));
        return str(len(pdList));