# Workshop_PyTest_Hypo

## Initial setup
### Done
1. install python
2. create virtual environment for your project eg. via procure described here: https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-virtual-environments
3. active/deactivate virtual env and remove it
4. download and install or turn on your favorite IDE eg.:
   5. vi/vim
   6. any test editor
   7. PyCharm https://www.jetbrains.com/pycharm/
   8. Visual Studio Code https://code.visualstudio.com/
   9. ....
10. Go to GitHub and create account https://github.com/
11. Download and install or find if you have git tool installed:
    12. comand line git --version
    13. GutHub Desktop https://desktop.github.com/download/
14. (Fork and ) Clone two repositories:
    15. https://github.com/SebaM/ShoPen <-- this will be localhost server for testing
    16. https://github.com/SebaM/Workshop_PyTest_Hypo  <-- your working repositories
17. Open cloned project in your IDE eg. PyCharm:
    18. some IDE are asking if create virtual env automatically, say *Yes*
19. Go to project *ShoPen*
    20. check ReadMe.md file and proceed
    20. check if dependency have been installed:
        21. pip list
        22. pip install -r requirements.txt
    23. start local server
        24. python -m local
    25. go to browser and check if http://localhost:8000/ is responding
26. Repeat steps for *Workshop_PyTest_Hypo*:
    27. Check ReadMe.md
    28. Check if you are working in virtual environment
    28. Check dependency and install if missing
    29. You can mark folders:
        30. source as source root
        31. tests as test root
29. Commit local changes
30. Do checkout of next branch ex1_calculator
## Unit Testing and First steps w/ PyTest
1. install pytest from requirements
   `pip install -r requirements.txt`
2. Run PyTest first time and check names and assertions
   ```
   pytest  tests/ex1_1_test.py
   py.test  tests/ex1_1_test.py
   ```
3. Now proceed in order, if test is failing fix it first:
   ```
    pytest  tests/ex1_2_test.py
    pytest  tests/ex1_3_test.py
    pytest -s  tests/ex1_3_test.py
    pytest -v  tests/ex1_3_test.py
    pytest -v tests/ex1_4_test.py
    pytest -v tests/ex1_5_0_test.py
    pytest -v tests/ex1_5_1_test.py
    pytest -v -m "not negative" tests/ex1_5_1_test.py
    pytest -v tests/ex1_6_test.py
   ```

# Other important info
## Semantic Commit Messages

See how a minor change to your commit message style can make you a better programmer.

Format: `<type>(<scope>): <subject>`

`<scope>` is optional

## Example

```
feat: add hat wobble
^--^  ^------------^
|     |
|     +-> Summary in present tense.
|
+-------> Type: chore, docs, feat, fix, refactor, style, or test.
```

More Examples:

- `feat`: (new feature for the user, not a new feature for build script)
- `fix`: (bug fix for the user, not a fix to a build script)
- `docs`: (changes to the documentation)
- `style`: (formatting, missing semi colons, etc; no production code change)
- `refactor`: (refactoring production code, eg. renaming a variable)
- `test`: (adding missing tests, refactoring tests; no production code change)
- `chore`: (updating grunt tasks etc; no production code change)

References:

- https://www.conventionalcommits.org/
- https://seesparkbox.com/foundry/semantic_commit_messages
- http://karma-runner.github.io/1.0/dev/git-commit-msg.html