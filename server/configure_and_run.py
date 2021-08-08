import subprocess
from pyngrok import ngrok

def main() -> None:
    """Start the bot."""

    http_tunnel = ngrok.connect(2781, bind_tls=True)
    with subprocess.Popen(['python3', 'server/flask_server.py', http_tunnel.public_url]) as proc:
        proc.wait()

if __name__ == '__main__':
    main()
