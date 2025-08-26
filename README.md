# 🤖 TalentScout Hiring Assistant

An AI-powered intelligent hiring assistant chatbot designed for initial candidate screening in technology recruitment. This application automates the preliminary interview process by gathering candidate information and conducting technical assessments based on their declared tech stack.

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [Database Schema](#database-schema)
- [Prompt Engineering](#prompt-engineering)
- [Architecture](#architecture)
- [Challenges & Solutions](#challenges--solutions)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Project Overview

TalentScout is an intelligent hiring assistant that streamlines the initial candidate screening process for technology positions. The system uses Large Language Models (LLMs) to generate contextual technical questions based on candidates' declared skill sets and provides an intuitive interface for both candidates and recruiters.

### Purpose
- **Automate Initial Screening**: Reduce manual effort in preliminary candidate assessment
- **Personalized Technical Assessment**: Generate relevant questions based on candidate's tech stack
- **Consistent Evaluation**: Standardize the screening process across all candidates
- **Data Collection**: Systematically gather and store candidate information for further review

## ✨ Features

### Core Functionality
- **🖐️ Interactive Greeting**: Welcome candidates and explain the screening process
- **📝 Information Collection**: Systematic gathering of candidate details including:
  - Full Name
  - Email Address
  - Phone Number
  - Years of Experience
  - Desired Position
  - Current Location
  - Technical Skills & Stack
- **🧠 Dynamic Question Generation**: AI-powered technical questions tailored to candidate's tech stack
- **📊 Real-time Assessment**: Immediate feedback on technical responses
- **💾 Data Persistence**: Secure storage of candidate information and responses
- **📈 Performance Analytics**: Score calculation and performance insights

### User Experience
- **🎨 Clean Interface**: Intuitive Streamlit-based UI
- **📱 Responsive Design**: Works across different screen sizes
- **🔄 Progress Tracking**: Visual indicators for assessment progress
- **⚡ Real-time Feedback**: Immediate response validation
- **🔐 Data Privacy**: Secure handling of candidate information

### Administrative Features
- **📊 Dashboard**: Real-time statistics and candidate metrics
- **📋 Candidate Management**: View and manage candidate records
- **🔍 Response Analysis**: Review technical responses and assessments
- **📈 Performance Reports**: Generate screening performance reports

## 🛠 Technology Stack

### Core Technologies
- **Python 3.8+**: Primary programming language
- **Streamlit**: Frontend framework for web interface
- **LangChain**: LLM integration and prompt management
- **Ollama**: Local LLM deployment (Llama 3)
- **SQLite**: Lightweight database for data persistence

### Libraries & Dependencies
```
streamlit>=1.28.0
langchain-ollama>=0.1.0
sqlite3 (built-in)
re (built-in)
json (built-in)
datetime (built-in)
```

### AI/ML Components
- **Large Language Model**: Llama 3 via Ollama
- **Prompt Engineering**: Custom prompts for question generation
- **Natural Language Processing**: Regex-based parsing and extraction

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Ollama installed and running
- Git (for cloning the repository)

### Step 1: Clone the Repository
```bash
git clone https://github.com/mohit26061999/talentscout-hiring-assistant.git
cd talentscout-hiring-assistant
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install streamlit langchain-ollama
```

### Step 4: Setup Ollama and Llama 3
```bash
# Install Ollama (visit https://ollama.ai for installation instructions)

# Pull Llama 3 model
ollama pull llama3

# Verify installation
ollama list
```

### Step 5: Initialize Database
```bash
# Run the migration script (if needed)
python migrate_db.py
```

### Step 6: Run the Application
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 📖 Usage Guide

### For Candidates

1. **Start Assessment**: Open the application and read the welcome message
2. **Provide Information**: Fill out the candidate information form with:
   - Personal details (name, email, phone)
   - Professional information (experience, desired position, location)
   - Technical skills and stack
3. **Technical Assessment**: Answer the generated multiple-choice questions
4. **Review Results**: View your performance score and feedback
5. **Completion**: Receive information about next steps

### For Administrators

1. **Monitor Progress**: Use the sidebar admin panel to track candidates
2. **View Statistics**: Check total candidates and response metrics
3. **Review Responses**: Access detailed candidate responses and assessments
4. **Manage Data**: Export or analyze candidate data as needed

### Sample Interaction Flow
```
1. Candidate opens application
2. System displays greeting and overview
3. Candidate completes information form
4. System generates 5 technical MCQs based on tech stack
5. Candidate answers questions with immediate feedback
6. System calculates score and provides performance insights
7. Candidate receives next steps information
```

## 🗄️ Database Schema

### Candidates Table
```sql
CREATE TABLE candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    email TEXT,
    phone TEXT,
    experience INTEGER,
    position TEXT,
    location TEXT,
    tech_stack TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Answers Table
```sql
CREATE TABLE answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id INTEGER,
    question TEXT,
    user_answer TEXT,
    correct_answer TEXT,
    is_correct BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(candidate_id) REFERENCES candidates(id)
);
```

## 🎨 Prompt Engineering

### Question Generation Prompt
The system uses carefully crafted prompts to generate relevant technical questions:

```python
prompt_mcq = f"""
Generate exactly 5 multiple-choice technical questions for a candidate with experience in: {tech_stack}

Use this EXACT format for each question:
Question 1: [Your question here]
A) Option A
B) Option B  
C) Option C
D) Option D
Answer: A

Make questions practical and relevant to the technologies mentioned.
"""
```

### Key Prompt Design Principles
- **Specificity**: Clear instructions for exact formatting
- **Context Awareness**: Incorporate candidate's tech stack
- **Consistency**: Standardized question structure
- **Relevance**: Focus on practical, job-relevant scenarios
- **Difficulty Scaling**: Appropriate for declared experience level

## 🏗️ Architecture

### System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │────│  Python Backend │────│   SQLite DB     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                         ┌─────────────────┐
                         │   Ollama LLM    │
                         └─────────────────┘
```

### Component Breakdown

1. **Frontend (Streamlit)**
   - User interface and interaction handling
   - Form processing and validation
   - Real-time updates and progress tracking

2. **Backend (Python)**
   - Business logic and data processing
   - LLM integration and prompt management
   - Database operations and data validation

3. **Database (SQLite)**
   - Candidate information storage
   - Response tracking and analytics
   - Session management

4. **AI Layer (Ollama + Llama 3)**
   - Question generation based on tech stack
   - Natural language processing
   - Response evaluation

### Data Flow
```
User Input → Streamlit → Python Logic → LLM Processing → Database Storage
                ↓              ↓              ↓              ↓
         UI Updates ← Response ← Generated Q's ← Stored Data
```

## 🧩 Challenges & Solutions

### Challenge 1: LLM Response Consistency
**Problem**: LLM-generated questions had inconsistent formatting
**Solution**: 
- Implemented regex-based parsing with multiple patterns
- Created fallback question bank for parsing failures
- Added response validation and cleaning

### Challenge 2: Database Schema Evolution
**Problem**: Adding new features required database schema changes
**Solution**:
- Implemented automatic schema migration
- Added backward compatibility checks
- Created safe database operation wrappers

### Challenge 3: Session State Management
**Problem**: Streamlit session state complexities with form resubmission
**Solution**:
- Structured session state initialization
- Implemented proper state reset mechanisms
- Added progress tracking across different phases

### Challenge 4: Error Handling
**Problem**: Various failure points (LLM, database, parsing)
**Solution**:
- Comprehensive try-catch blocks
- Graceful degradation with fallbacks
- User-friendly error messages

### Challenge 5: Question Quality Assurance
**Problem**: Ensuring generated questions are relevant and accurate
**Solution**:
- Refined prompt engineering with specific instructions
- Implemented question validation logic
- Created curated fallback questions for each tech stack

## 🔮 Future Enhancements

### Planned Features
- **🌐 Multilingual Support**: Support for multiple languages
- **💬 Conversational Interface**: Full chat-based interaction
- **📊 Advanced Analytics**: Detailed performance dashboards
- **🔐 User Authentication**: Secure login system
- **📧 Email Integration**: Automated notifications
- **🎯 Custom Question Banks**: Admin-configurable question sets
- **📱 Mobile App**: Native mobile application
- **🤖 AI Interviewer**: Voice-based interview capabilities

### Technical Improvements
- **☁️ Cloud Deployment**: AWS/GCP deployment
- **🔄 Real-time Sync**: Multi-user real-time capabilities
- **📈 Performance Optimization**: Response time improvements
- **🛡️ Enhanced Security**: Advanced data protection
- **📊 Reporting System**: Comprehensive reporting tools

### Contribution Guidelines
- Follow Python PEP 8 style guidelines
- Add comments for complex logic
- Include tests for new features
- Update documentation as needed
- Ensure backward compatibility

### Areas for Contribution
- 🐛 Bug fixes and improvements
- ✨ New features and enhancements
- 📚 Documentation improvements
- 🧪 Test coverage expansion
- 🎨 UI/UX improvements


## 📞 Contact & Support

- **Project Maintainer**: Mohit Kumar
- **Email**: mk079823@gmail.com
- **GitHub**: https://github.com/mohit26061999

## 🙏 Acknowledgments

- **Ollama Team** for providing excellent local LLM capabilities
- **Streamlit** for the intuitive web framework
- **LangChain** for LLM integration tools
- **Meta AI** for the Llama 3 model
- **Open Source Community** for continuous inspiration and support

