# 🤖 JARVIS - Just A Rather Very Intelligent System

A JARVIS-like AI assistant powered by Bhindi API, featuring voice interaction, task automation, and intelligent conversation.

![JARVIS](https://img.shields.io/badge/JARVIS-v1.0-00D9FF?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red?style=for-the-badge&logo=streamlit)
![Bhindi](https://img.shields.io/badge/Powered%20by-Bhindi%20AI-FFD700?style=for-the-badge)

## ✨ Features

- 🎤 **Voice Interaction** - Speak to JARVIS and hear responses
- 🧠 **Intelligent Conversation** - Context-aware responses with memory
- 📅 **Schedule Management** - Set reminders and manage tasks
- 🔍 **Web Search** - Search and retrieve information
- 🤖 **Task Automation** - Execute tasks using 200+ Bhindi agents
- 💡 **Proactive Suggestions** - Time-based helpful suggestions
- 🎨 **JARVIS-Style UI** - Dark, futuristic interface

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- Microphone (for voice input)
- Bhindi API key ([Get it here](https://bhindi.io/dashboard))

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/ShivanshDubey1704/jarvis-assistant.git
cd jarvis-assistant

# Install dependencies
pip install -r requirements.txt

# For macOS/Linux (PyAudio installation)
# macOS:
brew install portaudio
pip install pyaudio

# Linux:
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio

# Windows: PyAudio should install directly with pip
```

### 3. Configuration

Create a `.env` file in the project root:

```env
BHINDI_API_KEY=your_bhindi_api_key_here
VOICE_ENABLED=true
ASSISTANT_NAME=JARVIS
```

**To get your Bhindi API key:**
1. Visit [Bhindi Dashboard](https://bhindi.io/dashboard)
2. Navigate to API Settings or Developer Settings
3. Click "Create API Key" or "Generate Key"
4. Copy and paste it into your `.env` file

### 4. Run JARVIS

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 🎯 Usage Examples

### Voice Commands

- "JARVIS, what time is it?"
- "Remind me to call mom at 3 PM"
- "Search for the latest AI news"
- "What's the weather like today?"
- "Schedule a meeting tomorrow at 10 AM"

### Text Commands

Type in the chat interface:
- "Set a reminder for 5 PM today"
- "Search for Python tutorials"
- "What's today's date?"
- "Tell me about quantum computing"

## 🛠️ Project Structure

```
jarvis-assistant/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                   # Configuration (create this)
├── .env.example          # Configuration template
├── config.py             # Configuration management
├── core/
│   ├── __init__.py
│   ├── brain.py          # Main AI orchestrator
│   ├── memory.py         # Session memory
│   ├── voice.py          # Voice I/O
│   └── personality.py    # JARVIS personality
└── utils/
    ├── __init__.py
    ├── bhindi_client.py  # Bhindi API wrapper
    └── helpers.py        # Utility functions
```

## 🔧 Configuration Options

Edit `.env` file:

```env
# Required
BHINDI_API_KEY=your_key

# Optional
VOICE_ENABLED=true          # Enable/disable voice
VOICE_RATE=180             # Speech speed (150-200)
VOICE_VOLUME=0.9           # Volume (0.0-1.0)
CONTEXT_WINDOW=10          # Conversation memory size
```

## 🎤 Voice Setup

### Troubleshooting Voice Issues

**No microphone detected:**
```bash
# Test microphone
python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
```

**PyAudio installation issues:**
- **macOS**: `brew install portaudio && pip install pyaudio`
- **Linux**: `sudo apt-get install portaudio19-dev && pip install pyaudio`
- **Windows**: Download wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

## 📝 Available Commands

### Scheduling
- "Remind me to [task] at [time]"
- "Schedule [event] for [date/time]"
- "Set an alarm for [time]"

### Information
- "Search for [query]"
- "What is [question]"
- "Tell me about [topic]"

### Time & Date
- "What time is it?"
- "What's today's date?"

### General
- Any conversational query

## 🔐 Security

- Never commit your `.env` file
- Keep your Bhindi API key secure
- Use environment variables for sensitive data
- The `.gitignore` file is configured to exclude `.env`

## 🐛 Troubleshooting

### "BHINDI_API_KEY is required"
- Create `.env` file with your API key
- Restart the application

### Voice not working
- Check microphone permissions
- Verify PyAudio installation
- Test with: `python -c "import speech_recognition"`

### Slow responses
- Check internet connection
- Verify Bhindi API status
- Reduce CONTEXT_WINDOW in config

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

## 🚀 Future Enhancements

- [ ] Permanent memory with Bhindi Notes
- [ ] Multi-user support
- [ ] Custom agent creation
- [ ] Mobile app version
- [ ] Smart home integration
- [ ] Advanced task automation
- [ ] Learning from user patterns
- [ ] Multi-language support

## 📚 Documentation

- [Bhindi Documentation](https://docs.bhindi.io)
- [Bhindi Dashboard](https://bhindi.io/dashboard)
- [Streamlit Documentation](https://docs.streamlit.io)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

MIT License - Feel free to modify and use!

## 💬 Support

For issues or questions:
- Open an issue on GitHub
- Check [Bhindi Docs](https://docs.bhindi.io)
- Visit [Bhindi Dashboard](https://bhindi.io/dashboard)

## 🌟 Acknowledgments

- Built with [Bhindi AI](https://bhindi.io)
- Inspired by JARVIS from Iron Man
- Powered by [Streamlit](https://streamlit.io)

---

**Made with ❤️ by Shivansh Dubey**

*"Sometimes you gotta run before you can walk." - Tony Stark*