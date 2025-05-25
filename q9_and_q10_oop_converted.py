#1. Modifying the quiz 9 and quiz 10 by implementing inheritance 

import random

print("\n-------- QUIZ PROGRAM --------")

while True:
    print("\n-------- MAIN MENU --------")
    print("1. Create a new quiz")
    print("2. Take a quiz")
    print("3. Exit")

    user_choice = input("Enter your choice (1-3): ")

    if user_choice == "1":
        quiz_filename = input(
            "Enter a file name for your quiz file (without extension): "
        ) + ".txt"
        print("\n-------- QUIZ MAKER --------")

        with open(quiz_filename, "a") as quiz_file:
            while True:
                question_text = input("Enter question (or 'quit' to exit): ")
                if question_text.lower() == "quit":
                    break

                question_options = []
                for option_letter in ["a", "b", "c", "d"]:
                    option_text = input(f"Enter option {option_letter}: ")
                    question_options.append(option_text)

                while True:
                    prompt = "Enter correct answer/s (e.g., 'a', 'a and b', "
                    prompt += "'all', or 'none'): "
                    user_correct_answer = input(prompt).lower()

                    if user_correct_answer == "none":
                        formatted_correct_answer = "none."
                        break
                    if user_correct_answer == "all":
                        formatted_correct_answer = "all answers are correct."
                        break

                    valid_option_letters = []
                    for word in user_correct_answer.replace(',', ' ').split():
                        if word in ["a", "b", "c", "d"] and word not in valid_option_letters:
                            valid_option_letters.append(word)

                    if not valid_option_letters:
                        print("Invalid input! Use letters a-d, 'all', or 'none'.")
                        continue

                    if len(valid_option_letters) == 1:
                        formatted_correct_answer = valid_option_letters[0]
                    elif len(valid_option_letters) == 2:
                        formatted_correct_answer = " and ".join(valid_option_letters)
                    else:
                        formatted_correct_answer = ", ".join(
                            valid_option_letters[:-1]
                        ) + ", and " + valid_option_letters[-1]
                    break

                quiz_file.write(f"Question: {question_text}\n")
                for option_index, option_text in enumerate(question_options):
                    quiz_file.write(f"{chr(97+option_index)}) {option_text}\n")
                quiz_file.write(f"Correct: {formatted_correct_answer}\n\n")

                add_another = input("Add another question? (y/n): ").lower()
                if add_another != "y":
                    break

        print(f"Quiz saved to {quiz_filename}")

    elif user_choice == "2":
        quiz_filename = input(
            "Enter quiz file name (without extension): "
        ) + ".txt"

        try:
            all_questions = []
            current_qustion_data = []

            with open(quiz_filename, "r") as quiz_file:
                for file_line in quiz_file:
                    file_line = file_line.strip()
                    if file_line.startswith("Question: "):
                        if current_qustion_data:
                            all_questions.append(current_qustion_data)
                        current_qustion_data = {
                            "question_text": file_line[10:],
                            "question_options": [],
                            "correct_answer": ""
                        }
                    elif (file_line and file_line[0] in ['a', 'b', 'c', 'd']
                          and ') ' in file_line):
                        option_letter = file_line[0]
                        option_text = file_line[3:]
                        current_qustion_data['question_options'].append(
                            (option_letter, option_text)
                        )
                    elif file_line.startswith("Correct: "):
                        current_qustion_data['correct_answer'] = file_line[9:]

                if current_qustion_data:
                    all_questions.append(current_qustion_data)

            if not all_questions:
                print("No questions found in the file!")
                continue

            user_score = 0
            random.shuffle(all_questions)
            selected_quiz_question = all_questions
            user_question_responses = []

            print("\n-------- QUIZ TIME --------")
            print(f"Answer {len(selected_quiz_question)} question:\n")

            for question_number, question_data in enumerate(
                selected_quiz_question, 1
            ):
                print(f"Question {question_number}: {question_data["question_text"]}")
                for option_letter, option_text in question_data["question_options"]:
                    print(f"{option_letter}) {option_text}")

                while True:
                    user_response = input("Your answer: ").lower()
                    valid_responses = ["a", "b", "c", "d", "none", "all"]
                    if (user_response in valid_responses or 
                            all(char in ["a", "b", "c", "d",] for char in
                                user_response.replace(",", "").replace(" and ", "").split())):
                        break
                    print("Invalid input! Use a-d, 'none', or 'all'")

                user_question_responses.append((question_data, user_response))
                print()

            print("\n-------- RESULTS --------")
            for response_number, (question_data, user_response) in enumerate(
                user_question_responses, 1
            ):
                stored_correct_answer = question_data['correct_answer'].lower().rstrip('.')
                is_answer_correct = False

                if stored_correct_answer == "none":
                    is_answer_correct = (user_response == "none")
                elif stored_correct_answer == "all answers are correct":
                    is_answer_correct = (user_response == "all")
                else:
                    # Parse correct answers
                    correct_answer_parts = []
                    if " and " in stored_correct_answer:
                        answer_parts = stored_correct_answer.split(" and ")
                    elif ", and " in stored_correct_answer:
                        answer_parts = stored_correct_answer.split(", and ")
                    elif ", " in stored_correct_answer:
                        answer_parts = stored_correct_answer.split(", ")
                    else:
                        answer_parts = [stored_correct_answer]

                    for part in answer_parts:
                        if part in ['a', 'b', 'c', 'd']:
                            correct_answer_parts.append(part)

                    # Parse user answers
                    user_answer_parts = []
                    if " and " in user_response:
                        user_answer_parts = user_response.split(" and ")
                    elif ", and " in user_response:
                        user_answer_parts = user_response.split(", and ")
                    elif ", " in user_response:
                        user_answer_parts = user_response.split(", ")
                    else:
                        user_answer_parts = [user_response]

                    cleaned_user_answers = [
                        ans for ans in user_answer_parts
                        if ans in ['a', 'b', 'c', 'd']
                    ]
                    is_answer_correct = (
                        sorted(cleaned_user_answers) == sorted(correct_answer_parts)
                    )

                print(f"\nQuestion {response_number}: {question_data['question_text']}")
                for option_letter, option_text in question_data['question_options']:
                    print(f"{option_letter}) {option_text}")
                print(f"Your answer: {user_response}")
                print(f"Correct answer: {question_data['correct_answer']}")
                print("Result: " + ("CORRECT" if is_answer_correct else "INCORRECT"))

                if is_answer_correct:
                    user_score += 1

            print(
                f"\nFINAL SCORE: {user_score}/{len(selected_quiz_question)} "
                f"({user_score/len(selected_quiz_question):.0%})"
            )

        except FileNotFoundError:
            print(f"Error: File '{quiz_filename}' not found!")

    elif user_choice == "3":
        print("Thank you, Goodbye!")
        break

    else:
        print("Invalid choice. Please enter 1, 2, or 3")