import unittest
import subprocess
import time

class TestApplicationStartup(unittest.TestCase):
    def test_application_start(self):
        # Replace 'python BreakOut.py' with the actual command to start your application
        process = subprocess.Popen(['python', 'BreakOut.py'], stderr=subprocess.PIPE)
        
        # Wait for a short duration to allow the application to start
        time.sleep(5)  # Adjust the sleep duration as needed
        
        if process.poll() is None:
            # Application process is running, mark the test as successful
            self.assertTrue(True)
        else:
            # Application process exited or encountered an error
            returncode = process.returncode
            self.fail(f'Application exited with error code {returncode}')

if __name__ == '__main__':
    unittest.main()