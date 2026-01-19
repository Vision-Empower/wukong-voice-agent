# WuKong AI Voice Tutor

An AI-powered voice assistant that answers questions about AI research papers, specifically DeepSeek MLA (Multi-head Latent Attention) architecture.

Built for **NexHacks Hackathon** - LiveKit Track

## Features

- 🎤 **Real-time Voice Interaction**: Speak naturally and get spoken responses
- 🧠 **AI Research Expert**: Specialized knowledge about DeepSeek MLA architecture
- ⚡ **Low Latency**: Uses LiveKit's optimized STT-LLM-TTS pipeline
- 🔒 **No External API Keys**: Uses LiveKit Inference (all AI models included!)

## Tech Stack

- **LiveKit Agents Framework**: Python SDK for building voice AI agents
- **LiveKit Inference**: Built-in access to STT, LLM, and TTS models
  - STT: AssemblyAI Universal Streaming
  - LLM: OpenAI GPT-4.1 mini
  - TTS: Cartesia Sonic-3

## Quick Start

### Prerequisites

- Python 3.10+ (< 3.14)
- [uv](https://docs.astral.sh/uv/) package manager (recommended)
- LiveKit Cloud account (free tier available)

### Installation

1. Clone this repository or copy the files

2. Install dependencies:
   ```bash
   # Using uv (recommended)
   uv pip install -r requirements.txt
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. Set up environment variables by copying `.env.example` to `.env.local` and filling in your LiveKit credentials:
   ```
   LIVEKIT_URL=wss://your-project.livekit.cloud
   LIVEKIT_API_KEY=your_api_key
   LIVEKIT_API_SECRET=your_api_secret
   ```
   
   Optional model overrides:
   ```
   WUKONG_STT_MODEL=assemblyai/universal-streaming:en
   WUKONG_LLM_MODEL=openai/gpt-4.1-mini
   WUKONG_TTS_MODEL=cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc
   ```
   
   Optional greeting override:
   ```
   WUKONG_GREETING=Greet the user warmly as the WuKong AI Voice Tutor and ask what they want to learn.
   ```

### Running the Agent

**Development mode (connects to LiveKit Cloud):**
```bash
python agent.py dev
```

**Console mode (test in terminal):**
```bash
python agent.py console
```

**Production mode:**
```bash
python agent.py start
```

## How It Works

1. User connects to a LiveKit room via the web frontend
2. The agent joins the same room automatically
3. User speaks → AssemblyAI transcribes speech to text
4. GPT-4.1 mini processes the question with WuKong AI context
5. Cartesia TTS converts the response to natural speech
6. User hears the AI tutor's response in real-time

## Project Structure

```
wukong-voice-agent/
├── agent.py          # Main agent code
├── .env.local        # LiveKit credentials
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Hackathon Submission

- **Event**: NexHacks 2026
- **Track**: LiveKit ($750 + mechanical keyboard prize)
- **Project**: WuKong AI - AI Voice Tutor
- **Demo**: wukongai.io

## License

MIT License - Built for NexHacks Hackathon
