# eCOMET Chatbot

An AI-powered assistant for the [eCOMET](https://phytoecia.github.io/eCOMET/) R package (Eco-Metabolomics Toolkit).

**🔴 Live Demo**: [https://ecomet-chatbot.web.app](https://ecomet-chatbot.web.app)

This chatbot helps users troubleshoot installation issues, find function references, and generate code, snippets for metabolomics data analysis.

## Features
- **Knowledge Base**: Indexed with the full [eCOMET documentation](https://phytoecia.github.io/eCOMET/reference/index.html).
- **Dynamic Updates**: Automatically scrapes the documentation weekly to stay up-to-date.
- **Admin UI**: Password-protected dashboard for monitoring logs and updating the system persona.

## Links
- **Official eCOMET Package**: [https://phytoecia.github.io/eCOMET/](https://phytoecia.github.io/eCOMET/)
- **GitHub Repository**: [https://github.com/Phytoecia/ecomet-chatbot](https://github.com/Phytoecia/ecomet-chatbot)

## Tech Stack
- **Frontend**: Next.js 14, Tailwind CSS
- **Backend**: FastAPI, Google Gemini 2.5
- **Deployment**: Firebase Hosting (Frontend) + Cloud Run (Backend)
