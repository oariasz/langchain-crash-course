# Same code as the lesson 5 but implementing databases with ElephantSQL

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# PostgreSQL connection URL (replace placeholders with actual credentials from ElephantSQL)
DATABASE_URL = "postgresql://username:password@hostname:port/database"

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Define ChatMessage model
class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True)
    session_id = Column(String, nullable=False)
    sender = Column(String, nullable=False)  # 'user' or 'ai'
    message = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, default=datetime.datetime.utcnow)

# Create the table if it doesn't exist
Base.metadata.create_all(engine)

# Function to save a message to the database
def save_message(session_id, sender, message):
    chat_message = ChatMessage(session_id=session_id, sender=sender, message=message)
    session.add(chat_message)
    session.commit()

# Function to retrieve chat history for a session
def get_chat_history(session_id):
    messages = session.query(ChatMessage).filter_by(session_id=session_id).order_by(ChatMessage.timestamp).all()
    return [{"role": msg.sender, "content": msg.message} for msg in messages]

# Chat session setup
SESSION_ID = "user_session_new"  # Could be a username or unique ID
model = ChatOpenAI()

print("Start chatting with the AI. Type 'exit' to quit.")

# Load existing chat history
chat_history = get_chat_history(SESSION_ID)
print("Current Chat History:", chat_history)

while True:
    human_input = input("User: ")
    if human_input.lower() == "exit":
        break

    # Add user message to the database
    save_message(SESSION_ID, "user", human_input)

    # Get updated chat history
    chat_history = get_chat_history(SESSION_ID)

    # Invoke the AI model
    ai_response = model.invoke(chat_history)
    ai_message = ai_response.content

    # Add AI message to the database
    save_message(SESSION_ID, "ai", ai_message)

    print(f"AI: {ai_message}")
