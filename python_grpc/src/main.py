from .services.coach_agent import CoachAgent
from .services.summary_agent import SummaryAgent

# summary_agent = SummaryAgent()
# subjects = summary_agent.extract_subjects("What can the gurjaras do against the franks in imperial age?")
# print(subjects)

coach = CoachAgent()
coach.prompt("What are the unique techs for the sicillians??")
coach.handle_chat()