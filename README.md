# MoneyGrab
---
Using financial software (like YNAB) that requires you to routinely login and download your CSV or Quicken files was becoming tedious.  The more accounts you have or a more continuous balance sheet you want to keep becomes difficult.  We need a better and quicker way to do this.

I have started by making selenium scripts to download QFX files from Discover.  I am hoping to get more credit cards, banks and credit unions added (first my personal ones).

Currently, you can run ```python ff.py``` to download the most recent and previous statement.  Of course, credentials are not saved.

Please feel free to fork!

All you need:
```python
import selenium
```
and Firefox


**MIT LICENSE**
