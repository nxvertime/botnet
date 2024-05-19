#ifndef UTILS_H
#define UTILS_H
#include <winsock2.h>
#include <iostream>
#include <windows.h>
#include <ws2tcpip.h>
#include <string>
#include <codecvt>
#include <locale>
#include <windows.h>
#include "includes/json.hpp"

std::wstring mbcsToWideString(const std::string& mbcsStr);

std::string wideStringToUtf8(const std::wstring& wideStr);

constexpr int str2int(const char* str, int h = 0);

int strArrLength(vector<string> array[]);

bool copyFile(const LPCSTR& srcPath, const LPCSTR& destPath);


#endif 