#coding=utf-8
import xlrd
import os
from watson_developer_cloud import TextToSpeechV1
import  string
import types

text_to_speech = TextToSpeechV1(
    iam_apikey='qF4sb1e4TLG9h66RpeWCwLFR6noQefvNfP8Y1Wv5SHPn',
    url='https://stream.watsonplatform.net/text-to-speech/api'
)

def create_voice(content,filename):
    with open(filename, 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                content,
                'audio/mp3',
                'en-US_AllisonVoice'
            ).get_result().content)

def read_xlsx(fileName):
    data=xlrd.open_workbook(fileName)
    for i in data.sheet_names(): # 遍历sheet
        # 判断目录是否存在,如果目录存在则跳过当前课程
        isExist=os.path.exists("./"+i)
        if isExist:
            continue
        auido_path="./"+i
        os.mkdir(auido_path) #生成目录
        # 遍历每一个sheet,找对对应单元格的内容
        if string.rfind(i, "LessonExercise") != -1:
            table = data.sheet_by_name(i)
            cols=table.ncols
            voiceIndex = 1
            for i in range(table.nrows):
                row=table.row(i)
                first = row[0].value
                m = type(first)
                if m is types.StringType:
                    print  "kind is string"
                elif m is types.FloatType:
                    first = str(int(float(first)))
                elif m is types.IntType:
                    first = str(first)
                elif str(first.__class__).rfind("unicode") > 0:
                    first = first.encode('unicode-escape').decode('string_escape')
                if string.rfind(first, "test") == 0: # 表示新开了一个类型
                    tmp = string.split(first, "-")
                    file_path = auido_path + "/" + tmp[1] + "/"
                    os.makedirs(file_path)
                    # 找出声音的索引
                    for j in range(cols):
                        if string.rfind(row[j].value, "声音".decode('utf-8'))!=-1:
                            voiceIndex = j
                            break
                    continue
                content=row[voiceIndex].value # 找到要生成音频的内容
                if len(content)==0:
                    continue
                if int(float(first))==5: #level8之后生成的语音,第五道题不生成语音
                    continue


                fileName=file_path+row[voiceIndex+1].value+".mp3"
                print voiceIndex,"content=",content,"fileName=",fileName,"str(content)=",str(content)
                content= '<voice-transformation type=\"Custom\" rate=\"x-slow\">'+content+'</voice-transformation>'
                if len(content)==0:
                    continue
                create_voice(content,fileName)
        else:
            voiceIndex=-1
            table = data.sheet_by_name(i)
            cols = table.ncols
            for i in range(table.nrows):
                row=table.row(i)
                first=row[0].value
                m=type(first)
                if m is types.StringType:
                    print  "kind is string"
                elif m is types.FloatType:
                    first=str(int(float(first)))
                elif m is types.IntType:
                    first=str(first)
                elif str(first.__class__).rfind("unicode")>0:
                    first=first.encode('unicode-escape').decode('string_escape')

                if string.rfind(first,"test".decode('utf-8'))==0:
                    voiceIndex=0
                    tmp = string.split(row[0].value, "-")
                    file_path = auido_path + "/" + tmp[1] + "/"
                    os.makedirs(file_path)
                    # 找出声音的索引
                    for j in range(cols):
                        if string.rfind(row[j].value, "声音文件编号".decode('utf-8')) != -1:
                            voiceIndex = j
                            break
                    continue
                if voiceIndex==-1:
                    continue
                if voiceIndex==0:
                    break
                content = row[voiceIndex+1].value  # 找到要生成音频的内容
                if len(content)==0:
                    continue
                fileName = file_path + row[voiceIndex].value + ".mp3"
                print voiceIndex, "content=", content, "fileName=", fileName
                content = '<voice-transformation type=\"Custom\" rate=\"x-slow\">' + content + '</voice-transformation>'
                if len(content) == 0:
                    continue
                create_voice(content, fileName)
    print "create voice data end"

if __name__=="__main__":
    read_xlsx("L0.xlsx")
    # content='<voice-transformation type=\"Custom\" rate=\"x-slow\">'+"helloWorld"+'</voice-transformation>'
    # create_voice(content,"./output.mp3")




