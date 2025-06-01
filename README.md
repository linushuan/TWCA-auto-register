# TWCA-auto-register
## auto register TWCA competition
version 1.2 <br></br>
Wait for next test.
## setup
### python
 maybe python3.12 or higher version.
### need to install
- time
- tkinter
- selenium<br></br>
 How to install these?<br></br>
 Ask chatGPT or other AI. :)
### driver
 You need a chromedriver.<br></br>
 If you have any problems, ask chatGPT or other AI. :)
## feature
### input
- wcaid
- birth-year-month-day
- email
- choose events
### other
- report errors (but I don't know what it means) (I remove it now)
- report run time
- decide start time
- auto stop
- auto switch to 10% size
- avg speed: 9-13s

## future
- get element id more quickly
- choose T-shirt size
- enter phone number
- all event id check

## issues
- get element id too slow.
- code will click or fill with the place you can see (It means if you don't want to touch it, you need to let all the regions of website in the windows)

## tests
 - 4/8 20:00 2025ZhongshanOpen, fail with wcainput feild id change.
 - 4/15 20:00 2025ZhongshanOpen-second, fail with wcainput feild id keep changing.
 - 5/1 20:00 2025ChienKuoCubingParty, fail with laptop sleep.
 - 5/8 20:00 2025ChienKuoCubingParty-second, fail with unknow problem(start register botton didn't click.)
 - 5/31 21:30 2025TaipeiSummerBeQuiet, succeed.
