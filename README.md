[![](https://img.shields.io/pypi/l/fava-review.svg)](https://pypi.python.org/pypi/fava-review)
[![](https://img.shields.io/pypi/v/fava-review.svg)](https://pypi.python.org/pypi/fava-review)

# The problem
[Fava](https://beancount.github.io/fava/index.html) is a great UI for [Beancount](https://beancount.github.io/) however 
it only presents you with a snapshot of your finances for any given time period. Often it is useful to see ones' finances over a series of time periods to:
- Identify trends across accounts (e.g. spending more on food or earning less on interest?)
- Identify which accounts are the greatest contributors to our spending (e.g. the highest value accounts to try and reduce to save money)
- And to spot ingest mistakes (e.g. spikes in bills when it should be flat?)

# A solution

Fava Review is an [extension](https://beancount.github.io/fava/api/fava.ext.html) for 
[fava](https://beancount.github.io/fava/index.html) which takes your finances and presents them over time.

![](screenshot.png)

Fava review currently supports the following views:
- Income Statement
- Balance Sheet

And the views allow filtering your accounts by the usual date, account and payee/tag filters.
[Screenshot](screenshot-date-and-account-filter.png).

And it's also possible to sort your data.   
[Screenshot](screenshot-sorting.png).

# How it works
fava-review is very simple in its implementation. It uses bean-query through 
[fava](https://beancount.github.io/fava/index.html)'s FavaLedger class and retrieves the monthly data for each account. 
This information is then feed into [petl](https://petl.readthedocs.io/en/stable/) and pivoted into the appropriate view.

# How to install
`pip install fava-review`

## Requirements
- 1.21 <= fava >= 1.20 (There is a breaking change in fava 1.22 that needs to be addressed by the plugin - See https://github.com/kubauk/fava-review/issues/10)
- beancount <3, >=2.3.0

# Planned Features
- Support all currencies within beancount file.
- Percentage changes instead of absolute values.
- Setting projections and tracking actuals against estimates.
- [More](https://github.com/kubauk/fava-review/issues)
