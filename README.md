# 🤖 AI Code Review Agent

An intelligent multi-agent AI system that analyzes source code, detects potential bugs and security vulnerabilities, identifies performance and code-quality issues, and automatically generates improved code.

## 🚀 Project Overview

The AI Code Review Agent uses a multi-agent architecture where specialized AI agents independently analyze submitted source code.

The system provides:

- 🐞 Bug detection
- 🔐 Security vulnerability detection
- ⚡ Performance analysis
- 🧹 Code quality analysis
- 🤖 AI-powered auto-fix
- 📊 Code health score
- ⚠️ Risk level assessment
- 🔄 Before vs After code comparison
- 💡 Recommendations for improvement

## 🏗️ System Architecture

```text
                 User
                   │
                   ▼
             Web Interface
                   │
                   ▼
              FastAPI API
                   │
                   ▼
             LangGraph
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
   Bug Agent   Security    Performance
                Agent         Agent
       │           │           │
       └───────────┼───────────┘
                   ▼
              Quality Agent
                   │
                   ▼
             Deduplication
                   │
                   ▼
             Final Report
                   │
          ┌────────┴────────┐
          ▼                 ▼
     AI Findings        AI Auto-Fix
                            │
                            ▼
                     Improved Code