# Contributing to LogParser for RTI Connext

## Contributor License Agreement (CLA)
In order to accept your pull request, we need you to sign a Contributor License Agreement (CLA). Complete your CLA here: http://community.rti.com/cla. You only need to do this once, we cross-check your Github username with the list of contributors who have signed the CLA.

## Styleguides
In general terms your code shall be warning-free. We are using the program [pylama](https://github.com/klen/pylama) to check the warnings. To install and run follow these steps:
```
[sudo] pip install pylama pylama_pylint isort
cd $logparser_root_folder$
pylama
```

If there is any warning that you think it should be ignored, update the *pylama.ini* configuration file and make a Pull Request for discussion.

Optionally, you can install the pylama Git hook to force that your code doesn't have any warning before committing. You can install it running `pylama --hook` in the root folder of the project.

### Specific rules
* Prefer to use the percentage symbol for string substition. Use:
```python
log_cfg("Interface name: %s (%s)" % (name, opt))
```
instead of
```python
log_cfg("Interface name: {0} ({1})".format(name, opt))
log_cfg("Interface name: " + name + " (" + opt + ")")
```