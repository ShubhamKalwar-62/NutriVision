# Contributing to NutriVision

Thank you for your interest in contributing to NutriVision! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs
If you find a bug, please open an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- Screenshots (if applicable)
- Your environment (OS, Python version, etc.)

### Suggesting Enhancements
We love new ideas! Open an issue with:
- A clear description of the enhancement
- Why it would be useful
- Any implementation details you've considered

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/NutriVision.git
   cd NutriVision
   ```

2. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clear, commented code
   - Follow existing code style
   - Test your changes thoroughly

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```
   
   Use conventional commit messages:
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `style:` - Code style changes (formatting, etc.)
   - `refactor:` - Code refactoring
   - `test:` - Adding tests
   - `chore:` - Maintenance tasks

5. **Push and create a PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then open a Pull Request on GitHub.

## Development Setup

### Backend
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
python api_server.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Code Style

- **Python**: Follow PEP 8 guidelines
- **JavaScript/React**: Use ES6+ features, functional components with hooks
- **Comments**: Write clear comments for complex logic
- **Naming**: Use descriptive variable and function names

## Testing

Before submitting a PR:
- Test the backend API endpoints
- Test the frontend UI flows
- Ensure no console errors
- Test with different food images

## Questions?

Feel free to open an issue for any questions or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (CC BY-NC 4.0).
