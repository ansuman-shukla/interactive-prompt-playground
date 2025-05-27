# Interactive Prompt Playground

A Streamlit-based application for testing and experimenting with OpenAI's GPT models using configurable parameters. Perfect for creating and optimizing product descriptions with different AI settings.

## Features

- **Model Selection**: Choose between GPT-3.5-turbo, GPT-4, and GPT-4.1
- **Configurable Prompts**: Customize both system and user prompts
- **Parameter Testing**: Adjust temperature, max tokens, presence penalty, and frequency penalty



# Reflection on hyperparameters

## Stop Sequences
    - It is a special character or word. If that word is found in the LLM's output, the generation stops. This is what powers the tool calls. It causes the LLM to stop producing tokens after it has completed the tool call request and wait for the message from the tool call.   
## Frequency Penalty
    -It is a penalty imposed on the model when they use a particular word in a conversation repeatedly. It is a scaling penalty that increases as the word appears more frequently. While experimenting with this I realised the value between [0.2 ,0.8] is best for all the task where user wants to get output that doesn't contain repetitive words or "SOUND LIKE AI"
## Presence Penalty
    - It is imposed on the model when they use a particular word even once in a conversation. It is also called flat penalty due to its uniform nature - applying the same penalty regardless of frequency.This penalty looks at both the input prompt and generated output to discourage repetition from the entire conversation context  
## Max Tokens 
    - It is simple and stright forward as the name suggest this hyperparameter allow the number of tokens the LLM can produce in its response.

## Setup Instructions

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure OpenAI API Key**:
   - Open the `.env` file
   - Replace `your_openai_api_key_here` with your actual OpenAI API key
   - Get your API key from: https://platform.openai.com/api-keys

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and navigate to the displayed URL (usually `http://localhost:8501`)

## How to Use

### Configuration Panel (Sidebar)
- **Model Settings**: Select your preferred GPT model
- **Prompt Configuration**: Set system prompt and user prompt template
- **Product Input**: Enter the product you want to describe
- **AI Parameters**: Adjust the following parameters:
  - **Temperature** (0.0-1.2): Controls creativity and randomness
  - **Max Tokens** (50-500): Sets response length
  - **Presence Penalty** (0.0-1.5): Reduces likelihood of new topics
  - **Frequency Penalty** (0.0-1.5): Reduces repetition
  - **Stop Sequences**: Define where generation should stop

### Main Interface
- **Current Configuration**: View all active settings at a glance
- **Final Prompt**: See exactly what will be sent to the AI
- **Generated Response**: View the AI-generated product description
- **Quick Test Presets**: Try different parameter combinations instantly

## Parameter Guide

### Temperature Values
- **0.0**: Deterministic, consistent outputs
- **0.7**: Balanced creativity and consistency (recommended)
- **1.2**: Highly creative and varied outputs

### Token Limits
- **50**: Very concise descriptions
- **150**: Standard length descriptions (recommended)
- **300**: Detailed, comprehensive descriptions

### Penalty Settings
- **0.0**: No penalties applied
- **1.5**: Strong penalties for repetition/new topics


## File Structure

```
interactive-prompt-playground/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (API keys)
└── README.md          # This file
```

## Dependencies

- `streamlit`: Web application framework
- `openai`: Official OpenAI Python client
- `python-dotenv`: Environment variable management

## Security Note

Never commit your `.env` file with real API keys to version control. The provided `.env` file contains placeholder values only.

## Temperature
    - Temperature controls the randomness and creativity in LLM's - the lower the temperature the LLM will adhere to the user instructions and be more deterministic and hallucinate less. Higher temperature makes outputs more creative and diverse
