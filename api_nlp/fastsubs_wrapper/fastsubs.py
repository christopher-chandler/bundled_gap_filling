# Standard
import subprocess

# Pip
# None

# Custom
# None


class FastSubs:
    def __init__(self):
        self.n_gram = 2
        self.model = "../../data/language_model/en-70k-0.2-pruned.lm"
        self.incoming_data = " ../data/incoming_text_data/sentences.txt"

    def run_fastsubs(self, input_sentences):
        command = [
            "/Users/christopherchandler/code_repos/christopher-chandler/Python/nlp/"
            "rub/bundled_gap_filling/api_nlp/fastsubs_wrapper/fastsubs_m1",
            "-n",
            str(self.n_gram),
            self.model,
            self.incoming_data,
        ]

        # Open subprocess with stdin as a pipe and redirect stdout and stderr to pipes
        with subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ) as process:
            # Pass input sentences to the subprocess
            process_input = "\n".join(['Sarah eats apples too'])

            # Communicate with the subprocess
            process_output, _ = process.communicate(input=process_input)

            # Filter out and print lines that don't contain the initial message
            filtered_output = "\n".join(
                line
                for line in process_output.splitlines()
                if "free lm..." not in line
            )
            results = filtered_output.split("\n")

            print(input_sentences)
            prob_replace = dict()

            for row in results:
                row = row.split("\t")

                word, replacements = row[0], row[1:]
                prob_replace[word] = replacements

        return prob_replace


if __name__ == "__main__":
    fastsubs_instance = FastSubs()

    # Example input sentences
    input_sentences = ["Sarah eats apples too"]
    prob = fastsubs_instance.run_fastsubs(input_sentences)
    print(prob)
