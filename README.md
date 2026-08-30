# 📧 Gmail Reader - AI-Powered Email Voice Assistant

## Overview
Gmail Reader is an intelligent Python application that converts email messages into natural language voice output. It leverages AI to read, translate, and synthesize emails in multiple languages through voice commands—perfect for accessibility and hands-free email management.

## 🎯 Key Features

- **AI-Powered Email Reading**: Automatically fetch and process emails from Gmail
- **Multi-Language Translation**: Translate email content into any language in real-time
- **Voice Synthesis**: Convert text to natural-sounding speech
- **Voice Commands**: Hands-free control using voice input
- **Smart Filtering**: Filter emails by sender, subject, or date
- **Accessibility First**: Designed for users with visual impairments

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| **Language** | Python 3.8+ |
| **Email API** | Gmail API / IMAP |
| **AI/ML** | NLP for text processing, Transformer models |
| **Voice** | Text-to-Speech (gTTS, pyttsx3, Azure TTS) |
| **Audio** | Speech Recognition (SpeechRecognition) |
| **Translation** | Google Translate API / Hugging Face |
| **Package Manager** | pip |

## 📋 Requirements

```
python>=3.8
google-auth-oauthlib
google-auth-httplib2
google-api-python-client
pyttsx3
SpeechRecognition
google-cloud-translate
PyAudio
```

## 🚀 Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/KiranKadam959596/gmail-reader.git
cd gmail-reader

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. **Gmail API Setup**:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project
   - Enable Gmail API
   - Create OAuth 2.0 credentials (Desktop application)
   - Download credentials.json and place in project root

2. **Environment Variables** (create `.env` file):
   ```
   GMAIL_USER=your-email@gmail.com
   TRANSLATION_API_KEY=your-google-translate-key
   SPEECH_LANGUAGE=en-US
   ```

### Usage

```python
from gmail_reader import GmailReader, VoiceAssistant

# Initialize
reader = GmailReader()
assistant = VoiceAssistant(language='en')

# Authenticate with Gmail
reader.authenticate()

# Read latest emails
emails = reader.get_latest_emails(count=5)

# Convert to speech
for email in emails:
    text = f"From {email['sender']}: {email['subject']}"
    assistant.speak(text)
    
# Translate email to Spanish and speak
assistant.speak(text, translate_to='es')
```

## 📊 Project Structure

```
gmail-reader/
├── README.md
├── requirements.txt
├── .env.example
├── src/
│   ├── gmail_reader.py          # Core Gmail integration
│   ├── voice_assistant.py        # Voice processing & synthesis
│   ├── translator.py             # Multi-language translation
│   └── config.py                 # Configuration management
├── tests/
│   ├── test_gmail_reader.py
│   └── test_voice_assistant.py
├── examples/
│   ├── basic_usage.py
│   └── advanced_features.py
└── docs/
    └── API.md
```

## 💡 Use Cases

- ✅ **Accessibility**: Help visually impaired users manage emails
- ✅ **Multitasking**: Listen to emails while driving/exercising
- ✅ **Language Learning**: Hear emails in your target language
- ✅ **Productivity**: Hands-free email management
- ✅ **Global Communication**: Instant email translation

## 🔐 Security Features

- OAuth 2.0 authentication (no password storage)
- Encrypted credential management
- API rate limiting to prevent abuse
- Secure token refresh mechanism

## 📈 Future Enhancements

- [ ] Sentiment analysis of emails
- [ ] Smart reply suggestions
- [ ] Integration with other email providers (Outlook, Yahoo)
- [ ] Mobile app (Flutter/React Native)
- [ ] Custom voice models
- [ ] Offline mode with cached emails
- [ ] Integration with calendar events
- [ ] Email classification and smart folders

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## 📚 Documentation

See [API Documentation](docs/API.md) for detailed API reference.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👤 Author

**Kiran Kadam** - [@KiranKadam959596](https://github.com/KiranKadam959596)

## 📞 Support

- 📧 Open an issue for bug reports
- 💬 Discussions for feature requests
- 📖 Check the Wiki for FAQs

## 🌟 Show Your Support

If this project helped you, please consider:
- ⭐ Starring the repository
- 🔗 Sharing with others
- 💬 Providing feedback

---

**Last Updated**: January 2026 | **Status**: Active Development
