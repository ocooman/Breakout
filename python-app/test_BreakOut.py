import unittest
import subprocess
import time

class TestApplicationStartup(unittest.TestCase):
    def test_application_start(self):
        timeout_seconds = 10  # Timeout duration in seconds
        start_time = time.time()
        
        # Replace 'python my_application.py' with the actual command to start your application
        process = subprocess.Popen(['python', 'my_application.py'], stderr=subprocess.PIPE)
        
        while time.time() - start_time < timeout_seconds:
            if process.poll() is not None:
                # Application process has completed
                returncode = process.returncode
                if returncode == 0:
                    # Application started successfully
                    return
                else:
                    # Application encountered an error
                    self.fail(f'Application exited with error code {returncode}')
            time.sleep(1)  # Wait for 1 second before checking again

        # Timeout reached, terminate the process and fail the test
        process.terminate()
        self.fail('Application startup timed out')

if __name__ == '__main__':
    unittest.main()
