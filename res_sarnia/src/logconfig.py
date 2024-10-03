import utili, logging

utili.pathassigner("log")
logging.basicConfig(
    filename='myapp.log',    
    format='[%(levelname)s] %(asctime)s [%(module)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
    force=True
)