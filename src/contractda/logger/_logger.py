import logging

LOG = logging.getLogger("Test")
# LOG.setLevel(logging.CRITICAL)
LOG.setLevel(logging.ERROR)
# LOG.setLevel(logging.DEBUG)
#handler
handler = logging.StreamHandler()
#formatter
formatter = logging.Formatter(fmt='[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
handler.setFormatter(formatter)

LOG.addHandler(handler)


# LOG.debug("test")
# LOG.info("test")
# LOG.warning("test")
# LOG.error("test")
# LOG.critical("test")