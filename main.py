from utils.gpt_interface import ask_gpt

if __name__ == "__main__":
    idea = "How swarm intelligence could be used to run personalized knowledge workflows"
    result = ask_gpt(f'Turn this into a 400-word insight capsule: {idea}')
    print(result)
