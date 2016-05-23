function plonecontentXBlockInitStudio(runtime, element) {

    $(element).find('.action-cancel').bind('click', function() {
        runtime.notify('cancel', {});
    }); 

    $(element).find('.action-save').bind('click', function() {
        var data = { 
            'display_name': $('#plonecontent_edit_display_name').val(),
            'url': $('#plonecontent_edit_url').val(),
            'username': $('#plonecontent_edit_username').val(),
            'password': $('#plonecontent_edit_password').val(),
        };  
        
        runtime.notify('save', {state: 'start'});

        var handlerUrl = runtime.handlerUrl(element, 'save_plonecontent');
        $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
            if (response.result === 'success') {
                runtime.notify('save', {state: 'end'});
                // Reload the whole page :
                // window.location.reload(false);
            } else {
                runtime.notify('error', {msg: response.message})
            }   
         });
    }); 
} 
