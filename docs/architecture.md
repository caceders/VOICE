# System Architecture

## Overview

This document provides an overview of the system architecture for **VOICE**. The system functionality is divided into three main operations: **Hearing**, **thinking** and **speaking**. In addition to this the system will **hybernate** when it has spent some specified amount of time out of conversatinos. It will then need to be **awoken**.

## Components and data flow

**Hearing**
- **Real time voice transcriber**: Processes and recognizes voice data from system microphone. Outputs text.

- **Voice recognizer**: Processes voice data from system microphone and outputs voice properties.

**Thinking**
- **Voice activity gatekeeper**: Blocks audio transcripts information flow when system is generating a response or hybernating. Responsible for system **hybernation** and **awakening**.

- **Transcription formater**: Formats the transcription from voice for deliverance to the LLM responder. Uses the results from the voice recognizer to lookup names in the known persons register.

- **Known persons register**: Holds a register of known persons and their corresponding voice recognition properties.

- **LLM responder**: Generates a response based on initial configuration values, the formated transcription and memories from the memory archive.

- **Memory archiver**: Archives new information the LLM finds important and retrieves previously stored information. Updates the known persons register if person has been introduced.

**SPEAKING**
- **Text to speech converter**: Converts the output from the LLM responder to speech audio file and plays it. Notifies the voice activity gatekeeper when the system is done speaking and ready to get more user input.

## Interaction Diagram

![System Architecture Diagram](./images/architecture_diagram.png)

## Critique

System information diagram has some loops. This suggest entanglement in components. No current suggestions for fixes.