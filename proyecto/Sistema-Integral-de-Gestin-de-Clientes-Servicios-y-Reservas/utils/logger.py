import logging
import os
from logging.handlers import RotatingFileHandler

class LoggerSistema:
    _instancia = None
    
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._configurar()
        return cls._instancia
    
    def _configurar(self):
        try:
            os.makedirs('data', exist_ok=True)
        except:
            pass
        
        self.logger = logging.getLogger('SoftwareFJ')
        self.logger.setLevel(logging.DEBUG)
        
        if self.logger.handlers:
            return
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        try:
            handler = RotatingFileHandler(
                'data/eventos.log',
                maxBytes=1024*1024,
                backupCount=5,
                encoding='utf-8'
            )
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        except:
            pass
        
        console = logging.StreamHandler()
        console.setLevel(logging.WARNING)
        console.setFormatter(formatter)
        self.logger.addHandler(console)
        
        self.logger.info("sistema iniciado")
    
    def info(self, msg):
        self.logger.info(msg)
    
    def warning(self, msg):
        self.logger.warning(msg)
    
    def error(self, msg):
        self.logger.error(msg)
    
    def debug(self, msg):
        self.logger.debug(msg)
    
    def exception(self, msg):
        self.logger.exception(msg)


_logger = None

def get_logger():
    global _logger
    if _logger is None:
        _logger = LoggerSistema()
    return _logger