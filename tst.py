from api_nlp.fastsubs_wrapper.fastsubs import FastSubs

fastsubs_instance = FastSubs(
    model = "/Users/christopherchandler/code_repos/christopher-chandler/Python/nlp/rub/bundled_gap_filling/data/language_model/en-70k-0.2-pruned.lm",
    incoming_data="/Users/christopherchandler/code_repos/christopher-chandler/Python/nlp/rub/bundled_gap_filling/data/incoming_text_data/sentences.txt",
fastsubs_m1 = "/Users/christopherchandler/code_repos/christopher-chandler/Python/nlp/rub/bundled_gap_filling/api_nlp/fastsubs_wrapper/fastsubs_m1",
    n_gram=2
    )

# Example input sentences
input_sentences = ["Sarah eats apples too"]
prob = fastsubs_instance.run_fastsubs(input_sentences)
print(prob)
