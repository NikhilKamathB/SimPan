import requests
from langchain import hub
from django.conf import settings
from langchain.tools import tool
from django.core.cache import cache
from langchain_openai import ChatOpenAI
from pydantic.v1 import BaseModel, Field
from langchain.agents import AgentExecutor
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.runnables import RunnablePassthrough
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_core.utils.function_calling import convert_to_openai_function

from typing import Optional
from fabric.tasks import task
from fabric import Connection
from invoke import run as local
import re
from bs4 import BeautifulSoup

CONNECT_KWARGS = {"key_filename": ["/Users/tyche/.ssh/agi"]}
CONN = Connection(host="34.16.75.203", user="nikhilkb98",
                  connect_kwargs=CONNECT_KWARGS)


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

@tool(args_schema=HTMLInput)
def create_a_html_page(message: str, url: str) -> str:
    """
    Create a HTML page with a message
    """
    # Embedding function
    # Prompt
    _PROMPT = hub.pull("age-house-1")
    _PROMPT_2 = hub.pull("age-house-2")
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
    )
    css_content, soup = crawl_and_extract(url)
    # import pdb; pdb.set_trace()

    # Chain
    _CHAIN = (
        RunnablePassthrough.assign(question=(lambda x: x["css_content"]))
        | _PROMPT
        | _LLM
        | OpenAIFunctionsAgentOutputParser()
    )
    _CHAIN_2 = (
        RunnablePassthrough.assign(question=(lambda x: x["html_content"]))
        | _PROMPT_2
        | _LLM
        | OpenAIFunctionsAgentOutputParser()
    )
    # import pdb; pdb.set_trace()
    print("Invoked the chain")
    x = _CHAIN.invoke({"css_content": css_content})
    y = _CHAIN_2.invoke({"html_content": soup})
    color = x.return_values.get("output", "#000000")
    title = y.return_values.get("output", "Simple H1 Page")
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple H1 Page</title>
    <style>
        h1 {{
            color: {color};
        }}

        p {{
            overflow: visible;
            white-space: normal;
            word-wrap: break-word;
        }}
    </style>
</head>
<body>

<h1>{message}</h1>

<h2>The title of the site - {title}</h2>

<p>Lorem ipsum odor amet, consectetuer adipiscing elit. Hac ad pharetra bibendum cursus ac eget odio. Est diam senectus cursus vestibulum curae imperdiet adipiscing. Litora blandit proin lobortis etiam metus dapibus laoreet. Augue non fames sit est mus placerat ad cursus. Taciti penatibus elit accumsan dictumst ipsum. Potenti eros ultricies scelerisque sollicitudin eleifend bibendum parturient phasellus. Molestie natoque et per; fusce egestas urna. Porta elementum vestibulum tempus cubilia scelerisque tempor elit.</p>
<p>Lorem ipsum odor amet, consectetuer adipiscing elit. Hac ad pharetra bibendum cursus ac eget odio. Est diam senectus cursus vestibulum curae imperdiet adipiscing. Litora blandit proin lobortis etiam metus dapibus laoreet. Augue non fames sit est mus placerat ad cursus. Taciti penatibus elit accumsan dictumst ipsum. Potenti eros ultricies scelerisque sollicitudin eleifend bibendum parturient phasellus. Molestie natoque et per; fusce egestas urna. Porta elementum vestibulum tempus cubilia scelerisque tempor elit.</p>
<p>Lorem ipsum odor amet, consectetuer adipiscing elit. Hac ad pharetra bibendum cursus ac eget odio. Est diam senectus cursus vestibulum curae imperdiet adipiscing. Litora blandit proin lobortis etiam metus dapibus laoreet. Augue non fames sit est mus placerat ad cursus. Taciti penatibus elit accumsan dictumst ipsum. Potenti eros ultricies scelerisque sollicitudin eleifend bibendum parturient phasellus. Molestie natoque et per; fusce egestas urna. Porta elementum vestibulum tempus cubilia scelerisque tempor elit.</p>
<p>Lorem ipsum odor amet, consectetuer adipiscing elit. Hac ad pharetra bibendum cursus ac eget odio. Est diam senectus cursus vestibulum curae imperdiet adipiscing. Litora blandit proin lobortis etiam metus dapibus laoreet. Augue non fames sit est mus placerat ad cursus. Taciti penatibus elit accumsan dictumst ipsum. Potenti eros ultricies scelerisque sollicitudin eleifend bibendum parturient phasellus. Molestie natoque et per; fusce egestas urna. Porta elementum vestibulum tempus cubilia scelerisque tempor elit.</p>
<p>Lorem ipsum odor amet, consectetuer adipiscing elit. Hac ad pharetra bibendum cursus ac eget odio. Est diam senectus cursus vestibulum curae imperdiet adipiscing. Litora blandit proin lobortis etiam metus dapibus laoreet. Augue non fames sit est mus placerat ad cursus. Taciti penatibus elit accumsan dictumst ipsum. Potenti eros ultricies scelerisque sollicitudin eleifend bibendum parturient phasellus. Molestie natoque et per; fusce egestas urna. Porta elementum vestibulum tempus cubilia scelerisque tempor elit.</p>

</body>
</html>
"""


@tool(args_schema=HTMLBody)
def deploy(html: str):
    """
    Deploy a HTML page to a server
    """
    CONN.sudo("apt-get update -y")
    CONN.sudo("apt install nginx -y")
    CONN.run(f'''echo "{html}" | sudo tee /var/www/html/index.nginx-debian.html''')
    CONN.run("sudo systemctl is -active --quiet nginx && sudo systemctl restart nginx || sudo systemctl start nginx")
    return "Deployed and completed the task."


@tool
def create_carla_data_generator(html: str):
    """
    Create a Carla data generator
    """
    return "Trigger ID - C1"

# Langchain RAG settings
AGENT = None
# Embedding function
# Prompt
_PROMPT = hub.pull("age-house")
# Tools and function calling
_TOOLS = [
    create_a_html_page, deploy, create_carla_data_generator,
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
