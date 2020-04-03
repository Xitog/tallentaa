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
    # Bold & Italic
    if line.find('**') != -1 or line.find('~~') != -1 \
       or (line.find('*') != -1 and not line.startswith('* ')):
        new_line = ''
        in_bold = False
        in_italic = False
        in_strikethrough = False
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
            if char == '*' and next_char == '*':
                continue
            if char == '*' and next_char != '*' and prev_char != '*':
                if not in_italic:
                    new_line += '<i>'
                    in_italic = True
                else:
                    new_line += '</i>'
                    in_italic = False
                continue
            if char == '*' and prev_char == '*':
                if not in_bold:
                    new_line += '<b>'
                    in_bold = True
                else:
                    new_line += '</b>'
                    in_bold = False
                continue
            if char == '[' and char_index < len(line) - 1:
                ending = line.find(']', char_index)
                if ending != -1:
                    link = line[char_index + 1:ending]
                    if link in links:
                        new_line += f'<a href="{links[link]}">{link}</a>'
                    char_index += len(link) + 1
                    continue
            if char == '~' and next_char == '~':
                continue
            if char == '~' and prev_char == '~':
                if not in_strikethrough:
                    new_line += '<s>'
                    in_strikethrough = True
                else:
                    new_line += '</s>'
                    in_strikethrough = False
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
        if index < len(content) - 2:
            if content[index + 1].strip().startswith('|-'):
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
