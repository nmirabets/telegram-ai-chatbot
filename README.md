# 🤖 Telegram AI Chatbot

An intelligent Telegram chatbot powered by OpenAI GPT-4o-mini with memory capabilities, web search, and Notion integration.

## ✨ Features

- **AI-Powered Conversations** — Natural language processing using OpenAI's GPT-4o-mini model
- **Persistent Memory** — Stores user preferences and context using Pinecone vector database
- **Web Search** — Real-time web search capabilities via Tavily API
- **Notion Integration** — Create pages directly in your Notion workspace from chat
- **Conversation History** — Maintains context throughout the conversation

## 📁 Project Structure

```
telegram-ai-chatbot/
├── main.py                 # Basic bot (starter template)
├── main_solution.py        # Full-featured bot with AI agent
├── agent/
│   ├── agent.py            # Main agent logic with tool calling
│   ├── tools.py            # Tool definitions & implementations
│   ├── prompts.py          # System prompt generation
│   └── notion_functions.py # Notion API integration
├── Telegram_Guide.ipynb    # Tutorial notebook
├── Notion_Integration.ipynb
├── Web_Search_agent.ipynb
└── README.md
```

## 🛠️ Prerequisites

- Python 3.8+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- OpenAI API Key
- Pinecone Account & API Key
- Tavily API Key
- Notion Integration Token & Database ID

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/telegram-ai-chatbot.git
   cd telegram-ai-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install python-telegram-bot openai pinecone-client tavily-python notion-client python-dotenv markdown-it-py
   ```

3. **Create a `.env` file** in the root directory:
   ```env
   # Telegram
   TELEGRAM_TOKEN=your_telegram_bot_token

   # OpenAI
   OPENAI_API_KEY=your_openai_api_key

   # Pinecone (Vector Database)
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_INDEX_NAME=your_index_name
   PINECONE_NAMESPACE=your_namespace
   EMBEDDING_MODEL=text-embedding-3-small
   EMBEDDING_DIMENSIONS=1536

   # Tavily (Web Search)
   TAVILY_API_KEY=your_tavily_api_key

   # Notion
   NOTION_API_KEY=your_notion_integration_token
   NOTION_DATABASE_ID=your_database_id
   ```

## 🎮 Usage

### Run the basic bot (starter template)
```bash
python main.py
```

### Run the full-featured AI bot
```bash
python main_solution.py
```

Once running, open Telegram and send `/start` to your bot to begin chatting!

## 🔧 Available Tools

The AI agent has access to the following tools:

| Tool | Description |
|------|-------------|
| `save_memory` | Saves user preferences to the vector database |
| `web_search` | Searches the web for real-time information |
| `create_notion_page` | Creates a new page in your Notion workspace |

## 📝 How It Works

1. **User sends a message** → Telegram forwards it to the bot
2. **System prompt is generated** with relevant memories from Pinecone
3. **GPT-4o-mini processes** the message and decides if tools are needed
4. **Tool execution** (if applicable): web search, save memory, or create Notion page
5. **Response sent** back to the user via Telegram

## 🔐 Setting Up External Services

### Telegram Bot
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow the prompts
3. Copy the API token to your `.env` file

### Pinecone
1. Create an account at [pinecone.io](https://www.pinecone.io/)
2. Create a new index with the appropriate dimensions (1536 for `text-embedding-3-small`)
3. Copy your API key and index name to `.env`

### Tavily
1. Sign up at [tavily.com](https://tavily.com/)
2. Get your API key from the dashboard

### Notion
1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Create a new integration and copy the token
3. Share a database with your integration and copy its ID

## 📚 Notebooks

- `Telegram_Guide.ipynb` — Step-by-step guide to building the Telegram bot
- `Notion_Integration.ipynb` — Learn how to integrate with Notion API
- `Web_Search_agent.ipynb` — Tutorial on adding web search capabilities

## 📄 License

MIT License — feel free to use this project for learning and building your own AI chatbots!
