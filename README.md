# Workshop_PyTest_Hypo

## Initial setup
 *Done*
## Unit Testing and First steps w/ PyTest
### TODO:
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
4. Commit local changes 
5. Do checkout of next branch ex2_parametrize

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