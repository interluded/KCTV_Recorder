#include <iostream>
#include <curl/curl.h>

size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    return size * nmemb; // Ignore the contents, just return the size
}

int main() {
    CURL *curl;
    CURLcode res;
    long response_code;

    // Initialize libcurl
    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();

    if (curl) {
        // Set the URL
        curl_easy_setopt(curl, CURLOPT_URL, "http://64.95.150.17:8000");

        // Set the callback function to ignore the response body
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);

        // Perform the request, res will get the return code
        res = curl_easy_perform(curl);

        if (res == CURLE_OK) {
            // Check the response code
            curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
            if (response_code == 200) {
                std::cout << "Record" << std::endl;
            } else {
                std::cout << "DontRecord" << std::endl;
            }
        } else {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
            std::cout << "DontRecord" << std::endl;
        }

        // Clean up
        curl_easy_cleanup(curl);
    }

    // Global libcurl cleanup
    curl_global_cleanup();

    return 0;
}
