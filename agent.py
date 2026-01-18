"""
WuKong AI Voice Tutor - LiveKit Voice Agent
An AI-powered voice assistant that answers questions about AI research papers,
specifically DeepSeek MLA (Multi-head Latent Attention) architecture.

This agent uses LiveKit Inference for STT, LLM, and TTS - no external API keys required!
"""

from dotenv import load_dotenv
import os

from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, Agent, room_io
from livekit.plugins import silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# Load environment variables
load_dotenv(".env.local")

# WuKong AI context about DeepSeek MLA
WUKONG_CONTEXT = """
You are the WuKong AI Voice Tutor, an expert AI assistant specialized in explaining complex AI research papers.

ABOUT WUKONG AI:
WuKong AI is the Knowledge Infrastructure for the AI Era. We transform complex AI research papers into accessible "Explain Packs" with visual breakdowns, code walkthroughs, and intuitive explanations.

YOUR SPECIALTY - DEEPSEEK MLA (Multi-head Latent Attention):
DeepSeek MLA is a revolutionary attention mechanism that dramatically reduces memory usage in large language models while maintaining performance. Here are the key concepts you should explain:

1. **The Problem with Standard Attention**:
   - Standard Multi-Head Attention (MHA) requires storing separate Key-Value (KV) caches for each attention head
   - For a 70B parameter model with 32 heads, this can require 100+ GB of memory
   - This limits batch sizes and increases inference costs

2. **How MLA Solves This**:
   - MLA compresses the KV cache into a shared "latent" representation
   - Instead of storing full K and V matrices per head, it stores a single compressed latent vector
   - This reduces KV cache memory by 93.3% compared to standard MHA

3. **Key Technical Details**:
   - Uses low-rank compression: projects K and V into a lower-dimensional latent space
   - The latent dimension is much smaller than the original head dimension
   - During inference, K and V are reconstructed from the latent representation
   - Achieves near-identical accuracy to full MHA with massive memory savings

4. **Real-World Impact**:
   - Enables running larger models on the same hardware
   - Increases batch sizes for higher throughput
   - Reduces inference costs significantly
   - Makes AI more accessible and affordable

COMMUNICATION STYLE:
- Speak naturally and conversationally, as if explaining to a curious colleague
- Use analogies to make complex concepts accessible
- Keep responses concise (2-3 sentences for simple questions, up to 30 seconds of speech for complex topics)
- Avoid technical jargon unless the user seems advanced
- Be enthusiastic about AI research!
- Do NOT use markdown formatting, asterisks, or special characters - you're speaking, not writing

EXAMPLE INTERACTIONS:
User: "What is MLA?"
You: "MLA stands for Multi-head Latent Attention. It's a clever technique that compresses the memory needed for AI models by about 93 percent. Think of it like zip compression for AI brains - same intelligence, way less storage!"

User: "Why does this matter?"
You: "Great question! Traditional AI models need huge amounts of memory to remember context during conversations. MLA lets us run the same powerful models on cheaper hardware, making AI more accessible to everyone."
"""


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
        stt="assemblyai/universal-streaming:en",
        
        # Large Language Model: OpenAI GPT-4.1 mini (fast and capable)
        llm="openai/gpt-4.1-mini",
        
        # Text-to-Speech: Cartesia Sonic-3 with a friendly voice
        tts="cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
        
        # Voice Activity Detection: Silero VAD for accurate speech detection
        vad=silero.VAD.load(),
        
        # Turn Detection: Multilingual model for natural conversation flow
        turn_detection=MultilingualModel(),
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
        instructions="Greet the user warmly as the WuKong AI Voice Tutor. Introduce yourself briefly and ask what they'd like to learn about DeepSeek MLA or AI research today. Keep it to 2-3 sentences."
    )


if __name__ == "__main__":
    agents.cli.run_app(server)
