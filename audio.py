import requests
import base64
from tqdm import tqdm
import sys

master_json_url = sys.argv[1]
# master_json_url = 'https://skyfire.vimeocdn.com/1547381752-0x0ffb66d27b842a67e6dc939793df239d239b5cd1/289443352/sep/video/1095656952,1095657109,1095656947,1095656940/master.json?base64_init=1'
base_url = master_json_url[:master_json_url.rfind('/', 0, -26) + 1]
base_url = base_url.replace('/video/', '')
print ('Start base url', base_url)
resp = requests.get(master_json_url)
content = resp.json()

heights = [(i, d['height']) for (i, d) in enumerate(content['video'])]
print ('heights:', heights)
idx, _ = max(heights, key=lambda (_, h): h)
video = content['audio'][0]
video_base_url = base_url + video['base_url'].replace('..', '')
print 'base url:', video_base_url

filename = 'audio.mp4'.format(video['id'])
print 'saving to {}'.format(filename)

video_file = open(filename, 'wb')

init_segment = base64.b64decode(video['init_segment'])
video_file.write(init_segment)

for segment in tqdm(video['segments']):
    segment_url = video_base_url + segment['url']
    resp = requests.get(segment_url, stream=True)
    if resp.status_code != 200:
        print 'not 200!'
        print resp
        print segment_url
        break
    for chunk in resp:
        video_file.write(chunk)

video_file.flush()
video_file.close()
