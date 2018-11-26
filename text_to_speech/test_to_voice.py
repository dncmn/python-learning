from watson_developer_cloud import TextToSpeechV1
text_to_speech = TextToSpeechV1(
    iam_apikey='QbAV9t1aq389j5fF7CBzARrKj1UkosMQbhQ1ND1Tdg87',
    url='https://stream.watsonplatform.net/text-to-speech/api'
)

with open('hello_world.mp3', 'wb') as audio_file:
    audio_file.write(
        text_to_speech.synthesize(
            '<voice-transformation type=\"Custom\" rate=\"x-slow\">hello world</voice-transformation>',
            'audio/mp3',
            'en-US_AllisonVoice'
        ).get_result().content)