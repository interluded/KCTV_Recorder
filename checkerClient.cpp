#include <iostream>
#include <cstdlib>
#include <cstring>
#include <unistd.h>
#include <signal.h>
#include <sys/wait.h>

using namespace std;

const char* CHECK_UP_COMMAND = "./check_up";
const char* RECORD_COMMAND = "ffmpeg -headers \"Origin: https://kcnawatch.org\" "
                             "-headers \"Referer: https://kcnawatch.org\" "
                             "-i https://tv.nknews.org/tvhls/stream.m3u8 "
                             "-c copy output.mp4";

bool is_recording = false;
pid_t recording_pid = -1;

void start_recording() {
    cout << "Starting recording..." << endl;
    recording_pid = fork();
    if (recording_pid == 0) {
        // Child process
        execl("/bin/sh", "sh", "-c", RECORD_COMMAND, NULL);
        exit(0);  // Should not reach here unless execl fails
    } else if (recording_pid > 0) {
        // Parent process
        is_recording = true;
    } else {
        // Fork failed
        cerr << "Failed to fork process for recording." << endl;
    }
}

void stop_recording() {
    if (is_recording && recording_pid > 0) {
        cout << "Stopping recording..." << endl;
        kill(recording_pid, SIGTERM);
        waitpid(recording_pid, NULL, 0);
        is_recording = false;
        recording_pid = -1;
    }
}

void check_and_handle() {
    FILE* fp = popen(CHECK_UP_COMMAND, "r");
    if (fp == NULL) {
        cerr << "Failed to execute ./check_up." << endl;
        return;
    }

    char buffer[128];
    if (fgets(buffer, sizeof(buffer), fp) != NULL) {
        if (strcmp(buffer, "Record\n") == 0) {
            if (!is_recording) {
                start_recording();
            }
        } else {
            if (is_recording) {
                stop_recording();
            }
        }
    } else {
        cerr << "Error reading output from ./check_up." << endl;
    }

    pclose(fp);
}

int main() {
    while (true) {
        check_and_handle();
        sleep(10);  // Check every 10 seconds
    }
    return 0;
}
