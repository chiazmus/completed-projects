from langchain_ollama import OllamaLLM

model = OllamaLLM(model="llama3.2:3b")

def chat_with_npc(npc_name, npc_role, conversation_history, input_text):
    
    # NPC's initial prompt
    npc_prompt = f'''You are {npc_name}, a {npc_role} npc for dungeons and dragons.  You can make up reasonable details about your trade, history, and stock if you own a store.  
    Don't speak for the adventurer (ex. "adventurer: "), and keep your responses short and to the point.  You are not aware of the fact that you are a computer program.
    You have been given the following conversation history:\n{conversation_history}.
    Please respond in character to the following input:\nAdventurer: {input_text}.\n'''
    
    # NPC's response
    print('\nthinking...\n')
    npc_response = model.invoke(npc_prompt)

    conversation_history += f"Adventurer: {input_text}\n{npc_name}: {npc_response}\n"
    return npc_response, conversation_history

def main():
    while True:
        print("Welcome to the NPC chat simulation!")
        npc_name = input("Enter the NPC's name: ")
        npc_role = input("Enter the NPC's role: ")
        conversation_history = ""
        print("Type 'exit' to end the conversation.")
        while True:
            input_text = input("You: ")
            if input_text.lower() == 'exit':
                break
            npc_response, conversation_history = chat_with_npc(npc_name, npc_role, conversation_history, input_text)
            print(f"{npc_name}: {npc_response}")
        print('Conversation ended.  Would you like to start a new one? (yes/no)')
        if input().lower() != 'yes':
            break

if __name__ == "__main__":
    main()