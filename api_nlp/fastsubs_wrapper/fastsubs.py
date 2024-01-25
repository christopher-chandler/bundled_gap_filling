import subprocess


class FastSubs:
    def __init__(
        self,
        n_gram=2,
        model="../../data/language_model/en-70k-0.2-pruned.lm",
        incoming_data="../data/incoming_text_data/sentences.txt",
        fastsubs_m1="../../api_nlp/fastsubs_wrapper/fastsubs_m1",
    ):
        self.n_gram = n_gram
        self.model = model
        self.incoming_data = incoming_data
        self.fastsubs_m1 = fastsubs_m1

    def run_fastsubs(self, input_sentences):
        command = [
            self.fastsubs_m1,
            "-n",
            str(self.n_gram),
            self.model,
            self.incoming_data,
        ]

        with subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ) as process:
            process_input = "\n".join(input_sentences)
            process_output, _ = process.communicate(input=process_input)

            filtered_output = "\n".join(
                line for line in process_output.splitlines() if "free lm..." not in line
            )
            results = filtered_output.split("\n")

            prob_replace = dict()

            for row in results:
                row = row.split("\t")
                word, replacements = row[0], row[1:]
                prob_replace[word] = replacements

        return prob_replace


if __name__ == "__main__":
    pass
