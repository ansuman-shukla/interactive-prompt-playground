import streamlit as st
import openai
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Interactive Prompt Playground",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize OpenAI client
@st.cache_resource
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("⚠️ OpenAI API key not found! Please add your API key to the .env file.")
        st.stop()
    return openai.OpenAI(api_key=api_key)

def generate_response(client, model, system_prompt, user_prompt, temperature, max_tokens, 
                     presence_penalty, frequency_penalty, stop_sequences):
    """Generate response from OpenAI API"""
    try:
        messages = []
        
        if system_prompt.strip():
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": user_prompt})
        
        # Prepare stop sequences
        stop = None
        if stop_sequences and stop_sequences.strip():
            stop = [seq.strip() for seq in stop_sequences.split(',') if seq.strip()]
            if not stop:
                stop = None
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            stop=stop
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("🎮 Interactive Prompt Playground")
    st.markdown("*Create and test product descriptions with configurable AI parameters*")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # Model Selection
        st.subheader("Model Settings")
        model = st.selectbox(
            "Select Model",
            ["gpt-3.5-turbo", "gpt-4", "gpt-4.1"],
            index=0,
            help="Choose the OpenAI model to use"
        )
        
        # Prompt Configuration
        st.subheader("Prompt Configuration")
        
        system_prompt = st.text_area(
            "System Prompt",
            value="You are a creative marketing expert specializing in writing compelling product descriptions. Create engaging, informative, and persuasive descriptions that highlight key features and benefits.",
            height=100,
            help="Set the behavior and context for the AI"
        )
        
        user_prompt_template = st.text_area(
            "User Prompt Template",
            value="Write a compelling product description for: {product}",
            height=80,
            help="Use {product} as placeholder for the product name"
        )
        
        # Product Input
        st.subheader("Product Input")
        product_name = st.text_input(
            "Product Name",
            value="iPhone 15 Pro",
            help="Enter the product you want to describe"
        )
        
        # Parameter Configuration
        st.subheader("AI Parameters")
        
        # Temperature
        temperature = st.select_slider(
            "Temperature",
            options=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2],
            value=0.7,
            help="Controls randomness (0.0 = deterministic, 1.2 = very creative)"
        )
        
        # Max Tokens
        max_tokens = st.select_slider(
            "Max Tokens",
            options=[50, 100, 150, 200, 250, 300, 400, 500],
            value=150,
            help="Maximum length of the response"
        )
        
        # Presence Penalty
        presence_penalty = st.select_slider(
            "Presence Penalty",
            options=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5],
            value=0.0,
            help="Penalizes new topics (0.0 = no penalty, 1.5 = strong penalty)"
        )
        
        # Frequency Penalty
        frequency_penalty = st.select_slider(
            "Frequency Penalty",
            options=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5],
            value=0.0,
            help="Penalizes repetition (0.0 = no penalty, 1.5 = strong penalty)"
        )
        
        # Stop Sequences
        stop_sequences = st.text_input(
            "Stop Sequences",
            value="",
            help="Comma-separated list of sequences where generation should stop"
        )
        
        # Generate Button
        generate_button = st.button("🚀 Generate Description", type="primary", use_container_width=True)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Current Configuration")
        
        # Display current settings
        config_data = {
            "Model": model,
            "Product": product_name,
            "Temperature": temperature,
            "Max Tokens": max_tokens,
            "Presence Penalty": presence_penalty,
            "Frequency Penalty": frequency_penalty,
            "Stop Sequences": stop_sequences if stop_sequences else "None"
        }
        
        for key, value in config_data.items():
            st.metric(key, value)
        
        # Show the actual prompt that will be sent
        st.subheader("🎯 Final Prompt")
        final_user_prompt = user_prompt_template.format(product=product_name)
        
        with st.expander("System Prompt", expanded=False):
            st.code(system_prompt, language="text")
        
        with st.expander("User Prompt", expanded=True):
            st.code(final_user_prompt, language="text")
    
    with col2:
        st.subheader("🤖 Generated Response")
        
        if generate_button:
            if not product_name.strip():
                st.error("Please enter a product name!")
                return
            
            with st.spinner("Generating product description..."):
                client = get_openai_client()
                final_user_prompt = user_prompt_template.format(product=product_name)
                
                response = generate_response(
                    client=client,
                    model=model,
                    system_prompt=system_prompt,
                    user_prompt=final_user_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    presence_penalty=presence_penalty,
                    frequency_penalty=frequency_penalty,
                    stop_sequences=stop_sequences
                )
                
                st.success("✅ Description generated!")
                st.markdown("### Product Description:")
                st.markdown(f"**Product:** {product_name}")
                st.markdown("---")
                st.write(response)
                
                # Option to copy response
                st.code(response, language="text")
        
        else:
            st.info("👈 Configure your settings and click 'Generate Description' to see the AI response!")
    


if __name__ == "__main__":
    main()
