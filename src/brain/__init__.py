import datetime
import database
import logging

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


    def melateAnalyzed(self):
        numerosList= list();
        #Connect to database
        db = database.Database(self.props.get("DBNAME").data,self.props.get("USERDB").data,self.props.get("PASSDB").data);
        #Execute Query to read numeros
        result = db.queryMany("Select *  FROM sorteos.numeros where sorteoId = "+str(self._sorteoId)+" and date >= '"
                              +self._start.strftime("%Y-%m-%d")+"' and date <= '"+ self._end.strftime("%Y-%m-%d")+"'");
        #Close connection
        db.__exit__();
        #load to Model
        for item in result:
            model = NumerosModel(item[0],self.parseNumber(str(item[1])),item[2],item[3]);
            self.logger.debug("Item :"+str(model));
            numerosList.append(model);
        self.numerosList = numerosList;
        #TODO calculate here whaterever you want

        self.logger.info("resultTest "+str(len(self.numerosList)));