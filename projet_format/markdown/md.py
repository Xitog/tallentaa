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

file_name = 'Passe-temps'

source = open(file_name + '.md', mode='r', encoding='utf8')
content = source.readlines()
source.close()

output = open(file_name + '.html', mode='w', encoding='utf8')
output.write('<html>\n')
output.write('<head>\n')
output.write('</head>\n')
output.write('<body>\n')

in_list = False
in_table = False
links = {}

# prefetch links
filtered_content = []
for index, raw_line in enumerate(content):
    # Strip
    line = raw_line.strip()
    # Empty
    if len(line) == 0:
        continue
    # Special chars
    line = line.replace('&', '&amp;')
    # Links
    if line[0] == '[' and (line.find(']: https://') != -1 or line.find(']: http://') != -1):
        name = line[1:line.find(']: ')]
        link = line[line.find(']: ') + len(']: '):]
        links[name] = link
        continue
    filtered_content.append(line)

for index, raw_line in enumerate(filtered_content):
    line = raw_line
    if index < len(filtered_content) - 2:
        next_line = filtered_content[index + 1]
    else:
        next_line = None
    # Bold & Italic & Strikethrough & Underline & Power
    #or (line.find('*') != -1 and not line.startswith('* ')) \
    if line.find('**') != -1 or line.find('--') != -1 \
       or line.find('__') != -1 or line.find('^^') != -1 or line.find("''"):
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
            if char_index < len(line) - 2:
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
            if char == "'" and next_char == "'":
                continue
            if char == "'" and prev_char == "'":
                if not in_italic:
                    new_line += '<i>'
                    in_italic = True
                else:
                    new_line += '</i>'
                    in_italic = False
                continue
            # Strong
            if char == '*' and next_char == '*':
                continue
            if char == '*' and prev_char == '*':
                if not in_bold:
                    new_line += '<b>'
                    in_bold = True
                else:
                    new_line += '</b>'
                    in_bold = False
                continue
            # Strikethrough
            if char == '-' and next_char == '-':
                continue
            if char == '-' and prev_char == '-':
                if not in_strikethrough:
                    new_line += '<s>'
                    in_strikethrough = True
                else:
                    new_line += '</s>'
                    in_strikethrough = False
                continue
            # Underline
            if char == '_' and next_char == '_':
                continue
            if char == '_' and prev_char == '_':
                if not in_underline:
                    new_line += '<u>'
                    in_underline = True
                else:
                    new_line += '</u>'
                    in_underline = False
                continue
            # Power
            if char == '^' and next_char == '^':
                continue
            if char == '^' and prev_char == '^':
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
    if line.startswith('* '):
        if not in_list:
            output.write('<ul>\n')
            in_list = True
        line = '<li>' + line.replace('* ', '', 1).strip() + '</li>\n'
        output.write(line)
        continue
    elif in_list:
        output.write('</ul>\n')
        in_list = False
    # Table
    if line[0] == '|':
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
                    output.write(f'<{element}>{col}</{element}>')
            output.write('</tr>\n')
        continue
    elif in_table:
        output.write('</table>\n')
        in_table = False
    # Paragraph
    output.write('<p>' + line.strip() + '</p>\n')
output.write('</body>')
output.close()
