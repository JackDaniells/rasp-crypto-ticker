# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-11-22

### 🎉 Initial Release

First stable release of the Raspberry Pi Crypto Ticker.

### Added

- **6 Display Modules**: Weather/Time, Crypto Ticker, Fear & Greed Index, Bitcoin Dominance, Altcoin Season, Market Cap
- **Modular Architecture**: Easy to enable/disable modules and add custom ones
- **LCD Wrapper**: Automatic text truncation and positioning with `SafeLCD` class
- **Centralized Caching**: Unified API caching system across all modules
- **Configuration System**: Single `config.py` file for all settings
- **API Integrations**: CoinGecko, WeatherAPI.com, Alternative.me
- **Auto-start Support**: Systemd service configuration included
- **Comprehensive Documentation**: 6 guides covering setup, configuration, architecture, and troubleshooting

### Features

- Automatic text truncation for 16x2 LCD display
- Smart API caching with configurable intervals
- Graceful error handling (shows `--` for missing data)
- Customizable module order and display timing
- Temperature unit selection (Celsius/Fahrenheit)
- Auto-location detection via IP
- Large number formatting (K/M/B/T suffixes)

### Hardware Support

- Raspberry Pi 4 (tested), Pi 2/3/Zero W (compatible)
- 16x2 LCD with I2C adapter (PCF8574/PCF8574T)
- Simple 4-wire connection (VCC, GND, SDA, SCL)

### Dependencies

- `RPLCD >= 1.3.0`
- `requests >= 2.31.0`

---

## Release Notes Format

For future releases, use this format:

### [X.Y.Z] - YYYY-MM-DD

#### Added
- New features or modules

#### Changed
- Changes to existing functionality

#### Deprecated
- Features that will be removed in future versions

#### Removed
- Features removed in this release

#### Fixed
- Bug fixes

#### Security
- Security improvements or fixes

---

## Version History

- **[1.0.0]** - 2025-11-22 - Initial stable release

---

## Links

- [Repository](https://github.com/yourusername/rasp-crypto-ticker)
- [Issues](https://github.com/yourusername/rasp-crypto-ticker/issues)
- [Releases](https://github.com/yourusername/rasp-crypto-ticker/releases)

---

**Versioning Scheme**: [Semantic Versioning](https://semver.org/)
- **MAJOR** version: Incompatible API changes
- **MINOR** version: Backward-compatible functionality additions
- **PATCH** version: Backward-compatible bug fixes

