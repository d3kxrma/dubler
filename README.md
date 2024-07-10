# DUBLER

dubler is a program that translates videos from one language to another. It is an open-source project aimed at reducing language barriers. I would be happy if you join the development of the project!

# Project status

Currently, this project is in the MVP (Minimum Viable Product) stage, and I am the sole developer, though I hope this situation will change. This project has limitless potential for growth, but it will take a long time if I work on it alone.

# Plans for future
When I created it, I immediately thought that this project should be modular. What does this mean? It means that users will download the program with standard modules, such as STT (Speech-to-Text), translators, and TTS (Text-to-Speech). They will have the ability to create their own modules, for example, to use another service for speech translation. Additionally, users can download ready-made modules from GitHub or elsewhere and add them to the program.

First of all, I would like to refactor the project, rewriting it using classes. I also want to add a CLI (Command Line Interface) where modules can be selected, along with a bunch of other small improvements that will make this project better.

# How to run
To run the program, you need to download it, install the necessary libraries, and change the paths to the input and output videos in the config.py file, as well as the languages you want to translate the video from and to. After that, you can run dubler.py, and it will handle everything.

```bash
git clone https://github.com/d3kxrma/dubler
cd dubler
```
Don't forget to change config.py.
```bash
pip install -r requirements.txt
python dubler.py
```