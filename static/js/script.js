$(document).ready(function() {
    // Initialize select2 on the language select element
    $('#language').select2();

    function toggleLoading(button, isLoading) {
        if (isLoading) {
            button.addClass('loading-active');
            button.prop('disabled', true);
        } else {
            button.removeClass('loading-active');
            button.prop('disabled', false);
        }
    }

    function displayError(message) {
        $('#error-message').text(message).show();
        setTimeout(function() {
            $('#error-message').hide();
        }, 5000);
    }

    $('#speak-btn').click(function() {
        var button = $(this);
        var text = $('#text').val();
        var voice_id = $('#voice').val();
        toggleLoading(button, true);
        $.ajax({
            url: '/speak/',
            type: 'POST',
            data: { 'text': text, 'voice_id': voice_id },
            headers: { 'X-CSRFToken': '{{ csrf_token }}' },
            success: function(response) {
                if (response.status === 'success') {
                    alert('Text spoken successfully');
                } else {
                    displayError(response.message);
                }
            },
            error: function() {
                displayError('An unexpected error occurred');
            },
            complete: function() {
                toggleLoading(button, false);
            }
        });
    });

    $('#recognize-btn').click(function() {
        var button = $(this);
        var micIcon = $('#mic-icon');
        toggleLoading(button, true);
        micIcon.show();
        $.ajax({
            url: '/recognize/',
            type: 'POST',
            headers: { 'X-CSRFToken': '{{ csrf_token }}' },
            success: function(response) {
                if (response.status === 'success') {
                    $('#recognized-text').text('Recognized text: ' + response.text);
                } else {
                    displayError(response.message);
                }
            },
            error: function() {
                displayError('An unexpected error occurred');
            },
            complete: function() {
                toggleLoading(button, false);
                micIcon.hide();
            }
        });
    });

    $('#translate-btn').click(function() {
        var button = $(this);
        var text = $('#translate-text').val();
        var language = $('#language').val();
        toggleLoading(button, true);
        $.ajax({
            url: '/translate/',
            type: 'POST',
            data: { 'text': text, 'language': language },
            headers: { 'X-CSRFToken': '{{ csrf_token }}' },
            success: function(response) {
                if (response.status === 'success') {
                    $('#translated-text').text('Translated text: ' + response.translated_text);
                    $('#speak-translated-btn').show();
                } else {
                    displayError(response.message);
                }
            },
            error: function() {
                displayError('An unexpected error occurred');
            },
            complete: function() {
                toggleLoading(button, false);
            }
        });
    });

    $('#speak-translated-btn').click(function() {
        var button = $(this);
        var text = $('#translated-text').text().replace('Translated text: ', '');
        toggleLoading(button, true);
        $.ajax({
            url: '/speak/',
            type: 'POST',
            data: { 'text': text },
            headers: { 'X-CSRFToken': '{{ csrf_token }}' },
            success: function(response) {
                if (response.status === 'success') {
                    alert('Translated text spoken successfully');
                } else {
                    displayError(response.message);
                }
            },
            error: function() {
                displayError('An unexpected error occurred');
            },
            complete: function() {
                toggleLoading(button, false);
            }
        });
    });
});