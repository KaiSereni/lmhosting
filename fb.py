import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import ai

cred = credentials.Certificate('./anarchist-ai-0e9412a6ab55.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://anarchist-ai-default-rtdb.firebaseio.com'
})

USERNAME = 'k'
TASK_REQUESTS_PATH = USERNAME + "/task_requests/"


def runTaskRequest(e: db.Event | None = None):
    requested_task_ref = db.reference(TASK_REQUESTS_PATH)
    requested_task: dict | None = requested_task_ref.get() # type: ignore
    if requested_task is None:
        return
    chatid = requested_task.get("chatid")
    if chatid is None:
        return
    print(f"Running task {chatid}")

    chat_data_ref = db.reference(USERNAME + "/" + str(chatid))
    chat_data: ai.Messages = chat_data_ref.get() # type: ignore
    if not chat_data[-1]['role'] == "user":
        print("Detected another device making updates!")
        exit(1)
    response, history = ai.completion_text(chat_data)
    chat_data_ref.set(history)
    requested_task_ref.delete()


runTaskRequest()
db_listener = db.reference(TASK_REQUESTS_PATH).listen(runTaskRequest)