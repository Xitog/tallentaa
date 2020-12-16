var ITEMS = [
    // pisga0.png
    'data:image/png;base64,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'
];

var TEXTURES = [
    // aqf010.png
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAADAFBMVEUnJycjIyMvLy8TExMXDwcbGxtDQ0NPT09jY2ODg4PT09P////v7++3t7dra2vn5+ff39+rq6t3d3dvb29LS0uLi4ufn59bW1unp6fLy8u/v7+Tk5N/f39HR0fHx8ezs7MAAAAhISEiIiIjIyMkJCQlJSUmJiYnJycoKCgpKSkqKiorKyssLCwtLS0uLi4vLy8wMDAxMTEyMjIzMzM0NDQ1NTU2NjY3Nzc4ODg5OTk6Ojo7Ozs8PDw9PT0+Pj4/Pz9AQEBBQUFCQkJDQ0NERERFRUVGRkZHR0dISEhJSUlKSkpLS0tMTExNTU1OTk5PT09QUFBRUVFSUlJTU1NUVFRVVVVWVlZXV1dYWFhZWVlaWlpbW1tcXFxdXV1eXl5fX19gYGBhYWFiYmJjY2NkZGRlZWVmZmZnZ2doaGhpaWlqampra2tsbGxtbW1ubm5vb29wcHBxcXFycnJzc3N0dHR1dXV2dnZ3d3d4eHh5eXl6enp7e3t8fHx9fX1+fn5/f3+AgICBgYGCgoKDg4OEhISFhYWGhoaHh4eIiIiJiYmKioqLi4uMjIyNjY2Ojo6Pj4+QkJCRkZGSkpKTk5OUlJSVlZWWlpaXl5eYmJiZmZmampqbm5ucnJydnZ2enp6fn5+goKChoaGioqKjo6OkpKSlpaWmpqanp6eoqKipqamqqqqrq6usrKytra2urq6vr6+wsLCxsbGysrKzs7O0tLS1tbW2tra3t7e4uLi5ubm6urq7u7u8vLy9vb2+vr6/v7/AwMDBwcHCwsLDw8PExMTFxcXGxsbHx8fIyMjJycnKysrLy8vMzMzNzc3Ozs7Pz8/Q0NDR0dHS0tLT09PU1NTV1dXW1tbX19fY2NjZ2dna2trb29vc3Nzd3d3e3t7f39/g4ODh4eHi4uLj4+Pk5OTl5eXm5ubn5+fo6Ojp6enq6urr6+vs7Ozt7e3u7u7v7+/w8PDx8fHy8vLz8/P09PT19fX29vb39/f4+Pj5+fn6+vr7+/v8/Pz9/f3+/v7///+GOGHeAAACP0lEQVR4nO2X63KjMAyF5VXFxRfCpUAJSfr+b1kBaSK7M9EwdGf/rDMhc/gSYgsfIQEAGPMHtmG24y6Nb/gcb/f3Dg2U5UVprfMuhCrPWFflqXbLaNpVv+aAeWe920Zo3wnzfrhrG4qcNA449t/c2Y/RYFE/tAud0Thgbx/a+Y6wErphrXCgchJfaFk7oRuVA569ODMTXoS2rBUOOMspXgzO8h/ORuOAjfyHkrAVemKtcKCuEVOqWMsp9ioH7MJzRnVBOH485uz7kTTOG6kI9zN+6HOD7+33L7ztWCscMMvbbZL1qawyYl2FwDvX2rLIV/2Sw/WaZdf1sLyu172avbkOiD526P3+/wv5YJzPW5AGDtLq92Hz+3keM5XzbSyn+nmbpN/rqVz0aw4o3OaHgv0+PLfaVBqNs5lucqvGfr+x+xQOFNm1TPx+Vjng50mcuMR+P32SxgHFjDhhxH531mg8zge+jf3uG9I4kIjRjzW6m8oBg7xiskYfSOO/EQOh0zW6JQavOWC8Rt55Ut+Mxo/HgOI1As1SW5Uf3wfHY3D0LhyPweGdeDQGFEcZKI6yylMvULLXSeNpRjJJxjEaT0ocLiDinEcaP56Vjz8Xjj6Z/tcHa78gi6hFyyJK5WmZR0kZRxpPC02TFJJG43yBqJTlyjQqZUnjsV2XZ19cTKs8LfcpKedJ42nDYZKGwmg8MtOadeOWhjQOFDdVQHFTpfK07aOkrSONp42nSRpLo/GlX5CtLfcDUWtLGv/3+eALuHCk8b5vItsAAAAASUVORK5CYII=',
    // aqf018.png
    'data:image/png;base64,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',
    // flat1_2.png
    'data:image/png;base64,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',
    // floor4_6.png
    'data:image/png;base64,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',
    // rrock11.png
    'data:image/png;base64,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',
    
];

var RESOURCES = [
    ITEMS,
    TEXTURES
];

for (let r = 0 ; r < RESOURCES.length ; r++) {
    for (let i = 0 ; i < RESOURCES[r].length ; i++) {
        let raw_string = RESOURCES[r][i];
        RESOURCES[r][i] = new Image;
        RESOURCES[r][i].src = raw_string;
    }
}
