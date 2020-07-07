# Captcha-Breaker
This project aims at breaking simple captchas using Keras and Tensorflow, however the techniques can be tweaked a little to break complex captchas as well.
## Dataset
The file download.py automatically downloads captcha images from the specified url and then annotate.py helps annotate our data in a fairly simple and quick way
## The Model
Digits in the captcha images are trained using the Lenet Architecture and using a train set of 1600 digits we are able to obtain a near zero loss in just 20 epochs and 100% accuracy on the validation data.

![accuracy plot](https://user-images.githubusercontent.com/56725576/86794672-6625e200-c08a-11ea-8470-c219072d47d9.png)

## Improvements
The size and variety of dataset can be increased to build a more robust captcha breaker. The annotate.py will still come in handy to annotate our captchas.
### Dependencies
pip install requirements.txt
## References
https://github.com/jrosebr1/imutils
