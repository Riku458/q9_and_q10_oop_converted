#1. Modifying the quiz 9 and quiz 10 by implementing inheritance (I will use single inheritance)

import random

class QuizProgram:
    def __init__(self):
        print("\n-------- QUIZ PROGRAM --------")
    
    def run(self):
        while True:
            self.display_menu()
            user_choice = input("Enter your choice (1-3): ")
            
            if user_choice == "1":
                QuizMaker().create_quiz()
            elif user_choice == "2":
                QuizTaker().take_quiz()
            elif user_choice == "3":
                print("Thank you, Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3")
    
    def display_menu(self):
        print("\n-------- MAIN MENU --------")
        print("1. Create a new quiz")
        print("2. Take a quiz")
        print("3. Exit")


class QuizMaker(QuizProgram):
    def create_quiz(self):
        quiz_filename = input("Enter a file name for your quiz file (without extension): ") + ".txt"
        print("\n-------- QUIZ MAKER --------")

        with open(quiz_filename, "a") as quiz_file:
            while True:
                question_text = input("Enter question (or 'quit' to exit): ")
                if question_text.lower() == "quit":
                    break

                question_options = []
                for option_letter in ["a", "b", "c", "d"]:
                    while True:
                        option_text = input(f"Enter option {option_letter}: ").strip()
                        if option_text:  # Ensure option is not empty
                            question_options.append(option_text)
                            break
                        print("Error: Option cannot be empty. Please try again.")

                formatted_correct_answer = self.get_correct_answer()
                
                quiz_file.write(f"Question: {question_text}\n")
                for option_index, option_text in enumerate(question_options):
                    quiz_file.write(f"{chr(97+option_index)}) {option_text}\n")
                quiz_file.write(f"Correct: {formatted_correct_answer}\n\n")

                while True:
                    add_another = input("Add another question? (y/n): ").lower()
                    if add_another in ['y', 'n']:
                        break
                    print("Invalid input. Please enter 'y' or 'n'.")
                if add_another != 'y':
                    break

        print(f"Quiz saved to {quiz_filename}")
    
    def get_correct_answer(self):
        while True:
            prompt = "Enter correct answer/s (e.g., 'a', 'a and b', "
            prompt += "'all', or 'none'): "
            user_correct_answer = input(prompt).lower()

            if user_correct_answer == "none":
                return "none."
            if user_correct_answer == "all":
                return "all answers are correct."

            valid_option_letters = []
            for word in user_correct_answer.replace(',', ' ').split():
                if word in ["a", "b", "c", "d"] and word not in valid_option_letters:
                    valid_option_letters.append(word)

            if not valid_option_letters:
                print("Invalid input! Use letters a-d, 'all', or 'none'.")
                continue

            if len(valid_option_letters) == 1:
                return valid_option_letters[0]
            elif len(valid_option_letters) == 2:
                return " and ".join(valid_option_letters)
            else:
                return ", ".join(valid_option_letters[:-1]) + ", and " + valid_option_letters[-1]


class QuizTaker(QuizProgram):
    def take_quiz(self):
        quiz_filename = input("Enter quiz file name (without extension): ") + ".txt"

        try:
            all_questions = self.load_questions(quiz_filename)
            
            if not all_questions:
                print("No questions found in the file!")
                return

            random.shuffle(all_questions)
            user_responses = self.collect_answers(all_questions)
            self.display_results(user_responses)

        except FileNotFoundError:
            print(f"Error: File '{quiz_filename}' not found!")
    
    def load_questions(self, filename):
        all_questions = []
        current_question_data = {}

        with open(filename, "r") as quiz_file:
            for file_line in quiz_file:
                file_line = file_line.strip()
                if file_line.startswith("Question: "):
                    if current_question_data:
                        all_questions.append(current_question_data)
                    current_question_data = {
                        "question_text": file_line[10:],
                        "question_options": [],
                        "correct_answer": ""
                    }
                elif (file_line and file_line[0] in ['a', 'b', 'c', 'd']
                      and ') ' in file_line):
                    option_letter = file_line[0]
                    option_text = file_line[3:]
                    current_question_data['question_options'].append(
                        (option_letter, option_text)
                    )
                elif file_line.startswith("Correct: "):
                    current_question_data['correct_answer'] = file_line[9:]

            if current_question_data:
                all_questions.append(current_question_data)
        
        return all_questions
    
    def collect_answers(self, questions):
        responses = []
        for question_number, question_data in enumerate(questions, 1):
            print(f"\nQuestion {question_number}: {question_data['question_text']}")
            for option_letter, option_text in question_data["question_options"]:
                print(f"{option_letter}) {option_text}")

            while True:
                user_response = input("Your answer: ").lower()
                valid_responses = ["a", "b", "c", "d", "none", "all"]
                if (user_response in valid_responses or 
                        all(char in ["a", "b", "c", "d"] for char in
                            user_response.replace(",", "").replace(" and ", "").split())):
                    break
                print("Invalid input! Use a-d, 'none', or 'all'")

            responses.append((question_data, user_response))
        
        return responses
    
    def display_results(self, responses):
        print("\n-------- RESULTS --------")
        user_score = sum(1 for q, r in responses if self.check_answer(q['correct_answer'], r))
        
        for response_number, (question_data, user_response) in enumerate(responses, 1):
            is_correct = self.check_answer(question_data['correct_answer'], user_response)
            
            print(f"\nQuestion {response_number}: {question_data['question_text']}")
            for option_letter, option_text in question_data['question_options']:
                print(f"{option_letter}) {option_text}")
            print(f"Your answer: {user_response}")
            print(f"Correct answer: {question_data['correct_answer']}")
            print("Result: " + ("CORRECT" if is_correct else "INCORRECT"))

        print(f"\nFINAL SCORE: {user_score}/{len(responses)} "
              f"({user_score/len(responses):.0%})")
    
    def check_answer(self, stored_answer, user_answer):
        stored_correct_answer = stored_answer.lower().rstrip('.')
        
        if stored_correct_answer == "none":
            return user_answer == "none"
        elif stored_correct_answer == "all answers are correct":
            return user_answer == "all"
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
            if " and " in user_answer:
                user_answer_parts = user_answer.split(" and ")
            elif ", and " in user_answer:
                user_answer_parts = user_answer.split(", and ")
            elif ", " in user_answer:
                user_answer_parts = user_answer.split(", ")
            else:
                user_answer_parts = [user_answer]

            cleaned_user_answers = [
                ans for ans in user_answer_parts
                if ans in ['a', 'b', 'c', 'd']
            ]
            return sorted(cleaned_user_answers) == sorted(correct_answer_parts)


if __name__ == "__main__":
    QuizProgram().run()