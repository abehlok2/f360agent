import adsk.core
import adsk.fusion
import traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        # Your code to interact with Fusion 360's API goes here
        ui.messageBox('Hello from your Fusion 360 Add-on!')
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    # Perform any cleanup tasks here when the add-on is stopped
    pass
