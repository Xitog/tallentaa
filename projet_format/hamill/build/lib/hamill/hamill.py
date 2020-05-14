# -----------------------------------------------------------
# MIT Licence (Expat License Wording)
# -----------------------------------------------------------
# Copyright © 2020, Damien Gouteux
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# For more information about the Hamill lightweight markup language see:
# https://xitog.github.io/dgx/informatique/hamill.html

"""
Hamill: a simple lightweight markup language derived from markdown

**bold**
--strikethrough-- (insted of ~~, too hard to type)
__underline__ (instead of using __ for bold)
''italic'' (instead of * or _, too difficult to parse)

[link_ref] or [link_name->link_ref]

|Table|
|-----|
|data |

* liste

[link_ref]: http://youradress

Created 2020-04-03 as a buggy Markdown processor
Evolved 2020-04-07 as yet another language

"""

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

import os # for walk
import os.path # test if it is a directory or a file
import shutil

from hamill.tokenizer import RECOGNIZED_LANGUAGES, tokenize
from hamill.log import success, fail, info, warn, error

#-------------------------------------------------------------------------------
# Tool functions
#-------------------------------------------------------------------------------

def multi_start(string, starts):
    for key in starts:
        if string.startswith(key):
            return key

def multi_find(string, finds):
    for key in finds:
        if string.find(key) != -1:
            return key

def contains_only(string, things):
    for t in things:
        if string.startswith(t) and len(string.strip()) == len(t):
            return True
    return False

def escape(line):
    # Escaping
    if line.find('\\') == -1:
        return line
    new_line = ''
    index_char = 0
    while index_char < len(line):
        char = line[index_char]
        if index_char < len(line) - 1:
            next_char = line[index_char + 1]
        else:
            next_char = None
        if char == '\\' and next_char in ['*', "'", '^', '-', '_', '[', '@', '%', '!']:
            new_line += next_char
            index_char += 2    
        else:
            new_line += char
            index_char += 1
    return new_line

def safe(line):
    # Do not escape !html line
    if line.startswith('!html'):
        return line
    # Replace special glyph
    line = line.replace('<==', '⇐')
    line = line.replace('==>', '⇒')
    # Replace HTML special char
    new_line = ''
    index_char = 0
    while index_char < len(line):
        # current, next, prev
        char = line[index_char]
        if index_char < len(line) - 1:
            next_char = line[index_char + 1]
        else:
            next_char = None
        if index_char > 0:
            prev_char = line[index_char -1 ]
        else:
            prev_char = None
        # replace
        if char == '&':
            new_line += '&amp;'
        elif char == '<':
            new_line += '&lt;'
        elif char == '>' and next_char == '>' and index_char == 0: # must not replace >>
            new_line += '>>'
            index_char += 1
        elif char == '>' and prev_char != '-': # must not replace ->
            new_line += '&gt;'
        else:
            new_line += char
        index_char += 1
    return new_line

def find_title(line):
    c = 0
    nb = 0
    while c < len(line):
        if line[c] == '#':
            nb += 1
        else:
            break
        c += 1
    if nb > 0:
        title = line.replace('#' * nb, '', 1).strip()
        id_title = make_id(title)
        return nb, title, id_title
    return 0, None, None

def make_id(string):
    """Translate : A simple Title -> a_simple_title"""
    return string.replace(' ', '-').lower()

def write_code(line, code_lang, output=None):
    tokens = tokenize(line, code_lang)
    tokens_by_index = {}
    next_stop = None
    string = ''
    for tok in tokens:
        tokens_by_index[tok.start] = tok
    for index_char, char in enumerate(line):
        if index_char in tokens_by_index:
            tok = tokens_by_index[index_char]
            string += f'<span class="{tok.typ}">{char}'
            next_stop = tok.stop
        elif next_stop is not None and index_char == next_stop:
            string += f'{char}</span>'
        else:
            string += safe(char)
    if output is not None and hasattr(output, 'write'):
        output.write(string)
    else:
        return string

#-------------------------------------------------------------------------------
# Processors
#-------------------------------------------------------------------------------

