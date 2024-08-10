from langchain.chains.base import Chain
from langchain_community.llms import Ollama

lan_model = Ollama(model="llama3")

class ContentGenerationChain(Chain):
    @property
    def input_keys(self):
        return ["prompt"]

    @property
    def output_keys(self):
        return ["generated_content"]

    def _call(self, inputs):
        prompt = inputs["prompt"]
        response = lan_model.generate(prompts=[prompt])
        generated_content = response.generations[0][0].text
        return {"generated_content": generated_content}

content_generation_chain = ContentGenerationChain()


while True:
    question_prompt = (
        "You are a cyber security expert. "
        "Ask a question about cyber security in order to test another expert's knowledge "
        "There must be 1 correct choice and 2 incorrect choices in the multiple choice"
        "Do not provide the answer."
    )

    question = {"prompt": question_prompt}
    output_data = content_generation_chain(question)
    generated_question = output_data["generated_content"]
    print(generated_question)
    print("______________________________________________")

    ans = input("answer: (0 to exit)\n ")
    if ans == "0":
        break
    print(" ")

    validation_prompt = (
        "You are a security expert. "
        f"The question is: {generated_question} "
        f"Is the following answer to the question correct: {ans}? "
        "Start the response with 'true' or 'false' depending on whether the answer is correct."
    )

    check_data = {"prompt": validation_prompt}
    output_data = content_generation_chain(check_data)
    validation_response = output_data["generated_content"]
    print(validation_response)
    print("______________________________________________")
    print("______________________________________________")
