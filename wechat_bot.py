import itchat
from itchat.content import *
import uuid
import os

rec_tmp_dir = 'cache/'


# process face image, predict emotion and return result to the user
@itchat.msg_register([itchat.content.PICTURE], isGroupChat=True)
def face_reply(msg):
    group_name = msg.User['NickName']    
    user = msg.FromUserName

    print(group_name)
    print(user)

    if 'Tensorflow' not in group_name:
        print('Photo not in correct group')
        return
    itchat.send(msg='Processing Image', toUserName=user)

    original_file_name_stripped = rec_tmp_dir + msg['FileName'].split('.')[0]
    original_file_name = original_file_name_stripped + '.jpg'
    # print(msg['FileName'])

    msg.download(original_file_name)

    cmd = 'python3 client.py --server_url "http://localhost:8501/v1/models/faster_rcnn_resnet:predict" --image_path "$(pwd)/'+ original_file_name + '" --output_json "$(pwd)/'+original_file_name_stripped+'.json" --save_output_image "True" --label_map "$(pwd)/data/labels.pbtxt"'

    os.system(cmd)


    itchat.send_image(original_file_name_stripped+'.jpeg', toUserName=user)
    return #'@img@%s' % original_file_name_stripped+'.jpeg'

itchat.auto_login(enableCmdQR=2)
itchat.run()