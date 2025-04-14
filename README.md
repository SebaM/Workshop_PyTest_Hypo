# Workshop_PyTest_Hypo

## Initial setup
 *Done*
## Unit Testing and First steps w/ PyTest
 *Done*
## Chosen advanced aspects of PyTest & Hypothesis
### TODO:
1. Now proceed in order, if test is failing fix it first, uncomment 1st block of code (--):
   ```
    pytest -v tests/ex1
    pytest -v tests/ex2/ex2_1_test.py
   ```
   How many defects you have found?
3. Use ChatGPT or some other LLM to generate more cases:
   ```
   I have somple method in python that adds two digits. Pls propose me
   code of PyTest with parametrize feature that would test this method.
   ```
   next add cases proposed by it to the scope of testing. In case of lack connection uncomment next block of code (--). 
   work in file:
   ```
   pytest -v tests/ex2/ex2_2_test.py
   ```
   How many defects you have found?
4. Write your own test checking if amount is enough to get discount.
1. install pytest from requirements
   `pip install -r requirements.txt`
2. Working w/ next test, start from launching it:
   ```
   pytest -v tests/ex2/ex2_3_test.py
   ```
   Uncomment block and test and correct method.
3. Uncomment next block and define your own first strategy.
4. Try to test negative case as well.
4. Commit local changes 
5. Do checkout of next branch ex3_rest

References:

- https://hypothesis.readthedocs.io/en/latest/