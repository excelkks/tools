"""
change values of config file.\n
config file should like this
\tkey1    : value1    #comment1
\tkey2    : value2    #comment2
\t...
"""

def change_value(origin_data, change_data):
    assert type(change_data) == dict
    content = ''
    for line in origin_data:
        index_com = -1
        if '#' in line:
            index_com = line.find('#')
        line_data = line[:index_com].strip()
        # comment
        if not line_data or ':' not in line_data:
            content += line
            continue
        index_key = line.find(':')
        key_s = line[:index_key]
        value_s = line[index_key+1:index_com]
        comment_s = line[index_com:]
        key = key_s.strip()
        comment = comment_s.strip()
        if key in change_data.keys():
            change_value = str(change_data[key])
            this_line = key_s + ': ' + change_value
            space_length = index_com - len(this_line) if index_com else 0
            space_value = space_length * ' '
            content += this_line + space_value + comment + '\n'
        else:
            content += line
    return content

def new_config(src_file, dst_file, change_data):
    """
    new_config(src_file, dst_file, change_data)
    \tsrc_file:
    \tdst_file:
    \tchange_data: dict type contian all key-value to be changed
    """
    assert type(change_data) == dict
    dst_data = ''
    with open (src_file, 'r') as src_config:
        src_data = src_config.readlines()
        dst_data = change_value(src_data, change_data)
    with open(dst_file, 'w') as dst_config:
        dst_config.write(dst_data)

def change_config(config_file, change_data):
    """
    change_config(config_file, change_data)\n
    \tconfig_file: config file path
    \tchange_data: dict type contian all key-value to be changed
    """
    new_config(config_file, config_file, change_data)
