import eel

@eel.expose  # Eel function
def set_title():  # Example to send data for javascript/html
    return "Code example - Eel + Bootstrap 4 + MongoDb"

if __name__ == '__main__':
    set_title()  # Init mongodb
    eel.init('web')  # Give folder containing web files
    eel.start('index.html', size=(800, 600))    # Start