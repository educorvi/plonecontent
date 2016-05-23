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
    }); 
} 
