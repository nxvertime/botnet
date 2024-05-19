#include "utils.h"
using namespace std;


std::wstring mbcsToWideString(const std::string& mbcsStr) {
    int len = MultiByteToWideChar(CP_ACP, 0, mbcsStr.c_str(), -1, NULL, 0);
    std::wstring wideStr(len, L'\0');
    MultiByteToWideChar(CP_ACP, 0, mbcsStr.c_str(), -1, &wideStr[0], len);
    return wideStr;
}


std::string wideStringToUtf8(const std::wstring& wideStr) {
    int len = WideCharToMultiByte(CP_UTF8, 0, wideStr.c_str(), -1, NULL, 0, NULL, NULL);
    std::string utf8Str(len, '\0');
    WideCharToMultiByte(CP_UTF8, 0, wideStr.c_str(), -1, &utf8Str[0], len, NULL, NULL);
    return utf8Str;
}

constexpr int str2int(const char* str, int h = 0)
{
    return !str[h] ? 5381 : (str2int(str, h + 1) * 33) ^ str[h];
}


int strArrLength(vector<string> array[]) {

    return sizeof(array) / sizeof(array[0]);
}

bool copyFile(const LPCSTR& srcPath, const LPCSTR& destPath) {

    if (CopyFile(srcPath, destPath, FALSE)) {
        std::cout << "Copie réussie." << std::endl;
    }
    else {
        std::cerr << "Échec de la copie. Code d'erreur : " << GetLastError() << std::endl;
    }


    return true;
}