import logging
import brain
import brainCsv
from jproperties import Properties

global level;
global configs;
global logger;

configs = Properties();
def loadProperties():
    with open('sorteos.properties', 'rb') as read_prop:
        configs.load(read_prop);

def loggingDefinition():
    global logger;
    if(configs.get("LOG_LEVEL").data=="info"):
        logLevel= 20;
    elif(configs.get("LOG_LEVEL").data=="debug"):
        logLevel= 10;
    elif(configs.get("LOG_LEVEL").data=="error"):
        logLevel= 40;
    else:
        logLevel= 20;
    logging.basicConfig(filename='sorteos.log', level=logLevel, filemode=configs.get("LOG_MODE").data);
    logger = logging.getLogger('sorteosLogger');
    logger.setLevel(logLevel);

def executeBrain():
    logger.info('Calling Brain');
    if(configs.get("DATASET").data=="1"):
        executor = brain.Brain(configs);
        return executor.melateAnalyzedPandas();
    else:
        executor = brainCsv.BrainCSV(configs);
        return executor.melateAnalyzedPandas();

# args = sys.argv[1:] parameter from system
def main():
    loadProperties();
    loggingDefinition();
    logger.info('STARTING SORTEOS');
    result = executeBrain();
    print(result)

if __name__ == "__main__":
    main();
