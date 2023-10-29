from distutils.log import debug
from website import create_app 

# Only starts application when this file is ran, not imported
if __name__ == '__main__': 
    app = create_app()
    app.run(debug=True) # Automatically reruns server - turn off in production
