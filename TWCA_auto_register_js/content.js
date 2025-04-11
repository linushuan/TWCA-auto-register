window.onload = function() {
    var WCAIDbutton = document.getElementById('WCAID_input');
    var Previewbutton = document.getElementById('BTN_Preview');
    var GObutton = document.getElementsByClassName('btn btn-primary');
    var reload = 0;
    if(GObutton.length > 0){
        var reload = 1;
        setTimeout(function() {
            document.getElementsByClassName('btn btn-primary').click();
        }, 200);
    }
    if(WCAIDbutton) {
        var reload = 1;
        setTimeout(function() {
            document.getElementById('WCAID_input').value='2000AAAA00';
            setTimeout(function() {
                document.getElementById('WCAID_Button').click();
            }, 50000);
        }, 500);
    }
    if(Previewbutton) {
        var reload = 1;
        setTimeout(function() {
            document.getElementById('form_birthday_year').value='2000';
            document.getElementById('form_birthday_month').value='111';
            document.getElementById('form_birthday_day').value='111';
            document.getElementById('form_email').value='aa@gmail.com';
            document.getElementById('form_event_33').click();
            setTimeout(function() {
                document.getElementById('BTN_Preview').click();
                setTimeout(function() {
                    document.getElementById('BTN_Send').click();
                }, 500);
            }, 4000);
        }, 500);
    }
    if(reload === 0){
        setTimeout(function() {
            location.reload();
        }, 350);
    }
};
