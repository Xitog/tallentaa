//#pragma comment(lib, "user32.lib")
// LPSTR : Long Pointer on STRing
// LPCSTR : Long Point on Constant STRing

#include <windows.h>
#include <stdio.h>
#include <stdbool.h>

const char g_szClassName[] = "myWindowClass";

static BOOL attachOutputToConsole(void) {
    HANDLE consoleHandleOut, consoleHandleError;
    if (AttachConsole(ATTACH_PARENT_PROCESS)) {
        // Redirect unbuffered STDOUT to the console
        consoleHandleOut = GetStdHandle(STD_OUTPUT_HANDLE);
        if (consoleHandleOut != INVALID_HANDLE_VALUE) {
            freopen("CONOUT$", "w", stdout);
            setvbuf(stdout, NULL, _IONBF, 0);
        } else {
            return FALSE;
        }
        // Redirect unbuffered STDERR to the console
        consoleHandleError = GetStdHandle(STD_ERROR_HANDLE);
        if (consoleHandleError != INVALID_HANDLE_VALUE) {
            freopen("CONOUT$", "w", stderr);
            setvbuf(stderr, NULL, _IONBF, 0);
        } else {
            return FALSE;
        }
        return TRUE;
    }
    //Not a console application
    return FALSE;
}


// Step 4: the Window Procedure
LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    HDC hdc ;
    PAINTSTRUCT ps;
    RECT rect;
    switch(msg)
    {
        case WM_CREATE:
            printf("Program Started\n");
            return 0;
        case WM_CLOSE:
            DestroyWindow(hwnd);
        break;
        case WM_PAINT:
            hdc = BeginPaint (hwnd, &ps) ;
            GetClientRect (hwnd, &rect) ;
            DrawText (hdc, TEXT ("Hello, Windows 98!"), -1, &rect,
                DT_SINGLELINE | DT_CENTER | DT_VCENTER) ;
            EndPaint (hwnd, &ps) ;
            return 0 ;
        case WM_DESTROY:
            PostQuitMessage(0);
        break;
        default:
            return DefWindowProc(hwnd, msg, wParam, lParam);
    }
    return 0;
}

int main()
{
    printf("Hello from main!\n");
    WinMain(NULL, NULL, NULL, 0);
    return 0;
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
    LPSTR lpCmdLine, int nCmdShow)
{
    //MessageBox(NULL, "Goodbye, cruel world!", "Note", MB_OK);
    //return 0;

    bool hasConsole = attachOutputToConsole();

    printf("Hello from WinMain!\n");

    WNDCLASSEX wc;
    HWND hwnd;
    MSG msg;

    //Step 1: Registering the Window Class
    wc.cbSize        = sizeof(WNDCLASSEX);
    wc.style         = 0;
    wc.lpfnWndProc   = WndProc;
    wc.cbClsExtra    = 0;
    wc.cbWndExtra    = 0;
    wc.hInstance     = hInstance;
    wc.hIcon         = LoadIcon(NULL, IDI_APPLICATION);
    wc.hCursor       = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW+1);
    wc.lpszMenuName  = NULL;
    wc.lpszClassName = g_szClassName;
    wc.hIconSm       = LoadIcon(NULL, IDI_APPLICATION);

    if(!RegisterClassEx(&wc))
    {
        MessageBox(NULL, "Window Registration Failed!", "Error!",
            MB_ICONEXCLAMATION | MB_OK);
        return 0;
    }

    // Step 2: Creating the Window
    hwnd = CreateWindowEx(
        WS_EX_CLIENTEDGE,                       // dwExStyle
        g_szClassName,                          // lpClassName
        "The title of my window",               // lpWindowName window title
        WS_OVERLAPPEDWINDOW,                    // dwStyle
        CW_USEDEFAULT,                          // X            initial x position
        CW_USEDEFAULT,                          // Y            initial y position
        240,                                    // nWidth       initial width
        120,                                    // nHeight      initial length
        NULL,                                   // hWndParent   parent window handle
        NULL,                                   // hMenu        window menu handle
        hInstance,                              // hInstance    program instance handle
        NULL);                                  // lpParam      creation parameters

    if(hwnd == NULL)
    {
        MessageBox(NULL, "Window Creation Failed!", "Error!",
            MB_ICONEXCLAMATION | MB_OK);
        return 0;
    }

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    // Step 3: The Message Loop
    while(GetMessage(&msg, NULL, 0, 0) > 0)
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    return msg.wParam;
}
