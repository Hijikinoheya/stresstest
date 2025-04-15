#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <time.h>

void log_message(const char *message) {
    FILE *log_file = fopen("log.txt", "a");
    if (log_file) {
        time_t now = time(NULL);
        struct tm *tm_info = localtime(&now);
        char time_str[26];
        strftime(time_str, sizeof(time_str), "%Y-%m-%d %H:%M:%S", tm_info);
        fprintf(log_file, "[%s] %s\n", time_str, message);
        fclose(log_file);
    }
}

void cpu_stress(int duration) {
    log_message("Starting CPU stress test...");
    DWORD start_time = GetTickCount();
    while (GetTickCount() - start_time < duration * 1000) {
        // CPU負荷をかける処理
        volatile double x = 0;
        for (int i = 0; i < 1000000; i++) {
            x += i * 3.14159;
        }
    }
    log_message("CPU stress test completed.");
}

void memory_stress(int duration) {
    log_message("Starting memory stress test...");
    size_t size = 1024 * 1024 * 100; // 100MB
    void *ptr = malloc(size);
    if (ptr) {
        DWORD start_time = GetTickCount();
        while (GetTickCount() - start_time < duration * 1000) {
            // メモリ使用処理
            memset(ptr, 0, size);
        }
        free(ptr);
        log_message("Memory stress test completed.");
    } else {
        log_message("Memory allocation failed.");
    }
}

void get_cpu_clock_speed() {
    SYSTEM_INFO sys_info;
    GetSystemInfo(&sys_info);
    char message[100];
    snprintf(message, sizeof(message), "CPU clock speed: %u MHz", sys_info.dwProcessorType);
    log_message(message);
}

int main() {
    int duration;
    printf("Enter test duration in seconds: ");
    scanf("%d", &duration);

    get_cpu_clock_speed();
    cpu_stress(duration);
    memory_stress(duration);

    printf("Tests completed. Check log.txt for details.\n");
    return 0;
}
