# Functional Requirements for VOICEs modules

## Real Time Voice Transcriber
- Transcribe all recognized voice and communicate it to the **Voice Activity Gatekeeper**.
- When a voice is detected, transcribe it until the *section* is finished.


## Voice Activity Gatekeeper
- Receives the transcribed voices from **Real Time transcriber**. 
- Delivers the transcribed voice to the **Transcription Formater** only when specific conditions are met:
    - System is awake.
    - System is not responding.
    - System is hybernating, but wakeup-phrase has been received.
Else the transcribed message is dropped.
- Set recording to active until it gets *response finished* message from the **Text To Speech Converter**.
- Begins hybernation when system is out of conversation for a specified amount of time.
- Awakens when wakeup-phrase has been received.
- Keeps track of wether the system is responding or not.

## Transcription formater
- Receives the transcribed voice that has passed the **Voice Activity Gatekeeper**.
- Formats the transcribed voice with relevant information for the AI:
    - Timestamp.
    - Wakeup stamp if the system has just been awoken.
- Passes the formated transcription to the LLM responder.

## LLM Responder
- Receives the transcribed voice from the **Transcription Formater**.
- Sends the transcription as user prompt to LLM.
- Collects response from LLM and sends to the **Text To Speech Converter**.
- Initiates OpenAI LLM with initial promt defined from the configuration file.
- Retrieves relevant (all) past information from the memory archiver. Sends info to LLM upon initialisation
- Tells LLM to summarize new information on quit. Sends info to memory archiver.
- Sends summarized information to memory archiver.

## Memory Archiver
- Stores new information from the **LLM Respnder**
- Retrieves old information for the **LLM Responder**

## Text To Speech Converter
- Sets up and configures the OpenAI speech synthesis.
- Gets LLM response from the **LLM Responder**, converts it to speech through OpenAI speech synthesis.
- Plays the received speech synthesis.
- Sends *response finished* message to the **Voice Acticity Gatekeeper**.