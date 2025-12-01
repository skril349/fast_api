from fastapi import FastAPI, BackgroundTasks
import time

app = FastAPI()

def write_notification(email:str, message=""):
    time.sleep(4)  # Simula una tarea que toma tiempo
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)
    print("Termino de enviar la notificacion")

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}