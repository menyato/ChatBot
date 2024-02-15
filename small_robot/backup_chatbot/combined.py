from main import chat_bot as main_chat_bot
from data_base import query_data_base

def combined_chat_bot():
    first_question = True

    while True:
        if first_question:
            user_input = input("\nEnter your question (or type 'quit' to exit): ").strip()
        else:
            user_input = input("\nWhat's your next question (or type 'quit' to exit): ").strip()

        if user_input.lower() == "quit":
            break

        if user_input == "":
            continue

        first_question = False

        # Check with the main chat bot
        answer_from_main = main_chat_bot(user_input)

        if answer_from_main and "Bot: I don't know the answer. Can you teach me?" not in answer_from_main:
            # If an answer is found in the knowledge base, print and continue
            print("Answer from knowledge base:", answer_from_main)
        else:
            # If not in knowledge base, query the data_base.py
            answer_from_data_base = query_data_base(user_input)

            if answer_from_data_base:
                print("Answer from data base:", answer_from_data_base)
                # Save the new question and answer in the knowledge base
                main_chat_bot(user_input, answer_from_data_base)
            else:
                print("Bot: I don't know the answer. Can you teach me?")
                new_answer = input('Type the answer or "skip" to skip: ')

                if new_answer.lower() != 'skip':
                    # Save the new question and answer in the knowledge base
                    main_chat_bot(user_input, new_answer)
                    print('Bot: Thank you! I learned a new response!')

if __name__ == '__main__':
    combined_chat_bot()

