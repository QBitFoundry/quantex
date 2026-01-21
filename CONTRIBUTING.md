# 🧩 Contributing to Quantex

Thank you for your interest in contributing to **Quantex** — a next-generation open-source code editor built with **Python**, **PyQt6**, and **QScintilla**.  
We’re thrilled to have you join the community! 💻✨

---

## 🧰 Getting Started

### 1. Fork the repository
Click the **Fork** button at the top-right of the [main repository](https://github.com/QBitFoundry/quantex).  
This creates your own copy where you can make changes freely.

### 2. Clone your fork
```bash
git clone https://github.com/YOUR_USERNAME/quantex.git
cd quantex
```

### 3. Set up your environment

We recommend using a virtual environment to isolate dependencies:

```bash
python -m venv venv
# Activate on macOS/Linux
source venv/bin/activate
# Activate on Windows
venv\Scripts\activate
```

### 4. Install dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

---

## 🧠 Development Workflow

### 🔹 Create a new branch

Before making changes, create a new branch for your feature or fix:

```bash
git checkout -b feature/your-feature-name
```

Example:

```bash
git checkout -b feature/add-dark-theme
```

### 🔹 Make your changes

* Follow **PEP8** guidelines for Python code.
* Keep functions and classes well-documented.
* Make UI changes visually consistent with the editor’s design.

### 🔹 Test your changes

If possible, write or update tests in the `tests/` directory:

```bash
pytest
```

### 🔹 Commit your changes

Use clear and descriptive commit messages:

```bash
git add .
git commit -m "Added dark theme support"
```

### 🔹 Push your branch

```bash
git push origin feature/add-dark-theme
```

### 🔹 Submit a Pull Request (PR)

Go to your fork on GitHub and click:  
**“Compare & pull request” → Create pull request** ✅

---

## 🧭 Code Guidelines

* Follow [PEP8](https://peps.python.org/pep-0008/) for Python code.
* Use meaningful variable and function names.
* Keep UI elements modular — prefer reusable PyQt widgets.
* Avoid committing build or binary files (`.exe`, `.dmg`, `.AppImage`, etc.).
* Add docstrings (`"""Describe function purpose"""`) for all functions and classes.

---

## 🧩 Directory Overview

```
quantex/
├── quantex/          # Source code
├── tests/            # Unit tests
├── docs/             # Documentation and screenshots
├── assets/           # Icons, logos, and static resources
├── themes/           # Syntax highlighting and color themes
├── README.md         # Project overview
├── LICENSE           # Open-source license
└── CONTRIBUTING.md   # You're reading this file!
```

---

## 🧪 Reporting Bugs & Requesting Features

### 🐞 Reporting Bugs

If you find a bug, please open an [Issue](https://github.com/QBitFoundry/quantex/issues) and include:

* Clear title and detailed description  
* Steps to reproduce  
* Screenshots (if UI-related)  
* System info (OS, Python version, etc.)

### 💡 Requesting Features

To suggest a new feature, open an **Issue** and label it as `feature-request`.  
Describe what you’d like to see, why it’s useful, and any relevant examples.

---

## 💬 Community Guidelines

We believe in an inclusive, respectful, and collaborative community.  
Please:

* Be kind and constructive in discussions.  
* Give credit where it’s due.  
* Respect different perspectives — creativity thrives in diversity.  
* Follow GitHub’s [Community Guidelines](https://docs.github.com/en/site-policy/github-terms/github-community-guidelines).

---

## ❤️ Acknowledgments

Thanks to every contributor who helps make **Quantex** a powerful, open, and beautiful code editor.  
Your support shapes the future of coding tools for everyone!

> “Open source is not just code — it’s collaboration.” 🌍

---

**Happy coding, and welcome to the Quantex community!**
