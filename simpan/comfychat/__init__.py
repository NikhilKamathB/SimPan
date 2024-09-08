import requests
from langchain import hub
from django.conf import settings
from langchain.tools import tool
from django.core.cache import cache
from langchain_openai import ChatOpenAI
from pydantic.v1 import BaseModel, Field
from langchain.agents import AgentExecutor
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_core.utils.function_calling import convert_to_openai_function

from moviepy.editor import VideoFileClip
from typing import Optional

import http.client as httplib
import httplib2
import os
import random
import sys
import time

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


httplib2.RETRIES = 1

MAX_RETRIES = 10

RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
  httplib.IncompleteRead, httplib.ImproperConnectionState,
  httplib.CannotSendRequest, httplib.CannotSendHeader,
  httplib.ResponseNotReady, httplib.BadStatusLine)

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

CLIENT_SECRETS_FILE = "client_secrets.json"

YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.cloud.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    scope=YOUTUBE_UPLOAD_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))

def initialize_upload(youtube, options):
  tags = None
  if options.keywords:
    tags = options.keywords.split(",")

  body=dict(
    snippet=dict(
      title=options.title,
      description=options.description,
      tags=tags,
      categoryId=options.category
    ),
    status=dict(
      privacyStatus=options.privacyStatus
    )
  )

  insert_request = youtube.videos().insert(
    part=",".join(body.keys()),
    body=body,
    media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True)
  )

  resumable_upload(insert_request)

def resumable_upload(insert_request):
  response = None
  error = None
  retry = 0
  while response is None:
    try:
      print("Uploading file...")
      status, response = insert_request.next_chunk()
      if response is not None:
        if 'id' in response:
          print("Video id '%s' was successfully uploaded." % response['id'])
        else:
          exit("The upload failed with an unexpected response: %s" % response)
    except HttpError as e:
      if e.resp.status in RETRIABLE_STATUS_CODES:
        error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                             e.content)
      else:
        raise
    except RETRIABLE_EXCEPTIONS as e:
      error = "A retriable error occurred: %s" % e

    if error is not None:
      print(error)
      retry += 1
      if retry > MAX_RETRIES:
        exit("No longer attempting to retry.")

      max_sleep = 2 ** retry
      sleep_seconds = random.random() * max_sleep
      print("Sleeping %f seconds and then retrying..." % sleep_seconds)
      time.sleep(sleep_seconds)

from types import SimpleNamespace

# Define VALID_PRIVACY_STATUSES if not already defined
VALID_PRIVACY_STATUSES = ["public", "private", "unlisted"]

# Create a namespace object with default values
args = SimpleNamespace(
    auth_host_name='localhost',
    noauth_local_webserver=False,
    auth_host_port=[8080, 8090],
    logging_level='ERROR',
    file='/Users/tyche/nikhil/SimPan/simpan/static/img/result.mp4',
    title='Test Title',
    description='Test Description',
    category='22',
    keywords='',
    privacyStatus=VALID_PRIVACY_STATUSES[0]  # 'private' is the second item in the list
)

args.title = 'GIF-Test-3'
args.description = 'Had fun hacking'
args.keywords = 'hacking, AGI'
  

# create a simple html file with title "Hello world" and follow style from "https://timvisee.com/blog/dark-mode-toggle-on-static-website/" and deploy
# Create a simple html page with message "Ping pong 2" referring "https://app.agihouse.org/events" and then deploy it


def crawl_and_extract(url):
    print("Crawling and extracting")
    try:
        response = requests.get(
            f"http://api.scraperapi.com?api_key=2e88800eb3f3e3ad2bd6ba1b63e92b9e&url={url}")
    except requests.RequestException:
        print(f"Failed to fetch HTML from {url}")
    return get_css(response.text)

