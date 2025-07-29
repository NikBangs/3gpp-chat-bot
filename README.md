# 3GPP Chat Bot

A sophisticated chat bot application that analyzes 3GPP technical documents and provides intelligent responses about changes, specifications, and technical details through an interactive graph-based interface.

## 🚀 Features

- **Document Analysis**: Processes 3GPP technical documents (.doc, .docx)
- **Semantic Graph**: Creates interactive knowledge graphs from document content
- **AI-Powered Chat**: Uses OpenAI GPT for intelligent responses
- **Visual Interface**: React-based frontend with interactive graph visualization
- **Change Tracking**: Identifies and highlights changes between document versions
- **Search & Query**: Advanced search capabilities with TF-IDF and semantic similarity

## 🏗️ Architecture

```
3GPP Chat Bot/
├── backend/           # Flask API server
├── frontend/          # React web application
├── graph_builder/     # Document processing and graph generation
├── data/             # Document storage and generated graphs
└── lib/              # Shared libraries and assets
```

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- OpenAI API key
- Windows (for .doc file processing)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/3gpp-chat-bot.git
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
The React app will start on `http://localhost:3000`

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
- `app.py` - Flask API server with search and query endpoints

### Frontend (`frontend/`)
- React application with interactive graph visualization
- Chat interface for querying the knowledge base

### Graph Builder (`graph_builder/`)
- `main.py` - Main document processing pipeline
- `parser/` - Document parsing and section splitting
- `graphs/` - Graph building, visualization, and analysis
- `ui/` - Desktop GUI for graph viewing

### Data (`data/`)
- Document storage
- Generated graph files
- Visualization outputs

## 🔧 Configuration

### Document Processing
Place your 3GPP documents in the `data/` directory:
- Supported formats: `.doc`, `.docx`
- Documents are automatically processed and converted to semantic graphs

### API Configuration
- OpenAI API key required for advanced chat features
- TF-IDF search available without API key

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

## 📞 Support

For support and questions, please open an issue on GitHub or contact the development team. 