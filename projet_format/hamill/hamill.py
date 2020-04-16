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
import sys # colored output for IDLE
import os.path # test if it is a directory or a file
import shutil

#-------------------------------------------------------------------------------
# Logging
#-------------------------------------------------------------------------------

try:
    out = sys.stdout.shell
    IDLE = True
except AttributeError:
    out = sys.stdout
    IDLE = False

def success(*msg, sep=' '):
    msg = sep.join(msg)
    if IDLE:
        out.write('[SUCCESS] ' + msg + '\n', 'STRING')
    else:
        out.write(msg + '\n')

def fail(*msg, sep=' '):
    msg = sep.join(msg)
    if IDLE:
        out.write('[FAIL] ' + msg + '\n', 'COMMENT')
    else:
        out.write(msg + '\n')

def info(*msg, sep=' '):
    msg = sep.join(msg)
    if IDLE:
        out.write('[INFO] ' + msg + '\n', 'DEFINITION')
    else:
        out.write(msg + '\n')

def warn(*msg, sep=' '):
    msg = sep.join(msg)
    if IDLE:
        out.write('[WARN] ' + msg + '\n', 'KEYWORD')
    else:
        out.write(msg + '\n')

def error(*msg, sep=' '):
    msg = sep.join(msg)
    if IDLE:
        out.write('[ERROR] ' + msg + '\n', 'COMMENT')
    else:
        out.write(msg + '\n')

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

def escape(line):
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
        if char == '\\' and next_char in ['*', "'", '^', '-', '_', '[']:
            new_line += next_char
            index_char += 2    
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
        id_title = make_title(title)
        return nb, title, id_title
    return 0, None, None

def make_title(string):
    return string.replace(' ', '-').lower()

#-------------------------------------------------------------------------------
# Processors
#-------------------------------------------------------------------------------

