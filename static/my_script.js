//populate calendar


// $('#calendar').fullCalendar({

//   event: '/calendar.json',

//   eventClick: function(event) {
//     if (event.url) {
//       //if you want to open url in the same tab
//       location.href = "/index";
//       //if you want to open url in another window / tab, use the commented code below
//       //window.open(event.url);
//       return false;
//     }
//   }
// });

// var calendar = new Calendar(calendarEl, {
//     eventSources: '/calendar.json'

//     eventClick: function(event) {
//     if (event.url) {
//       //if you want to open url in the same tab
//       location.href = "/index";
//       //if you want to open url in another window / tab, use the commented code below
//       //window.open(event.url);
//       return false;
//     }
//   }
// });

//stars
// function showRating(ratings)

//Delete entry
$('#toggle-btn').on('click', function (evt) {

        evt.preventDefault();

        if ($(window).outerWidth() > 1194) {
            $('nav.side-navbar').toggleClass('shrink');
            $('.page').toggleClass('active');
        } else {
            $('nav.side-navbar').toggleClass('show-sm');
            $('.page').toggleClass('active-sm');
        }
    });
// $(document).ready(function () {

//     $('#sidebarCollapse').on('click', function () {
//         $('#sidebar').toggleClass('active');
//     });

// });




$('.delete-entry').click(function(){

    const entry_id = $(this).data('entry-id');

    $.post('/delete_entry', {'entry_id' : entry_id}, (res) => {
            $(this).parent().parent().parent().hide();
    });
    $.get('/stats', get_stats => {
    $('#total').html("<h3>" + get_stats.total_entries + "</h3>");
    $('#hours').html("<h3>" + get_stats.average_sleep + "</h3>");
    $('#lucid').html("<h3>" + get_stats.total_lucid_month + "</h3>");
  });

});


//upon click, send new material to db, close window, show updated entry
//TEST THIS FOR DELETING ENTRIES AFTER YOU FINISH THE OTHER CARDS
// $('.delete-entry').on('click', (evt) => {
//   evt.preventDefault();
//   $.get('/stats', get_stats => {
//     $('#total').html("<h3>" + get_stats.total_entries + "</h3>");
//   });
// });
$.get('/stats', get_stats => {
    $('#total').html("<h3>" + get_stats.total_entries + "</h3>");
    $('#hours').html("<h3>" + get_stats.average_sleep + "</h3>");
    $('#lucid').html("<h3>" + get_stats.total_lucid_month + "</h3>");
  });

$('.btnUpdate').click((evt) => {
    evt.preventDefault();

    const entry_id = $(evt.target).data('entry-id');
    const newTitle = $(`#modal-${entry_id} input[name="title"]`).val();
    const newText = $(`#modal-${entry_id} textarea[name="text"]`).val();

    const data = {
        title: newTitle,
        text: newText,
        entry_id: entry_id
    };

    $.post('/edit_entry', data, (res) => {
        //after closing modal, show index with updated title (if updated)
        $(`#modal-${entry_id}`).modal("hide");
        // getStuff($(this).data('entry-id'));
    });
});

$('.entryModal').on('hidden.bs.modal', (evt) => {
    const modalId = $(evt.target).attr('id');

    const entryId = modalId.split('-')[1];

    $.get(`/getPostTitle/${entryId}`, (data) => {
        let text = data['title'];
        $(`#entry-${entryId}`).html(text);
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


