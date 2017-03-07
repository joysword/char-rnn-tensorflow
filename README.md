# Generate Chinese poetry with char-rnn
![Alt text](screenshots/main_page.png?raw=true "Interface")
![Alt text](screenshots/sample.png?raw=true "Generated poems")

# char-rnn-tensorflow
Multi-layer Recurrent Neural Networks (LSTM, RNN) for character-level language models in Python using Tensorflow.

Inspired from Andrej Karpathy's [char-rnn](https://github.com/karpathy/char-rnn).
Forked from Sherjil Ozair's [char-rnn-tensorflow](https://github.com/sherjilozair/char-rnn-tensorflow). 

# (New) Live Demo!
https://sage2rtt.evl.uic.edu:8080/rnn_tang_poetry

# (New) Video Demo!
https://youtu.be/91lA5g6MF8s

# Requirements
- [Tensorflow 1.0](http://www.tensorflow.org)
- [Flask](http://flask.pocoo.org/)

# How to train 
To train with default parameters on the tangpoetry corpus, run `python train.py --save_dir '/path/to/output dir'`. The checkpoints will be stored to this save directory. 
To sample from a checkpointed model, `python sample.py --save_dir '/path/to/checkpointed models'`.

# Instructions for using the Interface 
- Clone or download this repository 
- Get the already trained [model](https://drive.google.com/a/uic.edu/file/d/0B5cqEQ62osgNR3U1NHRTLVlmNW8/view?usp=sharing) and put in the save directory. You can additionally train your own model as instructed above.
- Run `python rnn_tang_poetry.py` to go to the interface 
- Open in browser http://127.0.0.1:5000/ 
- Enjoy 

# Explanation 
- Corpus 
  We used a corpus consisting of more than 43,000 Tang poems. You can find the corpus [here](https://pan.baidu.com/s/1o7QlUhO)
- Preprocessing
  1. We firstly separate each poem from the text, adding brackets at the beginning and the end of each poem. In this way, the neural
  network would know where to end a poem after training. 
  2. Another issue we encountered is the handling of UTF-8 character set. We had to add a chinese character as a prime text to generate     poems in chinese. 
- Some possible interesting future directions including:
  1. Take the relations between characters into consideration;
  2. Take the tones of each character into consideration.
- These considerations are because the rules for writing authentic Tang poetry has some restriction on the tones of the last character in   some segments in a poem, and has some requirements for the relations of objects in two consecutive segments.
