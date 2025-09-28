import unittest
import requests
import threading
import time
from app import app

class TestWebServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start the Flask app in a separate thread for testing
        cls.server_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=3000, debug=False))
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(1)  # Give the server time to start

    def test_server_responds_on_port_3000(self):
        response = requests.get('http://localhost:3000')
        self.assertEqual(response.status_code, 200)

    def test_serves_html_content(self):
        response = requests.get('http://localhost:3000')
        self.assertIn('html', response.text.lower())

    def test_has_clean_design_elements(self):
        response = requests.get('http://localhost:3000')
        # Check for basic HTML structure
        self.assertIn('<title>', response.text)
        self.assertIn('<body>', response.text)

    def test_env_var_injection_missing(self):
        response = requests.get('http://localhost:3000')
        self.assertIn('SOME_ENV_VAR:', response.text)
        self.assertIn('(missing)', response.text)

    def test_env_var_injection_present(self):
        import os
        import subprocess
        import time

        # Test with environment variable set
        env = os.environ.copy()
        env['SOME_ENV_VAR'] = 'test-value'
        env['PORT'] = '3001'

        # Start server with env var
        proc = subprocess.Popen(['python3', 'app.py'], env=env)
        time.sleep(2)

        try:
            response = requests.get('http://localhost:3001')
            self.assertIn('SOME_ENV_VAR:', response.text)
            self.assertIn('test-value', response.text)
        finally:
            proc.terminate()
            proc.wait()

if __name__ == '__main__':
    unittest.main()