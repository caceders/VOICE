# PLAN

A tentative plan of how to tacle the project with enumerated tasks for refrence.

## 1 Implement Real Time Voice Transcriber Component

- 1.1 Implement Azures speech to text SDK
    - ~~1.1.1 Use dotenv to manage secrets and API keys~~
    - 1.1.2 Create a config file containing the setup configurations for Azure SDKs speech recognizer
    - Use [this](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-speech-to-text?tabs=windows%2Cterminal&pivots=programming-language-python) website for guide 
- 1.2 Use pika to prepare for message passing communication

## 2 Implement Voice Activity Gatekeeper

- 2.1 Create a main loop for message passing communication
- 2.2 Implement hibernation enter functionality
- 2.3 Implement awakening functionality
    -2.3.extra Add config variable for wakeup word
- 2.4 Implement check for wether or not to block voice activity transfer to processing subsystem ([thinking operation](./architecture.md))

## 3 Implement Transcription Reformater

- 3.1 Create main loop for message receiving.
- 3.2 Add timestamp to transcribed text to enable the AI to perceive passing of time
    - 3.2.1 Add variable to config file for wether or not to include timestamps in the text to AI

## 4 Implement LLM Responder

- 4.1 Setup API communication with OPENAi API for ChatGPT
    - 4.1.1 Add secrets to dotenv solution
- 4.2 Implement an initialisation of conversation with AI through the first system promt passed to the API
    - 4.2.1 Add variable of first system prompt to config file

## 5 Implement Memory Archiver

- 5.1 Decide on wether to use intermediate periodic saves for memory, save at end of sessoion or a combination.

## 6 Implement Text to Speech Converter

- 6.1 Create main loop for message passing communication.
- 6.2 Setup API communication with OPENAi TTS services
- 6.3 Create a method for playing audio files

## 7 Implement Known Persons Register

- Dependent on 8.1

## 8 Implement Voice Recognizer

- 8.1 Read the [documentation](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speaker-recognition-overview) for Azure speecher recognition and hope to god this is feasable with the current [architectural structure](architecture.md). 
    - It seems to be possible - but the supplied audio samples need to be at least 20 seconds for creating voice profiles - Perhaps ask for permission from user to store identification? Then start an enrollment prosess independent of the thinking process? Will need to experiment.

## 9 Others

- 9.1 Create implementation for initializing threads
    - 9.1.1 Voice Transcriber
    - 9.1.2 Voice Recognizer
    - 9.1.3 Voice Activity Gatekeeper
    - 9.1.4 Test to Speech Converter
