# This exports kindle highlights to markdown

desired_title = ''
filename = ''

list_of_highlights = []
temp_string = []
is_book = False
is_highlight = False
is_note = False
is_bookmark = False
is_duplicate = False

highlight_text = '- Your Highlight on Location '
note_text = '- Your Note on Location '
bookmark_text = '- Your Bookmark on Location '

seperator = '|'
dash_seperator = '-'

# Ask for file name
filename = input('Enter file path: ')

# Ask for book text to match
desired_title = input('Enter title of book: ')

with open(filename, encoding='utf-8') as file:
    for index, line in enumerate(file):
        
        if desired_title in line:
            is_book = True
            
        if is_book:
            # Stop logging at the deliminator, reset the book/highlight toggle
            if '==========' in line:
                if not is_duplicate:
                    list_of_highlights.append(temp_string)

                temp_string = []
                
                is_book = False
                is_highlight = False
                is_note = False
                is_duplicate = False



            # Skip lines with the title in them
            elif desired_title in line:
                pass

            # Skip blank lines
            elif line.strip() == '':
                pass

            # Toggle highlight (to add >), remove date information
            elif highlight_text in line:
                is_highlight = True
                stripped = line.split(seperator, 1)[0]
                location_string = stripped.replace(highlight_text, '')
                location_int = int(location_string.split(dash_seperator, 1)[0])
                formatted_header = '## Location ' + location_string

                if list_of_highlights:
                    for sublist in list_of_highlights:
                        if sublist[0] == location_int and sublist[1] == 1:
                            is_duplicate = True

                if not is_duplicate:
                    temp_string.append(location_int)
                    # Forces sort to put notes before highlights if same number
                    temp_string.append(1)
                    temp_string.append('\n')
                    temp_string.append(formatted_header.strip())

            # Process note lines
            elif note_text in line:
                is_note = True
                stripped = line.split(seperator, 1)[0]
                update_header = stripped.replace(note_text, '')
                note_number = int(update_header.strip())

                if list_of_highlights:
                    for sublist in list_of_highlights:
                        if sublist[0] == note_number and sublist[1] == 0:
                            is_duplicate = True

                if not is_duplicate:
                    temp_string.append(note_number)
                    # Forces sort to put notes before highlights if same number
                    temp_string.append(0)

            # Processing text lines
            else:
                if is_duplicate:
                    pass
                else:
                    if is_highlight:
                        added_carrot = ('>' + line.strip() + '\n')
                        temp_string.append(added_carrot)
                    elif is_note:
                        temp_string.append(line.strip())

sorted_highlights = sorted(list_of_highlights)

deindexed_list = [sublist[2:] for sublist in sorted_highlights]

for i in deindexed_list:
    for j in i:
        print(j, sep='/n') 
            
