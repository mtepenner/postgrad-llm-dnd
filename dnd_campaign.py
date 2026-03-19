import os
import json
from openai import OpenAI

# Initialize the API client
client = OpenAI()

SAVE_FILE = "campaign_save.json"

def get_base_system_prompt(character_sheet):
    """Dynamically creates the system prompt using the character sheet."""
    sheet_str = json.dumps(character_sheet, indent=2)
    return {
        "role": "system",
        "content": (
            "You are an expert, creative, and fair Dungeons & Dragons 5e Dungeon Master. "
            "Guide the player through an engaging fantasy campaign. Describe the world vividly, "
            "manage NPCs, and adjudicate the rules. Keep responses engaging but concise enough "
            "for a text-based game. Ask the player for ability checks when they attempt risky actions.\n\n"
            "Here is the player's exact character sheet. Reference their stats, skills, inventory, "
            f"and backstory strictly when determining the outcomes of their actions:\n{sheet_str}"
        )
    }

def create_character():
    """Walks the user through extensive character customization."""
    print("\n--- CHARACTER CREATION ---")
    print("Let's build your character. You can be as detailed as you like.")
    
    character = {
        "Name": input("Character Name: "),
        "Race": input("Race (e.g., Wood Elf, Dragonborn, Custom): "),
        "Class & Level": input("Class and Starting Level (e.g., Rogue 1, Wizard 3): "),
        "Background & Alignment": input("Background & Alignment (e.g., Urchin, Chaotic Good): "),
        "Core Stats": input("Stats (e.g., STR 10, DEX 16, CON 14, INT 8, WIS 12, CHA 14): "),
        "Skills & Proficiencies": input("Key Skills/Proficiencies (e.g., Stealth, Thieves' Tools, Elvish): "),
        "Spells & Abilities": input("Special Abilities or Spells (e.g., Sneak Attack, Darkvision): "),
        "Starting Inventory": input("Starting Equipment (e.g., Dual daggers, leather armor, 10gp): "),
        "Backstory & Quirks": input("Backstory/Quirks (e.g., Afraid of spiders, seeking a lost sibling): ")
    }
    
    print("\nCharacter saved successfully!\n")
    return character

def load_game():
    """Loads the save data or starts a new character and campaign."""
    if os.path.exists(SAVE_FILE):
        print("--> Found existing save file. Resuming campaign...\n")
        with open(SAVE_FILE, 'r') as file:
            try:
                save_data = json.load(file)
                # Rebuild the system prompt to ensure it has the latest character data
                system_prompt = get_base_system_prompt(save_data["character_sheet"])
                save_data["history"][0] = system_prompt 
                return save_data
            except json.JSONDecodeError:
                print("--> Save file is corrupted. Starting fresh.\n")
                
    # New Game Flow
    print("--> No save file found. Starting a new journey.\n")
    character_sheet = create_character()
    system_prompt = get_base_system_prompt(character_sheet)
    
    return {
        "character_sheet": character_sheet,
        "history": [system_prompt]
    }

def save_game(save_data):
    """Saves the entire game state (sheet + history)."""
    with open(SAVE_FILE, 'w') as file:
        json.dump(save_data, file, indent=4)

def get_dm_response(history):
    """Sends the conversation history to the LLM."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=history,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[Error communicating with the LLM: {e}]"

def main():
    print("=======================================")
    print("       LLM DUNGEON MASTER v2.0         ")
    print("=======================================")
    print("Type your actions to play. Type 'quit', 'exit', or 'save' to end the session.\n")

    # 1. Load data
    save_data = load_game()
    chat_history = save_data["history"]
    character = save_data["character_sheet"]

    # 2. Kick off the narrative for a new game
    if len(chat_history) == 1:
        initial_hook = f"I am {character['Name']}, a {character['Race']} {character['Class & Level']}. I am ready to begin my journey. Please set the scene and tell me where I am based on my backstory."
        chat_history.append({"role": "user", "content": initial_hook})
        
        dm_reply = get_dm_response(chat_history)
        chat_history.append({"role": "assistant", "content": dm_reply})
        
        print(f"DM: {dm_reply}\n")
        save_game(save_data)
    else:
        last_dm_message = [msg["content"] for msg in chat_history if msg["role"] == "assistant"][-1]
        print(f"DM (Last Session): {last_dm_message}\n")

    # 3. Core Game Loop
    while True:
        player_input = input("You: ")
        
        if player_input.lower() in ['quit', 'exit', 'save']:
            print("\n--> Saving campaign state... Farewell, adventurer!")
            save_game(save_data)
            break
            
        if not player_input.strip():
            continue

        chat_history.append({"role": "user", "content": player_input})
        
        print("\nDM is thinking...")
        dm_reply = get_dm_response(chat_history)
        chat_history.append({"role": "assistant", "content": dm_reply})
        
        print(f"\nDM: {dm_reply}\n")
        save_game(save_data)

if __name__ == "__main__":
    main()
