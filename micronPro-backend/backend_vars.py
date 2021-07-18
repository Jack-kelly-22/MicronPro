from config import BackendConfiguration
from database import MicroDatabase
import utils.logger as logger
log = logger.setup_logger("root")
configFile = BackendConfiguration()
database_client = MicroDatabase(configFile.get_configuration())
log.debug("initalized logger")

workers = {}
