let text = "";
function translating(){
    var myDataVar = {};                             // object
    myDataVar['text_area'] = $('#text_area').val(); // RHs bringing value of text_area and storing it in JSON object in LHS written in []
    myDataVar['option'] = $('#option').val(); // RHs bringing value of text_area and storing it in JSON object in LHS written in []

    $.ajax({
        type: "POST",
        url: "translating",   
        data: myDataVar,
        success: 
        function(resultData){
            console.log(resultData)
            $('#result_area').val(resultData.translated_text_is);
        },
        error: function() { }
    });
}

function swapping(){
    var textArea = $('#text_area').val(); 
    var resultArea = $('#result_area').val();
    $('#text_area').val(resultArea);
    $('#result_area').val("");
}

function addChar(char){
    text += char;
    $('#text_area').val(text);
    // $('#result_area').val("");
}