import os

class Config:
    '''
    General configuration parent class
    '''
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    SECRET_KEY='katewambui'
    
class ProdConfig(Config):
    '''
    production configuration child class
    
    Args:
        Config: The parent configuration class with general configuration settings
    '''
    uri = os.getenv('DATABASE_URL')
    if uri and uri.startswith('postgres://'):
        uri = uri.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = uri

class DevConfig(Config):
    '''
    Development configuration child class
    
    Args:
        Config: The parent configuration class with general configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:wambui@localhost/blogs'
    
    DEBUG  = True
    
config_options = {
    'development' : DevConfig,
    'production' : ProdConfig
}