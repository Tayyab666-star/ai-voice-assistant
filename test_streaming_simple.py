#!/usr/bin/env python3
"""
Simple test script for streaming transcription functionality
"""

import sys
import os
import asyncio
from unittest.mock import Mock, AsyncMock

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import streaming components
from stt_service.streaming import StreamingSession, StreamingSessionManager, AudioChunk
from stt_service.models import StreamTranscriptionRequest, StreamTranscriptionResponse
from stt_service.service import STTService


def test_streaming_session_creation():
    """Test creating a streaming session"""
    print("Testing StreamingSession creation...")
    
    request = StreamTranscriptionRequest(
        language="en",
        provider="whisper",
        sample_rate=16000,
        chunk_size=1024
    )
    
    session = StreamingSession(
        session_id="test-session",
        request=request
    )
    
    assert session.session_id == "test-session"
    assert session.request.language == "en"
    assert session.request.provider == "whisper"
    assert len(session.audio_buffer) == 0
    assert session.sequence_counter == 0
    
    print("✅ StreamingSession creation test passed")


def test_audio_chunk_processing():
    """Test adding audio data and creating chunks"""
    print("Testing audio chunk processing...")
    
    request = StreamTranscriptionRequest(
        language="en",
        provider="whisper",
        sample_rate=16000,
        chunk_size=1024
    )
    
    session = StreamingSession(
        session_id="test-session",
        request=request
    )
    
    # Create test audio data (1 second of silence)
    audio_data = b'\x00' * (16000 * 2)  # 16kHz, 16-bit, 1 second
    
    chunks = session.add_audio_data(audio_data)
    
    # Should produce at least one chunk
    assert len(chunks) >= 1
    assert all(isinstance(chunk, AudioChunk) for chunk in chunks)
    assert chunks[0].sequence_id == 0
    
    print(f"✅ Audio chunk processing test passed - created {len(chunks)} chunks")


def test_session_expiration():
    """Test session expiration logic"""
    print("Testing session expiration...")
    
    request = StreamTranscriptionRequest()
    session = StreamingSession(
        session_id="test-session",
        request=request
    )
    
    # New session should not be expired
    assert not session.is_expired(timeout_seconds=300)
    
    # Manually set old timestamp
    session.last_activity = session.last_activity - 400
    assert session.is_expired(timeout_seconds=300)
    
    print("✅ Session expiration test passed")


def test_transcription_update():
    """Test updating transcription results"""
    print("Testing transcription updates...")
    
    request = StreamTranscriptionRequest()
    session = StreamingSession(
        session_id="test-session",
        request=request
    )
    
    # Test interim result
    interim_response = StreamTranscriptionResponse(
        text="Hello",
        is_final=False,
        confidence=0.8,
        language="en"
    )
    
    session.update_transcription(interim_response)
    assert "Hello" in session.accumulated_text
    assert session.last_final_text == ""
    
    # Test final result
    final_response = StreamTranscriptionResponse(
        text="Hello world",
        is_final=True,
        confidence=0.9,
        language="en"
    )
    
    session.update_transcription(final_response)
    assert session.last_final_text == "Hello world"
    assert session.accumulated_text == "Hello world"
    assert session.get_average_confidence() == 0.85
    
    print("✅ Transcription update test passed")


async def test_session_manager():
    """Test StreamingSessionManager functionality"""
    print("Testing StreamingSessionManager...")
    
    # Create mock STT service
    mock_stt_service = Mock(spec=STTService)
    mock_response = StreamTranscriptionResponse(
        text="Test transcription",
        is_final=False,
        confidence=0.9,
        language="en"
    )
    mock_stt_service.transcribe_stream = AsyncMock(return_value=mock_response)
    
    # Create session manager
    manager = StreamingSessionManager(mock_stt_service)
    await manager.start()
    
    try:
        # Test creating a session
        request = StreamTranscriptionRequest(
            language="en",
            provider="whisper"
        )
        
        session = manager.create_session("test-session", request)
        assert session.session_id == "test-session"
        assert "test-session" in manager.sessions
        
        # Test retrieving session
        retrieved_session = manager.get_session("test-session")
        assert retrieved_session is not None
        assert retrieved_session.session_id == "test-session"
        
        # Test processing audio chunk
        audio_data = b'\x00' * (16000 * 2)  # 1 second of audio
        
        responses = []
        async for response in manager.process_audio_chunk("test-session", audio_data):
            responses.append(response)
        
        # Should have at least one response
        assert len(responses) >= 1
        
        # Test removing session
        removed = manager.remove_session("test-session")
        assert removed is True
        assert manager.get_session("test-session") is None
        
        print("✅ StreamingSessionManager test passed")
        
    finally:
        await manager.stop()


def main():
    """Run all tests"""
    print("Running streaming transcription tests...\n")
    
    try:
        # Run synchronous tests
        test_streaming_session_creation()
        test_audio_chunk_processing()
        test_session_expiration()
        test_transcription_update()
        
        # Run asynchronous tests
        asyncio.run(test_session_manager())
        
        print("\n🎉 All streaming tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()