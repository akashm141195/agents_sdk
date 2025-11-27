from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder

project = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint="https://ai-foundry-sandbox-akm.services.ai.azure.com/api/projects/firstProject")

agent = project.agents.get_agent("asst_IXoGzoQymGKxHFMuZCAsdgWf") # orchestration agent

thread = project.agents.threads.create()
print(f"Created thread, ID: {thread.id}")

message = project.agents.messages.create(
    thread_id=thread.id,
    role="user",
    content="find pet with id 256761"
)

run = project.agents.runs.create_and_process(
    thread_id=thread.id,
    agent_id=agent.id)

if run.status == "failed":
    print(f"Run failed: {run.last_error}")
else:
    messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)

    for message in messages:
        if message.text_messages:
            print(f"{message.role}: {message.text_messages[-1].text.value}")

while True:
    user_input = input("\nYou: ")
    
    project.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )
    
    run = project.agents.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id)
    
    messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    
    for message in messages:
        if message.role == "assistant" and message.text_messages:
            print(f"Assistant: {message.text_messages[-1].text.value}")