

//Delete entry

$('.delete-entry').click(function(){

    const entry_id = $(this).data('entry-id');

    $.post('/delete_entry', {'entry_id' : entry_id}, (res) => {
            $(this).parent().parent().hide();
    });

});




// CHARTS

var emotionsOptions = {
        responsive: true,
        title: {display: true,
                       text: 'Emotions',
                       fontSize: 20}
    };
    
var charactersOptions = {
    responsive: true,
    title: {display: true,
                       text: 'Characters',
                       fontSize: 20}
    };

var themesOptions = {
    responsive: true,
    title: {display: true,
                       text: 'Themes',
                       fontSize: 20}
    };

var settingsOptions = {
    responsive: true,
    title: {display: true,
                       text: 'Settings',
                       fontSize: 20}
    };

var lucidityOptions = {
        responsive: true,
        title: {display : true,
                    text: 'Lucidity',
                    fontSize: 20

        }
    };

var qualityOptions = {
        responsive: true,
        title: {display: true,
                            text: 'Sleep Quality',
                            fontSize: 20}
    };

var moodOptions = {
        // responsive = true,
        title: {display: true,
                            text: 'Mood Awake and Emotions',
                            fontSize: 20},
        scales: {
            xAxes: [{display: true, scaleLabel: {display:true, labelString: 'Date'}}],
            yAxes: [{
                type: 'linear',
                id: 'left-axis',
                display: true,
                position: 'left',
                scaleLabel: {display: true, labelString: 'mood'},
                ticks: {
                    max: 2,
                    min: -2,
                    stepSize: 1
                }
            }, {
                type:'linear',
                id: 'right-axis',
                display: true,
                position: 'right',
                scaleLabel: {display: true, labelString: 'emotion'},
                ticks: {
                    max: 4,
                    min: -4,

                    stepSize: 1
                }
            }]
        }
    };

    let ctx_emotion_donut = $("#emotionsChart").get(0).getContext("2d");
    let ctx_character_donut = $("#charactersChart").get(0).getContext("2d");
    let ctx_theme_donut = $("#themesChart").get(0).getContext("2d");
    let ctx_setting_donut = $("#settingsChart").get(0).getContext("2d");
    let ctx_lucidity_chart = $("#lucidityChart").get(0).getContext("2d");
    let ctx_quality_chart = $("#qualityChart").get(0).getContext("2d");
    let ctx_mood_chart = $("#moodChart").get(0).getContext("2d");

//Data and chart creation


    $.get('/emotions_data.json', function(data){
        let myDonutChart = new Chart(ctx_emotion_donut, {
                                                  type: 'doughnut',
                                                  data: data,
                                                  options: emotionsOptions
                                                });
          // $('#emotionLegend').html(myDonutChart.generateLegend());
    });
    $.get('/characters_data.json', function(data){
        let myDonutChart = new Chart(ctx_character_donut, {
                                                  type: 'doughnut',
                                                  data: data,
                                                  options: charactersOptions
                                                });
    });

    $.get('/themes_data.json', function(data){
        let myDonutChart = new Chart(ctx_theme_donut, {
                                                  type: 'doughnut',
                                                  data: data,
                                                  options: themesOptions
                                                });
    });

    $.get('/settings_data.json', function(data){
        let myDonutChart = new Chart(ctx_setting_donut, {
                                                  type: 'doughnut',
                                                  data: data,
                                                  options: settingsOptions
                                                });
    });

    $.get('/lucidity_data.json', function(data){
        let myLucidChart = new Chart(ctx_lucidity_chart, {
                                                  type: 'line',
                                                  data: data,
                                                  options: lucidityOptions
        });
    });

    $.get('/sleepquality_data.json', function(data){
        let myQualityChart = new Chart(ctx_quality_chart, {
                                                  type: 'line',
                                                  data: data,
                                                  options: qualityOptions
        });
    });

    $.get('/mood_data.json', function(data){
        let myMoodChart = new Chart(ctx_mood_chart, {
                                                  type: 'bar',
                                                  data: data,
                                                  options: moodOptions,

                                                  
        });
    });


