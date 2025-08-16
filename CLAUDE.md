# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an educational Python application for learning OpenAI API capabilities through interactive Streamlit demos. The project demonstrates comprehensive OpenAI API features including text generation, structured outputs, function calling, image/vision processing, audio handling, and conversation management.

## Development Commands

### Running Individual Demos
```bash
# Main integrated demo (port 8501)
streamlit run a10_00_responses_api.py --server.port=8501

# Structured outputs demo  
streamlit run a10_01_structured_outputs_parse_schema.py --server.port=8501

# Tools and Pydantic parsing (port 8502)
streamlit run a10_02_responses_tools_pydantic_parse.py --server.port=8502

# Images and vision (port 8503)
streamlit run a10_03_images_and_vision.py --server.port=8503

# Audio processing (port 8504)
streamlit run a10_04_audio_speeches.py --server.port=8504

# Conversation state management (port 8505)
streamlit run a10_05_conversation_state.py --server.port=8505

# Chain of thought reasoning (port 8506)
streamlit run a10_06_reasoning_chain_of_thought.py --server.port=8506
```

### Testing
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test types using markers
pytest -m unit        # Unit tests only
pytest -m integration # Integration tests only  
pytest -m api         # API tests only
pytest -m slow        # Long-running tests only
```

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Required environment variables
export OPENAI_API_KEY='your-openai-api-key'

# Optional API keys for extended functionality
export OPENWEATHER_API_KEY='your-openweather-api-key'
export EXCHANGERATE_API_KEY='your-exchangerate-api-key'
```

## Architecture

### Core Entry Points
- **a10_00_responses_api.py** - Main integrated demo showcasing all OpenAI features
- **a10_01_structured_outputs_parse_schema.py** - Structured outputs with schema validation 
- **a10_02_responses_tools_pydantic_parse.py** - Pydantic-based parsing and function calling
- **a10_03_images_and_vision.py** - Image generation and vision API demonstrations
- **a10_04_audio_speeches.py** - Text-to-speech, transcription, and realtime audio
- **a10_05_conversation_state.py** - Conversation state management using `previous_response_id`
- **a10_06_reasoning_chain_of_thought.py** - Chain-of-thought reasoning patterns

### Helper Modules

**helper_api.py** contains core API functionality:
- `ConfigManager` - Configuration file handling and model management
- `MessageManager` - Message history and conversation state  
- `TokenManager` - Token counting and cost calculation
- `ResponseProcessor` - Response parsing and error handling
- `OpenAIClient` - Unified OpenAI API client wrapper

**helper_st.py** provides Streamlit UI components:
- `UIHelper` - Common UI element creation
- `SessionStateManager` - Streamlit session state management
- `ResponseProcessorUI` - Response display and formatting
- `InfoPanelManager` - Information panel creation

### Configuration System
- **config.yml** - Central configuration with model definitions, pricing, and sample data
- Supports all OpenAI model categories: frontier (GPT-5), reasoning (o3/o4), standard (GPT-4o), vision, audio, realtime, image generation, and search models
- Environment variable support for API keys and external service configuration

### Key Features Demonstrated
- Comprehensive OpenAI API coverage (text, structured outputs, function calling, vision, audio)
- Pydantic model validation and parsing
- Vector Store integration for file search
- Web search tool integration  
- Conversation state management with `previous_response_id`
- Real-time audio processing
- Multi-modal input handling (text, images, audio)
- Chain-of-thought reasoning patterns

## Development Notes

- All documentation and comments are in Japanese
- Uses Streamlit for interactive web interfaces
- Modular design with comprehensive error handling
- Educational focus with detailed API usage examples
- Each demo runs on different ports for parallel testing
- Includes sample data files in `/data` and `/images` directories
- Test configuration supports multiple test types with custom markers