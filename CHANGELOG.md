# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-26

### Added
- Initial release of Blender Batch Product Renderer
- Core batch rendering functionality with View Layer control
- CONFIG-only editing approach for non-programmers
- Support for multiple cameras, backgrounds, lighting, and product variants
- Cartesian product rendering (all combinations)
- Manual render plan support (specific combinations only)
- Exclusion rules to skip unwanted combinations
- Configurable filename patterns with token replacement
- Comprehensive error checking and validation
- Progress logging during batch execution
- Auto-creation of output directories
- Format enforcement (PNG/JPEG/EXR, RGB/RGBA)
- Detailed README with beginner-friendly instructions
- Installation guide for Windows/macOS/Linux
- Quick reference card for common tasks
- Example configurations for various use cases
- Contributing guidelines
- MIT License

### Documentation
- README.md with setup, configuration, troubleshooting, FAQ
- INSTALLATION.md with step-by-step setup for all platforms
- QUICK_REFERENCE.md as a one-page cheat sheet
- EXAMPLE_CONFIG.py with 7 real-world examples
- CONTRIBUTING.md for open-source collaboration
- LINKEDIN_POST.txt with designer-focused announcement templates

### Features
- No external dependencies (stdlib + bpy only)
- Cross-platform (Windows, macOS, Linux)
- Blender 3.x and 4.x compatible
- Command-line and UI execution modes
- Headless rendering support for automation
- Collection-based visibility control
- Safe defaults with clear error messages

---

## [Unreleased]

### Planned
- Video tutorial series
- Multi-language README (Hindi, Spanish, Japanese)
- Resume capability (skip already-rendered files)
- Render time estimation
- Email/Slack notification on completion
- Automatic thumbnail generation
- Web UI for config editing
- Docker container for cloud rendering

### Under Consideration
- Animation support (frame range batching)
- Render farm integration (Flamenco, Deadline)
- Multi-blend orchestration
- Post-processing hooks (watermarks, compression)
- CSV export of render metadata

---

**How to suggest features:** Open an issue on GitHub tagged "enhancement"

**How to report bugs:** Open an issue with Blender version, OS, and CONFIG section
