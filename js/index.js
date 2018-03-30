models = []
$(document).ready(function() {

    $.ajax({
        url: "models",
        type: "get",
        dataType: 'json',
        success: function(json) {
            select = $('#model-select')
            models = json
            for (var i=0;i<json.length; i++){
                model = json[i]
                select.append($("<option></option>").attr("value", JSON.stringify(model)).text(model.model_name + " " + model.model_date+" "+model.model_score));
            }
        },
        error: function(xhr) {
        }
    });

    $("#go").click(function() {

        select = $('#model-select')
        model = JSON.parse(select.val())
        $.ajax({
            url: "analyze",
            type: "get",
            dataType: 'json',
            data: {
                song: $("#song").val(),
                artist: $("#artist").val(),
                model_name: model.model_name,
                model_date: model.model_date,
            },
            success: function(data) {
                if (data.code == 0){
                    max = 0
                    for (var i=1; i< data.probabilities.length; i++){
                        if (data.probabilities[max].probability<data.probabilities[i].probability){
                            max = i
                        }
                    }
                    pre_text = "Song "+$("#song").val()+" by "+$("#artist").val()+" is"
                    verdict_text = data.probabilities[max].label+" ("+(data.probabilities[max].probability*100).toFixed(2)+"%)"
                    result_text = pre_text+" "+verdict_text
                    $("#res").html("<div class=\"alert alert-dark\" role=\"alert\" id=\"res-alert\">"+result_text+" </div>");
                    time= new Date();
                    $("#res").append("<img src=\""+data.diagram_url+"?dummy="+time+"\"/>");
                }
                else{
                    $("#warn-alert").alert('close')
                    $("body").append("<div class=\"alert alert-warning fade show alert-bottom\" role=\"alert\" id=\"warn-alert\">"+data.text+" </div>")
                    setTimeout(function(){
                        $("#warn-alert").alert('close')
                    }, 3000)
                }
            },
            error: function(xhr) {
            }
        });
    });
});