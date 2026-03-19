# LLM Dungeon Master v2.0

LLM Dungeon Master is a lightweight Python application that transforms an OpenAI Large Language Model (LLM) into a creative and fair Dungeons & Dragons 5e Dungeon Master. The tool facilitates deep character customization, manages campaign history, and provides a text-based interface for immersive roleplaying sessions.

## 📖 Table of Contents

  - [Features](https://www.google.com/search?q=%23-features)
  - [Technologies Used](https://www.google.com/search?q=%23-technologies-used)
  - [Installation](https://www.google.com/search?q=%23-installation)
  - [Usage](https://www.google.com/search?q=%23-usage)
  - [Project Structure](https://www.google.com/search?q=%23-project-structure)

## 🚀 Features

  * **Dynamic Character Creation**: Walk through a detailed setup process covering Race, Class, Stats, Backstory, and more.
  * **Persistent Save System**: Automatically saves campaign progress, character sheets, and conversation history to a local JSON file.
  * **AI-Driven Narrative**: Uses advanced LLMs to vividy describe the world, manage NPCs, and adjudicate D\&D 5e rules.
  * **Context-Aware Gameplay**: The system prompt strictly references your character's unique skills and backstory to determine outcomes.

## 🛠️ Technologies Used

  * **Language**: Python 3.x
  * **AI Integration**: OpenAI API (specifically `gpt-4o-mini`)
  * **Data Storage**: JSON-based flat files

## 📥 Installation

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/mtepenner/postgrad-llm-dnd.git
    cd llm-dungeon-master
    ```

2.  **Install dependencies**:

    ```bash
    pip install openai
    ```

3.  **Set up your OpenAI API Key**:
    Ensure your `OPENAI_API_KEY` is set in your environment variables:

    ```bash
    export OPENAI_API_KEY='your-api-key-here'
    ```

## 🎮 Usage

Run the main script to start a new journey or resume a saved campaign:

```bash
python dnd_campaign.py
```

  * **In-Game Commands**:
      * Type your actions naturally (e.g., "I search the room for hidden traps").
      * Type `save`, `quit`, or `exit` to safely store your progress and end the session.

## 📂 Project Structure

  * `dnd_campaign.py`: The main application logic, including the game loop and LLM integration.
  * `campaign_save.json`: (Generated) Stores your character sheet and the full history of your adventure.
