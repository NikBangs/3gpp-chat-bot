# 3GPP Chat Bot

A sophisticated chat bot application that analyzes 3GPP technical documents and provides intelligent responses about changes, specifications, and technical details through an interactive graph-based interface.

## 🚀 Features

- **Document Analysis**: Processes 3GPP technical documents (.doc, .docx)
- **Semantic Graph**: Creates interactive knowledge graphs from document content
- **AI-Powered Chat**: Uses OpenAI GPT for intelligent responses with caching
- **Visual Interface**: React-based frontend with interactive graph visualization
- **Change Tracking**: Identifies and highlights changes between document versions
- **Smart Caching**: Fuzzy matching for similar queries to improve response times
- **Responsive Design**: Modern UI with real-time chat and graph interaction

## 🏗️ Architecture

```
3GPP Chat Bot/
├── backend/           # Flask API server with caching and AI integration
├── frontend/          # React web application with graph visualization
├── graph_builder/     # Document processing and graph generation
├── data/             # Document storage and generated graphs
└── lib/              # Shared libraries and assets
```

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- OpenAI API key
- Windows (for .doc file processing with pywin32)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/NikBangs/3gpp-chat-bot.git
cd 3gpp-chat-bot
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Set Up Frontend
```bash
cd frontend
npm install
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

## 🚀 Usage

### Starting the Backend
```bash
# From the root directory
cd backend
python app.py
```
The Flask server will start on `http://localhost:5000`

### Starting the Frontend
```bash
# From the frontend directory
cd frontend
npm start
```
The React app will start on `http://localhost:8080`

### Processing Documents
```bash
# From the root directory
cd graph_builder
python main.py
```

### GUI Graph Viewer
```bash
# From the graph_builder directory
cd ui
python run_graph_gui.py
```

## 📁 Project Structure

### Backend (`backend/`)
- `app.py` - Flask API server with search, query endpoints, and intelligent caching
- `cache_gpt_responses.json` - Cached responses for improved performance

### Frontend (`frontend/`)
- `src/App.js` - Main React application component
- `src/Chat.js` - Chat interface component
- `src/Graph.js` - Interactive graph visualization component
- `src/index.css` - Application styling

### Graph Builder (`graph_builder/`)
- `main.py` - Main document processing pipeline
- `parser/` - Document parsing and section splitting
  - `read_doc.py` - Document reading for .doc and .docx files
  - `split_sections.py` - Section extraction and structuring
- `graphs/` - Graph building, visualization, and analysis
  - `builder.py` - Semantic graph construction
  - `visualizer.py` - Graph visualization and HTML export
  - `traversals.py` - Graph traversal and impact analysis
  - `summarizer.py` - User-friendly summary generation
  - `summarize_nodes.py` - GPT-powered node summarization
- `ui/` - Desktop GUI for graph viewing
- `test_graph.py` - Graph testing and inspection utilities

### Data (`data/`)
- Document storage (3GPP .doc/.docx files)
- Generated graph files (.pkl)
- Visualization outputs (HTML)
- Change tracking data (JSON)

## 🔧 Configuration

### Document Processing
Place your 3GPP documents in the `data/` directory:
- Supported formats: `.doc`, `.docx`
- Documents are automatically processed and converted to semantic graphs
- Change detection between document versions

### API Configuration
- OpenAI API key required for advanced chat features
- Intelligent caching system for improved response times
- Fuzzy matching for similar queries

### Performance Optimizations
- Response caching with LRU eviction (max 50 entries)
- Semantic similarity matching for cache hits
- Optimized graph loading and processing

## 🎯 Key Features

### Smart Caching System
- Fuzzy matching for similar queries (85% similarity threshold)
- Automatic cache management with size limits
- Improved response times for repeated queries

### Interactive Graph Visualization
- Real-time graph rendering with D3.js
- Node highlighting based on query relevance
- Responsive design for different screen sizes

### Document Analysis
- Automatic section extraction and structuring
- Change detection between document versions
- Semantic similarity analysis for content comparison

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- 3GPP for technical specifications
- OpenAI for GPT integration
- React and Flask communities
- NetworkX for graph processing
- Sentence Transformers for semantic similarity

## 📞 Support

For support and questions, please open an issue on GitHub or contact the development team.

## 🔄 Recent Updates

- **Code Cleanup**: Removed unused imports and dependencies
- **Performance Optimization**: Improved caching system and response times
- **UI Improvements**: Cleaner React components and styling
- **Documentation**: Enhanced README with detailed project structure 