def to_html(input_name, output_name=None):
    EXPORT_COMMENT=False
    ADD_CSS=None
    TITLE=None
    BODY_CLASS=None
    BODY_ID=None
    DEFINITION_AS_PARAGRAPH=False

    source = open(input_name, mode='r', encoding='utf8')
    content = source.readlines()
    source.close()

    if output_name is None:
        if input_name.endswith('.hml'):
            output_name = input_name.replace('.hml', '.html')
        else:
            output_name = input_name + '.html'

    output = open(output_name, mode='w', encoding='utf8')
    output.write('<html>\n')
    output.write('<head>\n')
    output.write('<meta charset="utf-8">\n')
    output.write('<meta http-equiv="X-UA-Compatible" content="IE=edge">\n')
    output.write('<meta name="viewport" content="width=device-width, initial-scale=1">\n')

    list_level = []
    in_table = False
    links = {}
    inner_links = []
    in_definition_list = False

    list_starter = {'* ': 'ul', '- ': 'ul', '% ': 'ol'}

    # prefetch links, replace special HTML char, skip comments
    filtered_content = []
    final_lines = []
    for index, raw_line in enumerate(content):
        # Strip
        line = raw_line.strip()
        # Doctrines
        if line.startswith('!doctrine '):
            command, value = line.replace('!doctrine ', '').split('=')
            #print('Command =', command.strip(), 'Value =', value.strip())
            command = command.strip()
            value = value.strip()
            if command == 'EXPORT_COMMENT':
                if value == 'true':
                    EXPORT_COMMENT = True
                elif value == 'false':
                    EXPORT_COMMENT = False
            elif command == 'ADD_CSS':
                output.write(f'<link href="{value}" rel="stylesheet">\n')
            elif command == 'ADD_SCRIPT':
                final_lines.append(f'<script src="{value}"></script>\n')
            elif command == 'TITLE':
                output.write(f'<title>{value}</title>\n')
            elif command == 'ICON':
                output.write(f'<link rel="icon" href="{value}" type="image/x-icon" />')
                output.write(f'<link rel="shortcut icon" href="{value}" type="image/x-icon" />')
            elif command == 'BODY_CLASS':
                BODY_CLASS = value
            elif command == 'BODY_ID':
                BODY_ID = value
            elif command == 'PARAGRAPH_DEFINITION':
                if value == 'true':
                    DEFINITION_AS_PARAGRAPH = True
                else:
                    DEFINITION_AS_PARAGRAPH = False
            continue
        # Empty
        #if len(line) == 0:
        #    continue keep empty to separate lists!
        # CSS
        if line.startswith('!css '):
            output.write('<style type="text/css">\n')
            output.write(line.replace('!css ', '', 1).strip() + '\n')
            output.write('</style>\n')
            continue
        # Special chars
        line = line.replace('&', '&amp;')
        # Comment
        if line.startswith('--') and line.count('-') != len(line) and line.count('-') < 3:
            if EXPORT_COMMENT:
                line = line.replace('--', '<!--', 1) + ' -->'
            else:
                continue
        # Link library
        elif len(line) > 0 and line[0] == '[' and (line.find(']: https://') != -1 or line.find(']: http://') != -1):
            name = line[1:line.find(']: ')]
            link = line[line.find(']: ') + len(']: '):]
            links[name] = link
            continue
        # Inner links
        nb, title, id_title = find_title(line)
        if nb > 0:
            inner_links.append(id_title)
        filtered_content.append(line)

    output.write('</head>\n')

    if BODY_CLASS is None and BODY_ID is None:
        output.write('<body>\n')
    elif BODY_ID is None:
        output.write(f'<body class="{BODY_CLASS}">\n')
    elif BODY_CLASS is None:
        output.write(f'<body id="{BODY_ID}">\n')
    else:
        output.write(f'<body id="{BODY_ID}" class="{BODY_CLASS}">\n')
    output.write('<div id="main" class="container">\n')

    for index, raw_line in enumerate(filtered_content):
        line = raw_line
        # Comment
        if line.startswith('<!-- '):
            output.write(line + '\n')
            continue
        # Include
        if line.startswith('!include '):
            included = line.replace('!include ', '', 1)
            file = open(included, mode='r', encoding='utf8')
            file_content = file.read()
            file.close()
            output.write(file_content + '\n')
            continue
        # HTML
        if line.startswith('!html '):
            output.write(line.replace('!html ', '', 1) + '\n')
            continue
        # Next line
        if index < len(filtered_content) - 2:
            next_line = filtered_content[index + 1]
        else:
            next_line = None
        # HR
        if line.startswith('---'):
            if line.count('-') == len(line):
                output.write('<hr>\n')
                continue
        # BR
        if line.find(' !! ') != -1:
            line = line.replace(' !! ', '<br>')
        # Bold & Italic & Strikethrough & Underline & Power
        if multi_find(line, ('**', '--', '__', '^^', "''", "[", '@@')) and \
           not line.startswith('|-'):
            new_line = ''
            in_bold = False
            in_italic = False
            in_strikethrough = False
            in_underline = False
            in_power = False
            char_index = -1
            while char_index < len(line) - 1:
                char_index += 1
                char = line[char_index]
                if char_index > 0:
                    prev_char = line[char_index - 1]
                else:
                    prev_char = None
                if char_index > 1:
                    prev_prev_char = line[char_index - 2]
                else:
                    prev_prev_char = None
                if char_index < len(line) - 1:
                    next_char = line[char_index + 1]
                else:
                    next_char = None
                # Italic
                #if char == '*' and next_char != '*' and prev_char != '*':
                #    if not in_italic and next_char != ' ':
                #        new_line += '<i>'
                #        in_italic = True
                #    elif in_italic:
                #        new_line += '</i>'
                #        in_italic = False
                #    else:
                #        new_line += char # for * liste with **thing**
                #    continue
                # Link
                if char == '[' and next_char == '#' and prev_char != '\\':
                    ending = line.find(']', char_index)
                    if ending != -1:
                        link = line[char_index + 2:ending]
                        new_line += f'<a id="{link}">' + link + '</a>'
                        char_index = ending
                        continue
                elif char == '[' and char_index < len(line) - 1 and prev_char != '\\':
                    ending = line.find(']', char_index)
                    if ending != -1:
                        link = line[char_index + 1:ending]
                        if link not in links and link.find('->') != -1:
                            link_name, link = link.split('->', 1)
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
                            if make_title(link_name) in inner_links:
                                new_line += f'<a href="#{make_title(link_name)}">{link_name}</a>'
                            else:
                                new_line += f'<a href="#{link_name}">{link_name}</a>'
                        else:
                            warn('Undefined link:', link_name)
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
                    if not in_power:
                        new_line += '<code>'
                        in_power = True
                    else:
                        new_line += '</code>'
                        in_power = False
                    continue
                new_line += char
            line = new_line
        # Title
        nb, title, id_title = find_title(line)
        if nb > 0:
            line = f'<h{nb} id="{id_title}">{title}</h{nb}>\n'
            output.write(line)
            continue
        # Liste
        line_level = []
        tested = line
        to_cut = 0
        # 3.8 while found := multi_start(tested, list_starter):
        found = multi_start(tested, list_starter)
        while found:
            line_level.append(found)
            tested = tested.replace(found, '', 1)
            to_cut += len(found)
            found = multi_start(tested, list_starter)
        # reconciliation of lists: we must close before starting another
        if len(line_level) > 0:
            #if line == '- No':
                #print('line:', line_level)
                #print('file:', list_level)
            for level in range(min(len(line_level), len(list_level))):
                if list_level[level] != line_level[level]:
                    # on dépile le dessus
                    for after in range(len(list_level) - 1, level - 1, -1):
                        output.write(f'</{list_starter[list_level[-1]]}>\n')
                        list_level.pop()
            if len(list_level) != len(line_level):
                if len(line_level) >= len(list_level):
                    # on ouvre pour rattraper le level de la ligne
                    for level in range(len(list_level), len(line_level)):
                        list_level.append(line_level[level])
                        output.write(f'<{list_starter[list_level[-1]]}>\n')
                else:
                    # on ferme pour rattraper le level de la ligne
                    for level in range(len(list_level) - 1, level, -1):
                        output.write(f'</{list_starter[list_level[-1]]}>\n')
                        list_level.pop()
            line = '<li>' + escape(line[to_cut:]) + '</li>\n'
            output.write(line)
            continue
        elif len(list_level) > 0:
            for level in range(len(list_level) - 1, -1, -1):
                output.write(f'</{list_starter[list_level[-1]]}>\n')
                list_level.pop()
        # Table
        if len(line) > 0 and line[0] == '|':
            if not in_table:
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
                    if col != '':
                        output.write(f'<{element}>{escape(col)}</{element}>')
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
            if not DEFINITION_AS_PARAGRAPH:
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
            output.write('<p>' + line.strip() + '</p>\n')
    # Are a definition list still open?
    if in_definition_list:
        output.write('</dl>\n')
    # Are some lists still open?
    if len(list_level) > 0:
        for level in range(len(list_level) - 1, -1, -1):
            output.write(f'</{list_starter[list_level[-1]]}>\n')
            list_level.pop()
    # Are a table still open?
    if in_table:
        output.write('</table>\n')
        in_table = False
    # Do we have registered lines to write at the end?
    output.write('</div>\n')
    for line in final_lines:
        output.write(line)
    output.write('</body>')
    output.close()

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------

