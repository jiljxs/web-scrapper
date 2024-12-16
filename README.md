# Web Scraping and AI-powered Question Answering

The repository contains Python scripts that demonstrate web scraping, text processing, and AI-powered question answering using OpenAI's GPT-3.5 engine. The code is based on a variation of an existing project.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Examples](#examples)
- [References](#references)

## Overview

The scripts combine web scraping with AI-based natural language processing to answer questions based on the contents of a web page. It extracts text from a specified URL, processes it, and generates answers to user-input questions using OpenAI's GPT-3.5 model.

## Features

- Web scraping using `requests` and `BeautifulSoup`
- Text preprocessing and splitting
- AI-powered question answering with GPT-3.5
- User-friendly command-line interface

## Requirements

- Python 3.x
- Required Python packages are listed in the `requirements.txt` file.

## Installation

1. Clone the repository: `git clone https://github.com/Knl-Bill/Web_Scrapper_with_QndA.git`
2. Navigate to the project directory
3. Install the required packages: `pip install -r requirements.txt`

## Configuration

1. Create a config.json file containing your OpenAI API KEY having `"OPENAI_API_KEY" : "YOUR_OPENAI_API_KEY"`
2. Replace `"YOUR_OPENAI_API_KEY"` with your actual OpenAI API key.

## Examples

To use the script, follow these steps:

1. Run the script and provide a URL to scrape.
2. The script will extract text from the URL and preprocess it.
3. Input your question.
4. The script will generate an answer using GPT-3.5 based on the context and the question.

## References

This code is based on a variation of the original code at `"https://github.com/openai/openai-cookbook/blob/main/apps/web-crawl-q-and-a/web-qa.ipynb"`. The original code is in the OpenAI Cookbook 
