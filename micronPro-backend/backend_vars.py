from config import BackendConfiguration
import utils.logger as logger
log = logger.setup_logger("root")
configFile = BackendConfiguration()
log.debug("initalized logger")

workers = {5000: "0.0.0.0"}