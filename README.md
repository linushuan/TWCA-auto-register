# TWCA-auto-register
## auto register TWCA competition
version 1.0
Wait for next test.
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

## future
- get element id more quickly
- choose T-shirt size
- enter phone number
- all event id check
- change to use beautifulsoup

## issues
- get element id too slow.
- code will click or fill with the place you can see (It means if you don't want to touch it, you need to let all the regions of website in the windows)

## tests
 - 4/8 20:00 2025ZhongshanOpen, fail with wcainput feild id change.
 - 4/15 20:00 2025ZhongshanOpen-second, fail with wcainput feild id keep changing.
 - 5/1 20:00 2025ChienKuoCubingParty, fail with laptop sleep.
 - 5/8 20:00 2025ChienKuoCubingParty-second, fail with unknow problem(start register botton didn't click.)
 - 5/31 21:30 2025TaipeiSummerBeQuiet, succeed.
