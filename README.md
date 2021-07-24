# Stock-price-prediction
# Simple maths calculator

Simple math calculator for your everyday use.

## Installation

Use a python interface
and run `pip install git+https://github.com/Abimbola-ai/simple-calculator.git` to download all files.

## Usage

### How to create a calculator?

Example code below will create the calculator method for five different operations.

Import the calculator module and call the class:

```
from calculator.calc import Calculator
calculator = Calculator()
```

The current value on the calculator is 0. To perform Add operation:

```
calculator.add(5)
```

Returns 0 + 5 = 5

Other methods are `.subtract, .multipy(), .divide(), .nroot().`

What is what:

- [CalculatorModule](/calculator/calc.py) contains the calculation algorithm;
- [test](/tests/calculator_test.py) contains the `pytest` configuration for the `CalculatorModule`;

### How to calculate?

Select the operation you want to perform, using the instructions that get printed out.
The calculate default value is 0. To set a current value rather that 0, use `calculator.current_value = 9`

### More ideas how to use and extend calculator

- Undo the calculator 3 steps before;
- Reset memory without having to restart the calculator;
- Recall previous memory;
