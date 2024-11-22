from story_insights.crew import StoryTellerCrew

# Initialize StoryTellerCrew
crew_instance = StoryTellerCrew()

def run_story(story_input):
    """
    Run the crew with the given story input and get story details.
    """
    inputs = {'story': story_input}
    return crew_instance.crew().kickoff(inputs=inputs)