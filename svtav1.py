sequences = [
#       "huochezhan_3840x2160_25_150.yuv",
#       "yewandaolu_3840x2160_30_150.yuv",
#       "shizilukou1_2448x2048_25_250.yuv",
#       "shenwumen_1920x1080_50_500.yuv",
#       "tingchechang_1920x1080_25_250.yuv",
#       "xiangkou_1920x1080_25_250.yuv",
#       "yuxuedaolu_1920x1080_30_300.yuv",
#       "cheliangdaolu2_1920x1080_30_300.yuv",
        "chezaiyundong_1280x720_30_300.yuv",
        "shineichukou_1280x720_30_300.yuv"
        ]
seq_dir = "/mnt/10/算法/video_codec/svac2/yuv/"
encode_mode = [
#       "ai",
#       "ld",
        "ra"
        ]
qps = [22, 27, 32, 37]

encoder = ""
decoder = ""
encode_config = "Config/Sample.cfg"

frames = 'FrameToBeEncoded'
para_dict = {
#        'StatReport' : 0
        frames : -1      # -1 for all frames
        }


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
    assert type(change_data) == dict
    dst_data = ''
    with open (src_file, 'r') as src_config:
        src_data = src_config.readlines()
        dst_data = change_value(src_data, change_data)
    with open(dst_file, 'w') as dst_config:
        dst_config.write(dst_data)

for seq in sequences:
    seq_info = seq.split('_')
    assert len(seq_info)==4,"wrong sequence name format: "+seq
    seq_name = seq.split('.')[0]
    seq_width = seq_info[1].split('x')[0]
    seq_height = seq_info[1].split('x')[1]
    seq_frame_rate = seq_info[2]
    seq_encode_frame = seq_info[3].split('.')[0]
    if frames in para_dict.keys() and para_dict[frames] > 0:
        pass
    else:
        para_dict.update({frames: seq_encode_frame})
    seq_path = seq_dir + seq
    stream_name = seq_name + '.ivf'
    recon_name = 'recon' + seq_name + '.yuv'
    error_file = seq_name + '_err' + '.log'
    stat_file = seq_name + '_stat' + '.log'
    for mode in encode_mode:
        intra_period = -1
        pred_structure = 2
        if mode == 'ai':
            intra_period = 1
        elif mode == 'ld_p':
            pred_structure = 0
        elif mode == 'ld_B':
            pred_structure = 1
        else:
            pred_structure = 2
        for qp in qps:
            config_dict = {
                    'InputFile' : seq,
                    'StreamFile' : stream_name,
                    'ErrorFile' : error_file,
                    'StatFile': stat_file,
                    'SourceWidth': seq_width,
                    'SourceHeight': seq_height,
                    'FrameRate': seq_frame_rate,
                    'IntraPeriod': intra_period,
                    'QP': qp,
                    'PredStructrue': pred_structure
                    }
            config_dict.update(para_dict)
            seq_config = mode+'_'+seq_name+'_qp'+str(qp) + '.cfg'
            new_config(encode_config, seq_config, config_dict)
            encode_command = encoder + ' -c ' + config_dict +' > ' mode+'_'+seq_name+'_qp'+str(qp)+'.log'
            decode_command = decoder + ' -i ' + stream_name + ' -o ' + 'decode_'+seq
