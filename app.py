from langchain_openai import ChatOpenAI
from moviepy import *
import re
from gtts import gTTS
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=1,
    api_key="REPLACE_WITH_YOUR_API_KEY"
)
clips = []
count = 0
description = input("Enter a question: ")
messages = [
    ("system", 
     "You are an assistant generating educational video content. Your task is to create EXACTLY 5 question-and-answer pairs. Not 4. Not 6. Exactly 5. Follow the structure below without deviation:\n\n"
     "Question: <Insert question here>\n"
     "Answer: <Insert one-paragraph answer here, no more than 140 words>\n\n"
     "Repeat this EXACTLY 5 times. DO NOT include any introductions, summaries, explanations, or extra formatting. Just 5 question-answer pairs. If you do not follow this, the output is INVALID.\n\n"
     "AGAIN: Output ONLY 5 question-answer pairs using the format:\n"
     "Question: ...\n"
     "Answer: ...\n"
     "Repeat this format 5 times ONLY."),
    ("human", description)
]


response = llm.invoke(messages)
qa_pairs = re.findall(r"Question:\s*(.*?)\s*Answer:\s*(.*?)(?=\nQuestion:|\Z)", response.content, re.DOTALL)


for q, a in qa_pairs:
    tts_q = gTTS(q)
    tts_q.save(f'{count}.wav')
    qclipwav = AudioFileClip(f'{count}.wav')
    qclip = TextClip(
        text=q,
        font="NotoSansCJK-Light",
        font_size=70,
        color="black",
        bg_color="white",
        size=(1920, 1080),  # Ensure a size if needed
        method='caption'
    ).with_position(("center", "center")).with_duration(qclipwav.duration).with_audio(qclipwav)
    clips.append(qclip)
    count += 1

    # Answer
    tts_a = gTTS(a)
    tts_a.save(f'{count}.wav')
    aclipwav = AudioFileClip(f'{count}.wav')
    aclip = TextClip(
        text=a,
        font="NotoSansCJK-Light",
        font_size=40,
        color="black",
        bg_color="white",
        size=(1920, 1080),
        method='caption'
    ).with_position(("center", "center")).with_duration(aclipwav.duration).with_audio(aclipwav)
    clips.append(aclip)
    count += 1

final_clip = concatenate_videoclips(clips)
final_clip.write_videofile("result.mp4", temp_audiofile="temp-audio.m4a", remove_temp=True, fps=10, codec="libx264", preset="ultrafast", audio_codec="aac", audio=True)

