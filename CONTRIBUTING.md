# Contributing to Blender Batch Product Renderer

Thank you for considering contributing! This project aims to stay simple and accessible to non-programmers, so contributions should maintain that spirit.

## How to Contribute

### Reporting Bugs

Open an issue with:
- Blender version
- Operating system
- Your CONFIG section (without sensitive info)
- Full error message
- What you expected vs. what happened

### Suggesting Features

Open an issue tagged "enhancement" with:
- Use case description
- How it would work
- Why it's useful for product rendering workflows

### Submitting Code

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test with multiple Blender versions if possible (3.x and 4.x)
5. Update README.md if you add config options
6. Commit with clear messages
7. Push and open a pull request

### Code Guidelines

- Keep the CONFIG section beginner-friendly
- Add comments for any logic that isn't obvious
- Don't add external dependencies (keep it stdlib + bpy only)
- Validate inputs and provide helpful error messages
- Test on Windows, macOS, and Linux if possible

### Documentation

- Update README.md for new features
- Add examples to EXAMPLE_CONFIG.py
- Keep INSTALLATION.md current

## Priority Areas

We're especially interested in:
- Better error messages for common mistakes
- More example configs for different industries
- Video tutorials or GIFs for README
- Performance optimizations for large batch jobs
- Multi-language README translations

## Code of Conduct

Be respectful, constructive, and inclusive. We're here to help designers automate tedious work.

## Questions?

Open an issue tagged "question" — happy to help!
