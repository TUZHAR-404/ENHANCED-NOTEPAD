# 🎙️ Enhanced Notepad with Audio & 3D Visualization

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Platform-Windows-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen.svg" alt="Status">
</div>

<p align="center">
  <strong>A modern, feature-rich notepad application with speech recognition, text-to-speech, and stunning 3D visualizations.</strong>
</p>

## ✨ Features

### 📝 Core Text Editor
- **Modern Interface**: Built with CustomTkinter for a sleek, contemporary look
- **File Operations**: Create, open, save, and manage text files with ease
- **Standard Editing**: Cut, copy, paste functionality with keyboard shortcuts
- **Cross-Platform**: Designed for Windows with potential for multi-platform support

### 🎤 Speech Recognition
- **Real-time Speech-to-Text**: Convert your voice to text instantly
- **Configurable Microphone**: Select from available input devices
- **Adjustable Sensitivity**: Fine-tune recognition sensitivity (50-1000 range)
- **Background Processing**: Non-blocking speech recognition with threading

### 🔊 Text-to-Speech
- **Natural Voice Output**: Read your text aloud with customizable voices
- **Voice Selection**: Choose from available system voices
- **Adjustable Settings**: Control volume (0-100%) and speech rate (50-300 WPM)
- **Interrupt Control**: Start and stop reading at any time

### 🎨 3D Visualization
- **Animated Sphere**: Beautiful rotating 3D sphere with RGB color mapping
- **Real-time Animation**: Smooth 60 FPS animation using matplotlib
- **Toggle Control**: Enable/disable visualization as needed
- **Mathematical Precision**: Parametric sphere generation with numpy

### ⚙️ Advanced Settings
- **Audio Configuration**: Comprehensive audio settings panel
- **Device Management**: Automatic detection and selection of audio devices
- **Persistent Settings**: Settings are maintained across sessions
- **Status Updates**: Real-time status bar for user feedback

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Windows OS (recommended)
- Working microphone and speakers

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/enhanced-notepad-collaboration.git
cd enhanced-notepad-collaboration
```

### Step 2: Create Virtual Environment
```bash
python -m venv collab_env
collab_env\Scripts\activate  # On Windows
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python aigui2.py
```

## 📦 Dependencies

| Package | Purpose | Version |
|---------|---------|---------|
| `customtkinter` | Modern UI framework | Latest |
| `pyttsx3` | Text-to-speech engine | Latest |
| `pyaudio` | Audio input/output | Latest |
| `SpeechRecognition` | Speech-to-text processing | Latest |
| `numpy` | Mathematical operations | Latest |
| `matplotlib` | 3D visualization | Latest |

## 🎯 Usage

### Basic Text Editing
1. **New File**: `Ctrl+N` or File → New
2. **Open File**: `Ctrl+O` or File → Open
3. **Save File**: `Ctrl+S` or File → Save
4. **Text Operations**: Use standard `Ctrl+X`, `Ctrl+C`, `Ctrl+V`

### Speech Features
1. **Start Dictation**: Click the 🎤 button or use Audio → Speech to Text
2. **Stop Listening**: Click ⏹ Stop Listening button
3. **Read Aloud**: Click 🔊 button or Audio → Read Aloud
4. **Stop Reading**: Click ⏹ Stop Reading button

### 3D Visualization
- The 3D sphere appears in the right panel when activated
- Features a rotating sphere with dynamic RGB coloring
- Can be toggled on/off through the interface

### Audio Settings
- Access via Audio → Audio Settings
- Configure microphone sensitivity
- Select input/output devices
- Adjust voice parameters

## 🏗️ Architecture

```
Enhanced Notepad
├── Core Components
│   ├── NotepadApp (Main Application Class)
│   ├── GUI Framework (CustomTkinter)
│   └── Event Handling (Tkinter)
├── Audio Processing
│   ├── Speech Recognition (SpeechRecognition + PyAudio)
│   ├── Text-to-Speech (pyttsx3)
│   └── Device Management
├── Visualization
│   ├── 3D Rendering (matplotlib)
│   ├── Animation System (FuncAnimation)
│   └── Mathematical Modeling (numpy)
└── File Operations
    ├── Standard I/O Operations
    ├── File Dialog Integration
    └── Error Handling
```

## 🛠️ Technical Details

### Speech Processing
- Uses Google's Speech Recognition API
- Supports multiple microphone inputs
- Implements noise reduction and energy threshold filtering
- Threaded processing to prevent UI blocking

### 3D Visualization
- Parametric sphere generation: `x = cos(u)sin(v)`, `y = sin(u)sin(v)`, `z = cos(v)`
- RGB color mapping based on 3D coordinates
- Smooth rotation animation with configurable frame rates
- Memory-efficient rendering with matplotlib backend

### Audio Engine
- Cross-platform TTS engine support
- Dynamic voice enumeration and selection
- Real-time audio parameter adjustment
- Comprehensive error handling and device fallback

## 🎨 Screenshots

*Coming Soon - Screenshots will be added to showcase the modern interface and 3D visualization features.*

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the Repository**
2. **Create a Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Commit Changes**: `git commit -m 'Add amazing feature'`
4. **Push to Branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to new functions
- Test on Windows environment
- Ensure compatibility with Python 3.8+

## 🐛 Known Issues

- **macOS/Linux**: Limited testing on non-Windows platforms
- **Audio Drivers**: Some audio devices may require additional drivers
- **Performance**: 3D visualization may impact performance on older hardware

## 📋 Roadmap

- [ ] **Dark/Light Theme Toggle**
- [ ] **Plugin System Architecture**
- [ ] **Cloud Storage Integration**
- [ ] **Real-time Collaboration**
- [ ] **Advanced Text Formatting**
- [ ] **Custom Voice Training**
- [ ] **Multi-language Support**
- [ ] **Mobile App Version**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CustomTkinter**: For the modern UI framework
- **pyttsx3**: For reliable text-to-speech functionality
- **SpeechRecognition**: For robust speech processing
- **matplotlib**: For powerful 3D visualization capabilities
- **numpy**: For efficient mathematical operations

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](../../issues) section
2. Create a new issue with detailed description
3. Contact the development team

---

<div align="center">
  <p>Made with ❤️ by the Enhanced Notepad Team</p>
  <p>⭐ Star this repository if you found it helpful!</p>
</div>