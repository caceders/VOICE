# System Architecture

## Overview

This document provides an overview of the system architecture for **VOICE**. The system functionality is divided into three main operations: **Hearing**, **thinking** and **speaking**. In addition to this the system will **hibernate** when it has spent some specified amount of time out of conversatinos. It will then need to be **awakened**.

NOTE: This architecture contains the **Voice Recognizer** which has been temporarily emitted from the project, due to it not being strictly necessary for the fundamental desired functionality.

## Components and data flow

**Hearing**
- **Real Time Voice Transcriber**: Processes and recognizes voice data from system microphone. Outputs text.

- **Voice Recognizer**: Analyzes voice data from system microphone and outputs voice properties.

**Thinking**
- **Voice Activity Gatekeeper**: Blocks audio transcripts information flow when system is generating a response or hybernating. Responsible for system **hibernation** and **awakening**.

- **Transcription Formater**: Formats the transcription from voice for deliverance to the LLM responder. Uses the results from the voice recognizer to lookup names in the Known Persons Register.

- **Known Persons Register**: Holds a register of known persons and their corresponding voice recognition properties.

- **LLM Responder**: Generates a response based on initial configuration values, the formated transcription and memories from the Memory Archive.

- **Memory Archiver**: Archives new information the LLM finds important and retrieves previously stored information. Updates the Known Persons Register if person has been introduced.

**SPEAKING**
- **Text To Speech Converter**: Converts the output from the LLM Responder to speech audio file and plays it. Notifies the Voice Activity Gatekeeper when the system is done speaking and ready to get more user input.

## Interaction Diagram

![System Architecture Diagram](./images/architecture_diagram.png)

## Communication

The **Real Time Voice Transcriber**, the **Voice Recognizer** will be running on seperate threads and communicate to the **Voice Activity Gatekeeper** through messagepassing. This is due to the plan to use Azure Voice Recognition and Voice Transcription APIs concurrently.

The **Voice Activity Gatekeeper** will communicate to the **Transcription Formater** through messagepassing. This is again so that **Voice Activity Gatekeeper** can run concurrently and have a fast response time to deal with more Azure bullshit. The **Transcription Formater**, **LLM Responder** and **Memory Archiver** will communicate through dependency injection. This is due to the simple fact that it is easier to deal with.

The **Text to Speech Converter** will run concurrently on another thread and communicate through messages. This makes all communication to the **Voice Activation Gatekeeper** messaging, again to make it most responsive.

The **Transcription Formater** will communicate to the **Known Persons Register** through RESTApi calls. This is due to the fact that i am terrible with APIs and web communication and know as much about databases as a dry turd.

A figure containing the communication overview is shown in the figure below.

![System Communication Diagram](./images/communication_diagram.png)

## Critique

System architect diagram has some loops. This suggest entanglement and circular dependencies in components. No current suggestions for fixes.