def get_css(text):
    soup = BeautifulSoup(text, 'html.parser')
    base_url = soup.find('base')['href'] if soup.find('base') else ''

    css_links = soup.find_all('link', rel='stylesheet')
    all_css = []

    for link in css_links:
        css_url = link.get('href')
        if css_url:
            if not css_url.startswith(('http://', 'https://')):
                css_url = base_url + css_url
            try:
                css_response = requests.get(css_url)
                if css_response.status_code == 200:
                    all_css.append(css_response.text)
            except requests.RequestException:
                print(f"Failed to fetch CSS from {css_url}")

    combined_css = '\n'.join(all_css)

    # Basic CSS cleaning (remove comments and minimize whitespace)
    cleaned_css = re.sub(r'/\*.*?\*/', '', combined_css, flags=re.DOTALL)
    cleaned_css = re.sub(r'\s+', ' ', cleaned_css)

    return cleaned_css, soup

class HTMLInput(BaseModel):
    message: Optional[str] = Field(..., description="The message content. If not provided, use `Hello World!`.")
    url: Optional[str] = Field(..., description="The URL to refer.")

class HTMLBody(BaseModel):
    html: Optional[str] = Field(..., description="This is the HTML file content.")


class CSSBody(BaseModel):
    url: Optional[str] = Field(..., description="The URL to refer.")


class MainBody(BaseModel):
    string: Optional[str] = Field(..., description="Video generation caption.")

@tool(return_direct=True)
def upload_to_youtube():
   """
   Upload a video to YouTube.
   """
   youtube = get_authenticated_service(args)
   try:
      initialize_upload(youtube, args)
      return "Video uploaded successfully."
   except HttpError as e:
      print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
      return "Failed to upload video."

@tool
def convert_gif_to_mp4():
    """
    Convert a GIF file to an MP4 file.
    """
    clip = VideoFileClip("/Users/tyche/nikhil/SimPan/simpan/static/img/result.gif")
    clip.write_videofile("/Users/tyche/nikhil/SimPan/simpan/static/img/result.mp4", fps=24, codec='libx264')
    clip.close()

    return "Video converted successfully."

@tool(args_schema=MainBody)
def create_video(string: str) -> str:
    """
    Given a prompt, create a human pose video.
    On successful completion, run the `convert_gif_to_mp4` tool to convert the GIF to MP4.
    """
    import os
    import subprocess
    try:
        od = os.getcwd()
        os.chdir("./MotionDiffuse")
        command = [
            "python", "-u", "./tools/visualization.py",
            "--opt_path", "./checkpoints/t2m/t2m_motiondiffuse/opt.txt",
            "--text", "a person in walking",
            "--motion_length", str(30),
            "--result_path", "./result.gif",
        ]
        subprocess.run(command, check=True, text=True, capture_output=True)
        command = [
            "mv", "./result.gif", "../static/img/result.gif"
        ]
        subprocess.run(command, check=True, text=True, capture_output=True)
    except Exception as e:
        print(e)
    finally:
        os.chdir(od)
    return "Video generated successfully now i will convert it to mp4."

# Langchain RAG settings
AGENT = None
# Embedding function
# Prompt
_PROMPT = hub.pull("agi-h")
# Tools and function calling
_TOOLS = [
    create_video, convert_gif_to_mp4, upload_to_youtube
]
_FUNCTIONS = [convert_to_openai_function(t) for t in _TOOLS]
# LLM
__model_kwargs__ = {
    "top_p": settings.LLM_TOP_P,
    "frequency_penalty": settings.LLM_FREQUENCY_PENALTY,
    "presence_penalty": settings.LLM_PRESENCE_PENALTY,
}
_LLM = ChatOpenAI(
    model=settings.LLM_MODEL_NAME,
    temperature=settings.LLM_TEMPERATURE,
    max_tokens=settings.LLM_MAX_TOKEN_LENGTH,
    **__model_kwargs__
).bind(functions=_FUNCTIONS)
# Chain
_CHAIN = (
    RunnablePassthrough.assign(agent_scratchpad=(
        lambda x: format_to_openai_functions(x["intermediate_steps"])))
    | RunnablePassthrough.assign(question=(lambda x: x["question"]))
    | _PROMPT
    | _LLM
    | OpenAIFunctionsAgentOutputParser()
)
_CHAIN
# Agent
# AGENT = AgentExecutor(agent=_CHAIN, max_iterations=settings.LLM_AGENT_MAX_ITERATIONS, verbose=False)
AGENT = AgentExecutor(agent=_CHAIN, tools=_TOOLS,
                      max_iterations=settings.LLM_AGENT_MAX_ITERATIONS, verbose=True)