# File: ./mcp_servers/text_server.py

from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
from dotenv import load_dotenv
import openai, os

load_dotenv()
client = openai.OpenAI()

# Initialize the MCP server with name "text"
mcp = FastMCP("text")

@mcp.tool()
async def summarize(text: str) -> list[TextContent]:
    """
    Summarize the input text

    Args:
        text: Input string to summarize.
    Returns:
        A list containing one TextContent object with the result.
    """
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a summarizer that summarizes that text to one-fourth of its original size. Example: If the text is 100 words long, you summarize it to around 25-30 words. If the text is already too small, you try to summarize it, but if you can't you output saying the text is too small to be summarized."},
            {"role": "user", "content": text}
        ]
    )
    return [TextContent(type='text', text=resp.choices[0].message.content.strip())]

@mcp.tool()
async def extract_keywords(text: str) -> list[TextContent]:
    """
    Extracts 5 to 10 keywords from the input text.

    Args:
        text: Input string to summarize.
    Returns:
        A list containing one TextContent object with the result.
    """
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Extract 5 to 10 keywords from the given text. If the text is too small, adjust the number of keywords you extract. Say if the text is 20 words long, try to extract 5 6 keywords if you can, if not provide atleast 2 to 3 keywords"},
            {"role": "user", "content": text}
        ]
    )
    return [TextContent(type='text', text=resp.choices[0].message.content.strip())]

@mcp.tool()
async def translate(text: str, language: str) -> list[TextContent]:
    """
    Translates the input text into the given language.

    Args:
        text: Input string to summarize.
    Returns:
        A list containing one TextContent object with the result.
    """
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"Translate the input text into {language}."},
            {"role": "user", "content": text}
        ]
    )
    return [TextContent(type='text', text=resp.choices[0].message.content.strip())]

if __name__ == "__main__":
    import asyncio
    asyncio.run(mcp.run(transport="stdio"))
