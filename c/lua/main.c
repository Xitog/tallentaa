
#include "lua.h"
#include "lualib.h"
#include "lauxlib.h"
#include <stdlib.h>

static int twice (lua_State * lua) {
    double arg = lua_tonumber(lua, 1);  /* get argument */
    lua_pushnumber(lua, arg * 2);  /* push result */
    return 1;  /* number of results */
}

int main(int argc, char **argv){
    printf("Hello, World!\n");

    lua_State * lua = luaL_newstate();
    luaL_openlibs(lua);

    lua_pushcfunction(lua, twice);
    lua_setglobal(lua, "twiceC");

    int res = luaL_dostring(lua, "print(\"Lua is here\")");
    printf("retour = %d\n", res);

    res = luaL_dostring(lua, "a = twiceC(2)");
    printf("retour = %d\n", res);

    res = luaL_dostring(lua, "print(a)");
    printf("retour = %d\n", res);

    lua_close(lua);
    return 0;
}
