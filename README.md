# Generate Chinese poetry with char-rnn

# char-rnn-tensorflow
Multi-layer Recurrent Neural Networks (LSTM, RNN) for character-level language models in Python using Tensorflow.

Inspired from Andrej Karpathy's [char-rnn](https://github.com/karpathy/char-rnn).
Forked from Sherjil Ozair's [char-rnn-tensorflow](https://github.com/sherjilozair/char-rnn-tensorflow). 

# Requirements
- [Tensorflow 1.0](http://www.tensorflow.org)

# Basic Usage
To train with default parameters on the tangpoetry corpus, run `python train.py`.

To sample from a checkpointed model, `python sample.py`.
# Roadmap
- Add explanatory comments
- Expose more command-line arguments
- Compare accuracy and performance with char-rnn
