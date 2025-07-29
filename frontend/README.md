# 3GPP Chat Bot - Frontend

This is the React frontend for the 3GPP Chat Bot application. It provides an interactive web interface for querying 3GPP technical documents and visualizing semantic graphs.

## 🚀 Features

- **Interactive Graph Visualization**: Powered by D3.js for dynamic network graphs
- **Real-time Chat Interface**: Query the knowledge base with natural language
- **Responsive Design**: Works on desktop and mobile devices
- **Node Highlighting**: Visual feedback for search results
- **Modern UI**: Clean, intuitive interface

## 🛠️ Tech Stack

- **React 19.1.0** - Modern React with hooks
- **D3.js 7.9.0** - Data visualization library
- **CSS3** - Styling and animations
- **Fetch API** - HTTP requests to backend

## 📦 Installation

```bash
# Install dependencies
npm install

# Start development server
npm start
```

The application will be available at `http://localhost:3000`

## 🏗️ Project Structure

```
frontend/
├── public/           # Static assets
├── src/
│   ├── App.js       # Main application component
│   ├── Chat.js      # Chat interface component
│   ├── Graph.js     # Graph visualization component
│   └── index.js     # Application entry point
└── package.json     # Dependencies and scripts
```

## 🔧 Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from Create React App (one-way operation)

## 🔌 API Integration

The frontend communicates with the Flask backend API:

- **Endpoint**: `http://localhost:5000/api/query`
- **Method**: POST
- **Data**: `{ query: "user question" }`
- **Response**: `{ answer: "bot response", highlight: [node_ids] }`

## 🎨 Customization

### Styling
- Modify `App.css` for global styles
- Component-specific styles are inline for simplicity

### Graph Visualization
- Graph settings are in `Graph.js`
- Node colors and sizes can be customized
- Layout parameters can be adjusted

## 🚀 Deployment

```bash
# Build for production
npm run build

# The build folder contains the production-ready files
```

## 🤝 Contributing

1. Follow the existing code style
2. Test your changes thoroughly
3. Ensure the graph visualization works correctly
4. Update documentation if needed

## 📞 Support

For frontend-specific issues, please check the main project README or open an issue on GitHub.
