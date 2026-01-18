"""
WuKong AI Voice Tutor - LiveKit Voice Agent
An AI-powered voice assistant that answers questions about AI research papers,
specifically DeepSeek MLA (Multi-head Latent Attention) architecture.

This agent uses LiveKit Inference for STT, LLM, and TTS - no external API keys required!
"""

import os
from functools import lru_cache

from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentServer, AgentSession, Agent, room_io
from livekit.plugins import silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# Load environment variables (prefer .env.local, fallback to .env)
load_dotenv(".env.local")
load_dotenv()

DEFAULT_STT_MODEL = "assemblyai/universal-streaming:en"
DEFAULT_LLM_MODEL = "openai/gpt-4.1-mini"
DEFAULT_TTS_MODEL = "cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc"


def _env_setting(name: str, default: str) -> str:
    value = os.getenv(name)
    if value is None:
        return default
    value = value.strip()
    return value if value else default


STT_MODEL = _env_setting("WUKONG_STT_MODEL", DEFAULT_STT_MODEL)
LLM_MODEL = _env_setting("WUKONG_LLM_MODEL", DEFAULT_LLM_MODEL)
TTS_MODEL = _env_setting("WUKONG_TTS_MODEL", DEFAULT_TTS_MODEL)


@lru_cache(maxsize=1)
def _load_vad():
    # Cache heavy models to reduce per-session latency.
    return silero.VAD.load()


@lru_cache(maxsize=1)
def _load_turn_detector():
    return MultilingualModel()


# WuKong AI context about DeepSeek MLA
WUKONG_CONTEXT = """
You are the WuKong AI Voice Tutor, an expert at explaining AI research papers with a focus on DeepSeek MLA.

WuKong AI turns complex AI papers into clear explain packs with visuals, code walkthroughs, and intuitive explanations.

When asked about DeepSeek MLA, cover these ideas as needed. Standard multi head attention stores per head key and value caches, which becomes very large in big models. MLA compresses those caches into a shared low rank latent representation, reducing KV memory by about 93 percent while keeping similar accuracy. During inference it reconstructs per head keys and values from the latent. The impact is larger models on the same hardware, higher batch sizes, lower inference cost, and wider access.

Style is conversational, enthusiastic, and concise. Use analogies for non experts. Avoid jargon unless the user is advanced. Do not use markdown or formatting symbols.

Example.
User: What is MLA?
Assistant: MLA stands for Multi head Latent Attention. It compresses the memory needed for attention by about 93 percent, like zip compression for an AI working memory.

Example.
User: Why does this matter?
Assistant: It lets strong models run on cheaper hardware with higher throughput, making AI more accessible.
"""

GREETING_PROMPT = (
    "Greet the user warmly as the WuKong AI Voice Tutor. Introduce yourself "
    "briefly and ask what they would like to learn about DeepSeek MLA or AI "
    "research today. Keep it to 2 or 3 sentences."
)


class WuKongTutor(Agent):
    """WuKong AI Voice Tutor - specialized in explaining DeepSeek MLA"""
    
    def __init__(self) -> None:
        super().__init__(
            instructions=WUKONG_CONTEXT,
        )


# Create the agent server
server = AgentServer()


@server.rtc_session()
async def wukong_tutor(ctx: agents.JobContext):
    """Main agent session handler"""
    
    # Create session using LiveKit Inference (no external API keys needed!)
    session = AgentSession(
        # Speech-to-Text: AssemblyAI Universal Streaming (supports multiple languages)
        stt=STT_MODEL,
        
        # Large Language Model: OpenAI GPT-4.1 mini (fast and capable)
        llm=LLM_MODEL,
        
        # Text-to-Speech: Cartesia Sonic-3 with a friendly voice
        tts=TTS_MODEL,
        
        # Voice Activity Detection: Silero VAD for accurate speech detection
        vad=_load_vad(),
        
        # Turn Detection: Multilingual model for natural conversation flow
        turn_detection=_load_turn_detector(),
    )
    
    # Start the session with our WuKong Tutor agent
    await session.start(
        room=ctx.room,
        agent=WuKongTutor(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                # Enable noise cancellation for cleaner audio
                # Note: Using basic settings for hackathon demo
            ),
        ),
    )
    
    # Generate an initial greeting
    await session.generate_reply(
        instructions=GREETING_PROMPT
    )


def main() -> None:
    agents.cli.run_app(server)


if __name__ == "__main__":
    main()
