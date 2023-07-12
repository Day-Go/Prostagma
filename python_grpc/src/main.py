from .services.coach_agent import CoachAgent
from .services.summary_agent import SummaryAgent
from .services.prompt_agent import PromptAgent
from .services.data_agent import DataAgent

question = ("I just lost a game on arabia when i was playing as the franks against the ethiopians." 
            "he went all in arbalester and halb vs my knights. what else could i have done?")

# Pass user question into prompt agent. 
# The prompt agent will break the question down into short, concise statements.
prompt_agent = PromptAgent()
statements: list = prompt_agent.convert_to_statements(question)
print(statements)

data_agent = DataAgent()

for statement in statements:
    data_agent.get_data(statement)

