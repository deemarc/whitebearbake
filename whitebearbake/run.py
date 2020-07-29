import os
import code

from flask_script import Manager
from flask_migrate import MigrateCommand

from whitebearbake import create_app

port = int(os.environ.get('PORT', 5000))
app = create_app()

def run():
    app.run(host='0.0.0.0', port=port)

def cli():
    """ Interactive CLI session entrypoint """
    with app.app_context():
        code.interact(local=locals())
        
def manage():
    from whitebearbake import migrate
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    manager.run()

# Run entrypoint
if __name__ == '__main__':
    run()