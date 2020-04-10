"""
Simple language derived from markdown

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
        if char == '\\' and next_char in ['*', "'", '^', '-', '_']:
            new_line += next_char
            index_char += 2    
        else:
            new_line += char
            index_char += 1
    return new_line

def to_html(input_name, output_name=None):
    EXPORT_COMMENT=False
    ADD_CSS=None

    source = open(input_name, mode='r', encoding='utf8')
    content = source.readlines()
    source.close()

    if output_name is None:
        output_name = input_name.replace('.md', '.html')

    output = open(output_name, mode='w', encoding='utf8')
    output.write('<html>\n')
    output.write('<head>\n')

    list_level = []
    in_table = False
    links = {}

    list_starter = {'* ': 'ul', '- ': 'ul', '% ': 'ol'}

    # prefetch links, replace special HTML char, skip comments
    filtered_content = []
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
            continue
        # Empty
        #if len(line) == 0:
        #    continue keep empty to separate lists!
        # Special chars
        line = line.replace('&', '&amp;')
        # Comment
        if line.startswith('--'):
            if EXPORT_COMMENT:
                line = line.replace('--', '<!--', 1) + ' -->'
            else:
                continue
        # Links
        elif len(line) > 0 and line[0] == '[' and (line.find(']: https://') != -1 or line.find(']: http://') != -1):
            name = line[1:line.find(']: ')]
            link = line[line.find(']: ') + len(']: '):]
            links[name] = link
            continue
        filtered_content.append(line)

    output.write('</head>\n')
    output.write('<body>\n')
    #output.write('<body id="content" class="palatino">\n')

    for index, raw_line in enumerate(filtered_content):
        line = raw_line
        if line.startswith('<!-- '):
            output.write(line + '\n')
            continue
        if index < len(filtered_content) - 2:
            next_line = filtered_content[index + 1]
        else:
            next_line = None
        # Bold & Italic & Strikethrough & Underline & Power
        if multi_find(line, ('**', '--', '__', '^^', "''")):
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
                if char == '[' and char_index < len(line) - 1:
                    ending = line.find(']', char_index)
                    if ending != -1:
                        link = line[char_index + 1:ending]
                        if link not in links and link.find('->') != -1:
                            link_name, link = link.split('->', 1)
                        else:
                            link_name = link
                        if link in links:
                            new_line += f'<a href="{links[link]}">{link_name}</a>'
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
                new_line += char
            line = new_line
        # Title
        c = 0
        nb = 0
        while c < len(line):
            if line[c] == '#':
                nb += 1
            else:
                break
            c += 1
        if nb > 0:
            line = f'<h{nb}>' + line.replace('#' * nb, '', 1).strip() + f'</h{nb}>\n'
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
            if next_line is not None and next_line.strip().startswith('|-'):
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
        # Replace escaped char
        line = escape(line)
        # Paragraph
        if len(line) > 0:
            output.write('<p>' + line.strip() + '</p>\n')
    # Are they list still open?
    if len(list_level) > 0:
        for level in range(len(list_level) - 1, -1, -1):
            output.write(f'</{list_starter[list_level[-1]]}>\n')
            list_level.pop()
    # Are they table still open?
    if in_table:
        output.write('</table>\n')
        in_table = False
    output.write('</body>')
    output.close()

file_names = ['Passe-temps.md', 'Langage.md', 'Tests.md']
#file_names = ['Tests.md']

if __name__ == '__main__':
    for file in file_names:
        print('Processing:', file)
        to_html(file)
