import sys
from dotenv import load_dotenv
load_dotenv()

from agent.loop import run_session

if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) or "Give me 2 web VMs"
    run_session(prompt)