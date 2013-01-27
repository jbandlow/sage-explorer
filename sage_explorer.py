from flask import Flask
from flask import render_template
from flask import send_file

from reproducible_object import ReproducibleObject
from display import display_object, display_help, display_methods, display_properties
import config

##############################################################################
# Setup of the web application

# Stupid test that we are not running within Sage
if not "Permutations" in globals() and __name__ == "__main__":
    app = Flask(__name__)

    @app.route("/favicon.ico")
    def favicon():
        return send_file("images/favicon.ico")

    @app.route("/<sage_command>")
    def explore(sage_command):
        """
        TODO
        """
        sage_output = ReproducibleObject(sage_command)
        return render_template(
            'explore.html',
            sage_command      = sage_output.command,
            object_data       = display_object(sage_output, link=False),
            object_help       = display_help(sage_output),
            object_methods    = display_methods(sage_output),
            object_properties = display_properties(sage_output),
            )

    @app.route("/")
    def index():
        example_data = []
        for command in config.EXAMPLES:
            data = display_object(ReproducibleObject(command))
            data['command'] = command
            example_data.append(data)
        return render_template('index.html', example_data=example_data)

    app.run(debug=True)
