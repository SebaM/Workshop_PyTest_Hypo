# Workshop_PyTest_Hypo

## Initial setup
### TODO:
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