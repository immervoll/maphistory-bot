<!-- PROJECT LOGO -->
<br />
<p align="center">
    <h3 align="center">Map History Bot</h3>
    <p align="center">
        A Simple Discord / A2S Bot
        <br />
        <a href="https://github.com/immervoll/maphistory-bot"><strong>Explore the docs 📖</strong></a>
        <a href="https://github.com/immervoll/maphistory-bot/issues">Report Bug 🐛</a>
        <a href="https://github.com/immervoll/maphistory-bot/issues">Request Feature ✋</a>
        <a href="https://github.com/immervoll/maphistory-bot/releases/">Latest Release 📥</a>
    </p>
</p>

<!-- TABLE OF CONTENTS -->

## Table of Contents

- [Table of Contents](#table-of-contents)
- [About The Project](#about-the-project)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Contact](#contact)

<!-- ABOUT THE PROJECT -->

## About The Project

This is a simple implementation of a discord bot using A2S to query Source (Steam) Game-Servers for Maps.

### Built With

- [Discord.py](https://github.com/Rapptz/discord.py)
- [Python A2S](https://github.com/Yepoleb/python-a2s)

<!-- GETTING STARTED -->

## Getting Started

1.  Clone the project
2.  Edit your `configuration.json`
3.  launch `main.py`

### Prerequisites

Youll need the following packages and `Python 3.9.7` in order to run the bot:

- discord.py

```sh
pip3 install discord.py
```

- python-a2s

```sh
pip3 install python-a2s
```
- jaraco.docker
```sh
pip3 install jaraco.docker
```
### Installation

1. Get a discord Bot free Token at [Discord Developer Portal](https://discord.com/developers/applications), you can follow [this guide](https://discordpy.readthedocs.io/en/stable/discord.html) by the [Discord.py](https://github.com/Rapptz/discord.py) team
2. Clone the repo and create a `configuration.json`

```sh
gh repo clone immervoll/maphistory-bot
```
```json
{
    "TOKEN": "",
    "PREFIX": "!",
    "SERVER": {
        "IP": "",
        "PORT": 27165
    }
}
```

3. Install all the required packages

```sh
pip3 install -r requirements.txt
```

4. Enter your Token in `configiguration.json`

```JSON
"TOKEN": "your token here",
```

5. Enter your Server IP and PORT in `configiguration.json`

```JSON
    "SERVER": {
        "IP": "194.26.183.182",
        "PORT": 27165
    }
```

6. Invite the Bot to your discord via the [Discord Developer Portal](https://discord.com/developers/applications)
7. Profit 💯

<!-- USAGE EXAMPLES -->

## Usage

use `!history` or `!maps` on your discord in order to display the last 10 Maps

_For more examples, please refer to the [Documentation](https://github.com/immervoll/maphistory-bot)_

<!-- ROADMAP -->

## Roadmap

See the [open issues](https://github.com/immervoll/maphistory-bot/issues) for a list of proposed features (and known issues).

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- CONTACT -->

## Contact

Immervoll - [@immervoll](https://twitter.com/allswabbelvull)

Project maphistory-bot: [https://github.com/immervoll/maphistory-bot](https://github.com/immervoll/maphistory-bot)
