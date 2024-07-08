# Philippine Court Case Summarizer

This project is designed to summarize Philippine court case documents. The system consists of three main modules: Preprocessing, Topic Segmentation, and Latent Semantic Analysis (LSA).

## Table of Contents

- [Overview](#overview)
- [Modules](#modules)
  - [Preprocessing](#preprocessing)
  - [Topic Segmentation](#topic-segmentation)
  - [Latent Semantic Analysis (LSA)](#latent-semantic-analysis-lsa)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)

## Overview

The Philippine Court Case Summarizer processes court case documents and extracts meaningful segments to provide concise summaries. The system performs the following steps:

1. **Preprocessing**: Tokenization, stopword removal, POS tagging, and NER tagging.
2. **Topic Segmentation**: Identifies and segments the document into coherent topics.
3. **Latent Semantic Analysis (LSA)**: Extracts the main topics and themes from the segmented text.

## Modules

### Preprocessing

The preprocessing module handles the initial text processing tasks, including:

- **Tokenization**: Splits text into tokens (words or phrases).
- **Stopword Removal**: Removes common words that do not contribute significant meaning.
- **POS Tagging**: Labels each token with its corresponding part of speech.
- **NER Tagging**: Identifies and classifies named entities in the text.

### Topic Segmentation

This module segments the court case documents into coherent topics, making it easier to understand the structure and main points of the document.

### Latent Semantic Analysis (LSA)

LSA is used to analyze relationships between a set of documents and the terms they contain, providing a deeper understanding of the underlying topics.

## Dependencies

To set up the project, you need to install the following dependencies:

### Requirements File

The `requirements.txt` file contains a list of required Python packages. Install these packages using the following command:

```bash
pip install -r requirements.txt
