import os
import time
import speech_recognition as sr

from slack import WebClient


def transcribe_message(channel_id, message_id):
    # Pobierz plik audio wiadomości głosowej
    file_id = message_content["attachments"][0]["payload"]["file"]["id"]
    audio_file = client.files_info(file_id)["content"]["url"]

    # Przetwórz plik audio za pomocą biblioteki SpeechRecognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    # Wygeneruj transkrypcję
    try:
        # Wykorzystaj bibliotekę Whisperer do transkrypcji
        whisperer = whisperer.Whisperer(
            model_path="https://github.com/BGC-SC/Slack-W-bot/tree/main/whisper-main",
            api_key="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",
        )
        transcript = whisperer.transcribe_from_audio(audio)
    except sr.UnknownValueError:
        transcript = "Nie udało się rozpoznać wypowiedzi"
    except sr.RequestError:
        transcript = "Błąd połączenia z serwerem"

    # Wyślij transkrypcję do kanału
    client.chat_postMessage(channel=channel_id, text=transcript)


if __name__ == "__main__":
    # Utwórz klienta Slack
    client = WebClient(os.environ["https://hooks.slack.com/triggers/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"])

    # Odbierz wszystkie wiadomości
    for event in client.events_api().rtm_read():
        # Jeśli wiadomość jest wiadomością głosową
        if event and event["type"] == "message" and event["text"].startswith("https://api.slack.com/files/"):
            # Transkrybuj wiadomość głosową
            transcribe_message(event["channel"], event["channel_id"])
