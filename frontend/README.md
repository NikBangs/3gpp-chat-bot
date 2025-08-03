# 3GPP Chat Bot Frontend

A modern React-based frontend for the 3GPP Chat Bot application, providing an interactive interface to query 3GPP specifications and visualize knowledge graphs.

## 🚀 Features

- **Interactive Chat Interface**: Real-time chat with the 3GPP knowledge base
- **Graph Visualization**: Interactive knowledge graph display using iframe integration
- **Markdown Support**: Rich text rendering for responses
- **Responsive Design**: Modern UI built with Tailwind CSS and Radix UI
- **Real-time Updates**: Live highlighting of relevant graph nodes

## 🛠️ Tech Stack

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **UI Components**: Radix UI
- **Icons**: Lucide React
- **Markdown**: Marked
- **Routing**: React Router DOM
- **State Management**: React Query

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatPanel.tsx      # Chat interface component
│   │   ├── GraphPanel.tsx     # Graph visualization component
│   │   └── ui/               # Reusable UI components
│   ├── pages/
│   │   └── Index.tsx         # Main application page
│   ├── lib/
│   │   └── utils.ts          # Utility functions
│   ├── App.tsx               # Main application component
│   ├── main.tsx              # Application entry point
│   └── index.css             # Global styles
├── public/
│   └── data/
│       └── graph.html        # Graph visualization file
├── package.json
├── vite.config.ts
└── tailwind.config.ts
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend server running on `http://localhost:5000`

### Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Start development server**:
   ```bash
   npm run dev
   ```

3. **Open your browser**:
   Navigate to `http://localhost:5000` (or the port shown in terminal)

### Build for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## 🔧 Configuration

### Backend API

The frontend connects to the backend API at `http://localhost:5000`. Make sure your backend server is running before starting the frontend.

### Graph Visualization

The graph visualization is loaded from `/public/data/graph.html`. Ensure this file exists and contains a valid PyVis network visualization.

## 📝 Usage

1. **Start the application** and you'll see a split-screen interface
2. **Left panel**: Interactive knowledge graph visualization
3. **Right panel**: Chat interface for querying 3GPP specifications
4. **Ask questions** about 3GPP specifications, changes, or procedures
5. **View highlights** on the graph as relevant nodes are automatically highlighted

## 🎨 Customization

### Styling

The application uses Tailwind CSS for styling. You can customize the appearance by modifying:
- `src/index.css` - Global styles
- Component-specific CSS classes in each component

### Components

The main components can be customized:
- `ChatPanel.tsx` - Chat interface styling and behavior
- `GraphPanel.tsx` - Graph visualization integration
- `Index.tsx` - Main page layout and state management

## 🔍 Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Code Structure

- **TypeScript**: Full type safety throughout the application
- **Component-based**: Modular, reusable components
- **Hooks**: Custom React hooks for state management
- **Error Handling**: Comprehensive error handling and user feedback

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the 3GPP Chat Bot application.

## 🔗 Related

- [Backend API](../backend/) - Flask backend server
- [Graph Builder](../graph_builder/) - Knowledge graph generation tools 