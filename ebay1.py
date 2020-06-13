import subprocess
import json
import random
#import texttospeech

def listToDict(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

proc = subprocess.Popen("php /Applications/XAMPP/htdocs/find1.php", shell=True, stdout=subprocess.PIPE)
script_response = proc.stdout.read()
response = script_response.strip().decode('utf-8').split(':')
unkown_result = ['Sorry, could not understand the input','Enter valid input', 'Enter proper input']
if response[0] == 'no results found':
    out = random.choice(unkown_result)
    #texttospeech.tts(out)
    print(out)
else:
    response = listToDict(response)
    for key, value in response.items():
        #texttospeech.tts("The " + key + " is " + value)
        print("The " + key + " is " + value)