paths = ['input']
#paths = ['jeux.hml', 'hamill.hml', 'Tests.hml', 'tools_langs.hml']
#paths = ['Tests.hml']
#paths = ['tools_langs.hml']

def process(path):
    if os.path.isfile(path):
        info('Processing file:', path)
        to_html(path)
    elif os.path.isdir(path):
        info('Processing directory:', path)
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                process(os.path.join(path, file))
            for directory in dirnames:
                process(os.path.join(path, directory))

def mirror(path_input_dir, path_output_dir):
    for path in os.listdir(path_input_dir):
        if os.path.isfile(os.path.join(path_input_dir, path)):
            if path.endswith('.hml'):
                info('Processing file:', path)
                to_html(os.path.join(path_input_dir, path),
                        os.path.join(path_output_dir, path.replace('.hml', '.html')))
            else:
                shutil.copy2(os.join(path_input_dir, path), os.join(path_output_dir, path))
        elif os.path.isdir(os.path.join(path_input_dir, path)):
            os.mkdir(os.path.join(path_output_dir, path))
            mirror(os.path.join(path_input_dir, path), os.path.join(path_output_dir, path))

if __name__ == '__main__':
    if len(paths) == 1 and os.path.isdir(paths[0]):
        info('Mirroring:', paths[0])
        if os.path.isdir('output'):
            shutil.rmtree('output')
        os.mkdir('output')
        mirror(paths[0], 'output')
    else:
        for path in paths:
            process(path)
