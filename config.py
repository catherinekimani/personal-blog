import os

class Config:
    '''
    General configuration parent class
    '''
    
class ProdConfig(Config):
    '''
    production configuration child class
    
    Args:
        Config: The parent configuration class with general configuration settings
    '''
    pass

class DevConfig(Config):
    '''
    Development configuration child class
    
    Args:
        Config: The parent configuration class with general configuration settings
    '''
    
    DEBUG  = True
    
config_options = {
    'development' : DevConfig,
    'production' : ProdConfig
}