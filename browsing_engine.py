import webbrowser
import requests
from bs4 import BeautifulSoup
from ai_brain import get_ai_response


def search_google(query):
    """Opens a Google search for the query."""
    if not query:
        return "Sir, you didn't specify what to search for."
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Searching Google for: {query}."


def search_youtube(query):
    """Opens a YouTube search for the query."""
    if not query:
        return "Sir, you didn't specify what to search for on YouTube."
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Searching YouTube for: {query}."


def play_on_youtube(query):
    """Opens YouTube search for the query (closest to 'playing' without automation)."""
    if not query:
        return "Sir, what would you like me to play on YouTube?"
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Opening YouTube to play: {query}. Select your track, Sir."


def open_link(url):
    """Opens a specific URL in the default browser."""
    if not url:
        return "Sir, no URL was provided."
    # Ensure it has a scheme
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    webbrowser.open(url)
    return f"Opening link: {url}"


def read_news():
    """Opens Google News in the browser."""
    webbrowser.open("https://news.google.com")
    return "Opening Google News for you, Sir."


def get_page_content(url):
    """Scrapes the text content and title of a webpage."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for script in soup(["script", "style"]):
            script.extract()
            
        title = soup.title.string if soup.title else "No Title Found"
        text = soup.get_text()
        
        lines  = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text   = '\n'.join(chunk for chunk in chunks if chunk)
        
        return {"title": title, "content": text[:2000]}
    except Exception as e:
        return {"error": str(e)}


def summarize_webpage(url):
    """Scrapes a webpage and uses AI to summarize it."""
    data = get_page_content(url)
    if "error" in data:
        return f"I couldn't reach the webpage, Sir. Error: {data['error']}"
    
    prompt = f"Please summarize the following webpage content (Title: {data['title']}):\n\n{data['content']}"
    summary = get_ai_response(prompt)
    return f"Summary of '{data['title']}':\n{summary}"


def summarize_article(url=None):
    """Summarizes the article at the given URL, or asks user to provide one."""
    if not url:
        return "Sir, please provide the article URL. For example: 'Jarvis summarize this article https://example.com'"
    return summarize_webpage(url)


if __name__ == "__main__":
    pass
