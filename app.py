from flask import Flask, request
from flask_restful import Resource, Api
import applescript
import socket
import sys

app = Flask(__name__, static_url_path='/static')
api = Api(app)

script_block = applescript.AppleScript(
    ''' 
    on left_key()           
        tell application "System Events" 
            key code 123
        end tell
    end left_key
    
    on right_key()          
        tell application "System Events" 
            key code 124
        end tell
    end right_key
    
    on space_bar()          
        tell application "System Events" 
            key code 49
        end tell
    end space_bar
    
    on volume_change(level)
        set volume output volume level
    end volume_change
    '''
    )


class RemoteControl(Resource):
    def get(self, key):
        if key == 'left':
            script_block.call('left_key')

        elif key == 'right':
            script_block.call('right_key')

        elif key == 'space':
            script_block.call('space_bar')

        elif key == "volume":
            level = request.args.get('level')
            script_block.call('volume_change', level)


api.add_resource(RemoteControl, '/<string:key>')


@app.route('/')
def serve_controls_page():
    return app.send_static_file('controls.html')


if __name__ == '__main__':
    host, port = '0.0.0.0', '8081'
    print(f"Remote control URL - {socket.gethostbyname(socket.gethostname())}:{port}", file=sys.stdout)
    app.run(host=host, port=port)

