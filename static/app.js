var repString = '{{ instance.ques[0][3] }}';
    $(document).ready(function() {
        $("p").text(function(index, text) {
        return text.replace('%%P1%%',repString);
        });
});


    