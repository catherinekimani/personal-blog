from app import create_app,db
from flask_script import Manager,Server
from app.models import User,Blog,Comments
from flask_migrate import Migrate,MigrateCommand

# create app instance
app = create_app('development')

manager = Manager(app)
manager.add_command('server',Server)

@manager.shell
def make_shell_context():
    return dict(app = app, db = db, User = User, Blog = Blog, Comments = Comments)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

# test
@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