def prev_next(line, index):
    if index > 0:
        _prev = line[index - 1]
    else:
        _prev = None
    if index > 1:
        _prev_prev = line[index - 2]
    else:
        _prev_prev = None
    if index < len(line) - 1:
        _next = line[index + 1]
    else:
        _next = None
    return _prev, _next, _prev_prev


def translate(line, links, inner_links, DEFAULT_CODE, DEFAULT_FIND_IMAGE=None):
    new_line = ''
    in_bold = False
    in_italic = False
    in_strikethrough = False
    in_underline = False
    in_power = False
    in_code = False
    code = ''
    char_index = -1
    while char_index < len(line) - 1:
        char_index += 1
        char = line[char_index]
        prev_char, next_char, prev_prev_char = prev_next(line, char_index)
        # Link
        if char == '[' and next_char == '#' and prev_char != '\\': # [# ... ] inner link
            ending = line.find(']', char_index)
            if ending != -1:
                link_name = line[char_index + 2:ending]
                id_link = make_id(link_name)
                new_line += f'<span id="{id_link}">' + link_name + '</span>'
                char_index = ending
                continue
        elif char == '[' and next_char == '!' and prev_char != '\\': # [! ... ] image
            ending = line.find(']', char_index)
            if ending != -1:
                link = line[char_index + 2:ending]
                if DEFAULT_FIND_IMAGE is None:
                    new_line += f'<img src="{link}"></img>'
                else:
                    new_line += f'<img src="{DEFAULT_FIND_IMAGE}{link}"></img>'
                char_index = ending
                continue
        elif char == '[' and char_index < len(line) - 1 and prev_char != '\\':
            ending = line.find(']', char_index)
            if ending != -1:
                link = line[char_index + 1:ending]
                if link not in links and link.find('->') != -1:
                    link_name, link = link.split('->', 1)
                    link_name = translate(link_name, links, inner_links, DEFAULT_CODE)
                else:
                    link_name = link
                # check if we have registered this link
                # [LINK_NAME->LINK_REF]
                # [LINK_REF]: http://...
                # or
                # [LINK_NAME->http://]
                if link in links:
                    new_line += f'<a href="{links[link]}">{link_name}</a>'
                elif multi_start(link, ('https://', 'http://')):
                    new_line += f'<a href="{link}">{link_name}</a>'
                elif link == '#': # [Python->#] = to #Python
                    if make_id(link_name) in inner_links:
                        new_line += f'<a href="#{make_id(link_name)}">{link_name}</a>'
                    else:
                        new_line += f'<a href="#{link_name}">{link_name}</a>'
                else:
                    warn('Undefined link:', link_name, 'in', line)
                    new_line += link_name
                char_index = ending
                continue
        # Italic
        if char == "'" and next_char == "'" and prev_char != '\\':
            continue
        if char == "'" and prev_char == "'" and prev_prev_char != '\\':
            if not in_italic:
                new_line += '<i>'
                in_italic = True
            else:
                new_line += '</i>'
                in_italic = False
            continue
        # Strong
        if char == '*' and next_char == '*' and prev_char != '\\':
            continue
        if char == '*' and prev_char == '*' and prev_prev_char != '\\':
            if not in_bold:
                new_line += '<b>'
                in_bold = True
            else:
                new_line += '</b>'
                in_bold = False
            continue
        # Strikethrough
        if char == '-' and next_char == '-' and prev_char != '\\':
            continue
        if char == '-' and prev_char == '-' and prev_prev_char != '\\':
            if not in_strikethrough:
                new_line += '<s>'
                in_strikethrough = True
            else:
                new_line += '</s>'
                in_strikethrough = False
            continue
        # Underline
        if char == '_' and next_char == '_' and prev_char != '\\':
            continue
        if char == '_' and prev_char == '_' and prev_prev_char != '\\':
            if not in_underline:
                new_line += '<u>'
                in_underline = True
            else:
                new_line += '</u>'
                in_underline = False
            continue
        # Power
        if char == '^' and next_char == '^' and prev_char != '\\':
            continue
        if char == '^' and prev_char == '^' and prev_prev_char != '\\':
            if not in_power:
                new_line += '<sup>'
                in_power = True
            else:
                new_line += '</sup>'
                in_power = False
            continue
        # Code
        if char == '@' and next_char == '@' and prev_char != '\\':
            continue
        if char == '@' and prev_char == '@' and prev_prev_char != '\\':
            if not in_code:
                new_line += '<code>'
                in_code = True
                code = ''
            else:
                s = multi_start(code, RECOGNIZED_LANGUAGES)
                if s is not None:
                    code = code.replace(s, '', 1) # delete
                else:
                    s = DEFAULT_CODE
                new_line += write_code(code, s)
                new_line += '</code>'
                in_code = False
            continue
        if in_code:
            code += char
        else:
            new_line += char
    return new_line


