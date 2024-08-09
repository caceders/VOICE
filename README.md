# VOICE
VOICE (Voice-Oriented Interactive Communication and Engagement) is an upcomming project for an AI-driven voice chat platform that facilitates communication between users and an AI conversationalist.

It was created as a small hobby project.

## Vision

The goal of VOICE is to enable users to create a user-custom conversationalist they can talk to and interract with. The conversationalist should remember keypoints of conversations between sessions.

The project is designed to be somewhat modular to enable scalability and maintainability. For a detailed overview of the architecture see [Architecture Documentation](./docs/architecture.md).

## Status

Currently the project is in the planning phase. The following aspects are yet to be developed and/or implemented:

- Voice recognition.
- Interraction with ChatGPT API for response to user.
- Text to speech solutions for the response.

The speech recognition part of the project is not strictly necessary, and is currently emitted. This includes the [Known Persons Register](./docs/architecture.md)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/caceders/VOICE.git
    ```

2. Navigate into the project directory:

    ```bash
    cd VOICE
    ```

3. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

5. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the [MIT License](LICENSE). See the [LICENSE](LICENSE) file for details.

## Contact

Carl Anders Johnsgård Cederström <br>
[email](mailto:andersjohnsgaard@hotmail.com)  
[GitHub](https://github.com/caceders)