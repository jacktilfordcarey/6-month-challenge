"""Test TTS generation with male voice"""
from gtts import gTTS
import os

test_text = "This is a test of the male text to speech voice."

# Test different TLD options for more masculine voice
tlds = ['co.uk', 'com.au', 'co.in', 'com']

for tld in tlds:
    try:
        print(f"Trying TLD: {tld}")
        tts = gTTS(text=test_text, lang='en', slow=False, tld=tld)
        output_file = f'output_folder/test_voice_{tld.replace(".", "_")}.mp3'
        tts.save(output_file)
        print(f"✅ Saved: {output_file}")
    except Exception as e:
        print(f"❌ Failed for {tld}: {e}")

print("\nNote: gTTS uses Google's TTS which doesn't have true male/female options.")
print("Different TLDs may have slightly different voices.")
print("For true male voice, you'd need a different TTS engine like pyttsx3 or Azure TTS")
