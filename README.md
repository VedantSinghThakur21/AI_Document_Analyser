# AI Document Analyzer

A modern, AI-powered document analysis tool with a beautiful frontend and robust backend.

## 🌟 Features

- **Smart PDF Analysis**: Extract text, generate summaries, and identify named entities
- **Modern UI/UX**: Responsive design with dark/light mode toggle
- **Drag & Drop**: Intuitive file upload with progress indicators
- **Real-time Processing**: Live analysis with instant results
- **Free Hosting**: Deployed on GitHub Pages (zero cost)
- **AWS Integration**: Backend hosted on EC2 with S3 storage

## 🚀 Live Demo

Visit: **[https://vedantsinghthakur21.github.io/AI_Document_Analyser/](https://vedantsinghthakur21.github.io/AI_Document_Analyser/)**

## 🛠 Tech Stack

### Frontend
- **HTML5/CSS3**: Modern responsive design
- **Vanilla JavaScript**: No framework dependencies
- **GitHub Pages**: Free static hosting
- **Font Awesome**: Professional icons
- **Google Fonts**: Beautiful typography

### Backend
- **FastAPI**: High-performance Python web framework
- **NLTK**: Natural language processing
- **PDFPlumber**: PDF text extraction
- **AWS EC2**: Server hosting
- **AWS S3**: File storage

## 📱 Features

### ✨ Modern Design
- Clean, professional interface
- Dark/light mode toggle
- Smooth animations and transitions
- Mobile-responsive design
- Drag & drop file upload

### 🧠 AI Analysis
- Text summarization using extractive methods
- Named entity recognition
- Document statistics (word count, readability)
- Downloadable analysis reports

### 🔒 Secure & Scalable
- CORS-enabled API
- File validation and size limits
- Error handling and user feedback
- AWS free tier optimized

## 🎯 Free Tier Compliance

- **GitHub Pages**: Free static hosting
- **AWS EC2**: t2.micro (750 hours/month free)
- **AWS S3**: 5GB storage free
- **No additional costs**: 100% free tier eligible

## 🚀 Quick Start

1. **Visit the live demo**: [AI Document Analyzer](https://vedantsinghthakur21.github.io/AI_Document_Analyser/)
2. **Upload a PDF**: Drag & drop or click to browse
3. **Get Results**: View summary, entities, and statistics
4. **Download Report**: Save analysis as JSON file

## 🔧 Development

### Local Development
```bash
# Clone repository
git clone https://github.com/VedantSinghThakur21/AI_Document_Analyser.git

# Open index.html in browser
# No build process required!
```

### Backend Setup
```bash
# SSH into EC2 instance
ssh -i "key.pem" ec2-user@your-ec2-ip

# Navigate to project
cd AI_Document_Analyser
source venv/bin/activate
cd backend

# Start server
uvicorn app:app --host 0.0.0.0 --port 8000
```

## 📊 API Endpoints

- **GET** `/` - Health check
- **POST** `/analyze` - Upload and analyze PDF

## 🎨 Design System

- **Primary Color**: #2563eb (Blue 600)
- **Accent Color**: #0ea5e9 (Sky 500)
- **Success Color**: #10b981 (Emerald 500)
- **Typography**: Inter font family
- **Layout**: Mobile-first responsive design

## 🔄 Deployment

### Automatic GitHub Pages Deployment
1. Push to `master` branch
2. GitHub automatically builds and deploys
3. Available at: `https://username.github.io/AI_Document_Analyser/`

## 📈 Performance

- **Lighthouse Score**: 95+ performance
- **Mobile Friendly**: 100% responsive
- **Fast Loading**: Optimized assets
- **SEO Ready**: Proper meta tags

## 🛡 Security

- File type validation (PDF only)
- File size limits (10MB max)
- CORS configuration
- Input sanitization

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- AWS Free Tier for hosting
- GitHub Pages for frontend deployment
- NLTK for NLP capabilities
- Font Awesome for icons
- Inter font family for typography