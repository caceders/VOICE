from datetime import datetime
class TranscriptionFormater:
    def format(self, transcription_to_format) -> str:
        spoken, awokentag = transcription_to_format
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        current_time = f"[{current_time}]"
        if awokentag != "":
            awokentag = f"[{awokentag}]"

        formated_transcript = current_time + awokentag + spoken

        return formated_transcript