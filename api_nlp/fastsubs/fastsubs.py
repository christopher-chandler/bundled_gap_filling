# Standard
import subprocess
import os

# Pip
# None

# Custom
# None


class FastSubs:
    def __init__(self):
        self.n_gram = 2
        self.model = "../../data/language_model/en-70k-0.2-pruned.lm"
        self.incoming_data = "data/incoming_text_data/test.txt"

    def run_fastsubs(self, input_sentences):
        command = [
            "./fastsubs_m1",
            "-n",
            str(self.n_gram),
            self.model,
            self.incoming_data,
        ]

        try:
            # Open subprocess with stdin as a pipe and redirect stdout and stderr to pipes
            with subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            ) as process:
                # Pass input sentences to the subprocess
                process_input = "\n".join(input_sentences)

                # Communicate with the subprocess
                process_output, _ = process.communicate(input=process_input)

                # Filter out and print lines that don't contain the initial message
                filtered_output = "\n".join(
                    line
                    for line in process_output.splitlines()
                    if "free lm..." not in line
                )
                print("Subprocess output:", filtered_output)

        except subprocess.CalledProcessError as e:
            print(f"Error running fastsubs: {e}")


if __name__ == "__main__":
    fastsubs_instance = FastSubs()

    # Example input sentences
    input_sentences = ["This is a sample sentence.", "Another sentence."]

    fastsubs_instance.run_fastsubs(input_sentences)
