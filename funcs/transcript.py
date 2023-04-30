from youtube_transcript_api import YouTubeTranscriptApi


# Provides trancript for any youtube video.
# Note: Argument here is the video_id not the URL
def youtube_transcript(video_id):
  '''youtube_transcript taskes "video_id" and not the youtube url as input'''
  transcript_list = []  # Adds each line of text in the list
  yt_transcript = YouTubeTranscriptApi.get_transcript(
    video_id)  # Retrives the transription in the form of a dictionary
  for i in yt_transcript:
    transcript_list.append(
      i['text'])  # Appends each line to the list 'transcript_list'
  return "\n".join(
    transcript_list
  )  # Joins all the lines and adds newline after every element in the list


def upload_transcript():
  '''upload_transcript takes file name (with extension) as input to read its content and return the text in it.'''
  with open(
      "/uploads/file.txt", "r"
  ) as file:  # Opens the file with read access mode and the file is closed as the code progress because of the use of "with" keyword
    return file.read()  # Returns all the text ppresent in the file


if __name__ == "__main__":
  # Test Case for youtube transcript
  print(youtube_transcript("TQMbvJNRpLE"))