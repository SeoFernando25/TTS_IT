# TTS-IT

A **WINDOWS ONLY** shell that plays [AWS Polly](https://aws.amazon.com/polly/)/[StreamLabs](https://blog.streamlabs.com/how-to-add-text-to-speech-to-donations-to-your-stream-548e9908b451) text-to-speech on [Soundpad](https://leppsoft.com/soundpad/en/)

## Requirements

- [Soundpad](https://leppsoft.com/soundpad/en/) (Either steam version or DRM-Free should)
- An amazon AWS account
- [Python 3](https://www.python.org/downloads/)
- `pip install boto3`

## How to use

- Download the repository
- Create a file named `credentials.ini` in the same folder and paste the following replacing `MY_AWS_ACCESS_KEY` by your AWS Access key and `MY_AWS_SECRET_KEY` by your secret   

  ```ini
  [Credentials]
  AccessKeyId = MY_AWS_ACCESS_KEY
  SecretKey = MY_AWS_SECRET_KEY
  ```

  if you don't already have AWS credentials you can get one by [clicking this link](https://console.aws.amazon.com/iam/home?#/security_credentials) and creating a new one in the `Access keys` tab
- Open SoundPad
- Run `py tts_it.py credentials.ini`

## Commands

- `help`
  - shows a list of availible commands
- `quit`
  - quits
- `say {arg}`
  - Sends an API call to Polly to download the line and plays it through SoundPad
  - If no argument is provided the program will enter in "immediate say mode." You can leave it by pressing CTRL-C
- `search {arg}`
  - Search for voices that match argument
  - If no arguments is provided list all voices
- `set {arg}`
  - Sets the voice to closest match
  - If no argument is provided load the first voice in voices.json
