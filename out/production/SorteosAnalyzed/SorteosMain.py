import logging
import brain
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
    if(configs.get("Log_Level").data=="info"):
        logLevel= 20;
    elif(configs.get("Log_Level").data=="debug"):
        logLevel= 10;
    elif(configs.get("Log_Level").data=="error"):
        logLevel= 40;
    else:
        logLevel= 20;
    logging.basicConfig(filename='sorteos.log', level=logLevel);
    logger = logging.getLogger('sorteosLogger');
    logger.setLevel(logLevel);

def executeBrain():
    logger.info('Calling Brain');
    executor = brain.Brain(configs);
    executor.melateAnalyzed();

# args = sys.argv[1:] parameter from system
def main():
    loadProperties();
    loggingDefinition();
    logger.info('STARTING SORTEOS');
    executeBrain();

if __name__ == "__main__":
    main();
