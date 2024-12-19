
from dotenv import load_dotenv
from datetime import datetime
import os
import azure.cognitiveservices.speech as speech_sdk

def main():
    try:
        # Load environment variables
        load_dotenv()
        ai_key = os.getenv('SPEECH_KEY')
        ai_region = os.getenv('SPEECH_REGION')

        # Check if the environment variables are loaded
        if not ai_key or not ai_region:
            raise ValueError("Speech API key or region is missing from environment variables.")

        # Configure speech service
        speech_config = speech_sdk.SpeechConfig(subscription=ai_key, region=ai_region)
        print('Ready to use speech service in:', speech_config.region)

        # Get spoken input
        command = TranscribeCommand(speech_config)

        if command.lower() == 'what time is it?':
            TellTime(speech_config)

    except Exception as ex:
        print("An error occurred:", ex)

def TranscribeCommand(speech_config):
    command = ''
    # Configure speech recognition
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
    print('Speak now...')

    # Process speech input
    speech = speech_recognizer.recognize_once_async().get()
    
    if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        command = speech.text
        print("Recognized command:", command)
    else:
        print(speech.reason)
        if speech.reason == speech_sdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print("Speech recognition canceled:", cancellation.reason)
            print("Error details:", cancellation.error_details)

    # Return the command
    return command

def TellTime(speech_config):
    now = datetime.now()
    response_text = 'The time is {}:{:02d}'.format(now.hour, now.minute)
    
    # Configure speech synthesis
    speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"  # Consistent voice with config
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config=speech_config)

    # SSML response for speech synthesis
    responseSsml = f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
        <voice name='en-GB-RyanNeural'>
            {response_text}
            <break strength='weak'/>
            Time to end this lab!
        </voice>
    </speak>
    """

    # Synthesize spoken output
    speak = speech_synthesizer.speak_ssml_async(responseSsml).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print("Error during speech synthesis:", speak.reason)
    
    # Print the response text
    print(response_text)

if __name__ == "__main__":
    main()
