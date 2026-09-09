//#pragma comment(lib, "user32.lib")
// LPSTR : Long Pointer on STRing
// LPCSTR : Long Point on Constant STRing

#include <windows.h>
#include <stdio.h>
#include <stdbool.h>

#define ID_EDIT_X 1001
#define ID_EDIT_Y 1002
#define ID_BUTTON 1003

const char g_szClassName[] = "myWindowClass";
static HWND g_edit_x;
static HWND g_edit_y;
static int g_rect_x = 100;
static int g_rect_y = 100;

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
    switch(msg)
    {
        case WM_CREATE:
            printf("Program Started\n");

            // Label X
            CreateWindow(
                "STATIC",
                "X :",
                WS_VISIBLE | WS_CHILD,
                10, 10, 20, 25,
                hwnd,
                NULL,
                NULL,
                NULL
            );
            // Champ X
            g_edit_x = CreateWindow(
                "EDIT",
                "100",
                WS_VISIBLE | WS_CHILD | WS_BORDER,
                35, 10, 80, 25,
                hwnd,
                (HMENU)ID_EDIT_X,
                NULL,
                NULL
            );
            // Label Y
            CreateWindow(
                "STATIC",
                "Y :",
                WS_VISIBLE | WS_CHILD,
                130, 10, 20, 25,
                hwnd,
                NULL,
                NULL,
                NULL
            );
            // Champ Y
            g_edit_y = CreateWindow(
                "EDIT",
                "100",
                WS_VISIBLE | WS_CHILD | WS_BORDER,
                155, 10, 80, 25,
                hwnd,
                (HMENU)ID_EDIT_Y,
                NULL,
                NULL
            );
            // Button
            CreateWindow(
                "BUTTON",
                "Dessiner",
                WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
                250, 10, 90, 25,
                hwnd,
                (HMENU)ID_BUTTON,
                NULL,
                NULL
            );
            break;
        case WM_PAINT:
            HDC hdc ;
            PAINTSTRUCT ps;
            RECT rect;
            hdc = BeginPaint (hwnd, &ps) ;
            GetClientRect (hwnd, &rect) ;
            DrawText (hdc, TEXT ("Hello, Windows 98!"), -1, &rect,
                DT_SINGLELINE | DT_CENTER | DT_VCENTER) ;
            HBRUSH red_brush = CreateSolidBrush(RGB(255, 0, 0));
            HBRUSH old_brush = SelectObject(hdc, red_brush);
            Rectangle(hdc, g_rect_x, g_rect_y, g_rect_x + 100, g_rect_y + 50);
            SelectObject(hdc, old_brush);
            DeleteObject(red_brush);
            EndPaint (hwnd, &ps) ;
            break;
        case WM_COMMAND:
            if (LOWORD(wParam) == ID_BUTTON)
            {
                char buffer[32];
                GetWindowText(g_edit_x, buffer, sizeof(buffer));
                g_rect_x = atoi(buffer);
                GetWindowText(g_edit_y, buffer, sizeof(buffer));
                g_rect_y = atoi(buffer);
                InvalidateRect(hwnd, NULL, TRUE);
            }
            break;
        case WM_DESTROY:
            PostQuitMessage(0);
            break;
        case WM_CLOSE:
            DestroyWindow(hwnd);
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
        640,                                    // nWidth       initial width
        480,                                    // nHeight      initial length
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
    MSG msg;
    while(GetMessage(&msg, NULL, 0, 0) > 0)
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    return msg.wParam;
}
