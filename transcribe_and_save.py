import whisper
from docx import Document

# Load the Whisper model
model = whisper.load_model("small")  # You can use "small", "medium", or "large" based on accuracy needs

# Transcribe the audio file
audio_file = "D:\\Uni Work\\Python\\Speech Recognition\\data\\sentences\\sentence_1_1.wav"  # Replace with your audio file path
result = model.transcribe(audio_file)

# Print the transcription
print("Transcription:\n", result["text"])

# Create a new Word document and add the transcription text
doc = Document()
doc.add_paragraph(result["text"])  # Add transcription text to the document

# Save the document
doc_name = "D:\\Uni Work\\Python\\Speech Recognition\\New Model\\Transcription.docx"
doc.save(doc_name)

print(f"Transcription saved to {doc_name}")
