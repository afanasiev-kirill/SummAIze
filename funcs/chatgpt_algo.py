import openai
import os

# Transcript - Youtube / Text / File
from funcs.transcript import *

# Initialize OpenAI API key
openai.api_key = os.environ['OpenAIKey']


def split_text(text):
  '''Define function to split text into chunks of 1300 tokens'''
  words = text.split()
  word_limit = 1300
  num_parts = len(words) // word_limit + 1
  parts = []
  for i in range(num_parts):
    start_index = i * word_limit
    end_index = (i + 1) * word_limit
    parts.append(' '.join(words[start_index:end_index]))
  return parts


transcript = ''  # Initailising the transcript variable


def user_select_type(type: int, data):
  '''Function for selecting type from user input'''
  if type == 0:
    transcript = youtube_transcript(data)
  elif type == 1:
    transcript = upload_transcript(data)
  else:
    print("Error! No options selected.")


def ChatGPT():
  '''Function used to access ChatGPT's api'''
  # Split transcript into chunks of 1300 tokens
  chunks = split_text(transcript)

  # Summarize each chunk using OpenAI GPT 3.5 Turbo API
  summary_list = []
  for i, chunk in enumerate(chunks):
      prompt = [{
      "role":
      "system",
      "content":
      "Act as a meeting note taker, and summarize this meeting transcript. Highlight to-do lists and important keypoints from each speaker as highly precisely as possible. Make sure not to give any numbering to anything but add a new line after every keypoint. Additionally, add curly brackets around each speaker name."
    }, {
      "role": "user",
      "content": chunk
    }, {
      "role": "assistant",
      "content": "Keypoints:"
    }]
      response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=prompt, max_tokens=300, temperature=0.6, n=1, stop=None)
      result = response.choices[0].message['content'].strip()
      summary_list.append(result)

  # Join all summaries into one string
  result = '\n'.join(summary_list)

  return result


# Print final summary
if __name__ == "__main__":
  user_select_type(0, "TQMbvJNRpLE")
  print(ChatGPT())
