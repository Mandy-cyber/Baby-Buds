from distutils.log import debug
from website import create_app 

# only starts application when this file is ran, not imported
if __name__ == '__main__': 
    app = create_app()
    app.run(debug=True) # automatically reruns server - turn off in production
