import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_blog_topics(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Generate similar blog topics:\n1. {prompt}\n",
        temperature=0.4,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['text']


def generate_blog_sections(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Create an outline for a blog on the topic {prompt}:\n",
        temperature=0,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['text']

 
def blog_from_section(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Create a 500-word long blog with the following outline: {prompt}\n",
        temperature=0.9,
        max_tokens=600,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['text']


dir = "./blogs/"
if not os.path.exists(dir):
  os.makedirs(dir)

prompt = input("Enter the blog topic: ")

with open(dir + f"{prompt}.txt", "a") as f:
    blog_sections = generate_blog_sections(prompt)
    blog_content = blog_from_section(blog_sections)
    f.write(blog_content)

blog_topics = generate_blog_topics(prompt)
for blog_topic in iter(blog_topics.splitlines()):
    blog_topic = blog_topic.partition(" ")[2]
    if blog_topic:
        blog_sections = generate_blog_sections(blog_topic)
        with open(dir + f"{blog_topic}.txt", "a") as f:
            blog_content = blog_from_section(blog_sections)
            f.write(blog_content)
