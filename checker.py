import subprocess
import time

def check_output():
    try:
        result = subprocess.run(['python3', 'testcard.py'], capture_output=True, text=True, timeout=10)
        output = result.stdout.strip().lower()  # Convert output to lowercase and remove extra whitespace
        return output
    except subprocess.TimeoutExpired:
        return None
    except Exception as e:
        print(f"Error running testcard.py: {e}")
        return None

def start_web_server():
    try:
        subprocess.Popen(['python3', '-m', 'http.server'])
    except Exception as e:
        print(f"Error starting web server: {e}")

if __name__ == "__main__":
    web_server_started = False
    
    while True:
        output = check_output()
        
        if output != "testcard":
            if not web_server_started:
                print("Starting web server...")
                start_web_server()
                web_server_started = True
            else:
                print("Still recording. Checking again in 10 seconds...")
            
        else:
            print("still have testcard. checking again in 10 seconds.")
            web_server_started = False
        
        time.sleep(10)  # Wait for 10 seconds before checking again
