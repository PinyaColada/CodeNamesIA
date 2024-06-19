# CodeNamesIA
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">CodeNamesIA</h3>

  <p align="center">
    An intelligent agent playing Codenames as both Spymaster and Spy
    <br />
    <a href="https://github.com/PinyaColada/CodeNamesIA"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/PinyaColada/CodeNamesIA/tree/master/Source">View Source</a>
    ·
    <a href="https://github.com/PinyaColada/CodeNamesIA/blob/master/Source/main.py">View main.py</a>
    ·
    <a href="https://github.com/PinyaColada/CodeNamesIA/issues">Request Feature or Report Bug</a>
  </p>
</div>

<!-- CodeNamesIA -->
## CodeNamesIA

CodeNamesIA is a project aimed at mimicking human-like gameplay in Codenames. The agent plays as both the Spymaster and the Spy. While optimal play is straightforward (mapping each combination to a word), CodeNamesIA employs a more human-like approach.

The agent uses the GloVe (Global Vectors for Word Representation) model to convert words into 300-dimensional vectors. It then selects words that are most likely to give the highest score based on these vectors. As the Spy also uses the same GloVe model, it rarely makes mistakes, making it challenging but not impossible to win against the agent.

<div align="center">
  <img src="https://github.com/PinyaColada/CodeNamesIA/blob/master/demo/CodeNamesIA.gif" alt="CodeNames agent Demo">
  <p>Display of the agent playing both sides</p>
</div>


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Features

CodeNamesIA includes the following features:
* GloVe word embeddings to convert words into 300-dimensional vectors
* Intelligent hint generation by the Spymaster
* Accurate word selection by the Spy based on hints
* High-level human-like play strategy

<p align="right">(<a href="#readme-top">back to top</a>)</p>