def get(line):
    if line.startswith('!const'):
        command, value = line.replace('!const ', '').split('=')
    elif line.startswith('!var'):
        command, value = line.replace('!var ', '').split('=')
    else:
        raise Exception('No variable or constant defined here: ' + line)
    command = command.strip()
    value = value.strip()
    return command, value

LIST_STARTERS = {'* ': 'ul', '- ': 'ul', '% ': 'ol'}

def count_list_level(line):
    starter = line[0]
    if starter + ' ' not in LIST_STARTERS:
        raise Exception('Unknown list starter: ' + line[0] + ' in ' + line)
    level = 0
    while line.startswith(starter + ' '):
        level += 1
        line = line[2:]
    return level, starter


def to_html(input_name, output_name=None, default_lang=None, includes=None):
    VAR_EXPORT_COMMENT=False
    VAR_DEFINITION_AS_PARAGRAPH=False
    VAR_DEFAULT_CODE='text'
    VAR_DEFAULT_PAR_CLASS=None
    VAR_DEFAULT_TAB_CLASS=None
    VAR_NEXT_PAR_CLASS=None
    VAR_NEXT_TAB_CLASS=None
    VAR_DEFAULT_FIND_IMAGE=None
    # HTML Parameters
    CONST_TITLE = None
    CONST_ENCODING = 'utf-8'
    CONST_LANG = default_lang
    CONST_ICON = None
    CONST_BODY_CLASS = None
    CONST_BODY_ID = None
    
    source = open(input_name, mode='r', encoding='utf8')
    content = source.readlines()
    source.close()

    if output_name is None:
        if input_name.endswith('.hml'):
            output_name = input_name.replace('.hml', '.html')
        else:
            output_name = input_name + '.html'

    in_table = False
    links = {}
    inner_links = []
    in_definition_list = False
    in_code_free_block = False
    in_code_block = False
    in_pre_block = False
    code_lang = None
    
    # 1st Pass : prefetch links, replace special HTML char, skip comments
    # Empty line must be kept to separate lists!
    after = []
    link_to_put_in_head = []
    css_to_put_in_head = []
    for line in content:
        # Constant must be read first, are defined once, anywhere in the doc
        if line.startswith('!const '):
            command, value = get(line)
            if command == 'TITLE':
                CONST_TITLE = value
            elif command == 'ENCODING':
                CONST_ENCODING = value
            elif command == 'ICON':
                CONST_ICON = value
            elif command == 'LANG':
                CONST_LANG = value
            elif command == 'BODY_CLASS':
                CONST_BODY_CLASS = value
            elif command == 'BODY_ID':
                CONST_BODY_ID = value
            else:
                raise Exception('Unknown constant: ' + command + 'with value= ' + value)
        elif line.startswith('!require ') and line.strip().endswith('.css'):
            required = line.replace('!require ', '', 1).strip()
            link_to_put_in_head.append(f'  <link href="{required}" rel="stylesheet">\n')
        # Inline CSS
        elif line.startswith('!css '):
            css_to_put_in_head.append(line.replace('!css ', '', 1).strip())
        else:
            # Block of code
            if len(line) > 2 and line[0:3] == '@@@':
                if not in_code_free_block:
                    in_code_free_block = True
                else:
                    in_code_free_block = False
            if line.startswith('@@'):
                in_code_block = True
            else:
                in_code_block = False
            # Strip
            if not in_code_free_block and not in_code_block:
                line = line.strip()
            # Special chars
            line = safe(line)
            # Link library
            if len(line) > 0 and line[0] == '[' and (line.find(']: https://') != -1 or line.find(']: http://') != -1):
                name = line[1:line.find(']: ')]
                link = line[line.find(']: ') + len(']: '):]
                links[name] = link
                continue
            # Inner links
            if line.find('[#') != -1:
                char_index = 0
                while char_index < len(line):
                    char = line[char_index]
                    prev_char, next_char, prev_prev_char = prev_next(line, char_index)
                    if char == '[' and next_char == '#' and prev_char != '\\': # [# ... ] inner link
                        ending = line.find(']', char_index)
                        if ending != -1:
                            link_name = line[char_index + 2:ending]
                            id_link = make_id(link_name)
                            if id_link in inner_links:
                                log.warn("Multiple definitions of anchor: " + id_link)
                            inner_links.append(id_link)
                            char_index = ending
                            continue
                    char_index += 1
            # Inner links from Title
            nb, title, id_title = find_title(line)
            if nb > 0:
                inner_links.append(id_title)
            after.append(line)
    content = after
    
    # Start of output
    output = open(output_name, mode='w', encoding='utf8')
    if CONST_LANG is not None:
        output.write(f'<html lang="{CONST_LANG}">\n')
    else:
        output.write(f'<html>\n')
    output.write('<head>\n')
    output.write(f'  <meta charset={CONST_ENCODING}>\n')
    output.write('  <meta http-equiv="X-UA-Compatible" content="IE=edge">\n')
    output.write('  <meta name="viewport" content="width=device-width, initial-scale=1">\n')
    if CONST_TITLE is not None:
        output.write(f'  <title>{CONST_TITLE}</title>\n')
    if CONST_ICON is not None:
        output.write(f'  <link rel="icon" href="{CONST_ICON}" type="image/x-icon" />\n')
        output.write(f'  <link rel="shortcut icon" href="{CONST_ICON}" type="image/x-icon" />\n')

    # should I put script in head?
    for line in link_to_put_in_head:
        output.write(line)
    # Inline CSS
    for line in css_to_put_in_head:
        output.write('<style type="text/css">\n')
        output.write(line + '\n')
        output.write('</style>\n')
        
    output.write('</head>\n')

    if CONST_BODY_CLASS is None and CONST_BODY_ID is None:
        output.write('<body>\n')
    elif CONST_BODY_ID is None:
        output.write(f'<body class="{CONST_BODY_CLASS}">\n')
    elif CONST_BODY_CLASS is None:
        output.write(f'<body id="{CONST_BODY_ID}">\n')
    else:
        output.write(f'<body id="{CONST_BODY_ID}" class="{CONST_BODY_CLASS}">\n')
    output.write('  <div id="main" class="container">\n')

    prev_level_list = []

    # 2nd Pass
    index = -1
    while index < len(content) - 1:
        index += 1
        line = content[index]
        # Next line
        if index < len(content) - 2:
            next_line = content[index + 1]
        else:
            next_line = None
        # Variables
        if line.startswith('!var '):
            command, value = get(line)
            if command == 'EXPORT_COMMENT':
                if value == 'true':
                    VAR_EXPORT_COMMENT = True
                elif value == 'false':
                    VAR_EXPORT_COMMENT = False
            elif command == 'PARAGRAPH_DEFINITION':
                if value == 'true':
                    VAR_DEFINITION_AS_PARAGRAPH = True
                else:
                    VAR_DEFINITION_AS_PARAGRAPH = False
            elif command == 'DEFAULT_CODE':
                if value in RECOGNIZED_LANGUAGES:
                    VAR_DEFAULT_CODE = value
                else:
                    warn('Not recognized language in var VAR_DEFAULT_CODE:', value)
            elif command == 'NEXT_PAR_CLASS':
                VAR_NEXT_PAR_CLASS = value if value != 'reset' else None
            elif command == 'DEFAULT_PAR_CLASS':
                VAR_DEFAULT_PAR_CLASS = value if value != 'reset' else None
            elif command == 'NEXT_TAB_CLASS':
                VAR_NEXT_TAB_CLASS = value if value != 'reset' else None
            elif command == 'DEFAULT_TAB_CLASS':
                VAR_DEFAULT_TAB_CLASS = value if value != 'reset' else None
            elif command == 'DEFAULT_FIND_IMAGE':
                VAR_DEFAULT_FIND_IMAGE = value if value != 'reset' else None
            else:
                raise Exception('Var unknown: ' + command + ' with value = ' + value)
            continue
        # Comment
        if line.startswith('--') and line.count('-') != len(line):
            if VAR_EXPORT_COMMENT:
                line = line.replace('--', '<!--', 1) + ' -->'
                output.write(line + '\n')    
            else:
                continue
            continue
        # Require CSS or JS file
        if line.startswith('!require '):
            required = line.replace('!require ', '', 1)
            if required.endswith('.js'):
                output.write(f'  <script src="{required}"></script>\n')
            else:
                raise Exception("I don't known how to handle this file: " + required)
            continue
        # Include HTML file
        if line.startswith('!include '):
            included = line.replace('!include ', '', 1).strip()
            if includes is not None:
                filepath = None
                for file in includes:
                    if os.path.basename(file) == included:
                        filepath = file
                if filepath is not None:
                    file = open(filepath, mode='r', encoding='utf8')
                    file_content = file.read()
                    file.close()
                    output.write(file_content + '\n')
                else:
                    warn('Included file', included, 'not found in includes.')
            else:
                warn('No included files for generation.')
            continue
        # Inline HTML
        if line.startswith('!html '):
            output.write(line.replace('!html ', '', 1) + '\n')
            continue
        # HR
        if line.startswith('---'):
            if line.count('-') == len(line):
                output.write('<hr>\n')
                continue
        # BR
        if line.find(' !! ') != -1:
            line = line.replace(' !! ', '<br>')
        # Block of pre
        if line.startswith('>>'):
            if not in_pre_block:
                output.write('<pre>\n')
                in_pre_block = True
            line = escape(line[2:])
            output.write(line + '\n')
            continue
        elif in_pre_block:
            output.write('</pre>\n')
            in_pre_block = False
        # Block of code 1
        if len(line) > 2 and line[0:3] == '@@@':
            if not in_code_free_block:
                output.write('<pre class="code">\n')
                in_code_free_block = True
                code_lang = line.replace('@@@', '', 1).strip()
                if len(code_lang) == 0:
                    code_lang = VAR_DEFAULT_CODE
            else:
                output.write('</pre>\n')
                in_code_free_block = False
            continue 
        # Block of code 2
        if line.startswith('@@') and (len(line.strip()) == 2 or line[2] != '@'):
            if not in_code_block:
                output.write('<pre class="code">\n')
                in_code_block = True
                code_lang = line.replace('@@', '', 1).strip()
                if len(code_lang) == 0:
                    code_lang = VAR_DEFAULT_CODE
                continue
        elif in_code_block:
            output.write('</pre>\n')
            in_code_block = False
        if in_code_free_block or in_code_block:
            if in_code_block:
                line = line[2:] # remove starting @@
            write_code(line, code_lang, output)
            # output.write('\n')
            continue
        # Bold & Italic & Strikethrough & Underline & Power
        if multi_find(line, ('**', '--', '__', '^^', "''", "[", '@@')) and \
           not line.startswith('|-'):
            line = translate(line, links, inner_links, VAR_DEFAULT_CODE, VAR_DEFAULT_FIND_IMAGE)
        # Title
        nb, title, id_title = find_title(line)
        if nb > 0:
            line = f'<h{nb} id="{id_title}">{title}</h{nb}>\n'
            output.write(line)
            continue
        # Liste
        found = multi_start(line, LIST_STARTERS)
        if found:
            level, starter = count_list_level(line)
            list_markup = LIST_STARTERS[starter + ' ']
            while len(prev_level_list) < level :
                output.write(f'<{list_markup}>\n')
                prev_level_list.append(list_markup)
            while len(prev_level_list) > level:
                output.write(f'</{prev_level_list[-1]}>\n')
                prev_level_list.pop()
            line = '<li>' + escape(line[level * 2:]) + '</li>\n'
            output.write(line)
            continue
        elif len(prev_level_list) > 0:
            while len(prev_level_list) > 0:
                output.write(f'</{prev_level_list[-1]}>\n')
                prev_level_list.pop()
        # Table
        if len(line) > 0 and line[0] == '|':
            if not in_table:
                if VAR_DEFAULT_TAB_CLASS is not None:
                    output.write(f'<table class="{VAR_DEFAULT_TAB_CLASS}">\n')
                elif VAR_NEXT_TAB_CLASS is not None:
                    output.write(f'<table class="{VAR_NEXT_TAB_CLASS}">\n')
                    VAR_NEXT_TAB_CLASS = None
                else:
                    output.write('<table>\n')
                in_table = True
            if next_line is not None and next_line.startswith('|-'):
                element = 'th'
            else:
                element = 'td'
            columns = line.split('|')
            skip = True
            for col in columns:
                if len(col.replace('-', '').strip()) != 0:
                    skip = False
            if not skip:
                output.write('<tr>')
                for col in columns:
                    if col != '': # center or right-align
                        if col[0] == '>':
                            align = ' align="right"'
                            col = col[1:]
                        elif col[0] == '=':
                            align = ' align="center"'
                            col = col[1:]
                        else:
                            align = ''
                        val = translate(escape(col), links, inner_links, VAR_DEFAULT_CODE, VAR_DEFAULT_FIND_IMAGE)
                        output.write(f'<{element}{align}>{val}</{element}>')
                output.write('</tr>\n')
            continue
        elif in_table:
            output.write('</table>\n')
            in_table = False
        # Definition list
        if line.startswith('$ '):
            if not in_definition_list:
                in_definition_list = True
                output.write('<dl>\n')
            else:
                output.write('</dd>\n')
            output.write(f'<dt>{line.replace("$ ", "", 1)}</dt>\n<dd>\n')
            continue
        elif len(line) != 0 and in_definition_list:
            if not VAR_DEFINITION_AS_PARAGRAPH:
                output.write(escape(line) +'\n')
            else:
                output.write('<p>' + escape(line) +'</p>\n')
            continue
        # empty line
        elif len(line) == 0 and in_definition_list:
            in_definition_list = False
            output.write('</dl>\n')
            continue
        # Replace escaped char
        line = escape(line)
        # Paragraph
        if len(line) > 0:
            if VAR_DEFAULT_PAR_CLASS is not None:
                output.write(f'<p class="{VAR_DEFAULT_PAR_CLASS}">' + line.strip() + '</p>\n')
            elif VAR_NEXT_PAR_CLASS is not None:
                output.write(f'<p class="{VAR_NEXT_PAR_CLASS}">' + line.strip() + '</p>\n')
                VAR_NEXT_PAR_CLASS = None
            else:
                output.write('<p>' + line.strip() + '</p>\n')
    # Are a definition list still open?
    if in_definition_list:
        output.write('</dl>\n')
    # Are some lists still open?
    while len(prev_level_list) > 0:
        output.write(f'</{prev_level_list[-1]}>\n')
        prev_level_list.pop()
    # Are a table still open?
    if in_table:
        output.write('</table>\n')
        in_table = False
    # Are we stil in in_pre_block?
    if in_pre_block:
        output.write('</pre>')
    # Are we still in in_code_block?
    if in_code_block:
        output.write('</pre>')
    # Do we have registered lines to write at the end?
    output.write('  </div>\n')
    #for line in final_lines:
    #    output.write(line)
    output.write('</body>')
    output.close()

#-------------------------------------------------------------------------------
# Main functions
#-------------------------------------------------------------------------------

def process(source, dest, default_lang=None, includes=None):
    """Process a file or directory :
            - If it is a .hml file, it is translated in HTML
            - Else the file is copied into the new directory
       The destination directory is systematically DELETED at each run.
    """
    if os.path.isfile(source):
        info('Processing file:', source)
        to_html(source, dest, default_lang, includes)
    elif os.path.isdir(source):
        info('Processing directory:', source)
        if os.path.isdir(dest):
            shutil.rmtree(dest)
        info('Making dir:', dest)
        os.mkdir(dest)
        for name_ext in os.listdir(source):
            path = os.path.join(source, name_ext)
            if os.path.isfile(path):
                name, ext = os.path.splitext(name_ext)
                if ext == '.hml':
                    info('Processing file:', path)
                    to_html(path, os.path.join(dest, name + '.html'), default_lang, includes)
                else:
                    info('Copying file:', path)
                    shutil.copy2(path, os.path.join(dest, name_ext))
            elif os.path.isdir(path):
                process(path, os.path.join(dest, name_ext), default_lang, includes)
    else:
        warn(source, 'not found.')
