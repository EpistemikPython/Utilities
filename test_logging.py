import logging as lg
import logging.config as lgconf
import yaml

with open('logging.yaml', 'r') as fp:
    log_cfg = yaml.safe_load(fp.read())
lgconf.dictConfig(log_cfg)
# lgr = lg.getLogger('gnucash')
