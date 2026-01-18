#!/usr/bin/env python3
"""Test script to verify LiveKit Agents imports"""

success = True

try:
    from livekit.agents import AgentServer, AgentSession, Agent
    print("✓ LiveKit Agents core imported successfully")
except ImportError as e:
    success = False
    print(f"✗ Failed to import LiveKit Agents: {e}")

try:
    from livekit.plugins import silero
    print("✓ Silero VAD plugin imported successfully")
except ImportError as e:
    success = False
    print(f"✗ Failed to import Silero: {e}")

try:
    from livekit.plugins.turn_detector.multilingual import MultilingualModel
    print("✓ Turn detector plugin imported successfully")
except ImportError as e:
    success = False
    print(f"✗ Failed to import Turn detector: {e}")

try:
    from dotenv import load_dotenv
    print("✓ python-dotenv imported successfully")
except ImportError as e:
    success = False
    print(f"✗ Failed to import dotenv: {e}")

if success:
    print("\nAll imports successful! Agent is ready to run.")
else:
    print("\nOne or more imports failed. Install dependencies before running the agent.")
